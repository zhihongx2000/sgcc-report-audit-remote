# Splitter 接口设计说明

> 涉及文件：`base_splitter.py` / `recursive_character_splitter.py` / `parent_child_splitter.py`  
> 测试文件：`tests/unit/test_splitter_recursive.py`

---

## 1. `base_splitter.py` — 抽象契约层

```
┌─────────────────────────────────────────────────┐
│              BaseSplitter  (ABC)                │
├─────────────────────────────────────────────────┤
│  @abstractmethod                                │
│  split(doc: Document) -> list[Chunk]            │  ← 子类必须实现
│                                                 │
│  split_parent_child(doc, *,                     │  ← 默认抛 NotImplementedError
│    parent_chunk_size,                           │    子类按需覆盖
│    child_chunk_size,                            │
│    chunk_overlap=0)                             │
│  -> list[tuple[Chunk, list[Chunk]]]             │
└─────────────────────────────────────────────────┘
```

设计意图：

- `split()` 是**必须实现**的核心语义切分接口
- `split_parent_child()` 是**可选扩展**，基类给出 `NotImplementedError`，不会强迫所有子类实现

---

## 2. `recursive_character_splitter.py` — 主实现层

```
BaseSplitter
    │
    └── RecursiveCharacterSplitter
            ├── __init__(chunk_size, chunk_overlap, separators)
            │
            ├── _build_lc_splitter(chunk_size, chunk_overlap)
            │       └── 内部工厂方法，生成 LangChain 实例
            │
            ├── split(doc) -> list[Chunk]
            │       └── 调用 LangChain，逐块组装 Chunk（附 offsets）
            │
            └── split_parent_child(doc, *, parent_chunk_size,
                        child_chunk_size, chunk_overlap)
                    └── 先切父块 → 再切子块，子块 offset 基准为原文
```

### `split()` 数据流

```
原始 Document.text（Markdown）
  "## Section 1\n\nFirst paragraph...\n\n## Section 2\n..."
         │
         ▼  LangChain RecursiveCharacterTextSplitter
         │  separators: ["\n## ", "\n### ", "\n\n", "\n", " ", ""]
         │  add_start_index=True  ← 记录切分起始位置
         │
  ┌──────┴──────────────────────────────────────┐
  │  LangChain Document list                    │
  │  [{"page_content":"## Section 1\n...",      │
  │    "metadata":{"start_index": 0, ...}},     │
  │   {"page_content":"## Section 2\n...",      │
  │    "metadata":{"start_index": 78, ...}},    │
  │   ...]                                      │
  └──────┬──────────────────────────────────────┘
         │ 逐项转换为 Chunk dataclass
         ▼
  Chunk(text="## Section 1\n...",
        source="doc.md",
        chunk_index=0,
        start_offset=0,
        end_offset=75)

  Chunk(text="## Section 2\n...",
        source="doc.md",
        chunk_index=1,
        start_offset=78,
        end_offset=155)
  ...
```

### `split_parent_child()` 数据流

```
原始文档（500 字符）
  ├─ 第一步：用 parent_chunk_size=300 切父块
  │
  │   parent_chunk[0]  offset[0~280]   "## Sec1 ... full context ..."
  │   parent_chunk[1]  offset[281~500] "## Sec2 ... full context ..."
  │
  └─ 第二步：对每个父块，用 child_chunk_size=100 再切子块
           （子块 offset = 父块起点 + 子块在父块内的相对偏移）

      parent_chunk[0] (offset 0~280)
        ├── child[0]  offset[0~95]    "## Sec1 intro..."
        ├── child[1]  offset[95~190]  "continued para..."
        └── child[2]  offset[190~280] "last part..."

      parent_chunk[1] (offset 281~500)
        ├── child[0]  offset[281~375] "## Sec2 intro..."
        └── child[1]  offset[375~500] "rest of sec2..."

返回值：
  [
    (parent_chunk[0], [child[0], child[1], child[2]]),
    (parent_chunk[1], [child[0], child[1]]),
  ]
```

**父子检索的用途：**

> 子块（小）进入向量索引，命中后拉取对应的父块（大）作为上下文送给 LLM，兼顾检索精度和答案完整性。

---

## 3. `parent_child_splitter.py` — 便捷封装层

```
BaseSplitter
    │
    └── RecursiveCharacterSplitter
                │
                └── ParentChildSplitter
                        ├── 默认参数：parent=2000 / child=400 / overlap=50
                        │
                        ├── split(doc)
                        │     └── super().split()  以 child_chunk_size 为准
                        │
                        └── split_parent_child(doc, *, ...)
                              └── super().split_parent_child()
                                    参数省略时使用构造函数默认值
```

```
使用对比：

RecursiveCharacterSplitter(chunk_size=400).split(doc)
  → 等价于
ParentChildSplitter(child_chunk_size=400).split(doc)


ParentChildSplitter().split_parent_child(doc)
  → 内部等价于调用：
     RecursiveCharacterSplitter.split_parent_child(
         doc,
         parent_chunk_size=2000,
         child_chunk_size=400,
         chunk_overlap=50,
     )
```

---

## 4. 测试覆盖一览（`test_splitter_recursive.py`）

### `TestRecursiveCharacterSplitter`（9 个测试）

| 测试名                                        | 验证点                                          |
| --------------------------------------------- | ----------------------------------------------- |
| `test_split_returns_at_least_one_chunk`       | 不返回空列表                                    |
| `test_chunk_index_is_sequential`              | `chunk_index` 从 0 连续递增                     |
| `test_chunk_source_matches_document`          | 每个 chunk 的 `source` 与原文档一致             |
| `test_end_offset_greater_than_start`          | `end_offset > start_offset`，无零长 chunk       |
| `test_offsets_within_original_text_bounds`    | offset 不超出原文长度（允许 5 字符 strip 容差） |
| `test_smaller_chunk_size_yields_more_chunks`  | chunk_size 越小切出越多块                       |
| `test_content_preserved_across_chunks`        | 所有关键词（Section 1/2/3）在合并内容中仍存在   |
| `test_chunk_text_non_empty`                   | 无空文本 chunk                                  |
| `test_large_chunk_size_produces_single_chunk` | `chunk_size=10000` 时全文是一块                 |

### `TestParentChildSplitter`（7 个测试）

| 测试名                                            | 验证点                                                   |
| ------------------------------------------------- | -------------------------------------------------------- |
| `test_split_parent_child_returns_pairs`           | 返回非空的 `(parent, [children])` 列表且每对至少一个子块 |
| `test_parent_text_longer_than_each_child`         | 父块长度 ≥ 每个子块长度                                  |
| `test_child_source_matches_document`              | 子块 `source` 与文档一致                                 |
| `test_child_chunk_index_sequential_within_parent` | 每组子块内 `chunk_index` 从 0 连续                       |
| `test_child_start_offset_within_parent_range`     | 子块 `start_offset ≥` 父块 `start_offset`                |
| `test_split_returns_child_sized_chunks`           | `split()` 返回的是小尺寸子块，不是父块尺寸               |
| `test_default_sizes_produce_valid_splits`         | 无参构造可正常工作                                       |
