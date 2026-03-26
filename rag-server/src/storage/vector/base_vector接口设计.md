# VectorStore 接口设计说明

> 对应文件：`base_vector_store.py` / `pgvector_store.py`
> 任务编号：D6

---

## 一、接口分层设计

```
┌─────────────────────────────────────────────────────────────┐
│                      调用者（Pipeline）                       │
│   ingestion / retrieval / document_manager                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ 只依赖抽象，不知道底层是哪个数据库
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  BaseVectorStore  (ABC)                     │
│                                                             │
│  @abstractmethod                @abstractmethod            │
│  upsert(records) -> int         query(vec, ...) -> results  │
│                                                             │
│  @abstractmethod                default (raise)            │
│  delete(filter) -> int          get_all() / get_by_metadata │
└──────────────────────┬──────────────────────────────────────┘
                       │ 子类实现
          ┌────────────┴────────────┐
          ▼                         ▼  （未来扩展位）
   PgVectorStore              QdrantStore / ChromaStore
   （当前唯一实现）
```

### 设计意图

调用方（Ingestion Pipeline、Retrieval、Dashboard）全部面向 `BaseVectorStore` 编程，不导入任何 `pgvector_store` 模块。未来若要切换向量数据库，只需：

1. 新增一个实现类；
2. 在 `VectorStoreFactory` 中按配置路由；
3. 业务代码零修改。

---

## 二、数据契约（两个 dataclass）

```
VectorRecord                          QueryResult
─────────────────────────────         ─────────────────────
id            : str  ← 全局唯一ID      id     : str
text          : str  ← 原始文本         text   : str
dense_vector  : list[float] ← 语义向量  score  : float ← 相似度
sparse_vector : dict | None ← BM25权重  metadata: dict
metadata      : dict ← 来源/页码等
```

- **写入用 `VectorRecord`**：携带向量和元数据，由 Pipeline 构造后传给 `upsert()`。
- **读取返回 `QueryResult`**：只包含文本、分数和元数据，不回传原始向量（节省带宽）。

---

## 三、方法职责边界

| 方法                | 是否必须实现                     | 调用场景                      |
| ------------------- | -------------------------------- | ----------------------------- |
| `upsert()`          | ✅ `@abstractmethod`             | Ingestion Pipeline 写入 chunk |
| `query()`           | ✅ `@abstractmethod`             | Retrieval 检索相似候选        |
| `delete()`          | ✅ `@abstractmethod`             | 文档删除/重建索引             |
| `get_all()`         | 默认 `raise NotImplementedError` | Dashboard 数据浏览页          |
| `get_by_metadata()` | 默认 `raise NotImplementedError` | Dashboard 按条件筛选          |

`get_all / get_by_metadata` 用 `raise` 而非 `@abstractmethod` 的原因：

- 它们只被 Dashboard 调用，并非所有后端都需要支持；
- 避免强迫未来的 Qdrant 等实现实现不必要方法（接口最小化原则）。

---

## 四、PgVectorStore — `upsert()` 数据流

```
调用方传入 list[VectorRecord]
          │
          │  records = [VectorRecord(id="abc", text="...",
          │              dense_vector=[0.1,0.2,...],
          │              sparse_vector={"关键词":0.8},
          │              metadata={"source":"report.pdf"})]
          ▼
┌─────────────────────────────────────────────────┐
│  Step 1: Python → SQL 参数序列化                  │
│                                                 │
│  dense_vector  list[float]                      │
│     → "[0.1,0.2,0.3,...]"  ← 手动拼接字符串      │
│                                                 │
│  sparse_vector dict | None                      │
│     → json.dumps({"关键词": 0.8})  或  None      │
│                                                 │
│  metadata dict                                  │
│     → json.dumps({"source": "report.pdf"})      │
└─────────────────────┬───────────────────────────┘
                      │
                      │  ⚠️  为什么 dense_vector 要手动拼字符串？
                      │      SQLAlchemy text() 中 "::vector" 会与
                      │      参数占位符 ":" 冲突（psycopg2 解析错误）。
                      │      改用 CAST(:param AS vector) 后，
                      │      psycopg2 不识别 list[float] 类型，
                      │      必须先序列化为 pgvector 接受的字符串格式
                      │      "[x1,x2,...,xn]"。
                      ▼
┌─────────────────────────────────────────────────┐
│  Step 2: 执行 INSERT ... ON CONFLICT DO UPDATE   │
│                                                 │
│  INSERT INTO rag_chunks                         │
│    (id, content, dense_vector,                  │
│     sparse_vector, metadata)                    │
│  VALUES (                                       │
│    :id,                                         │
│    :content,                                    │
│    CAST(:dense_vector AS vector),  ← 字符串→向量  │
│    CAST(:sparse_vector AS jsonb),  ← 字符串→JSONB │
│    CAST(:metadata AS jsonb)        ← 字符串→JSONB │
│  )                                              │
│  ON CONFLICT (id) DO UPDATE SET    ← 幂等保证    │
│    content       = EXCLUDED.content,            │
│    dense_vector  = EXCLUDED.dense_vector,       │
│    sparse_vector = EXCLUDED.sparse_vector,      │
│    metadata      = EXCLUDED.metadata            │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
               session.commit()
               return len(records)
```

