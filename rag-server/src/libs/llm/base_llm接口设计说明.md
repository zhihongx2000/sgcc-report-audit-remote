# `base_llm.py` 接口设计说明

> 结合 `vllm_llm.py` 实现讲解 `BaseLLM` 的设计意图与代码逻辑。

---

## 一、整体设计模式

这套设计采用了两个经典模式的组合：**模板方法模式（Template Method）** + **依赖注入（Dependency Injection）**。

```
┌──────────────────────────────────────────────────────────────┐
│  BaseLLM（模板方法模式）                                        │
│                                                              │
│  公开 API:  generate() / chat()       ← 业务代码调用的入口     │
│       │            │                                        │
│       ▼            ▼                                        │
│  [retry_call 重试层]  ← RetryPolicy 依赖注入                  │
│       │            │                                        │
│       ▼            ▼                                        │
│  _generate_once() / _chat_once()     ← 抽象方法（子类实现）    │
│       ↑            ↑                                        │
│  子类（如 VLLMLLM）只需实现这两个方法                            │
└──────────────────────────────────────────────────────────────┘
```

**核心思想**：父类负责"通用横切关注点"（重试、输入校验、消息归一化），子类只负责"Provider 差异"（实际 HTTP 调用）。上层业务代码调用 `generate()` / `chat()`，完全不感知底层 Provider 是 OpenAI、vLLM 还是 Ollama。

---

## 二、`base_llm.py` 逐层拆解

### 1. 数据载体：`ChatMessage`

```python
@dataclass(slots=True, frozen=True)
class ChatMessage:
    role: str
    content: str
```

| 修饰符        | 作用                                                                            |
| ------------- | ------------------------------------------------------------------------------- |
| `slots=True`  | 用 `__slots__` 替代 `__dict__`，节省内存，属性访问更快                          |
| `frozen=True` | 实例创建后不可变，`role`/`content` 不能被修改，保证消息在传递过程中不被意外篡改 |

这是所有 Provider 共享的**消息格式**，不依赖任何第三方 SDK 的类型。子类收到的 `messages` 永远是这个统一类型，无需关心输入来源。

---

### 2. 构造函数：可选依赖注入 `RetryPolicy`

```python
def __init__(self, *, retry_policy: RetryPolicy | None = None) -> None:
    self._retry_policy = retry_policy or RetryPolicy()
```

- `*` 强制所有参数必须以关键字方式传入（`BaseLLM(retry_policy=xxx)`），防止位置参数混淆。
- `retry_policy or RetryPolicy()` 是**可选注入**：
  - 调用方可传入自定义策略（测试时常传 `RetryPolicy(max_attempts=1, base_delay_seconds=0)` 彻底关闭重试和等待）。
  - 不传则使用默认值（3 次重试，指数退避）。

---

### 3. 公开方法：`generate()` — 模板方法

```python
def generate(self, prompt: str, *, temperature=None, max_tokens=None, **kwargs) -> str:
    if not prompt:
        raise ValueError("prompt must not be empty")   # ① 输入校验

    return retry_call(                                 # ② 重试包装
        lambda: self._generate_once(                  # ③ 委托给子类
            prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        ),
        policy=self._retry_policy,
    )
```

三个职责层级非常清晰：

1. **校验层**：空 prompt 直接报错，不浪费网络调用。
2. **重试层**：`retry_call` 捕获异常并按策略重试，子类完全不需要写 try/except 循环。
3. **委托层**：通过 `lambda` 延迟调用子类实现（每次重试都重新执行 `_generate_once`）。

---

### 4. 公开方法：`chat()` — 多了消息归一化步骤

```python
def chat(self, messages: Sequence[ChatMessage | Mapping[str, str]], ...) -> str:
    normalized_messages = self._normalize_messages(messages)  # ① 归一化
    if not normalized_messages:
        raise ValueError("messages must not be empty")        # ② 校验

    return retry_call(
        lambda: self._chat_once(normalized_messages, ...),    # ③ 重试 + 委托
        policy=self._retry_policy,
    )
```

`chat()` 比 `generate()` 多一个**消息格式归一化**步骤，因为它接受两种输入形式，方便调用方：

```python
# 两种写法都合法：
llm.chat([ChatMessage(role="user", content="hello")])
llm.chat([{"role": "user", "content": "hello"}])
```

---

### 5. 静态方法：`_normalize_messages()` — 消息类型统一

```python
@staticmethod
def _normalize_messages(messages):
    normalized = []
    for message in messages:
        if isinstance(message, ChatMessage):
            normalized.append(message)          # 已是标准类型，直接用
            continue

        role = message.get("role")
        content = message.get("content")
        if not role or not content:
            raise ValueError(...)               # 字典缺字段时报错
        normalized.append(ChatMessage(role=role, content=content))  # 转换
    return normalized
```

- `@staticmethod` 表明这是**纯函数**——不依赖实例状态，输入相同输出一定相同，可以单独测试。
- 归一化的意义：子类的 `_chat_once` 签名里 `messages` 永远是 `Sequence[ChatMessage]`，不必再处理字典情况，**降低每个 Provider 实现的复杂度**。