**幂等性保证**：`ON CONFLICT (id) DO UPDATE` 确保对同一 `id` 重复写入时只更新，不产生重复行。这是 Ingestion Pipeline 重复摄取同一文档不产生重复数据的基础。

---

## 五、PgVectorStore — `query()` 检索流

```
调用方: query([0.8, 0.1, ...], top_k=5, metadata_filter={"source":"rpt.pdf"})
          │
          ▼
┌──────────────────────────────────────────────────────────┐
│  Step 1: 构建 WHERE 子句（可选）                            │
│                                                          │
│  有 filter: "WHERE metadata @> CAST(:filter AS jsonb)"   │
│   ↑ @> 是 JSONB 包含运算符：                               │
│     {"source":"a","page":3} @> {"source":"a"} = TRUE    │
│     {"source":"b"}          @> {"source":"a"} = FALSE   │
│                                                          │
│  无 filter: WHERE 子句为空字符串                            │
└──────────────────────────────┬───────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────┐
│  Step 2: 构建相似度得分表达式                               │
│                                                          │
│  cosine:         1 - (vec <=> query)                     │
│      ↑  <=> 返回 [0,2] 的余弦距离（0=完全相同）             │
│         1 - distance 转为 [-1,1] 相似度（1=最相似）         │
│                                                          │
│  l2:             -(vec <-> query)                        │
│  inner_product:  -(vec <#> query)                        │
│      ↑  取负值统一语义：score 越高 = 越相关                  │
└──────────────────────────────┬───────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────┐
│  Step 3: 执行 SQL                                         │
│                                                          │
│  SELECT id, content, metadata,                           │
│    1-(dense_vector <=> CAST(:vec AS vector)) AS score    │
│  FROM rag_chunks                                         │
│  WHERE metadata @> CAST(:filter AS jsonb)  ← 可选        │
│  ORDER BY dense_vector <=> CAST(:vec AS vector)  ← 升序  │
│  LIMIT :top_k                                            │
│                                                          │
│  注意: ORDER BY 用距离升序（小=近）                          │
│        SELECT score 用 1-距离（高=相似）                    │
│        两者逻辑一致，只是方向转换给调用方用                    │
└──────────────────────────────┬───────────────────────────┘
                               │
                               ▼
                  list[QueryResult]  (score 高 → 排前)
```

---

## 六、Schema Bootstrap（`_ensure_table`）

`PgVectorStore.__init__()` 被调用时自动执行，无需手动迁移：

```
CREATE EXTENSION IF NOT EXISTS vector
        │
        ▼
CREATE TABLE IF NOT EXISTS rag_chunks (
  id           TEXT PRIMARY KEY,    ← upsert 冲突键
  content      TEXT NOT NULL,       ← 原始文本
  dense_vector vector(1536),        ← pgvector 专有类型
  sparse_vector JSONB,              ← BM25 权重（可为 NULL）
  metadata     JSONB DEFAULT '{}'   ← 来源/页码/标签等
)
        │
        ▼
CREATE INDEX IF NOT EXISTS ... USING hnsw (dense_vector vector_cosine_ops)
        ↑
        HNSW 图索引（Hierarchical Navigable Small World）
        - 支持空表建索引（ivfflat 需要已有数据才能建）
        - 近似最近邻，检索时间复杂度 O(log N)
```

---

## 七、关键设计决策汇总

| 决策                | 方案                          | 原因                                                 |
| ------------------- | ----------------------------- | ---------------------------------------------------- |
| 类型转换            | `CAST(:param AS vector)`      | `::vector` 与 psycopg2 占位符 `:` 语法冲突           |
| dense_vector 序列化 | 手动拼 `"[x1,x2,...]"` 字符串 | psycopg2 无法自动将 `list[float]` 绑定为 vector 类型 |
| 幂等写入            | `ON CONFLICT (id) DO UPDATE`  | 重复摄取同一文档不产生重复记录                       |
| 空表索引            | HNSW 而非 ivfflat             | ivfflat 需要先有数据才能建索引                       |
| 全删防护            | `delete({})` 抛 `ValueError`  | 防止误传空 filter 导致全表删除                       |
| score 方向          | `1 - cosine_distance`         | 统一语义：score 越高越相关，调用方无需感知距离方向   |
| 浏览方法不强制实现  | `raise NotImplementedError`   | 接口最小化，Dashboard 专用，不强迫所有后端实现       |