---

### 6. 抽象方法：最小子类接口约定

```python
@abstractmethod
def _generate_once(self, prompt, *, temperature, max_tokens, **kwargs) -> str: ...

@abstractmethod
def _chat_once(self, messages: Sequence[ChatMessage], *, temperature, max_tokens, **kwargs) -> str: ...
```

- 以 `_` 开头表示**内部方法**，不对外暴露，不是给业务代码调用的。
- `abstractmethod` 约束：子类**必须**实现这两个方法，否则 Python 拒绝实例化（`TypeError`）。
- `**kwargs` 为将来扩展预留通道（如 `stream=True`、`top_p=0.9`），不破坏现有子类签名。

---

## 三、`vllm_llm.py` 实现逻辑

`VLLMLLM` 是最典型的 OpenAI-compatible 模式适配器实现，逻辑最扁平，适合作为理解模板。

### 构造函数

```python
def __init__(self, *, base_url, model, api_key="vllm",
             temperature=None, max_tokens=None,
             timeout_seconds=60.0, retry_policy=None):
    super().__init__(retry_policy=retry_policy)  # 把重试策略交给父类管理

    self._client = openai.OpenAI(
        api_key=api_key,      # vLLM 不校验 key，"vllm" 是约定占位符
        base_url=base_url,    # 指向本地 vLLM 服务器（如 http://localhost:8000/v1）
        timeout=timeout_seconds,
    )
    self._model = model
    self._temperature = temperature   # 实例级默认值，可被调用时覆盖
    self._max_tokens = max_tokens
```

`api_key="vllm"` 是 vLLM 的约定——本地服务器不校验 key，但 openai SDK 要求必填，传一个占位字符串即可。

---

### `_generate_once()` — 最薄的委托

```python
def _generate_once(self, prompt, *, temperature=None, max_tokens=None, **kwargs):
    return self._chat_once(
        [ChatMessage(role="user", content=prompt)],  # prompt 包成单条 user 消息
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )
```

vLLM 的 API 端点本质上是 Chat Completions，所以 `_generate_once` 只是把 prompt 包装成一条 `user` 消息，复用 `_chat_once` 的逻辑，**避免代码重复**。

---

### `_chat_once()` — 真正的 HTTP 调用

```python
def _chat_once(self, messages, *, temperature=None, max_tokens=None, **kwargs):
    # ① 把统一的 ChatMessage 转回 SDK 要求的字典格式
    api_msgs = [{"role": m.role, "content": m.content} for m in messages]

    create_kwargs = {"model": self._model, "messages": api_msgs}

    # ② 参数优先级：调用时传入 > 实例默认值 > 不传（API 服务端默认）
    resolved_temp = temperature if temperature is not None else self._temperature
    resolved_max  = max_tokens  if max_tokens  is not None else self._max_tokens

    # ③ None 值不加入请求，让 API 服务端使用其默认值
    if resolved_temp is not None:
        create_kwargs["temperature"] = resolved_temp
    if resolved_max  is not None:
        create_kwargs["max_tokens"]  = resolved_max

    # ④ 发起 HTTP 请求，只返回文本内容，屏蔽 SDK 类型
    resp = self._client.chat.completions.create(**create_kwargs)
    return resp.choices[0].message.content
```

**参数优先级链**（`None` 表示"未指定"）：

```
llm.generate("x", temperature=0.9)   ← 调用时传入，最高优先级
    > self._temperature = 0.1         ← 构造时指定的实例默认值
        > 不传                         ← 让 API 服务端使用其自身默认值
```

这样设计让同一个实例在不同场景下可以临时覆盖默认值，而不需要重新创建对象。

---

## 四、完整调用链总结

以 `llm.generate("你好")` 为例：

```
llm.generate("你好")
  │  [继承自 BaseLLM]
  ├─ ① 校验: prompt 非空 ✓
  ├─ ② retry_call(lambda: _generate_once(...), policy)
  │     │  [最多重试 N 次，指数退避]
  │     └─ ③ VLLMLLM._generate_once("你好")
  │           │  [包装成单条 user 消息]
  │           └─ ④ VLLMLLM._chat_once([ChatMessage("user","你好")])
  │                 │  [组装 create_kwargs，解析参数优先级]
  │                 └─ ⑤ openai_client.chat.completions.create(...)
  │                       │  [HTTP → vLLM 本地服务器]
  │                       └─ ⑥ resp.choices[0].message.content → str
  └─ 返回 "你好，有什么可以帮你？"
```

---

## 五、扩展新 Provider 的最小步骤

理解了上述设计后，新增一个 Provider（如 `MistralLLM`）只需：

1. 继承 `BaseLLM`，调用 `super().__init__(retry_policy=retry_policy)`。
2. 在构造函数中初始化该 Provider 的 SDK 客户端。
3. 实现 `_generate_once()`（通常直接委托给 `_chat_once`）。
4. 实现 `_chat_once()`（组装请求参数，调用 SDK，返回文本字符串）。

**不需要**写重试逻辑、消息归一化、空值校验——这些父类已全部处理。
