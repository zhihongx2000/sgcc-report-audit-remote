# DEV_SPEC - 电能质量报告审查系统开发规范

## 1. 项目概述

### 1.1 业务需求

本项目用于审查电能质量评估报告，输入为 `WORD/PDF` 报告文件，输出为结构化审查结果。审查结果需覆盖 20 个审查要点，并给出每一项的:

- 判定结果: `满足/不满足/需人工复核`
- 判定说明: 为什么这么判
- 证据定位: 来自报告的页码、段落、截图或表格引用

项目需支持的典型干扰源与关注指标见表 1。

表 1 典型电能质量干扰源及主要关注指标

| 评价对象 (也称为“干扰源”) | 主要扰动设备               | 所属行业         | 主要关注的电能质量指标                   |
| :------------------------ | :------------------------- | :--------------- | :--------------------------------------- |
| 电气化铁路用户            | 电力机车                   | 交通             | 谐波、负序、电压偏差                     |
| 陆地风电场                | 风力发电设备               | 电力             | 谐波、电压波动和闪变                     |
| 海上风电场                | 风力发电设备               | 电力             | 谐波、电压偏差、电压波动和闪变、谐波谐振 |
| 光伏电站                  | 光伏发电设备               | 电力             | 谐波、电压波动和闪变                     |
| 城市轨道交通用户          | 有轨及无轨电车、地铁、轻轨 | 交通             | 谐波、电压波动和闪变                     |
| 冶炼用户                  | 交流电弧炉                 | 冶金、机械       | 谐波、电压波动和闪变、负序               |
| 冶炼用户                  | 中频炉                     | 冶金、机械、化工 | 谐波、电压波动和闪变                     |
| 冶炼用户                  | 直流电弧炉、精炼炉         | 冶金、机械       | 谐波、电压波动和闪变                     |
| 冶炼用户                  | 交、直流轧机、大型电动机   | 冶金             | 谐波、电压波动和闪变                     |
| 储能电站                  | 变流器、逆变器             | 电力             | 谐波                                     |

审查覆盖的 20 个要点见表 2-1。

表 2-1 评估报告审查要点

| 序号 | 审查要点       | 具体要求                                                                                                                                                                                                                                                                 | 是否满足 |
| :--- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- |
| 1    | 评估单位       | 评估单位需提供资质证明文件，如 CNAS 电能质量相关资质或 CMA 电能质量相关资质或工程咨询或设计资质等，资质在有效期内。                                                                                                                                                      |          |
| 2    | 报告审批       | 报告封面应注明评估报告出具单位并加盖公章，应有评估报告编写人员、审批人员签名。                                                                                                                                                                                           |          |
| 3    | 评估依据       | 报告应说明评估依据的标准、规范、文件。                                                                                                                                                                                                                                   |          |
| 4    | 用户接入信息   | 报告应说明用户接入容量、接入系统方案、并网线路参数。                                                                                                                                                                                                                     |          |
| 5    | 用户设备参数   | 报告应提供用户内部电气接线情况、用户侧变压器(如有)等主设备参数。                                                                                                                                                                                                         |          |
| 6    | 用户干扰源特性 | 报告应提供主要干扰源设备的试验报告、检测报告或同类型、同容量设备的典型参数。                                                                                                                                                                                             |          |
| 7    | 原始提资资料   | 报告应提供原始提资资料，原始资料需加盖委托方或用户公章。                                                                                                                                                                                                                 |          |
| 8    | 电网设备信息   | 报告应说明接入变电站情况，提供电网侧变电站变压器等主设备参数。                                                                                                                                                                                                           |          |
| 9    | 电网容量信息   | 报告应说明公共连接点最小短路容量和供电设备容量。                                                                                                                                                                                                                         |          |
| 10   | 评估指标       | 报告应说明评估的电能质量指标，应至少包含表 1 所列的评估指标。                                                                                                                                                                                                            |          |
| 11   | 指标限值       | 电能质量评估指标限值选取应符合 GB/T 14549 《电能质量 公用电网谐波》、 GB/T 12325 《电能质量 供电电压偏差》、 GB/T 15543 《电能质量 三相电压不平衡》、 GB/T 12326 《电能质量 电压波动和闪变》等国标相关要求。其中谐波电流限值与闪变限值应通过修正计算求取，可参考表 2-2。 |          |
| 12   | 背景测试       | 报告应提供电能质量背景测试数据，并说明数据来源。                                                                                                                                                                                                                         |          |
| 13   | 叠加计算       | 背景测试数据需要与计算结果进行叠加计算，可参考表 2-2。当用户为海上风电时，背景谐波应采用仿真叠加方式。                                                                                                                                                                   |          |
| 14   | 仿真模型       | 谐波评估部分应附仿真软件建模界面截图、软件计算结果截图，截图中显示的结果数值应与评估结论一致，可参考图 1。                                                                                                                                                               |          |
| 15   | 评估考核点     | 评估考核点应为公共连接点。                                                                                                                                                                                                                                               |          |
| 16   | 运行方式       | 评估时应考虑负荷投产年、达产年系统正常运行的最小方式(或较小方式)。                                                                                                                                                                                                       |          |
| 17   | 计算结果       | 报告应说明各指标计算结果。                                                                                                                                                                                                                                               |          |
| 18   | 评估结论       | 报告应给出明确的评估结论，评估结论和计算结果应相互匹配。                                                                                                                                                                                                                 |          |
| 19   | 治理建议       | 评估结果超出限值时，报告应提出相应的电能质量治理措施和建议，常用措施可参考表 3。若评估结论未超标该项得满分。                                                                                                                                                             |          |
| 20   | 监测建议       | 报告应提出电能质量监测建议。                                                                                                                                                                                                                                             |          |

### 1.2 设计理念

- 本地优先: 默认单机部署，降低环境依赖。
- 可解释优先: 每个审查结论都必须可追溯到证据。
- 配置优先: 通过 `settings.yaml` 切换模型、检索策略和组件实现。
- 可插拔优先: LLM/Embedding/Reranker/VectorStore/Splitter/Evaluator 全部可替换。
- 教学友好: 模块边界清晰、示例完整、便于录制课程和面试讲解。

### 1.3 项目定位

- 生产可用的电能质量报告审查后端与可视化前端。
- 面向学习与面试的实战项目模板。
- 同时提供 MCP Server 能力，作为统一能力入口。

### 1.4 项目意义

希望通过这个项目，掌握`AI Coding`驱动的一整套工程化思路：

- 如何编写 DEV_SPEC (开发规格文档) 来驱动开发，AI Prompt具体见[GENERATE_SPEC](./GENERATE_SPEC.md) 。
- 如何使用`skill-creator`创造`agent skills`。
- 如何用`skill`基于`DEV_SPEC`自动完成代码编写
- 如何使用`skill`进行自动化测试、打包、环境配置。
- 如何基于可插拔架构进行扩展

### 1.5 核心能力一览

| 模块                | 能力                                                         | 说明                                                                                                                                                                                                         |
| ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Ingestions Pipeline | PDF -> Markdown -> Chunk -> Transform -> Embedding -> Upsert | 全链路数据摄取，支持多模态图片描述（Image Caption）                                                                                                                                                          |
| Hybrid Search       | Dense(向量) + Sparse(BM25) + RRF Fusion + Rerank             | 粗排召回+精排重排的两段式检索架构                                                                                                                                                                            |
| MCP Server          | 标注 MCP 协议暴露 Tools                                      | `query_knowledge_hub(query,filters)`,`list_collections()`,`get_document_summary(document_id)`,`ingest_document(file_path, metadata)`,`retrieve_context(query, top_k, filters)`,`reindex_document(file_path)` |
| Dashboard           | Vue + Vite 页面管理平台                                      | 电能质量报告审查/数据浏览/Ingestion管理/摄取追踪/查询追踪/评估面板                                                                                                                                           |
| Evaluation          | Ragas + Custom 评估体系                                      | 支持 golden test set 回归测试，拒绝"凭感觉"调优                                                                                                                                                              |
| Observability       | 全链路白盒化追踪                                             | Ingestion 与 Query 两条链路的每一个中间状态透明可见                                                                                                                                                          |

## 2. 核心特点

1. 智能分块与多层次召回:

- 语义分块 + 父子文档机制。
- 命中同一父文档子块数超过阈值 `k=3` 时直接召回父文档。

2. 混合检索与融合:

- BM25(稀疏) + Dense Embedding(稠密) 双路召回。
- 使用 RRF 融合减少单路偏差。

3. 两段式重排:

- 粗排后执行 Cross-Encoder 或 LLM Rerank 精排。
- 支持按场景切换低成本/高精度模式。

4. 多模态增强(轻量方案):

- 采用 Image-to-Text，将图表/截图转文本注入 chunk。
- 不引入 CLIP 向量链路，降低复杂度。

5. 全链路可观测性:

- Ingestion/Query 全链路 Trace。
- 结构化 JSON Lines 日志 + 自研 Vue Dashboard。

6. 可插拔评估体系:

- 支持 Ragas 与自定义指标(hit_rate、MRR、coverage、groundedness)。

7. MCP 原生集成:

- 基于 Python 官方 MCP SDK。
- 使用 `Stdio Transport`，适配本地子进程模式。

---

## 3. 技术选型

### 3.1 总体技术栈

- 后端: `Python 3.11+`, `FastAPI`, `Pydantic`, `SQLAlchemy`
- RAG 框架: 自研 文件解析、LLM/Embedding/Reranker模型接入等模块
- 向量库: `PostgreSQL + PgVector`(首期唯一实现)
- 前端: `Vue 3 + Vite + TypeScript + Pinia + Vue Router`
- 测试: `pytest` + `pytest-asyncio` + `httpx` + `Playwright`
- 通信: MCP `Stdio Transport`，不做 HTTP MCP 部署

### 3.2 RAG 核心流水线设计

#### 3.2.1 Ingestion Pipeline

**目标：**

构建统一、可配置、可观测的数据摄取流水线，涵盖文档加载、格式解析、语义切分、多模态增强、嵌入计算、去重与批量上传到向量存储功能。该数据摄取流水线是可重用的库模块，便于在Dashboard管理面板、离线批处理和测试中调用。

**特点：**

- 采用自研的数据摄取Pipeline框架，设计灵感参考LlamaIndex分层思想，但不依赖LlamaIndex库
- 定义自定义的抽象接口(`BaseLoader`/`BaseSplitter`/`BaseTransform`/`BaseEmbedding`/`BaseVectorStore`)，实现完全可插拔架构。
- 支持可随机组合的 `Loader -> Splitter -> Transform -> Embed -> Upsert`流程，便于实现可观测的流水线。

**设计要点：**

- 明确分层职责：
  - Loader：负责把原始文件解析为统一的 `Document` 对象(`text` + `metadata`；类型定义集中在 `src/core/types.py`)。在当前阶段，仅实现 PDF、Word 格式的 Loader。
  - 统一输出格式采用规范化 Markdown作为 Document.text，这样可以更好的配合后面的Splitter(Langchain RecursiveCharacterTextSplitte)方法产出高质量切块。
  - Loader 同时抽取/补齐基础 metadata(如 `source_path`, `doc_type=pdf/dox/docx`, `page`, `title/heading_outline`, `images` 引用列表等)，为定位、回溯与后续 Transform 提供依据。
    - Splitter：基于 Markdown 结构（标题/段落/代码块等）与参数配置把 Document 切为若干 Chunk，保留原始位置与上下文引用。
    - Transform：可插入的处理步骤(`ImageCaptioning`、`OCR`、`code-block normalization`、`html-to-text cleanup` 等)，Transform 可以选择把额外信息追加到 `chunk.text` 或放入 `chunk.metadata`(推荐默认追加到 text 以保证检索覆盖)。
    - Embed & Upsert：按批次计算 embedding，并上载到向量存储；支持向量 + metadata 上载，并提供幂等 upsert 策略(基于 id/hash)。
    - Dedup & Normalize：在上载前运行向量/文本去重与哈希过滤，避免重复索引。

**关键实现要素：**

- Loader（统一格式与元数据）
  - **前置去重 (Early Exit / File Integrity Check)**：
    - 机制：在解析文件前，计算原始文件的 SHA256 哈希指纹。
    - 动作：检索 `ingestion_history` 表，若发现相同 Hash 且状态为 `success` 的记录，则认定该文件未发生变更，直接跳过后续所有处理（解析、切分、LLM重写），实现**零成本 (Zero-Cost)** 的增量更新。
    - **存储方案**（初期实现，可插拔）：
      - **默认选择：PostgreSQL**，数据库连接配置从`setting.yaml`读取。
      - **表结构**：
        ```sql
        CREATE TABLE ingestion_history (
            file_hash TEXT PRIMARY KEY,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            status TEXT NOT NULL CHECK(status IN ('success', 'failed', 'processing')),
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            error_msg TEXT,
            chunk_count INTEGER
        );
        CREATE INDEX idx_status ON ingestion_history(status);
        CREATE INDEX idx_processed_at ON ingestion_history(processed_at);
        ```
      - **查询逻辑**：`SELECT status FROM ingestion_history WHERE file_hash = ? AND status = 'success'`
      - **替换路径**：后续可增加 Redis（分布式缓存）实现。

  > **📌 持久化存储架构统一说明**
  >
  > 本项目在多个核心模块中采用 **PostgreSQL** 作为企业级持久化存储方案，保持本地优先（Local-First）的设计理念：
  >
  > | 存储模块            | 数据库文件            | 用途                                             | 表结构关键字段                        |
  > | ------------------- | --------------------- | ------------------------------------------------ | ------------------------------------- |
  > | **文件完整性检查**  | `ingestion_history`表 | 记录已处理文件的 SHA256 哈希，实现增量摄取       | `file_hash`, `status`, `processed_at` |
  > | **图片索引映射**    | `image_index`表       | 记录 image_id → 文件路径映射，支持图片检索与引用 | `image_id`, `file_path`, `collection` |
  > | **BM25 索引元数据** | `bm25`表              | 存储倒排索引和 IDF 统计信息                      |                                       |
  >
  > **设计优势**：
  >
  > - **并发安全**：WAL (Write-Ahead Logging) 模式支持多进程安全读写
  > - **持久化保证**：摄取历史和索引映射在进程重启后自动恢复，避免重复计算
  > - **架构一致性**：所有 PostgreSQL 模块遵循相同的初始化、查询与错误处理模式，便于维护与扩展
  >
  > **升级路径**：可添加Redis中间层，无需修改上层业务逻辑。
  - **解析与标准化**：
    - 当前范围：**仅实现 PDF/WORD(`.doc`，`.docx`) -> canonical Markdown 子集** 的转换。
  - 技术选型（Python PDF -> Markdown）：
    - **首选：MarkItDown**（作为默认 PDF 解析/转换引擎）。优点是直接产出 Markdown 形态文本，且解析速度快，便于与后续 `RecursiveCharacterTextSplitter` 的 separators 配合。
  - 输出标准 `Document`：`id|source|text(markdown)|metadata`。metadata 至少包含 `source_path`, `doc_type`, `title/heading_outline`, `page/slide`（如适用）, `images`（图片引用列表）。
  - Loader 不负责切分：只做“格式统一 + 结构抽取 + 引用收集”，确保切分策略可独立迭代与度量。

- Splitter（LangChain 负责切分；独立、可控）
  - **实现方案：使用 LangChain 的 `RecursiveCharacterTextSplitter` 进行切分。**
    - 优势：该方法对 Markdown 文档的结构（标题、段落、列表、代码块）有天然的适配性，能够通过配置语义断点（Separators）实现高质量、语义完整的切块。
  - Splitter 输入：Loader 产出的 Markdown `Document`。
  - Splitter 输出：若干 `Chunk`（或 Document-like chunks），每个 chunk 必须携带稳定的定位信息与来源信息：`source`, `chunk_index`, `start_offset/end_offset`（或等价定位字段）。

- Transform & Enrichment（结构转换与深度增强）
  本阶段是 ETL 管道的核心“智力”环节，负责将 Splitter 产出的非结构化文本块转化为结构化、富语义的智能切片(Smart Chunk)，即丰富切片的信息。
  - **结构转换 (Structure Transformation)**：将原始的 `String` 类型数据转化为强类型的 `Record/Object`，为下游检索提供字段级支持。
  - **核心增强策略**：
    1. **智能重组 (Smart Chunking & Refinement)**：
       - 策略：利用 LLM 的语义理解能力，对上一阶段“粗切分”的片段进行二次加工。
       - 动作：合并在逻辑上紧密相关但被物理切断的段落，剔除无意义的页眉页脚或乱码（去噪），确保每个 Chunk 是自包含（Self-contained）的语义单元。
    2. **语义元数据注入 (Semantic Metadata Enrichment)**：
       - 策略：在基础元数据（路径、页码）之上，利用 LLM 提取高维语义特征。
       - 产出：为每个 Chunk 自动生成 `Title`（精准小标题）、`Summary`（内容摘要）和 `Tags`（主题标签），并将其注入到 Metadata 字段中，支持后续的混合检索与精确过滤。
    3. **多模态增强 (Multimodal Enrichment / Image Captioning)**：
       - 策略：扫描文档片段中的图像引用，调用 Vision LLM（如 Qwen-VL）进行视觉理解。
       - 动作：生成准确的文本描述（Caption），描述图表逻辑或提取截图文字。
       - 存储：将 Caption 文本“缝合”进 Chunk 的正文或 Metadata 中，打通模态隔阂，实现“搜文出图”。
  - **工程特性**：Transform 步骤设计为原子化与幂等操作，支持针对特定 Chunk 的独立重试与增量更新，避免因 LLM 调用失败导致整个文档处理中断。

- **Embedding (双路向量化)**
  - **差量计算 (Incremental Embedding / Cost Optimization)**：
    - 策略：在调用昂贵的 Embedding API 之前，计算 Chunk 的内容哈希（Content Hash）。仅针对数据库中不存在的新内容哈希执行向量化计算，对于文件名变更但内容未变的片段，直接复用已有向量，显著降低 API 调用成本。
  - **核心策略**：为了支持高精度的混合检索（Hybrid Search），系统对每个 Chunk 并行执行双路编码计算。
    - **Dense Embeddings（语义向量）**：调用 Embedding 模型（如 OpenAI text-embedding-3 或 BGE）生成高维浮点向量，捕捉文本的深层语义关联，解决“词不同意同”的检索难题。
    - **Sparse Embeddings（稀疏向量）**：利用 BM25 编码器或 SPLADE 模型生成稀疏向量（Keyword Weights），捕捉精确的关键词匹配信息，解决专有名词查找问题。
  - **批处理优化**：所有计算均采用 `batch_size` 驱动的批处理模式，最大化 CPU 利用率并减少网络 RTT。

- **Upsert & Storage (索引存储)**
  - **存储后端**：统一使用向量数据库（如 PgVector）作为存储引擎，同时持久化存储 Dense Vector、Sparse Vector 以及 Transform 阶段生成的富 Metadata。
  - **All-in-One 存储策略**：执行原子化存储，每条记录同时包含：
    1. **Index Data**: 用于计算相似度的 Dense Vector 和 Sparse Vector。
    2. **Payload Data**: 完整的 Chunk 原始文本 (Content) 及 Metadata。
       **机制优势**：确保检索命中 ID 后能立即取回对应的正文内容，无需额外的查库操作 (Lookup)，保障了 Retrieve 阶段的毫秒级响应。

- **幂等性设计 (Idempotency)**：
  - 为每个 Chunk 生成全局唯一的 `chunk_id`，生成算法采用确定的哈希组合：`hash(source_path + heading_path + relative_chunk_index)`。其中，`heading_path + relative_chunk_index`表示相对于标题的逻辑定位。
  - 写入时采用 "Upsert"（更新或插入）语义，确保同一文档即使被多次处理，数据库中也永远只有一份最新副本，彻底避免重复索引问题。
  - **原子性保证**：以 Batch 为单位进行事务性写入，确保索引状态的一致性。

- **文档生命周期管理 (Document Lifecycle Management)**

  为支持 Dashboard 管理面板中的文档浏览与删除功能，Ingestion 层需要提供完整的文档生命周期管理能力：
  - **DocumentManager（文档管理器）**：独立于 Pipeline 的文档管理模块（`src/ingestion/document_manager.py`），负责跨存储的协调操作：
    - `list_documents(collection?) -> List[DocumentInfo]`：列出已摄入文档及其统计信息（chunk 数、图片数、摄入时间）。
    - `get_document_detail(doc_id) -> DocumentDetail`：获取单个文档的详细信息（所有 chunk 内容、metadata、关联图片）。
    - `delete_document(source_path, collection) -> DeleteResult`：协调删除跨 4 个存储的关联数据：
      1.  **PgVector** — 按 `metadata.source` 删除所有 chunk 向量
      2.  **BM25 Indexer** — 移除对应文档的倒排索引条目
      3.  **ImageStorage** — 删除该文档关联的所有图片文件
      4.  **FileIntegrity** — 移除处理记录，使文件可重新摄入
    - `get_collection_stats(collection?) -> CollectionStats`：返回集合级统计（文档数、chunk 数、存储大小等）。

  - **Pipeline 进度回调 (Progress Callback)**：在 `IngestionPipeline.run()` 方法中新增可选 `on_progress` 参数：

    ```python
    def run(self, source_path: str, collection: str = "default",
            on_progress: Callable[[str, int, int], None] | None = None) -> IngestionResult:
    ```

    - 回调签名：`on_progress(stage_name: str, current: int, total: int)`
    - 各阶段（load / split / transform / embed / upsert）在处理每个 batch 时调用回调，Dashboard 据此展示实时进度条。
    - `on_progress` 为 `None` 时行为与当前完全一致，不影响 CLI 和测试场景。

  - **存储层接口扩展**：为支持 DocumentManager 的删除操作，需扩展以下存储接口：
    - `BaseVectorStore` 新增 `delete_by_metadata(filter: dict) -> int` — 按 metadata 条件批量删除
    - `BM25Indexer` 新增 `remove_document(source: str) -> None` — 移除指定文档的索引条目
    - `FileIntegrityChecker` 新增 `remove_record(file_hash: str) -> None` 和 `list_processed() -> List[dict]`

#### 3.2.2 Retrieval Pipeline检索流水线

本模块实现核心的 RAG 检索引擎，采用 **“多阶段过滤 (Multi-stage Filtering)”** 架构，负责接收已消歧的独立查询（Standalone Query），并精准召回 Top-K 最相关片段。

- **Query Processing (查询预处理)**
  - **核心假设**：输入 Query 已由上游（Client/MCP Host）完成会话上下文补全（De-referencing），不仅如此，还进行了指代消歧。
  - **查询转换 (Transformation) 与扩张策略 (Expansion Strategy)**：
    - **Keyword Extraction**：利用 NLP 工具提取 Query 中的关键实体与动词（去停用词），生成用于稀疏检索的 Token 列表。
    - **Query Expansion **：
      - 系统可做 Synonym/Alias Expansion（同义词/别名/缩写扩展），默认策略采用“**扩展融入稀疏检索、稠密检索保持单次**”以控制成本与复杂度。
      - 系统可提供`假设性文档嵌入（Hypothetical Document Embeddings）`开关，使得系统在面对复杂的专业领域知识时，可捕捉更深层次的查询意图。
      - **Sparse Route (BM25)**：将“关键词 + 同义词/别名”合并为一个查询表达式（逻辑上按 `OR` 扩展），**只执行一次稀疏检索**。原始关键词可赋予更高权重以抑制语义漂移。
      - **Dense Route (Embedding)**：使用原始 query（或轻度改写后的语义 query）生成 embedding，**只执行一次稠密检索**；默认不为每个同义词单独触发额外的向量检索请求。

  - **Hybrid Search Execution (双路混合检索)**
    - **并行召回 (Parallel Execution)**：
      - **Dense Route**：计算 Query Embedding -> 检索向量库（Cosine Similarity）-> 返回 Top-N 语义候选。
      - **Sparse Route**：使用 BM25 算法 -> 检索倒排索引 -> 返回 Top-N 关键词候选。
    - **结果融合 (Fusion)**：
      - 采用 **RRF (Reciprocal Rank Fusion)** 算法，不依赖各路分数的绝对值，而是基于排名的倒数进行加权融合。
      - 公式策略：`Score = 1 / (k + Rank_Dense) + 1 / (k + Rank_Sparse)`，平滑因单一模态缺陷导致的漏召回。

  - **Filtering & Reranking (精确过滤与重排)**
    - **Metadata Filtering Strategy (通用过滤策略)**：
      - **原则：先解析、能前置则前置、无法前置则后置兜底。**
      - Query Processing 阶段应将结构化约束解析为通用 `filters`（例如 `collection`/`doc_type`/`language`/`time_range`/`access_level` 等）。
      - 若底层索引支持且属于硬约束（Hard Filter），则在 Dense/Sparse 检索阶段做 Pre-filter 以缩小候选集、降低成本。
      - 无法前置的过滤（索引不支持或字段缺失/质量不稳）在 Rerank 前统一做 Post-filter 作为 safety net；对缺失字段默认采取“宽松包含”(missing->include) 以避免误杀召回。
      - 软偏好（Soft Preference，例如“更近期更好”）不应硬过滤，而应作为排序信号在融合/重排阶段加权。
    - **Rerank Backend (可插拔精排后端)**：
      - **目标**：在 Top-M 候选上进行高精度排序/过滤；该模块必须可关闭，并提供稳定回退策略。
      - **后端选项**：
        1.  **None (关闭精排)**：直接返回融合后的 Top-K（RRF 排名作为最终结果）。
        2.  **Cross-Encoder Rerank (本地/托管模型)**：输入为 `[Query, Chunk]` 对，输出相关性分数并排序；适合稳定、结构化输出。CPU 环境下建议默认仅对较小的 Top-M 执行（例如 M=10~30），并提供超时回退。
        3.  **LLM Rerank (可选)**：使用 LLM 对候选集排序/选择；适合需要更强指令理解或无本地模型环境时。为控制成本与稳定性，候选数应更小（例如 M<=20），并要求输出严格结构化格式（如 JSON 的 ranked ids）。
      - **默认与回退 (Fallback)**：
        - 默认策略面向通用框架与 CPU 环境：优先保证“可用与可控”，Cross-Encoder/LLM 均为可选增强。
        - 当精排不可用/超时/失败时，必须回退到融合阶段的排序（RRF Top-K），确保系统可用性与结果稳定性。

### 3.3 MCP 服务设计(MCP Service Design)

**目标：** 设计并实现一个符合 Model Context Protocol (MCP) 规范的 Server，使其能够作为知识上下文提供者，无缝对接主流 MCP Clients（如 GitHub Copilot、Claude Desktop 等），在本项目中，该 MCP Server为电能质量报告审查提供数据处理等核心后端能力。

#### 3.3.1 核心设计理念

- **协议优先 (Protocol-First)**：严格遵循 MCP 官方规范（JSON-RPC 2.0），确保与任何合规 Client 的互操作性。
- **开箱即用 (Zero-Config for Clients)**：Client 端无需任何特殊配置，只需在配置文件中添加 Server 连接信息即可使用全部功能。
- **引用透明 (Citation Transparency)**：所有检索结果必须携带完整的来源信息，支持 Client 端展示"回答依据"，增强用户对 AI 输出的信任。
- **多模态友好 (Multimodal-Ready)**：返回格式应支持文本与图像等多种内容类型，为未来的富媒体展示预留扩展空间。

#### 3.3.2 传输协议：Stdio 本地通信

本项目采用 **Stdio Transport** 作为唯一通信模式。

- **工作方式**：Client（VS Code Copilot、Claude Desktop）以子进程方式启动我们的 Server，双方通过标准输入/输出交换 JSON-RPC 消息。
- **选型理由**：
  - **零配置**：无需网络端口、无需鉴权，用户只需在 Client 配置文件中指定启动命令即可使用。
  - **隐私安全**：数据不经过网络，天然适合处理私有知识库与敏感业务数据。
  - **契合定位**：Stdio 完美适配开发者本地工作流，满足私有知识管理与快速原型验证需求。
- **实现约束**：
  - `stdout` 仅输出合法 MCP 消息，禁止混入任何日志或调试信息。
  - 日志统一输出至 `stderr`，避免污染通信通道。

#### 3.3.3 SDK 与实现库选型

- **首选：Python 官方 MCP SDK (`mcp`)**
  - **优势**：
    - 官方维护，与协议规范同步更新，保证最新特性支持（如 `outputSchema`、`annotations` 等）。
    - 提供 `@server.tool()` 等装饰器，声明式定义 Tools/Resources/Prompts，代码简洁。
    - 内置 Stdio 与 HTTP Transport 支持，无需手动处理 JSON-RPC 序列化与生命周期管理。
  - **适用**：本项目的默认实现方案。

- **备选：FastAPI + 自定义协议层**
  - **场景**：需要深度定制 HTTP 行为（如自定义中间件、复杂鉴权流程）或希望学习 MCP 协议底层细节时可考虑。
  - **权衡**：开发成本更高，需自行实现能力协商 (Capability Negotiation)、错误码映射等，且需持续跟进协议版本更新。

- **协议版本**：跟踪 MCP 最新稳定版本（如 `2025-06-18`），在 `initialize` 阶段进行版本协商，确保 Client/Server 兼容性。

#### 3.3.4 对外暴露的工具函数设计 (Tools Design)

Server 通过 `tools/list` 向 Client 注册可调用的工具函数。工具设计应遵循"单一职责、参数明确、输出丰富"原则。

- **核心工具集**：

| 工具名称                 | 功能描述                                          | 典型输入参数                                          | 输出特点                   |
| ------------------------ | ------------------------------------------------- | ----------------------------------------------------- | -------------------------- |
| `query_knowledge_hub`    | 主检索入口，执行混合检索 + Rerank，返回最相关片段 | `query: string`, `top_k?: int`, `collection?: string` | 返回带引用的结构化结果     |
| `list_collections`       | 列举知识库中可用的文档集合                        | 无                                                    | 集合名称、描述、文档数量   |
| `get_document_summary`   | 获取指定文档的摘要与元信息                        | `doc_id: string`                                      | 标题、摘要、创建时间、标签 |
| `verify_answer`          | 事实核查工具，检测生成内容是否有依据支撑。        | `query:string`,</br>`answer:string`                   | 返回支持生成内容的事实依据 |
| `list_document_sections` | 浏览文档目录结构，支持多步导航式检索。            | `source`                                              |                            |

#### 3.3.5 返回内容与引用透明设计 (Response & Citation Design)

MCP 协议的 Tool 返回格式支持多种内容类型（`content` 数组），本项目将充分利用这一特性实现"可溯源"的回答：

- **结构化引用设计**：
  - 每个检索结果片段应包含完整的定位信息：`source_file`（文件名/路径）、`page`（页码，如适用）、`chunk_id`（片段标识）、`score`（相关性分数）。
  - 推荐在返回的 `structuredContent` 中采用统一的 Citation 格式：
    ```
    {
      "answer": "...",
      "citations": [
        { "id": 1, "source": "xxx.pdf", "page": 5, "text": "原文片段...", "score": 0.92 },
        ...
      ]
    }
    ```
  - 同时在 `content` 数组中以 Markdown 格式呈现人类可读的带引用回答（`[1]` 标注），保证 Client 无论是否解析结构化内容都能展示引用。

- **多模态内容返回**：
  - **文本内容 (TextContent)**：默认返回类型，Markdown 格式，支持代码块、列表等富文本。
  - **图像内容 (ImageContent)**：当检索结果关联图像时，Server 读取本地图片文件并编码为 Base64 返回。
    - **格式**：`{ "type": "image", "data": "<base64>", "mimeType": "image/png" }`
    - **工作流程**：数据摄取阶段存储图片本地路径 → 检索命中后 Server 动态读取 → 编码为 Base64 → 嵌入返回消息。
    - **Client 兼容性**：图像展示能力取决于 Client 实现，GitHub Copilot 可能降级处理，Claude Desktop 支持完整渲染。Server 端统一返回 Base64 格式，由 Client 决定如何渲染。

### 3.4 可插拔架构设计

**目标：** 定义清晰的抽象层与接口契约，使 RAG 链路的每个核心组件都能够独立替换与升级，避免技术锁定，支持低成本的 A/B 测试与环境迁移。

> **术语说明**：本节中的"提供者 (Provider)"、"实现 (Implementation)"指的是完成某项功能的**具体技术方案**，而非传统 Web 架构中的"后端服务器"。例如，LLM 提供者可以是远程的 Qwen API，也可以是本地运行的 vLLM；向量存储可以是本地嵌入式的 PgVector，也可以是云端托管的 Pinecone。本项目作为本地 MCP Server，通过统一接口对接这些不同的提供者，实现灵活切换。

#### 3.4.1 设计原则

- **接口隔离 (Interface Segregation)**：为每类组件定义最小化的抽象接口，上层业务逻辑仅依赖接口而非具体实现。
- **配置驱动 (Configuration-Driven)**：通过统一配置文件（如 `settings.yaml`）指定各组件的具体后端，代码无需修改即可切换实现。
- **工厂模式 (Factory Pattern)**：使用工厂函数根据配置动态实例化对应的实现类，实现"一处配置，处处生效"。
- **优雅降级 (Graceful Fallback)**：当首选后端不可用时，系统应自动回退到备选方案或安全默认值，保障可用性。

**通用结构示意（适用于 3.4.2 / 3.4.3 / 3.4.4 等可插拔组件）**：

```
业务代码
  │
  ▼
<Component>Factory.get_xxx()  ← 读取配置，决定用哪个实现
  │
  ├─→ ImplementationA()
  ├─→ ImplementationB()
  └─→ ImplementationC()
      │
      ▼
    都实现了统一的抽象接口
```

#### 3.4.2 LLM 与 Embedding 提供者抽象

这是可插拔设计的核心环节，因为模型提供者的选择直接影响成本、性能与隐私合规。

- **统一接口层 (Unified API Abstraction)**：
  - **设计思路**：无论底层使用 Azure OpenAI、OpenAI 原生 API、DeepSeek 还是本地 Ollama，上层调用代码应保持一致。
  - **关键抽象**：
    - `LLMClient`：暴露 `chat(messages) -> response` 方法，屏蔽不同 Provider 的认证方式与请求格式差异。
    - `EmbeddingClient`：暴露 `embed(texts) -> vectors` 方法，统一处理批量请求与维度归一化。

- **提供者选项与切换场景**：

| 提供者类型               | 典型场景                                   | 配置切换点                                                   |
| ------------------------ | ------------------------------------------ | ------------------------------------------------------------ |
| **Azure OpenAI**         | 企业合规、私有云部署、区域数据驻留         | `provider: azure`, `endpoint`, `api_key`, `deployment_name`  |
| **OpenAI 原生**          | 通用开发、最新模型尝鲜                     | `provider: openai`, `api_key`, `model`                       |
| **DeepSeek / 其他云端**  | 成本优化、特定语言优化                     | `provider: deepseek`, `api_key`, `model`                     |
| **Ollama / vLLM (本地)** | 完全离线、隐私敏感、无 API 成本            | `provider: ollama`, `base_url`, `model`                      |
| **OpenAI-Compatible**    | 面向国内的AI提供者，兼容OpenAI接口方式接入 | `provider: openai-compatible`, `base_url`, `model`,`api_key` |

- **技术选型建议**：
  - 本项目采用自研的 `BaseLLM` / `BaseEmbedding` 抽象基类，配合工厂模式（`llm_factory.py` / `embedding_factory.py`）实现统一调用接口。已内置 Azure OpenAI、OpenAI、Ollama、DeepSeek 四种 Provider 适配。
  - 对于其他 Provider，可通过 **OpenAI-Compatible 模式**接入（设置自定义 `api_base`），或实现 `BaseLLM` 接口并在工厂中注册。

  - 对于企业级需求，可在其基础上增加统一的 **重试、限流、日志** 中间层，提升生产可靠性，但本项目暂不实现，这里仅提供思路。
  - **Vision LLM 扩展**：针对图像描述生成（Image Captioning）需求，系统扩展了 `BaseVisionLLM` 接口，支持文本+图片的多模态输入。当前实现：
    - **Azure OpenAI Vision**（GPT-4o/GPT-4-Vision）：企业级合规部署，支持复杂图表解析，与 Azure 生态深度集成。
    - **Qwen2.5-VL(vLLM)**：本地部署vLLM，符合合规性要求

#### 3.4.3 检索策略抽象

检索层的可插拔性决定了系统在不同数据规模与查询模式下的适应能力。

**设计模式：抽象工厂模式**

与 3.4.2 节的 LLM 抽象类似，检索层各组件的可插拔性同样依赖两层设计：

1. **自研的统一抽象接口**：本项目为向量数据库（`BaseVectorStore`）、Embedding（`BaseEmbedding`）、分块（`BaseSplitter`）等核心组件定义了统一的抽象基类，不同实现只需遵循相同接口即可无缝替换。

2. **工厂函数路由**：每个抽象层配套工厂函数（如 `embedding_factory.py`、`splitter_factory.py`），根据 `settings.yaml` 中的配置字段自动实例化对应实现，实现"改配置不改代码"的切换体验。

通用的”配置驱动 + 工厂路由”结构示意见 3.4.1 节。

下面分别说明各组件如何应用这一模式：

---

**1. 分块策略 (Chunking Strategy)**

分块是 Ingestion Pipeline 的核心环节之一，决定了文档如何被切分为适合检索的语义单元。本项目的 Splitter 层采用可插拔设计（BaseSplitter 抽象接口 + SplitterFactory 工厂），不同分块实现只需遵循相同接口即可无缝替换。

常见的分块策略包括：

- **固定长度切分**：按字符数或 Token 数切分，简单但可能破坏语义完整性。
- **递归字符切分**：按层级分隔符（段落→句子→字符）递归切分，在长度限制内尽量保持语义边界。
- **语义切分**：利用 Embedding 相似度检测语义断点，确保每个 Chunk 是自包含的语义单元。
- **结构感知切分**：根据文档结构（Markdown 标题、代码块、列表等）进行切分。

本项目当前采用 **LangChain 的 `RecursiveCharacterTextSplitter`** 进行切分，该方法对 Markdown 文档的结构（标题、段落、列表、代码块）有天然的适配性，能够通过配置语义断点（Separators）实现高质量、语义完整的切块。

> **当前实现说明**：目前系统使用 LangChain RecursiveCharacterTextSplitter。架构设计上预留了切换能力，如需切换为 SentenceSplitter、SemanticSplitter 或自定义切分器，只需实现 BaseSplitter 接口并在配置中指定即可。

---

**2. 向量数据库 (Vector Store)**

本项目自定义了统一的 BaseVectorStore 抽象接口，暴露 .add()、.query()、.delete() 等方法。所有向量数据库后端（Chroma、Qdrant、Pinecone 等）只需实现该接口即可插拔替换，通过 VectorStoreFactory 根据配置自动选择具体实现。

本项目选用 **PgVector** 作为向量数据库。

> **当前实现说明**：目前系统仅实现了 PgVector 后端。虽然架构设计上预留了工厂模式以支持未来扩展，但当前版本尚未实现其他向量数据库的适配器。

---

**3. 向量编码策略 (Embedding Strategy)**

向量编码是 Ingestion Pipeline 的关键环节，决定了 Chunk 如何被转换为可检索的向量表示。本项目自定义了 BaseEmbedding 抽象接口（src/libs/embedding/base_embedding.py），支持不同 Embedding 模型的可插拔替换。

常见的编码策略包括：

- **纯稠密编码（Dense Only）**：仅生成语义向量，适合通用场景。
- **纯稀疏编码（Sparse Only）**：仅生成关键词权重向量，适合精确匹配场景。
- **双路编码（Dense + Sparse）**：同时生成稠密向量和稀疏向量，为混合检索提供数据基础。

本项目当前采用 **双路编码（Dense + Sparse）** 策略：

- **Dense Embeddings（语义向量）**：调用 Embedding 模型（如 OpenAI text-embedding-3）生成高维浮点向量，捕捉文本的深层语义关联。
- **Sparse Embeddings（稀疏向量）**：利用 BM25 编码器生成稀疏向量（Keyword Weights），捕捉精确的关键词匹配信息。

存储时，Dense Vector 和 Sparse Vector 与 Chunk 原文、Metadata 一起原子化写入向量数据库，确保检索时可同时利用两种向量。

> **当前实现说明**：目前系统实现了 Dense + Sparse 双路编码。架构设计上预留了切换能力，如需使用其他 Embedding 模型（如 BGE、Ollama 本地模型）或调整编码策略，可在 Pipeline 中替换相应组件。

---

**4. 召回策略 (Retrieval Strategy)**

召回策略决定了查询阶段如何从知识库中检索相关内容。基于 Ingestion 阶段存储的向量类型，可采用不同的召回方案：

- **纯稠密召回（Dense Only）**：仅使用语义向量进行相似度匹配。
- **纯稀疏召回（Sparse Only）**：仅使用 BM25 进行关键词匹配。
- **混合召回（Hybrid）**：并行执行稠密和稀疏两路召回，再通过融合算法合并结果。
- **混合召回 + 精排（Hybrid + Rerank）**：在混合召回基础上，增加精排步骤进一步提升相关性。

本项目当前采用 **混合召回 + 精排（Hybrid + Rerank）** 策略：

- **稠密召回（Dense Route）**：计算 Query Embedding，在向量库中进行 Cosine Similarity 检索，返回 Top-N 语义候选。
- **稀疏召回（Sparse Route）**：使用 BM25 算法检索倒排索引，返回 Top-N 关键词候选。
- **融合（Fusion）**：使用 RRF (Reciprocal Rank Fusion) 算法将两路结果合并排序。
- **精排（Rerank）**：对融合后的候选集进行重排序，支持 None / Cross-Encoder / LLM Rerank 三种模式。

> **当前实现说明**：目前系统实现了 Hybrid + Rerank 策略。架构设计上预留了策略切换能力，如需使用纯稠密或纯稀疏召回，可通过配置切换；融合算法和 Reranker 同样支持替换。

#### 3.4.4 评估框架抽象

评估体系的可插拔性确保团队可以根据业务目标灵活选择或组合不同的质量度量维度。

- **设计思路**：
  - 定义统一的 `Evaluator` 接口，暴露 `evaluate(query, retrieved_chunks, generated_answer, ground_truth) -> metrics` 方法。
  - 各评估框架实现该接口，输出标准化的指标字典。

- **可选评估框架**：

| 框架           | 特点                                                                       | 适用场景                          |
| -------------- | -------------------------------------------------------------------------- | --------------------------------- |
| **Ragas**      | RAG 专用、指标丰富（Faithfulness, Answer Relevancy, Context Precision 等） | 全面评估 RAG 质量、学术对比       |
| **DeepEval**   | LLM-as-Judge 模式、支持自定义评估标准                                      | 需要主观质量判断、复杂业务规则    |
| **自定义指标** | Hit Rate, MRR, Latency P99 等基础工程指标                                  | 快速回归测试、上线前 Sanity Check |

- **组合与扩展**：
  - 评估模块设计为**组合模式**，可同时挂载多个 Evaluator，生成综合报告。
  - 配置示例：`evaluation.backends: [ragas, custom]`，系统并行执行并汇总结果。

#### 3.4.5 配置管理与切换流程

- **配置文件结构示例** (`rag-server/config/settings.yaml`，精简版，完整版见 5.6.1)：

  ```yaml
  llm:
    provider: azure # azure | openai | deepseek | ollama | openai-compatible
    model: gpt-4o
    temperature: 0.1
    max_tokens: 2000
    timeout_sec: 60

  embedding:
    provider: openai # openai | azure | ollama | bge | openai-compatible
    model: text-embedding-3-small
    embedding_dim: 1536

  postgres:
    host: "${PG_HOST}"
    port: 5432
    database: "${PG_DATABASE}"
    user: "${PG_USER}"
    password: "${PG_PASSWORD}"
    schema: public
    sslmode: disable
    pool_size: 10
    pool_timeout_sec: 30
    statement_timeout_ms: 30000

  vector_store:
    backend: pgvector # 当前仅实现 pgvector，保留扩展位
    table: rag_chunks
    embedding_dim: 1536
    distance_metric: cosine
    enable_sparse_fields: true
    metadata_jsonb: true

  retrieval:
    mode: hybrid # dense | sparse | hybrid
    sparse_backend: bm25 # bm25
    fusion_algorithm: rrf # rrf | weighted_sum(预留)

  rerank:
    backend: cross_encoder # none | cross_encoder | llm
    model: bge-reranker-v2-m3

  evaluation:
    backends: [ragas, custom]

  observability:
    enabled: true
    sink: postgres # postgres | jsonl | both
    jsonl_mirror_enabled: true
    jsonl_file: "./logs/rag/traces.jsonl"
  ```

- **postgres 配置完整性检查（最低必需项）**：
  - 连接信息：`host`、`port`、`database`、`user`、`password`
  - 运行参数：`schema`、`sslmode`、`pool_size`、`pool_timeout_sec`、`statement_timeout_ms`
- **vector_store 配置完整性检查（最低必需项）**：
  - 存储定义：`backend=pgvector`、`table`、`embedding_dim`、`distance_metric`
  - 数据能力：`enable_sparse_fields`（混合检索）与 `metadata_jsonb`（过滤/审计）

- **切换流程**：
  1.  修改 `settings.yaml` 中对应组件的 `backend` / `provider` 字段。
  2.  确保新后端的依赖已安装、凭据已配置。
  3.  重启服务，工厂函数自动加载新实现，无需修改业务代码。

### 3.5 可观测性与可视化管理平台设计 (Observability & Visual Management Platform Design)

**目标：** 针对 RAG 系统常见的"黑盒"问题，设计全链路可观测的追踪体系与完整的可视化管理平台。覆盖 **Ingestion（摄取链路）** 与 **Query（查询链路）** 两条完整流水线的追踪记录，同时提供数据浏览、文档管理、组件概览等管理功能，使整个系统**透明可见**、**可管理**且**可量化**。

#### 3.5.1 设计理念

- **双链路全覆盖追踪 (Dual-Pipeline Tracing)**：
  - **Ingestion Trace**：以 `trace_id` 为核心，记录一次摄取从文件加载到存储完成的全过程（load → split → transform → embed → upsert），包含各阶段耗时、处理的 chunk 数量、跳过/失败详情。
  - **Query Trace**：以 `trace_id` 为核心，记录一次查询从 Query 输入到 Response 输出的全过程（query_processing → dense → sparse → fusion → rerank），包含各阶段候选数量、分数分布与耗时。
- **透明可回溯 (Transparent & Traceable)**：每个阶段的中间状态都被记录，开发者可以清晰看到"系统为什么召回了这些文档"、"Rerank 前后排名如何变化"，从而精准定位问题。
- **低侵入性 (Low Intrusiveness)**：追踪逻辑与业务逻辑解耦，通过 `TraceContext` 显式调用模式注入，避免污染核心代码。
- **轻量本地化 (Lightweight & Local)**：采用 PostgreSQL Trace 专表 + 可选结构化日志镜像 + 本地 Dashboard 的方案，零外部依赖，开箱即用。
- **动态组件感知 (Dynamic Component Awareness)**：Dashboard 基于 Trace 中的 `method`/`provider`/`details` 字段动态渲染，更换可插拔组件后自动适配展示内容，无需修改 Dashboard 代码。

#### 3.5.2 追踪数据结构

系统定义两类 Trace 记录，分别覆盖查询与摄取两条链路：

**A. Query Trace（查询追踪）**

每次查询请求生成唯一的 `trace_id`，记录从 Query 输入到 Response 输出的全过程：

**基础信息**：

- `trace_id`：请求唯一标识
- `trace_type`：`"query"`
- `timestamp`：请求时间戳
- `user_query`：用户原始查询
- `collection`：检索的知识库集合

**各阶段详情 (Stages)**：

| 阶段                 | 记录内容                                                     |
| -------------------- | ------------------------------------------------------------ |
| **Query Processing** | 原始 Query、改写后 Query（若有）、提取的关键词、method、耗时 |
| **Dense Retrieval**  | 返回的 Top-N 候选及相似度分数、provider、耗时                |
| **Sparse Retrieval** | 返回的 Top-N 候选及 BM25 分数、method、耗时                  |
| **Fusion**           | 融合后的统一排名、algorithm、耗时                            |
| **Rerank**           | 重排后的最终排名及分数、backend、是否触发 Fallback、耗时     |

**汇总指标**：

- `total_latency`：端到端总耗时
- `top_k_results`：最终返回的 Top-K 文档 ID
- `error`：异常信息（若有）

**评估指标 (Evaluation Metrics)**：

- `context_relevance`：召回文档与 Query 的相关性分数
- `answer_faithfulness`：生成答案与召回文档的一致性分数（若有生成环节）

**B. Ingestion Trace（摄取追踪）**

每次文档摄取生成唯一的 `trace_id`，记录从文件加载到存储完成的全过程：

**基础信息**：

- `trace_id`：摄取唯一标识
- `trace_type`：`"ingestion"`
- `timestamp`：摄取开始时间
- `source_path`：源文件路径
- `collection`：目标集合名称

**各阶段详情 (Stages)**：

| 阶段          | 记录内容                                                                           |
| ------------- | ---------------------------------------------------------------------------------- |
| **Load**      | 文件大小、解析器（method: markitdown）、提取的图片数、耗时                         |
| **Split**     | splitter 类型（method）、产出 chunk 数、平均 chunk 长度、耗时                      |
| **Transform** | 各 transform 名称与处理详情（refined/enriched/captioned 数量）、LLM provider、耗时 |
| **Embed**     | embedding provider、batch 数、向量维度、dense + sparse 编码耗时                    |
| **Upsert**    | 存储后端（method: pgvector）、upsert 数量、BM25 索引更新、图片存储、耗时           |

**汇总指标**：

- `total_latency`：端到端总耗时
- `total_chunks`：最终存储的 chunk 数量
- `total_images`：处理的图片数量
- `skipped`：跳过的文件/chunk 数（已存在、未变更等）
- `error`：异常信息（若有）

#### 3.5.3 技术方案：PostgreSQL Trace 专用表 + 本地 Web Dashboard

本项目采用 **"PostgreSQL Trace 专用表 + 本地 Web Dashboard"** 作为可观测性的实现方案，`JSON Lines` 作为可选镜像导出。

**选型理由**：

- **零外部依赖**：不依赖 LangSmith、LangFuse 等第三方平台，无需网络连接与账号注册，完全本地化运行。
- **数据一致性更好**：Trace 与业务数据同库管理（PostgreSQL），便于事务控制、关联查询与历史统计。
- **学习成本可控**：仍可保留 JSONL 镜像文件用于 `jq`/`grep` 快速排障。
- **契合项目定位**：本项目面向本地 MCP Server 场景，单用户、单机运行，无需分布式追踪或多租户隔离等企业级能力。

**实现架构**：

```
RAG Pipeline
    │
    ▼
Trace Collector (装饰器/回调)
    │
    ▼
PostgreSQL Trace Tables (`obs_traces`, `obs_trace_stages`)
    │
    ▼
本地 Web Dashboard (Vue3 + Vite)
    │
    ▼
按 trace_id 查看各阶段详情与性能指标
```

**Trace 专用表建表 SQL（建议放入 `backend/sql/001_observability.sql`）**：

```sql
CREATE TABLE IF NOT EXISTS obs_traces (
  trace_id UUID PRIMARY KEY,
  trace_type TEXT NOT NULL CHECK (trace_type IN ('ingestion', 'query', 'audit')),
  status TEXT NOT NULL CHECK (status IN ('running', 'success', 'failed')),
  collection TEXT,
  source_path TEXT,
  user_query TEXT,
  total_latency_ms INTEGER,
  error_code TEXT,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  finished_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_obs_traces_type_created
ON obs_traces (trace_type, created_at DESC);

CREATE TABLE IF NOT EXISTS obs_trace_stages (
  id BIGSERIAL PRIMARY KEY,
  trace_id UUID NOT NULL REFERENCES obs_traces(trace_id) ON DELETE CASCADE,
  stage_name TEXT NOT NULL,
  stage_order INTEGER NOT NULL,
  method TEXT,
  provider TEXT,
  latency_ms INTEGER,
  input_count INTEGER,
  output_count INTEGER,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (trace_id, stage_name, stage_order)
);

CREATE INDEX IF NOT EXISTS idx_obs_trace_stages_trace
ON obs_trace_stages (trace_id, stage_order);
```

**核心组件**：

- **Trace 持久化层**：基于 `TraceRepository` 将主 Trace 写入 `obs_traces`，阶段明细写入 `obs_trace_stages`。
- **可选 JSONL 镜像层**：按配置将 Trace 异步导出到 `logs/traces.jsonl`，用于本地排障和离线分析。
- **本地 Web Dashboard**：基于 Vue3+Vite 构建的 Web UI，优先读取 PostgreSQL Trace 表并提供交互式可视化。核心功能是按 `trace_id` 检索并展示单次请求的完整追踪链路。

#### 3.5.4 追踪机制实现

为确保各 RAG 阶段（可替换、可自定义）都能输出统一格式的追踪日志，系统采用 **TraceContext（追踪上下文）** 作为核心机制。

**工作原理**：

1. **请求开始**：Pipeline 入口创建一个 `TraceContext` 实例，生成唯一 `trace_id`，记录请求基础信息（Query、Collection 等）。

2. **阶段记录**：`TraceContext` 提供 `record_stage()` 方法，各阶段执行完毕后调用该方法，传入阶段名称、耗时、输入输出等数据。

3. **请求结束**：调用 `trace.finish()`，`TraceContext` 将汇总数据写入 `obs_traces`，并将阶段数据逐条写入 `obs_trace_stages`；如开启镜像，再异步输出 JSONL。

**与可插拔组件的配合**：

- 各阶段组件（Retriever、Reranker 等）的接口约定中包含 `TraceContext` 参数。
- 组件实现者在执行核心逻辑后，调用 `trace.record_stage()` 记录本阶段的关键信息。
- 这是**显式调用**模式：不强制、不会因未调用而报错，但依赖开发者主动记录。好处是代码透明，开发者清楚知道哪些数据被记录；代价是需要开发者自觉遵守约定。

**阶段划分原则**：

- **Stage 是固定的通用大类**：`retrieval`（检索）、`rerank`（重排）、`generation`（生成）等，不随具体实现方案变化。
- **具体实现是阶段内部的细节**：在 `record_stage()` 中通过 `method` 字段记录采用的具体方法（如 `bm25`、`hybrid`），通过 `details` 字段记录方法相关的细节数据。
- 这样无论底层方案怎么替换，阶段结构保持稳定，Dashboard 展示逻辑无需调整。

#### 3.5.5 Dashboard 功能设计（七页面架构）

Dashboard 基于 Vue3 构建多页面应用，提供七大功能页面：

**页面 1：电能质量报告审查结果展示**

- **组件配置卡片**：展示电能质量报告审查结果，页面底部包含其他页面（页面2-页面7）的超链接。
  - 目录栏（左侧放置），展示进行审查/审查完成的电能质量报告（约占1/4页面）
  - 结果一览区（右侧放置），展示对应报告20条审查要点、审查结果、审查结果支撑（原文chunk，并展示对应的页码）
  - 其余页面超链接（底部放置），方便用户对审查结果进行查看，并调整相关配置。

**页面 2：系统总览 (Overview)**

- **组件配置卡片**：读取 `Settings`，展示当前可插拔组件的配置状态：
  - LLM：provider + model（如 `azure / gpt-4o`）
  - Embedding：provider + model + 维度
  - Splitter：类型 + chunk_size + overlap
  - Reranker：backend + model（或 None）
  - Evaluator：已启用的 backends 列表
- **数据资产统计**：调用 `DocumentManager.get_collection_stats()` 展示各集合的文档数、chunk 数、图片数。
- **系统健康指标**：最近一次 Ingestion/Query trace 的时间与耗时。

**页面 3：数据浏览器 (Data Browser)**

- **文档列表视图**：展示已摄入的文档（source_path、集合、chunk 数、摄入时间），支持按集合筛选与关键词搜索。
- **Chunk 详情视图**：点击文档展开其所有 chunk，每个 chunk 显示：
  - 原文内容（可折叠长文本）
  - Metadata 各字段（title、summary、tags、page、image_refs 等）
  - 关联图片预览（从 ImageStorage 读取并展示缩略图）
- **数据来源**：通过 `PgVectorStore.get_all()` 或 `get_by_metadata()` 读取 chunk 数据。

**页面 4：Ingestion 管理 (Ingestion Manager)**

- **文件选择与摄取触发**：
  - 文件上传组件或目录路径输入
  - 选择目标集合（下拉选择或新建）
  - 点击"开始摄取"按钮触发
  - 实时显示当前阶段与处理进度
- **文档删除**：
  - 在文档列表中提供"删除"按钮
  - 调用 `DocumentManager.delete_document()` 协调跨存储删除
  - 删除完成后刷新列表

**页面 5：Ingestion 追踪 (Ingestion Traces)**

- **摄取历史列表**：按时间倒序展示 `trace_type == "ingestion"` 的历史记录，显示文件名、集合、总耗时、状态（成功/失败）。
- **单次摄取详情**：
  - **阶段耗时瀑布图**：横向条形图展示 load/split/transform/embed/upsert 各阶段时间分布。
  - **处理统计**：chunk 数、图片数、跳过数、失败数。
  - **各阶段详情展开**：点击查看 method/provider、输入输出样本。

**页面 6：Query 追踪 (Query Traces)**

- **查询历史列表**：按时间倒序展示 `trace_type == "query"` 的历史记录，支持按 Query 关键词筛选。
- **单次查询详情**：
  - **耗时瀑布图**：展示 query_processing/dense/sparse/fusion/rerank 各阶段时间分布。
  - **Dense vs Sparse 对比**：并列展示两路召回结果的 Top-N 文档 ID 与分数。
  - **Rerank 前后对比**：展示融合排名与精排后排名的变化（排名跃升/下降标记）。
  - **最终结果表**：展示 Top-K 候选文档的标题、分数、来源。

**页面 7：评估面板 (Evaluation Panel)**

- **评估运行**：选择评估后端（Ragas / Custom / All）与 golden test set，点击运行。
- **指标展示**：以表格和图表展示 hit_rate、mrr、faithfulness 等指标。
- **历史趋势**：对比不同时间的评估结果，观察策略调整的效果。
- **注意**：评估面板在 Phase H 实现，Phase G 完成后该页面显示"评估模块尚未启用"的占位提示。

**Dashboard 技术架构**：

```
front_end/
└── pages/
  ├── sgcc-report-audit/    # 页面 1：电能质量报告审查结果
  ├── overview.py           # 页面 2：系统总览
  ├── data_browser.py       # 页面 3：数据浏览器
  ├── ingestion_manager.py  # 页面 4：Ingestion 管理
  ├── ingestion_traces.py   # 页面 5：Ingestion 追踪
  ├── query_traces.py       # 页面 6：Query 追踪
  └── evaluation_panel.py   # 页面 7：评估面板
backend/
└── services/
  ├── trace_service.py      # Trace 数据读取服务（查询 obs_traces/obs_trace_stages）
  ├── data_service.py       # 数据浏览服务（封装 PgVector/ImageStorage 读取）
  └── config_service.py     # 配置读取服务（封装 Settings 读取与展示）
```

**Dashboard 与 Trace 的数据关系**：

- Dashboard 页面 5/6 读取 `obs_traces` 与 `obs_trace_stages`（通过 `TraceService`），按 `trace_type` 分类展示。
- Dashboard 页面 2/3/4 直接读取存储层（通过 `DataService` 封装 PgVectorStore/ImageStorage/FileIntegrity），不依赖 Trace。
- 所有页面基于 Trace 中 `method`/`provider` 字段动态渲染标签，更换组件后自动适配。

#### 3.5.6 配置示例

```yaml
observability:
  enabled: true

  # Trace 主存储（推荐）
  storage:
    backend: postgresql # postgresql | jsonl
    traces_table: obs_traces
    trace_stages_table: obs_trace_stages
    write_mode: sync # sync | async

  # 可选 JSONL 镜像
  logging:
    mirror_to_jsonl: true
    log_file: logs/traces.jsonl
    log_level: INFO # DEBUG | INFO | WARNING

  # 追踪粒度控制
  detail_level: standard # minimal | standard | verbose

# Dashboard 管理平台配置
dashboard:
  enabled: true
  port: 8501 # 前端页面服务端口
  trace_source: postgresql # postgresql | jsonl
  traces_dir: ./logs # 当 trace_source=jsonl 时生效
  auto_refresh: true # 是否自动刷新（轮询新 trace）
  refresh_interval: 5 # 自动刷新间隔（秒）
```

### 3.6 多模态图片处理设计 (Multimodal Image Processing Design)

**目标：** 设计一套完整的图片处理方案，使 RAG 系统能够理解、索引并检索文档中的图片内容，实现"用自然语言搜索图片"的能力，同时保持架构的简洁性与可扩展性。

#### 3.6.1 设计理念与策略选型

多模态 RAG 的核心挑战在于：**如何让纯文本的检索系统"看懂"图片**。业界主要有两种技术路线：

| 策略                             | 核心思路                                                  | 优势                         | 劣势                                    |
| -------------------------------- | --------------------------------------------------------- | ---------------------------- | --------------------------------------- |
| **Image-to-Text (图转文)**       | 利用 Vision LLM 将图片转化为文本描述，复用纯文本 RAG 链路 | 架构统一、实现简单、成本可控 | 描述质量依赖 LLM 能力，可能丢失视觉细节 |
| **Multi-Embedding (多模态向量)** | 使用 CLIP 等模型将图文统一映射到同一向量空间              | 保留原始视觉特征，支持图搜图 | 需引入额外向量库，架构复杂度高          |

**本项目选型：Image-to-Text（图转文）策略**

选型理由：

- **架构统一**：无需引入 CLIP 等多模态 Embedding 模型，无需维护独立的图像向量库，完全复用现有的文本 RAG 链路（Ingestion → Hybrid Search → Rerank）。
- **语义对齐**：通过 LLM 将图片的视觉信息转化为自然语言描述，天然与用户的文本查询在同一语义空间，检索效果可预期。
- **成本可控**：仅在数据摄取阶段一次性调用 Vision LLM，检索阶段无额外成本。
- **渐进增强**：未来如需支持"图搜图"等高级能力，可在此基础上叠加 CLIP Embedding，无需重构核心链路。

#### 3.6.2 图片处理全流程设计

图片处理贯穿 Ingestion Pipeline 的多个阶段，整体流程如下：

```
原始文档 (PDF/WORD/PPT/Markdown)
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Loader 阶段：图片提取与引用收集                           │
│  - 解析文档，识别并提取嵌入的图片资源                        │
│  - 为每张图片生成唯一标识 (image_id)                       │
│  - 在文档文本中插入图片占位符/引用标记                       │
│  - 输出：Document (text + metadata.images[])             │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Splitter 阶段：保持图文关联                               │
│  - 切分时保留图片引用标记在对应 Chunk 中                     │
│  - 确保图片与其上下文段落保持关联                            │
│  - 输出：Chunks (各自携带关联的 image_refs)                │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Transform 阶段：图片理解与描述生成                         │
│  - 调用 Vision LLM 对每张图片生成结构化描述                  │
│  - 将描述文本注入到关联 Chunk 的正文或 Metadata 中           │
│  - 输出：Enriched Chunks (含图片语义信息)                  │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Storage 阶段：双轨存储                                    │
│  - 向量库：存储增强后的 Chunk (含图片描述) 用于检索           │
│  - 文件系统/Blob：存储原始图片文件用于返回展示                │
└─────────────────────────────────────────────────────────┘
```

#### 3.6.3 各阶段技术要点

**1. Loader 阶段：图片提取与引用收集**

- **提取策略**：
  - 解析文档时识别嵌入的图片资源（PDF 中的 XObject、PPT 中的媒体文件、Markdown 中的 `![]()` 引用）。
  - 为每张图片生成全局唯一的 `image_id`（建议格式：`{doc_hash}_{page}_{seq}`）。
  - 将图片二进制数据提取并暂存，记录其在原文档中的位置信息。

- **引用标记**：
  - 在转换后的 Markdown 文本中，于图片原始位置插入占位符（如 `[IMAGE: {image_id}]`）。
  - 在 Document 的 Metadata 中维护 `images` 列表，记录每张图片的 `image_id`、原始路径、页码、尺寸等基础信息。

- **存储原始图片**：
  - 将提取的图片保存至本地文件系统的约定目录（如 `data/images/{collection}/{image_id}.png`）。
  - 仅保存需要的图片格式（推荐统一转换为 PNG/JPEG），控制存储体积。

**2. Splitter 阶段：保持图文关联**

- **关联保持原则**：
  - 图片引用标记应与其说明性文字（Caption、前后段落）尽量保持在同一 Chunk 中。
  - 若图片出现在章节开头或结尾，切分时应将其归入语义上最相关的 Chunk。

- **Chunk Metadata 扩展**：
  - 每个 Chunk 的 Metadata 中增加 `image_refs: List[image_id]` 字段，记录该 Chunk 关联的图片列表。
  - 此字段用于后续 Transform 阶段定位需要处理的图片，以及检索命中后定位需要返回的图片。

**3. Transform 阶段：图片理解与描述生成**

这是多模态处理的核心环节，负责将视觉信息转化为可检索的文本语义。

- **Vision LLM 选型**：

| 模型                  | 提供商             | 特点                                              | 适用场景                             | 推荐指数   |
| --------------------- | ------------------ | ------------------------------------------------- | ------------------------------------ | ---------- |
| **GPT-4o**            | OpenAI / Azure     | 理解能力强，支持复杂图表解读，英文文档表现优异    | 高质量需求、复杂业务文档、国际化场景 | ⭐⭐⭐⭐⭐ |
| **Qwen-VL-Max**       | 阿里云 (DashScope) | 中文理解能力出色，性价比高，对中文图表/文档支持好 | 中文文档、国内部署、成本敏感场景     | ⭐⭐⭐⭐⭐ |
| **Qwen-VL-Plus**      | 阿里云 (DashScope) | 速度更快，成本更低，适合大批量处理                | 大批量中文文档、快速迭代场景         | ⭐⭐⭐⭐   |
| **Claude 3.5 Sonnet** | Anthropic          | 多模态原生支持，长上下文                          | 需要结合大段文字理解图片             | ⭐⭐⭐⭐   |
| **Gemini Pro Vision** | Google             | 成本较低，速度较快                                | 大批量处理、成本敏感场景             | ⭐⭐⭐     |
| **GLM-4V**            | 智谱 AI (ZhipuAI)  | 国内老牌，稳定性好，中文支持佳                    | 国内部署备选、企业级应用             | ⭐⭐⭐⭐   |

**双模型选型策略（推荐）**：

本项目采用**国内 + 国外双模型**方案，通过配置切换，兼顾不同部署环境和文档类型：

| 部署环境                  | 主选模型       | 备选模型          | 说明                                          |
| ------------------------- | -------------- | ----------------- | --------------------------------------------- |
| **国际化 / Azure 环境**   | GPT-4o (Azure) | Qwen-VL-Max       | 英文文档优先用 GPT-4o，中文文档可切换 Qwen-VL |
| **国内部署 / 纯中文场景** | Qwen-VL-Max    | GPT-4o            | 中文图表理解用 Qwen-VL，特殊需求可切换 GPT-4o |
| **成本敏感 / 大批量**     | Qwen-VL-Plus   | Gemini Pro Vision | 牺牲部分质量换取速度和成本                    |

**选型理由**：

1. **GPT-4o (国外首选)**：
   - 视觉理解能力业界领先，复杂图表解读准确率高
   - Azure 部署可满足企业合规要求
   - 英文技术文档理解效果最佳

2. **Qwen-VL-Max (国内首选)**：
   - 中文场景下表现与 GPT-4o 接近，部分中文图表任务甚至更优
   - 通过阿里云 DashScope API 调用，国内访问稳定、延迟低
   - 价格约为 GPT-4o 的 1/3 ~ 1/5，性价比极高
   - 原生支持中文 OCR，对中文截图、表格识别更准确

- **描述生成策略**：
  - **结构化 Prompt**：设计专用的图片理解 Prompt，引导 LLM 输出结构化描述，而非自由发挥。
  - **上下文感知**：将图片的前后文本段落一并传入 Vision LLM，帮助其理解图片在文档中的语境与作用。
  - **分类型处理**：针对不同类型的图片采用差异化的理解策略：

| 图片类型          | 理解重点                     | Prompt 引导方向                  |
| ----------------- | ---------------------------- | -------------------------------- |
| **流程图/架构图** | 节点、连接关系、流程逻辑     | "描述这张图的结构和流程步骤"     |
| **数据图表**      | 数据趋势、关键数值、对比关系 | "提取图表中的关键数据和结论"     |
| **截图/UI**       | 界面元素、操作指引、状态信息 | "描述截图中的界面内容和关键信息" |
| **照片/插图**     | 主体对象、场景、视觉特征     | "描述图片中的主要内容"           |

- **描述注入方式**：
  - **推荐：注入正文**：将生成的描述直接替换或追加到 Chunk 正文中的图片占位符位置，格式如 `[图片描述: {caption}]`。这样描述会被 Embedding 覆盖，可被直接检索。
  - **备选：注入 Metadata**：将描述存入 `chunk.metadata.image_captions` 字段。需确保检索时该字段也被索引。

- **幂等与增量处理**：
  - 为每张图片的描述计算内容哈希，存入 `processing_cache` 表。
  - 重复处理时，若图片内容未变且 Prompt 版本一致，直接复用缓存的描述，避免重复调用 Vision LLM。

**4. Storage 阶段：双轨存储**

- **向量库存储（用于检索）**：
  - 存储增强后的 Chunk，其正文已包含图片描述，Metadata 包含 `image_refs` 列表。
  - 检索时通过文本相似度即可命中包含相关图片描述的 Chunk。

- **原始图片存储（用于返回）**：
  - 图片文件存储于本地文件系统，路径记录在独立的 `images` 索引表中。
  - 索引表字段：`image_id`, `file_path`, `source_doc`, `page`, `width`, `height`, `mime_type`。
  - 检索命中后，根据 Chunk 的 `image_refs` 查询索引表，获取图片文件路径用于返回。

#### 3.6.4 检索与返回流程

当用户查询命中包含图片的 Chunk 时，系统需要将图片与文本一并返回：

```
用户查询: "系统架构是什么样的？"
    │
    ▼
Hybrid Search 命中 Chunk（正文含 "[图片描述: 系统采用三层架构...]"）
    │
    ▼
从 Chunk.metadata.image_refs 获取关联的 image_id 列表
    │
    ▼
查询 images 索引表，获取图片文件路径
    │
    ▼
读取图片文件，编码为 Base64
    │
    ▼
构造 MCP 响应，包含 TextContent + ImageContent
```

**MCP 响应格式**：

```json
{
  "content": [
    {
      "type": "text",
      "text": "根据文档，系统架构如下：...\n\n[1] 来源: architecture.pdf, 第5页"
    },
    {
      "type": "image",
      "data": "<base64-encoded-image>",
      "mimeType": "image/png"
    }
  ]
}
```

#### 3.6.5 质量保障与边界处理

- **描述质量检测**：
  - 对生成的描述进行基础质量检查（长度、是否包含关键信息）。
  - 若描述过短或 LLM 返回"无法识别"，标记该图片为 `low_quality`，可选择人工复核或跳过索引。

- **大尺寸/特殊图片处理**：
  - 超大图片在传入 Vision LLM 前进行压缩（保持宽高比，限制最大边长）。
  - 对于纯装饰性图片（如分隔线、背景图），可通过尺寸或位置规则过滤，不进入描述生成流程。

- **批量处理优化**：
  - 图片描述生成支持批量异步调用，提高吞吐量。
  - 单个文档处理失败时，记录失败的图片 ID，不影响其他图片的处理进度。

- **降级策略**：
  - 当 Vision LLM 不可用时，系统回退到"仅保留图片占位符"模式，图片不参与检索但不阻塞 Ingestion 流程。
  - 在 Chunk 中标记 `has_unprocessed_images: true`，后续可增量补充描述。

## 4. 测试方案

### 4.1 设计理念：测试驱动开发 (TDD)

本项目采用**测试驱动开发（Test-Driven Development）**作为核心开发范式，确保每个组件在实现前就已明确其预期行为，通过自动化测试持续验证系统质量。

**核心原则**：

- **早测试、常测试**：每个功能模块实现的同时就编写对应的单元测试，而非事后补测。
- **测试即文档**：测试用例本身就是最准确的行为规范，新加入的开发者可通过阅读测试快速理解各模块功能。
- **快速反馈循环**：单元测试应在秒级完成，支持开发者高频执行，立即发现引入的问题。
- **分层测试金字塔**：大量快速的单元测试作为基座，少量关键路径的集成测试作为保障，极少数端到端测试验证完整流程。

```
        /\
       /E2E\         <- 少量，验证关键业务流程
      /------\
     /Integration\   <- 中量，验证模块协作
    /------------\
   /  Unit Tests  \  <- 大量，验证单个函数/类
  /________________\
```

### 4.2 测试分层策略

#### 4.2.1 单元测试 (Unit Tests)

**目标**：验证每个独立组件的内部逻辑正确性，隔离外部依赖。

**覆盖范围**：

| 模块                    | 测试重点                           | 典型测试用例                                                                                        |
| ----------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------- |
| **Loader (文档解析器)** | 格式解析、元数据提取、图片引用收集 | - 测试解析单页/多页 PDF<br>- 验证 Markdown 标题层级提取<br>- 检查图片占位符插入位置                 |
| **Splitter (切分器)**   | 切分边界、上下文保留、元数据传递   | - 验证按标题切分不破坏段落<br>- 测试超长文本的递归切分<br>- 检查 Chunk 的 `source` 字段正确性       |
| **Transform (增强器)**  | 图片描述生成、元数据注入           | - Mock Vision LLM，验证描述注入逻辑<br>- 测试无图片时的降级行为<br>- 验证幂等性（重复处理相同输入） |
| **Embedding (向量化)**  | 批处理、差量计算、向量维度         | - 验证相同文本生成相同向量<br>- 测试批量请求的拆分与合并<br>- 检查缓存命中逻辑                      |
| **BM25 (稀疏编码)**     | 关键词提取、权重计算               | - 验证停用词过滤<br>- 测试 IDF 计算准确性<br>- 检查稀疏向量格式                                     |
| **Retrieval (检索器)**  | 召回精度、融合算法                 | - 测试纯 Dense/Sparse/Hybrid 三种模式<br>- 验证 RRF 融合分数计算<br>- 检查 Top-K 结果排序           |
| **Reranker (重排器)**   | 分数归一化、降级回退               | - Mock Cross-Encoder，验证分数重排<br>- 测试超时后的 Fallback 逻辑<br>- 验证空候选集处理            |

**技术选型**：

- **测试框架**：`pytest`（Python 标准选择，支持参数化测试、Fixture 机制）
- **Mock 工具**：`unittest.mock` / `pytest-mock`（隔离外部依赖，如 LLM API）
- **断言增强**：`pytest-check`（支持多断言不中断执行）

#### 4.2.2 集成测试 (Integration Tests)

**目标**：验证多个组件协作时的数据流转与接口兼容性。

**覆盖范围**：

| 测试场景               | 验证要点                                           | 测试策略                                                                                                        |
| ---------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Ingestion Pipeline** | Loader → Splitter → Transform → Storage 的完整流程 | - 使用真实的测试 PDF 文件<br>- 验证最终存入向量库的数据完整性<br>- 检查中间产物（如临时图片文件）是否正确清理   |
| **Hybrid Search**      | Dense + Sparse 召回的融合结果                      | - 准备已知答案的查询-文档对<br>- 验证融合后的 Top-1 是否命中正确文档<br>- 测试极端情况（某一路无结果）          |
| **Rerank Pipeline**    | 召回 → 过滤 → 重排的组合                           | - 验证 Metadata 过滤后的候选集正确性<br>- 检查 Reranker 是否改变了 Top-1 结果<br>- 测试 Reranker 失败时的回退   |
| **MCP Server**         | 工具调用的端到端流程                               | - 模拟 MCP Client 发送 JSON-RPC 请求<br>- 验证返回的 `content` 格式符合协议<br>- 测试错误处理（如查询语法错误） |

**技术选型**：

- **数据隔离**：每个测试使用独立的临时数据库/向量库（pytest 内置 `tmp_path` fixture，或 `pytest-postgresql` 用于隔离真实 PG 实例）
- **异步测试**：`pytest-asyncio`（若 MCP Server 采用异步实现）
- **契约测试**：定义各模块间的 Schema，确保接口不漂移

#### 4.2.3 端到端测试 (End-to-End Tests)

**目标**：模拟真实用户操作，验证完整业务流程的可用性。

**核心场景**：

**场景 1：数据准备（离线摄取）**

- **测试目标**：验证文档摄取流程的完整性与正确性
- **测试步骤**：
  - 准备测试文档（PDF 文件，包含文本、图片、表格等多种元素）
  - 执行离线摄取脚本，将文档导入知识库
  - 验证摄取结果：检查生成的 Chunk 数量、元数据完整性、图片描述生成
  - 验证存储状态：确认向量库和 BM25 索引正确创建
  - 验证幂等性：重复摄取同一文档，确保不产生重复数据
- **验证要点**：
  - Chunk 的切分质量（语义完整性、上下文保留）
  - 元数据字段完整性（source、page、title、tags 等）
  - 图片处理结果（Caption 生成、Base64 编码存储）
  - 向量与稀疏索引的正确性

**场景 2：召回测试**

- **测试目标**：验证检索系统的召回精度与排序质量
- **测试步骤**：
  - 基于已摄取的知识库，准备一组测试查询（包含不同难度与类型）
  - 执行混合检索（Dense + Sparse + Rerank）
  - 验证召回结果：检查 Top-K 文档是否包含预期来源
  - 对比不同检索策略的效果（纯 Dense、纯 Sparse、Hybrid）
  - 验证 Rerank 的影响：对比重排前后的结果变化
- **验证要点**：
  - Hit Rate@K：Top-K 结果命中率是否达标
  - 排序质量：正确答案是否排在前列（MRR、NDCG）
  - 边界情况处理：空查询、无结果查询、超长查询
  - 多模态召回：包含图片的文档是否能通过文本查询召回

**场景 3：MCP Client 功能测试**

- **测试目标**：验证 MCP Server 与 Client（如 GitHub Copilot）的协议兼容性与功能完整性
- **测试步骤**：
  - 启动 MCP Server（Stdio Transport 模式）
  - 模拟 MCP Client 发送各类 JSON-RPC 请求
  - 测试工具调用：`query_knowledge_hub`、`list_collections` 等
  - 验证返回格式：符合 MCP 协议规范（content 数组、structuredContent）
  - 测试引用透明性：返回结果包含完整的 Citation 信息
  - 测试多模态返回：包含图片的响应正确编码为 Base64
- **验证要点**：
  - 协议合规性：JSON-RPC 2.0 格式、错误码映射
  - 工具注册：`tools/list` 返回所有可用工具及其 Schema
  - 响应格式：TextContent 与 ImageContent 的正确组合
  - 错误处理：无效参数、超时、服务不可用等异常场景
  - 性能指标：单次请求的端到端延迟（含检索、重排、格式化）

**测试工具**：

- **BDD 框架**：`pytest-bdd`（以 Gherkin 语法描述场景）
- **环境准备**：
  - 临时测试向量库（独立于生产数据）
  - 预置的标准测试文档集
  - 本地 MCP Server 进程（Stdio Transport）

**场景 4：电能质量报告审查 功能测试**

- **测试目标**：验证 SGCC-REPORT-AUDIT 业务层能基于 RAG MCP 服务，稳定输出可追溯的 20 项审查结果。

- **测试前置数据（最小集）**：

| 用例ID | 报告类型       | 核心特征                         | 关键断言                                              |
| :----- | :------------- | :------------------------------- | :---------------------------------------------------- |
| A1     | 基准合格报告   | 资质、审批、指标、结论完整       | 20 项均返回，整体结果以 `pass/review` 为主            |
| A2     | 资质缺失报告   | 缺少 CNAS/CMA 或资质过期         | 第 1 项应为 `fail` 或 `review`，并给出证据            |
| A3     | 海上风电报告   | 含海上风电、谐波背景仿真叠加说明 | 第 13 项需命中“仿真叠加”相关证据                      |
| A4     | 超标未治理报告 | 指标超限且未给治理措施           | 第 19 项应为 `fail`，原因中需说明“超标但未给治理建议” |

- **测试步骤**：
  1. 通过业务接口提交报告审查任务（例如 `run_report_audit` 对应 API）。
  2. 轮询或查询任务结果（例如 `get_audit_result` 对应 API）直到完成。
  3. 校验响应结构：`audit_id/report_name/generated_at/overall_status/items` 字段齐全。
  4. 校验 `items` 数量必须为 20，且 `check_id` 覆盖 `1..20` 不重复。
  5. 校验每项必填字段：`status`、`reason`、`evidence`；`status` 仅允许 `pass|fail|review`。
  6. 校验证据可追溯：每项至少 1 条证据，且证据包含 `source` 与 `page`（或等价定位字段）。
  7. 按 A1~A4 用例执行关键业务断言（资质缺失、海上风电叠加、超标治理建议等）。
  8. 触发一次结果页渲染检查，确认前端可正确展示 20 项结论与证据跳转。

- **验证要点**：
  - **完整性**：20 项审查结果必须全部返回，不允许缺项。
  - **一致性**：`reason` 与 `status` 逻辑一致，且与证据内容不冲突。
  - **规则符合性**：第 1/13/19 项等关键规则在对应用例中必须命中预期。
  - **可追溯性**：每项结论可回溯到原文页码或等价定位信息。
  - **稳定性**：同一输入多次执行，关键结论（尤其 fail 项）应保持稳定。

- **通过标准**：
  - A1~A4 用例全部通过。
  - 结构校验通过率 100%。
  - 关键规则断言通过率 100%。
  - 端到端单次审查耗时满足项目基线（见 6.1 排期验收口径）。

**测试工具**：

- `pytest` + `pytest-asyncio`：执行业务 API 端到端流程。
- `httpx`：调用审查提交与结果查询接口。
- `jsonschema`：校验审查结果 JSON 结构与枚举值。
- `Playwright`：验证结果页 20 项展示与证据跳转。
- `pytest-bdd`（可选）：将 A1~A4 用例写成 Gherkin 场景，便于评审与回归。

### 4.3 RAG 质量评估测试

**目标**：验证已设计的评估体系（见 3.4.4 评估框架抽象）是否正确实现，并能有效评估 RAG 系统的召回与生成质量。

**测试要点**：

1. **黄金测试集准备**
   - 构建标准的"问题-答案-来源文档"测试集（JSON 格式）
   - 初期人工标注核心场景，后期持续积累坏 Case

2. **评估框架实现验证**
   - 验证 Ragas/DeepEval 等评估框架的正确集成
   - 确认评估接口能输出标准化的指标字典
   - 测试多评估器并行执行与结果汇总

3. **关键指标参考基线**（非硬性门禁，供调优参考）
   - 检索指标：Hit Rate@K ≥ 90%、MRR ≥ 0.8、NDCG@K ≥ 0.85
   - 生成指标：Faithfulness ≥ 0.9、Answer Relevancy ≥ 0.85
   - 定期运行评估，监控指标是否回归

**说明**：本节重点是验证评估体系的工程实现，而非重新设计评估方法（评估方法的设计见第 3 章技术选型）。

### 4.4 性能与压力测试（可选）

> **说明**：本项目定位为本地 MCP Server，单用户开发环境，采用 Stdio Transport 通信方式。性能与压力测试在当前阶段**不是必需的**，此处列出主要用于：
>
> 1. **架构完整性**：展示完整的工程化测试体系，体现系统设计的专业性
> 2. **未来扩展性**：若后续需要云端部署或多用户支持，可直接参考此方案
> 3. **性能基准建立**：通过基础性能测试了解系统瓶颈，为优化提供数据支撑

**可选测试场景**：

| 测试类型         | 验证点                      | 工具               | 优先级                 |
| ---------------- | --------------------------- | ------------------ | ---------------------- |
| **延迟测试**     | 单次查询的 P50/P95/P99 延迟 | `pytest-benchmark` | 中（可帮助识别慢查询） |
| **吞吐量测试**   | 并发查询时的 QPS 上限       | `locust`           | 低（本地单用户无需求） |
| **内存泄漏检测** | 长时间运行后的内存占用      | `memory_profiler`  | 低（短期运行无影响）   |
| **向量库性能**   | 不同数据规模下的查询速度    | 自定义 Benchmark   | 中（验证扩展性）       |

### 4.5 测试工具链与 CI/CD 集成

**本地开发工作流**：

- **快速验证**：仅运行单元测试，秒级反馈
- **完整验证**：单元测试 + 集成测试，生成覆盖率报告
- **质量评估**：定期执行 RAG 质量测试，监控指标变化

**CI/CD Pipeline 设计**（可选）：

> **说明**：本地项目不强制要求 CI/CD，但配置自动化测试流程有助于代码质量保障与持续集成实践。

- **单元测试阶段**：每次提交自动触发，验证基础功能，生成覆盖率报告
- **集成测试阶段**：单元测试通过后执行，验证模块协作
- **质量评估阶段**：PR 触发，运行完整的 RAG 质量测试，发布评估报告

**测试覆盖率目标**：

- **单元测试**：核心逻辑覆盖率 ≥ 80%
- **集成测试**：关键路径覆盖率 100%（如 Ingestion、Hybrid Search）
- **E2E 测试**：核心用户场景覆盖率 100%（至少 3 个关键流程）

## 5. 系统架构与模块设计

### 5.1 系统整体架构图 (ASCII Art)

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      外部调用层 (Clients/UI)                                     │
│                                                                                                  │
│  ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────────────────────┐ │
│  │ GitHub Copilot       │   │ Claude Desktop       │   │ SGCC Dashboard (Vue3 + Vite)        │ │
│  │ 其他 MCP Client      │   │ 其他 MCP Agent       │   │ 审查结果/总览/数据/Trace/评估        │ │
│  └──────────┬───────────┘   └──────────┬───────────┘   └──────────────────┬───────────────────┘ │
│         JSON-RPC 2.0 (Stdio)        JSON-RPC 2.0 (Stdio)              HTTP/REST                  │
└─────────────┼──────────────────────────┼──────────────────────────────────┼────────────────────┘
              │                          │                                  │
              ▼                          ▼                                  ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   接口与编排层 (Python Backend)                                  │
│                                                                                                  │
│  ┌────────────────────────────────────────────────────┐   ┌────────────────────────────────────┐ │
│  │ MCP Server (Protocol Handler)                      │◄──│ SGCC Report Audit API (FastAPI,MVC)│ │
│  │ initialize / tools/list / tools/call               │   │ submit_audit / get_result / traces │ │
│  │ stdout: MCP消息, stderr: 日志                       │   │ 业务编排与结果聚合                 │ │
│  │                              Stdio 子进程调用 ──────┘   │ rag_mcp_client.py:                 │ │
│  │ Tool Facade (MCP 注册工具):                        │   │ 以Stdio子进程方式调用 MCP Server   │ │
│  │  query_knowledge_hub | retrieve_context            │   └────────────────────────────────────┘ │
│  │  verify_answer | list_collections                  │                                          │
│  │  get_document_summary | list_document_sections     │                                          │
│  │  ingest_document | reindex_document                │                                          │
│  └───────────────────────────────────────┬────────────┘                                          │
└──────────────────────────────────────────┼───────────────────────────────────────────────────────┘
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      核心引擎层 (RAG Core)                                       │
│                                                                                                  │
│  ┌──────────────────────────────────────── Query Engine ───────────────────────────────────────┐ │
│  │ Query Processor -> Hybrid Retrieval (Dense + Sparse + RRF) -> Reranker(可选) -> Response  │ │
│  │ 核心能力: 查询扩展/过滤解析 | 双路召回 | 融合重排 | 引用生成(Citation) | 多模态返回(Text+Image) │ │
│  └───────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                  │
│  ┌────────────────────────────────────── Ingestion Pipeline ────────────────────────────────────┐ │
│  │ File Integrity Check -> Loader -> Splitter -> Transform -> Embedding -> Upsert              │ │
│  │ 核心能力: 增量跳过 | Markdown标准化 | 语义切分 | 图片描述增强 | Dense+Sparse编码 | 幂等写入      │ │
│  └───────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                  │
│  ┌──────────────────────────────────── Document Lifecycle Manager ───────────────────────────────┐ │
│  │ list_documents / get_document_detail / delete_document / get_collection_stats                │ │
│  │ 跨存储一致性删除: PgVector + BM25 + ImageStore + FileIntegrity                               │ │
│  └───────────────────────────────────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬───────────────────────────────────────┬──────────────────────────┘
                                │                                       │
                                ▼                                       ▼
┌─────────────────────────────────────────────────┐     ┌──────────────────────────────────────────┐
│            可插拔组件层 (Factory Pattern)       │     │        可观测性层 (Trace as Cross-cut)   │
│  LLMFactory / VisionLLMFactory                 │     │  TraceContext: trace_id + stage记录       │
│  EmbeddingFactory / SplitterFactory            │     │  obs_traces / obs_trace_stages            │
│  VectorStoreFactory / RerankerFactory          │     │  Dashboard: Ingestion/Query 瀑布图与详情  │
│  EvaluatorFactory                              │     │  可选 JSONL 镜像: logs/traces.jsonl       │
└───────────────────────────────┬─────────────────┘     └──────────────────────┬───────────────────┘
                                └──────────────────────────────┬─────────────────┘
                                                               ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       存储层 (PostgreSQL + FS)                                   │
│                                                                                                  │
│  PostgreSQL                                                                                      │
│  - rag_chunks (PgVector): dense_vector / sparse_vector / content / metadata                     │
│  - bm25相关表: 倒排索引与统计信息                                                                  │
│  - ingestion_history: 文件哈希去重与处理状态                                                       │
│  - image_index: image_id -> file_path 映射                                                        │
│  - processing_cache: 图片描述内容哈希缓存，避免重复调用 Vision LLM                                  │
│  - obs_traces, obs_trace_stages: 全链路追踪                                                       │
│                                                                                                  │
│  File System                                                                                     │
│  - data/images/* : 原图存储                                                                        │
│  - logs/traces.jsonl : 可选追踪镜像                                                                │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 完整目录结构树（业务与 RAG Server 解耦）

> 目录设计原则：
>
> - `rag-server/` 为可复用的通用 RAG 服务代码，独立演进，一次编写处处运行。
> - `sgcc-report-audit-app/` 为电能质量审查业务应用，前后端分离，后端按 MVC 架构组织。
> - 业务侧的 `data/`、`cache/`、`logs/` 均采用可配置映射（软链接/挂载）到 `rag-server` 对应目录，保障 RAG Server 目录完整迁移。

```text
sgcc-report-audit-workspace/
├── .gitignore                                    # 全局忽略规则
├── DEV_SPEC.md                                    # 开发规范主文档
├── GENERATE_SPEC.md                               # 代码生成规范说明
├── README.md                                      # 项目说明文档
├── docker/                                        # 容器化目录
│   ├── docker-compose.yml                         # 全栈编排文件
│   ├── rag-server.Dockerfile                      # RAG Server 镜像定义
│   ├── backend.Dockerfile                         # 业务后端镜像定义
│   ├── frontend.Dockerfile                        # 前端镜像定义
│   ├── .dockerignore                              # Docker 构建忽略配置
│   └── .env.docker.example                        # 容器运行环境变量模板
│
├── rag-server/                                    # 通用 RAG Server（独立可复用）
│   ├── pyproject.toml                             # uv 项目定义
│   ├── uv.lock                                    # uv 锁文件
│   ├── pytest.ini                                 # pytest 配置文件
│   ├── .python-version                            # Python 版本声明
│   ├── .env.example                               # 环境变量模板
│   ├── README.md                                  # 项目说明文档
│   ├── src/                                       # 源代码目录
│   │   ├── core/                                  # 核心基础模块目录
│   │   │   ├── __init__.py                        # Python 包初始化
│   │   │   ├── types.py                           # Document/Chunk/Result 核心类型
│   │   │   ├── settings.py                        # 配置加载与校验
│   │   │   ├── constants.py                       # 常量定义
│   │   │   ├── exceptions.py                      # 异常定义
│   │   │   └── logging.py                         # 日志配置与封装
│   │   ├── mcp_server/                            # MCP 服务层目录
│   │   │   ├── __init__.py                        # Python 包初始化
│   │   │   ├── server.py                          # MCP Server 入口
│   │   │   ├── lifecycle.py                       # initialize/health/shutdown
│   │   │   ├── tool_registry.py                   # tools/list 注册
│   │   │   ├── schemas.py                         # Tool 输入输出 Schema
│   │   │   └── tools/                             # MCP 工具实现目录
│   │   │       ├── __init__.py                    # Python 包初始化
│   │   │       ├── query_knowledge_hub.py         # 主检索工具
│   │   │       ├── retrieve_context.py            # 上下文检索工具
│   │   │       ├── list_collections.py            # 集合列表工具
│   │   │       ├── get_document_summary.py        # 文档摘要工具
│   │   │       ├── list_document_sections.py      # 文档章节浏览工具
│   │   │       ├── ingest_document.py             # 文档摄取工具
│   │   │       ├── reindex_document.py            # 文档重建索引工具
│   │   │       └── verify_answer.py               # 答案事实核查工具
│   │   ├── ingestion/                              # 摄取流水线目录
│   │   │   ├── __init__.py                        # Python 包初始化
│   │   │   ├── pipeline.py                        # IngestionPipeline 主流程
│   │   │   ├── document_manager.py                # 文档生命周期管理
│   │   │   ├── file_integrity_checker.py         # 文件哈希去重
│   │   │   ├── progress_callback.py               # 摄取进度回调定义
│   │   │   ├── loaders/                           # 文档加载器目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   ├── base_loader.py                 # 加载器抽象接口
│   │   │   │   ├── pdf_loader_markitdown.py       # PDF 解析加载器
│   │   │   │   └── word_loader_markitdown.py      # Word 解析加载器
│   │   │   ├── splitters/                         # 文本切分器目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   ├── base_splitter.py               # 切分器抽象接口
│   │   │   │   ├── recursive_character_splitter.py# 递归字符切分实现
│   │   │   │   └── parent_child_splitter.py       # 父子块切分实现
│   │   │   ├── transforms/                        # 数据增强转换目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   ├── base_transform.py              # 转换器抽象接口
│   │   │   │   ├── chunk_refine_transform.py      # Chunk 精炼转换实现
│   │   │   │   ├── metadata_enrich_transform.py   # 元数据增强转换实现
│   │   │   │   └── image_caption_transform.py     # 图片描述增强实现
│   │   │   ├── embedding/                          # 向量编码目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   ├── dense_embedder.py              # 稠密向量编码实现
│   │   │   │   ├── sparse_encoder_bm25.py         # BM25 稀疏编码实现
│   │   │   │   └── incremental_embedding.py       # 增量向量化策略实现
│   │   │   └── upsert/                            # 写入与幂等目录
│   │   │       ├── __init__.py                    # Python 包初始化
│   │   │       ├── upsert_service.py              # 批量写入服务
│   │   │       ├── dedup_service.py               # 去重服务
│   │   │       └── chunk_id.py                    # Chunk ID 生成策略
│   │   ├── retrieval/                              # 检索流水线目录
│   │   │   ├── __init__.py                        # Python 包初始化
│   │   │   ├── retrieval_pipeline.py              # 检索主流程实现
│   │   │   ├── query_processor.py                 # 查询预处理实现
│   │   │   ├── keyword_extractor.py               # 关键词提取实现
│   │   │   ├── query_expander.py                  # 查询扩展实现
│   │   │   ├── metadata_filter_parser.py          # 元数据过滤解析
│   │   │   ├── dense_retriever.py                 # 稠密检索实现
│   │   │   ├── sparse_retriever.py                # 稀疏检索实现
│   │   │   ├── hybrid_retriever.py                # 混合检索实现
│   │   │   ├── rrf_fusion.py                      # RRF 融合实现
│   │   │   ├── parent_child_resolver.py           # 父子文档聚合解析
│   │   │   └── response_builder.py                # 检索响应构建
│   │   ├── rerank/                                 # 重排模块目录
│   │   │   ├── __init__.py                        # Python 包初始化
│   │   │   ├── base_reranker.py                   # 重排器抽象接口
│   │   │   ├── none_reranker.py                   # 空重排实现
│   │   │   ├── cross_encoder_reranker.py          # Cross-Encoder 重排实现
│   │   │   └── llm_reranker.py                    # LLM 重排实现
│   │   ├── storage/                                # 存储适配目录
│   │   │   ├── __init__.py                        # Python 包初始化
│   │   │   ├── vector/                            # 向量存储实现目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   ├── base_vector_store.py           # 向量存储抽象接口
│   │   │   │   └── pgvector_store.py              # PgVector 存储实现
│   │   │   ├── bm25/                              # BM25 稀疏检索目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   ├── bm25_indexer.py               # BM25 索引构建实现
│   │   │   │   └── bm25_repository.py             # BM25 持久化访问实现
│   │   │   ├── image/                              # 图片存储与索引目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   ├── image_storage.py               # 图片文件存储实现
│   │   │   │   └── image_index_repository.py      # 图片索引访问实现
│   │   │   ├── integrity/                          # 完整性记录目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   └── ingestion_history_repository.py# 摄取历史访问实现
│   │   │   ├── cache/                              # 处理缓存记录目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   └── processing_cache_repository.py # 图片描述哈希缓存访问实现
│   │   │   └── db/                                 # 数据库连接与会话目录
│   │   │       ├── __init__.py                    # Python 包初始化
│   │   │       ├── engine.py                      # 数据库引擎创建
│   │   │       └── session.py                     # 数据库会话管理
│   │   ├── observability/                          # 可观测追踪目录
│   │   │   ├── __init__.py                        # Python 包初始化
│   │   │   ├── trace_context.py                   # 追踪上下文实现
│   │   │   ├── trace_models.py                    # 追踪数据模型
│   │   │   ├── trace_repository.py                # 追踪持久化访问
│   │   │   ├── trace_exporter_jsonl.py            # JSONL 追踪导出实现
│   │   │   └── trace_service.py                   # 追踪查询服务
│   │   ├── factories/                              # 工厂模式实例化目录
│   │   │   ├── __init__.py                        # Python 包初始化
│   │   │   ├── llm_factory.py                     # LLM 实例工厂
│   │   │   ├── vision_llm_factory.py              # Vision LLM 实例工厂
│   │   │   ├── embedding_factory.py               # Embedding 实例工厂
│   │   │   ├── splitter_factory.py                # Splitter 实例工厂
│   │   │   ├── vector_store_factory.py            # 向量存储实例工厂
│   │   │   ├── reranker_factory.py                # Reranker 实例工厂
│   │   │   └── evaluator_factory.py               # Evaluator 实例工厂
│   │   ├── evaluation/                             # 评估体系目录
│   │   │   ├── __init__.py                        # Python 包初始化
│   │   │   ├── base_evaluator.py                  # 评估器抽象接口
│   │   │   ├── ragas_evaluator.py                 # Ragas 评估器实现
│   │   │   ├── custom_metrics_evaluator.py        # 自定义指标评估器实现
│   │   │   ├── composite_evaluator.py             # 组合评估器实现
│   │   │   └── eval_runner.py                     # 评估任务执行器
│   │   ├── libs/                                   # 第三方能力封装目录
│   │   │   ├── llm/                                # LLM 适配实现目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   ├── base_llm.py                    # LLM 抽象基类
│   │   │   │   ├── azure_openai_llm.py            # Azure OpenAI 适配
│   │   │   │   ├── openai_llm.py                  # OpenAI 适配
│   │   │   │   ├── qwen_llm.py                    # QWEN 适配
│   │   │   │   ├── vllm_llm.py                    # VLLM 适配
│   │   │   │   ├── deepseek_llm.py                # DeepSeek 适配
│   │   │   │   └── ollama_llm.py                  # Ollama 适配
│   │   │   ├── embedding/                          # 向量编码目录
│   │   │   │   ├── __init__.py                    # Python 包初始化
│   │   │   │   ├── base_embedding.py                        # Embedding 抽象基类
│   │   │   │   ├── openai_embedding.py            # OpenAI Embedding 适配
│   │   │   │   ├── bge_embedding.py               # BGE Embedding 适配
│   │   │   │   └── ollama_embedding.py            # Ollama Embedding 适配
│   │   │   └── vision/                             # 视觉模型适配目录
│   │   │       ├── __init__.py                    # Python 包初始化
│   │   │       ├── base_vision_llm.py             # 视觉模型抽象基类
│   │   │       ├── azure_vision_llm.py            # Azure Vision 适配
│   │   │       └── qwen_vl_client.py              # Qwen-VL 客户端适配
│   │   └── utils/                                  # 通用工具函数目录
│   │       ├── __init__.py                        # Python 包初始化
│   │       ├── hash_utils.py                      # 哈希工具函数
│   │       ├── file_utils.py                      # 文件工具函数
│   │       ├── text_utils.py                      # 文本工具函数
│   │       └── retry.py                           # 重试策略工具
│   │
│   ├── config/                                    # 配置目录
│   │   ├── settings.yaml                          # 运行参数配置
│   │   └── prompts/                               # 提示词模板目录
│   │       ├── query_rewrite.md                   # 查询改写提示词
│   │       ├── rerank_policy.md                   # 重排策略提示词
│   │       └── image_caption.md                   # 图片描述提示词，区分图片类型
│   ├── sql/                                       # 数据库初始化脚本目录（Docker 可映射至 /docker-entrypoint-initdb.d/）
│   │   ├── 001_observability.sql                  # 追踪表初始化脚本
│   │   ├── 002_ingestion_history.sql              # 摄取历史表初始化脚本
│   │   ├── 003_image_index.sql                    # 图片索引表初始化脚本
│   │   ├── 004_bm25_meta.sql                      # BM25 元数据表初始化脚本
│   │   └── 005_processing_cache.sql               # 图片描述哈希缓存表初始化脚本
│   │
│   ├── data/                                       # RAG Server 约定数据目录
│   │   ├── documents/                              # 原始文档存放
│   │   │   └── {collection}/                       # 按集合分类
│   │   ├── eval/                                   # 评估样本目录
│   │   │   └── golden_set.jsonl                    # 黄金评估样本集
│   │   ├── images/                                 # 提取图片存放
│   │   │   └── {collection}/                       # 按集合分类
│   │   │       └── {doc_hash}/                     # 按文档哈希分目录
│   │   └── db/                                     # PostgreSQL 数据卷挂载点（Docker 持久化）
│   ├── cache/                                      # 统一缓存根目录（便于整体迁移）
│   │   ├── embedding/                              # 向量编码目录
│   │   ├── image_caption/                          # 图片描述缓存目录
│   │   └── processing_state/                       # 处理状态缓存目录
│   ├── logs/                                       # 统一日志根目录（便于整体迁移）
│   │   └── rag/                                    # RAG 服务日志目录
│   │       ├── app.jsonl                           # 应用结构化日志文件
│   │       └── traces.jsonl                        # 追踪日志导出文件
│   │
│   ├── scripts/                                    # 运行与维护脚本目录
│   │   ├── run_mcp_server.py                       # 启动 MCP Server 脚本
│   │   ├── ingest_document.py                      # 手动摄取文档脚本
│   │   ├── reindex_document.py                     # 重建索引脚本
│   │   ├── init_db.py                              # 初始化数据库脚本
│   │   ├── export_traces.py                        # 导出追踪数据脚本
│   │   └── run_eval.py                             # 评估任务执行脚本
│   └── tests/                                      # 自动化测试目录
│       ├── conftest.py                             # 共享 Fixture 定义
│       ├── unit/                                   # 单元测试目录
│       │   ├── test_loader_pdf.py                  # Python 自动化测试
│       │   ├── test_splitter_recursive.py          # Python 自动化测试
│       │   ├── test_transform_image_caption.py     # Python 自动化测试
│       │   ├── test_rrf_fusion.py                  # Python 自动化测试
│       │   ├── test_reranker_fallback.py           # Python 自动化测试
│       │   └── test_trace_context.py               # Python 自动化测试
│       ├── integration/                            # 集成测试目录
│       │   ├── test_ingestion_pipeline.py          # Python 自动化测试
│       │   ├── test_hybrid_retrieval.py            # Python 自动化测试
│       │   ├── test_mcp_tools.py                   # Python 自动化测试
│       │   └── test_document_manager.py            # Python 自动化测试
│       └── e2e/                                    # 端到端测试目录
│           ├── test_stdio_workflow.py              # Python 自动化测试
│           └── test_multimodal_response.py         # Python 自动化测试
│
├── sgcc-report-audit-app/                          # 业务应用（前后端分离）
│   ├── .env                                         # 本地环境变量配置
│   ├── .env.example                                 # 环境变量模板
│   ├── README.md                                    # 项目说明文档
│   │
│   ├── config/                                      # 配置目录
│   │   ├── settings.yaml                            # 业务主配置
│   │   ├── mcp_client.yaml                          # RAG Server 连接配置
│   │   ├── data_mapping.yaml                        # data 映射路径配置（可配置）
│   │   ├── logging.yaml                             # 日志配置
│   │   └── prompts/                                 # 20 个审查要点定制提示词
│   │       ├── common/                              # 通用提示词目录
│   │       │   ├── system.md                        # 系统提示词模板
│   │       │   └── output_schema.md                 # 输出结构约束模板
│   │       ├── check_01_qualification.md            # 单项审查提示词
│   │       ├── check_02_approval.md                 # 单项审查提示词
│   │       ├── check_03_basis.md                    # 单项审查提示词
│   │       ├── check_04_access_info.md              # 单项审查提示词
│   │       ├── check_05_equipment_params.md         # 单项审查提示词
│   │       ├── check_06_disturbance_source.md       # 单项审查提示词
│   │       ├── check_07_raw_materials.md            # 单项审查提示词
│   │       ├── check_08_grid_equipment.md           # 单项审查提示词
│   │       ├── check_09_grid_capacity.md            # 单项审查提示词
│   │       ├── check_10_indicators.md               # 单项审查提示词
│   │       ├── check_11_limits.md                   # 单项审查提示词
│   │       ├── check_12_background_test.md          # 单项审查提示词
│   │       ├── check_13_superposition.md            # 单项审查提示词
│   │       ├── check_14_simulation_model.md         # 单项审查提示词
│   │       ├── check_15_assessment_point.md         # 单项审查提示词
│   │       ├── check_16_operation_mode.md           # 单项审查提示词
│   │       ├── check_17_calculation_result.md       # 单项审查提示词
│   │       ├── check_18_conclusion.md               # 单项审查提示词
│   │       ├── check_19_governance.md               # 单项审查提示词
│   │       └── check_20_monitoring.md               # 单项审查提示词
│   │
│   ├── cache@ -> ../rag-server/cache/               # 链接到 RAG Server 缓存目录
│   ├── logs@ -> ../rag-server/logs/                 # 链接到 RAG Server 日志目录
│   │
│   ├── data/                                         # 不落原始文档，仅做映射入口
│   │   ├── documents@ -> ../../rag-server/data/documents/# 链接映射入口
│   │   ├── images@ -> ../../rag-server/data/images/ # 链接映射入口
│   │   └── README.md                                 # 说明该目录为映射目录
│   │
│   ├── backend/                                      # MVC 后端（核心能力调用 RAG Server）
│   │   ├── pyproject.toml                            # Python 项目与依赖配置
│   │   ├── uv.lock                                   # uv 依赖锁定文件
│   │   ├── pytest.ini                                # pytest 配置文件
│   │   ├── README.md                                 # 项目说明文档
│   │   ├── src/                                      # 源代码目录
│   │   │   └── sgcc_audit/                          # 业务后端主包目录
│   │   │       ├── __init__.py                      # Python 包初始化
│   │   │       ├── main.py                          # FastAPI 入口
│   │   │       ├── controllers/                     # C: 路由入口与请求编排
│   │   │       │   ├── __init__.py                  # Python 包初始化
│   │   │       │   ├── health_controller.py         # 健康检查控制器
│   │   │       │   ├── audit_controller.py          # 审查任务控制器
│   │   │       │   ├── trace_controller.py          # 追踪查询控制器
│   │   │       │   └── document_controller.py       # 文档管理控制器
│   │   │       ├── models/                          # M: 领域模型/ORM
│   │   │       │   ├── __init__.py                  # Python 包初始化
│   │   │       │   ├── audit_task.py                # 审查任务模型
│   │   │       │   ├── audit_result.py              # 审查结果模型
│   │   │       │   ├── check_item.py                # 单项审查结果模型
│   │   │       │   ├── evidence.py                  # 证据模型
│   │   │       │   └── report_profile.py            # 报告画像模型
│   │   │       ├── views/                           # V: 响应视图/DTO 序列化
│   │   │       │   ├── __init__.py                  # Python 包初始化
│   │   │       │   ├── audit_response_view.py       # 审查结果视图模型
│   │   │       │   └── error_view.py                # 错误响应视图模型
│   │   │       ├── services/                        # 业务服务（20项审查编排）
│   │   │       │   ├── __init__.py                  # Python 包初始化
│   │   │       │   ├── audit_orchestrator.py        # 审查编排服务
│   │   │       │   ├── check_dispatcher.py          # 规则分发服务
│   │   │       │   ├── evidence_service.py          # 证据聚合服务
│   │   │       │   ├── result_merge_service.py      # 结果合并服务
│   │   │       │   ├── prompt_service.py            # 提示词加载服务
│   │   │       │   └── checks/                      # 20 项规则实现目录
│   │   │       │       ├── __init__.py              # Python 包初始化
│   │   │       │       ├── check_01_qualification.py# 单项审查规则实现
│   │   │       │       ├── check_02_approval.py     # 单项审查规则实现
│   │   │       │       ├── check_03_basis.py        # 单项审查规则实现
│   │   │       │       ├── check_04_access_info.py  # 单项审查规则实现
│   │   │       │       ├── check_05_equipment_params.py# 单项审查规则实现
│   │   │       │       ├── check_06_disturbance_source.py# 单项审查规则实现
│   │   │       │       ├── check_07_raw_materials.py# 单项审查规则实现
│   │   │       │       ├── check_08_grid_equipment.py# 单项审查规则实现
│   │   │       │       ├── check_09_grid_capacity.py# 单项审查规则实现
│   │   │       │       ├── check_10_indicators.py   # 单项审查规则实现
│   │   │       │       ├── check_11_limits.py       # 单项审查规则实现
│   │   │       │       ├── check_12_background_test.py# 单项审查规则实现
│   │   │       │       ├── check_13_superposition.py# 单项审查规则实现
│   │   │       │       ├── check_14_simulation_model.py# 单项审查规则实现
│   │   │       │       ├── check_15_assessment_point.py# 单项审查规则实现
│   │   │       │       ├── check_16_operation_mode.py# 单项审查规则实现
│   │   │       │       ├── check_17_calculation_result.py# 单项审查规则实现
│   │   │       │       ├── check_18_conclusion.py   # 单项审查规则实现
│   │   │       │       ├── check_19_governance.py   # 单项审查规则实现
│   │   │       │       └── check_20_monitoring.py   # 单项审查规则实现
│   │   │       ├── repositories/                    # 数据访问
│   │   │       │   ├── __init__.py                  # Python 包初始化
│   │   │       │   ├── audit_task_repository.py     # 审查任务仓储
│   │   │       │   ├── audit_result_repository.py   # 审查结果仓储
│   │   │       │   └── trace_repository.py          # 追踪持久化访问
│   │   │       ├── clients/                         # 外部服务客户端目录
│   │   │       │   ├── __init__.py                  # Python 包初始化
│   │   │       │   ├── rag_mcp_client.py            # MCP 客户端，调用 rag-server
│   │   │       │   └── rag_tool_adapter.py          # RAG 工具调用适配
│   │   │       ├── schemas/                         # 请求响应模型目录
│   │   │       │   ├── __init__.py                  # Python 包初始化
│   │   │       │   ├── request_models.py            # 请求模型定义
│   │   │       │   ├── response_models.py           # 响应模型定义
│   │   │       │   └── enums.py                     # 枚举定义
│   │   │       └── core/                            # 核心基础模块目录
│   │   │           ├── __init__.py                  # Python 包初始化
│   │   │           ├── config.py                    # 配置读取封装
│   │   │           ├── dependencies.py              # 依赖注入定义
│   │   │           ├── logging.py                   # 日志配置与封装
│   │   │           ├── constants.py                 # 常量定义
│   │   │           └── exceptions.py                # 异常定义
│   │   ├── sql/                                      # 业务数据库初始化脚本目录
│   │   │   └── 001_audit_tables.sql                  # 审查任务与结果表初始化脚本
│   │   └── tests/                                    # 自动化测试目录
│   │       ├── conftest.py                           # 共享 Fixture 定义
│   │       ├── unit/                                 # 单元测试目录
│   │       │   ├── test_check_dispatcher.py         # Python 自动化测试
│   │       │   ├── test_evidence_service.py         # Python 自动化测试
│   │       │   └── test_result_merge_service.py     # Python 自动化测试
│   │       ├── integration/                          # 集成测试目录
│   │       │   ├── test_submit_audit_api.py         # Python 自动化测试
│   │       │   └── test_get_result_api.py           # Python 自动化测试
│   │       └── e2e/                                  # 端到端测试目录
│   │           └── test_a1_a4_business_cases.py     # Python 自动化测试
│   │
│   ├── frontend/                                     # Vue3 前端
│   │   ├── package.json                              # 前端项目与脚本配置
│   │   ├── package-lock.json                         # npm 依赖锁定文件
│   │   ├── vite.config.ts                            # Vite 构建配置
│   │   ├── tsconfig.json                             # TypeScript 编译配置
│   │   ├── env.d.ts                                  # 前端环境变量类型声明
│   │   ├── index.html                                # 前端入口 HTML
│   │   ├── public/                                   # 前端静态资源目录
│   │   │   └── favicon.ico                          # 站点图标
│   │   └── src/                                      # 源代码目录
│   │       ├── main.ts                               # 前端应用启动入口
│   │       ├── App.vue                               # 前端根组件
│   │       ├── router/                               # 前端路由目录
│   │       │   └── index.ts                          # 路由表定义
│   │       ├── layouts/                              # 前端布局目录
│   │       │   └── AppShell.vue                      # 全局壳层布局组件
│   │       ├── stores/                               # 前端状态管理目录
│   │       │   ├── app.ts                            # 全局状态仓库
│   │       │   ├── audit.ts                          # 审查状态仓库
│   │       │   └── trace.ts                          # 追踪状态仓库
│   │       ├── api/                                  # 前端 API 调用目录
│   │       │   ├── http.ts                           # HTTP 客户端封装
│   │       │   ├── audit.ts                          # 审查 API 封装
│   │       │   ├── trace.ts                          # 追踪 API 封装
│   │       │   └── documents.ts                      # 文档 API 封装
│   │       ├── views/                                # 前端页面目录
│   │       │   ├── AuditResultView.vue               # 审查结果页面
│   │       │   ├── OverviewView.vue                  # 系统总览页面
│   │       │   ├── DataBrowserView.vue               # 数据浏览页面
│   │       │   ├── IngestionManagerView.vue          # 摄取管理页面
│   │       │   ├── IngestionTracesView.vue           # 摄取追踪页面
│   │       │   ├── QueryTracesView.vue               # 查询追踪页面
│   │       │   └── EvaluationPanelView.vue           # 评估面板页面
│   │       ├── components/                           # 前端组件目录
│   │       │   ├── audit/                            # 审查结果组件目录
│   │       │   │   ├── CheckItemTable.vue            # 审查项表格组件
│   │       │   │   └── EvidenceDrawer.vue            # 证据侧栏组件
│   │       │   ├── traces/                           # 追踪可视化组件目录
│   │       │   │   ├── WaterfallChart.vue            # 瀑布图组件
│   │       │   │   └── TraceDetailPanel.vue          # 追踪详情组件
│   │       │   ├── data/                             # 数据浏览组件目录
│   │       │   │   ├── ChunkViewer.vue               # Chunk 浏览组件
│   │       │   │   └── ImagePreview.vue              # 图片预览组件
│   │       │   └── common/                           # 通用组件目录
│   │       │       ├── StatusTag.vue                 # 状态标签组件
│   │       │       └── EmptyState.vue                # 空状态组件
│   │       ├── assets/                               # 前端资源目录
│   │       │   ├── styles/                           # 前端样式目录
│   │       │   │   ├── variables.css                 # 样式变量定义
│   │       │   │   └── global.css                    # 全局样式定义
│   │       │   └── images/                           # 图片资源目录
│   │       ├── mock/                                 # 前端 Mock 数据目录
│   │       │   └── mock.ts                           # Mock 数据与拦截逻辑
│   │       └── types/                                # 前端类型定义目录
│   │           └── index.ts                          # 前端接口类型定义
│   ├── tests/                                        # 自动化测试目录
│   │   ├── playwright.config.ts                      # Playwright 测试配置
│   │   └── e2e/                                      # 端到端测试目录
│   │       ├── audit-result.spec.ts                  # 审查结果页面 E2E 测试
│   │       └── traces.spec.ts                        # 追踪页面 E2E 测试
│   │
│   └── scripts/                                      # 运行与维护脚本目录
│       ├── run_backend.sh                            # 启动业务后端脚本
│       ├── run_frontend.sh                           # 启动业务前端脚本
│       ├── sync_workspace_links.sh                  # 按配置创建/刷新 data/cache/logs 映射
│       ├── init_db.py                                # 初始化业务数据库表脚本
│       ├── docker_up.sh                              # Docker 一键启动脚本
│       ├── docker_down.sh                            # Docker 一键停止脚本
│       └── docker_logs.sh                            # Docker 日志查看脚本
│
└── docs/                                            # 项目文档目录
    ├── architecture/                                # 架构文档目录
    │   ├── context.md                               # 系统上下文架构文档
    │   ├── containers.md                            # 容器级架构文档
    │   └── components.md                            # 组件级架构文档
    ├── api/                                         # API 文档目录
    │   ├── sgcc-backend-openapi.md                  # 业务后端 API 文档
    │   └── mcp-tools.md                             # MCP 工具说明文档
    └── runbooks/                                    # 运维手册目录
        ├── local-dev.md                             # 本地开发运行手册
        ├── deployment.md                            # 部署手册
        └── troubleshooting.md                       # 故障排查手册
```

**映射配置约定（`sgcc-report-audit-app/config/data_mapping.yaml`）**

```yaml
rag_data_root: "../../rag-server/data"
documents_target: "${rag_data_root}/documents"
images_target: "${rag_data_root}/images"
local_data_dir: "./data"
rag_cache_root: "../rag-server/cache"
local_cache_link: "./cache"
rag_logs_root: "../rag-server/logs"
local_logs_link: "./logs"
mapping_mode: "symlink" # symlink | bind_mount
read_only: true
```

说明：`sgcc-report-audit-app` 的 `data/`、`cache/`、`logs/` 均为业务侧统一入口，不直接作为独立持久化根目录；实际持久化由 `rag-server` 统一托管。

### 5.3 启动与部署目录约定

#### 5.3.1 启动顺序与命令约定

统一约定：先初始化目录映射，再初始化数据库，再启动 RAG Server（如需外部 MCP Client 直连），再启动业务后端，最后启动前端。

1. 初始化工作区映射（`data/cache/logs`）

```bash
cd sgcc-report-audit-app
bash scripts/sync_workspace_links.sh \
  --config config/data_mapping.yaml \
  --mode symlink \
  --force
```

2. 初始化数据库（首次部署或表结构变更时执行）

```bash
# 初始化 RAG Server 表（obs_traces, ingestion_history, image_index, bm25_meta, processing_cache）
cd rag-server
uv run python scripts/init_db.py --config config/settings.yaml

# 初始化业务表（audit_tasks, audit_results 等）
cd sgcc-report-audit-app
python scripts/init_db.py --config config/settings.yaml
```

3. 启动 RAG Server（仅用于外部 MCP Client 直连场景；SGCC 全栈模式可跳过——FastAPI 后端会通过 `rag_mcp_client.py` 自动以子进程方式启动 MCP Server）

```bash
cd rag-server
uv sync
uv run python scripts/run_mcp_server.py --config config/settings.yaml
```

4. 启动 SGCC 后端（MVC，`uv`）

```bash
cd sgcc-report-audit-app/backend
uv sync
uv run python -m sgcc_audit.main --host 0.0.0.0 --port 8080
```

5. 启动 SGCC 前端（Vue3 + Vite）

```bash
cd sgcc-report-audit-app/frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

#### 5.3.2 部署目录与运行约定

1. 持久化根目录统一放在 `rag-server/` 下：`data/`、`cache/`、`logs/`。
2. `sgcc-report-audit-app/` 仅通过链接访问持久化目录，不单独持久化同名目录。
3. 所有运行命令以各自子项目目录作为 CWD，避免相对路径漂移。
4. 配置来源统一：
   - RAG Server 使用 `rag-server/config/settings.yaml`
   - SGCC 业务应用使用 `sgcc-report-audit-app/config/settings.yaml`
   - 映射规则使用 `sgcc-report-audit-app/config/data_mapping.yaml`
5. 生产环境建议：
   - 后端服务可替换为 `uv run uvicorn sgcc_audit.main:app --host 0.0.0.0 --port 8080 --workers 2`
   - 前端使用 `npm run build` 后由静态 Web Server 托管
   - `sync_workspace_links.sh` 在部署前作为必执行步骤

#### 5.3.3 `sync_workspace_links.sh` 规范伪代码

```bash
#!/usr/bin/env bash
set -euo pipefail

# 输入参数（建议）
# --config <path>    默认: config/data_mapping.yaml
# --mode <mode>      symlink | bind_mount（默认读取配置）
# --force            目标已存在时覆盖
# --dry-run          只打印不执行

CONFIG_PATH="config/data_mapping.yaml"
MODE_OVERRIDE=""
FORCE="false"
DRY_RUN="false"

parse_args "$@"

# 从 YAML 读取配置（可用 yq 或 python -c）
RAG_DATA_ROOT=read_yaml "$CONFIG_PATH" "rag_data_root"
DOCS_TARGET=read_yaml "$CONFIG_PATH" "documents_target"
IMAGES_TARGET=read_yaml "$CONFIG_PATH" "images_target"
LOCAL_DATA_DIR=read_yaml "$CONFIG_PATH" "local_data_dir"
RAG_CACHE_ROOT=read_yaml "$CONFIG_PATH" "rag_cache_root"
LOCAL_CACHE_LINK=read_yaml "$CONFIG_PATH" "local_cache_link"
RAG_LOGS_ROOT=read_yaml "$CONFIG_PATH" "rag_logs_root"
LOCAL_LOGS_LINK=read_yaml "$CONFIG_PATH" "local_logs_link"
MODE_CFG=read_yaml "$CONFIG_PATH" "mapping_mode"
READ_ONLY=read_yaml "$CONFIG_PATH" "read_only"

MODE="${MODE_OVERRIDE:-$MODE_CFG}"

ensure_dir "$DOCS_TARGET"
ensure_dir "$IMAGES_TARGET"
ensure_dir "$RAG_CACHE_ROOT"
ensure_dir "$RAG_LOGS_ROOT"
ensure_dir "$LOCAL_DATA_DIR"

ensure_link() {
  local link_path="$1"
  local target_path="$2"

  if [[ -L "$link_path" ]]; then
    local current
    current="$(readlink "$link_path")"
    if [[ "$(realpath -m "$current")" == "$(realpath -m "$target_path")" ]]; then
      return 0
    fi
    [[ "$FORCE" == "true" ]] || { echo "link exists and points elsewhere: $link_path"; exit 1; }
    run rm -f "$link_path"
  elif [[ -e "$link_path" ]]; then
    [[ "$FORCE" == "true" ]] || { echo "path exists and is not symlink: $link_path"; exit 1; }
    run rm -rf "$link_path"
  fi

  run ln -s "$target_path" "$link_path"
}

ensure_bind_mount() {
  local mount_point="$1"
  local source_path="$2"

  ensure_dir "$mount_point"

  # 需要 root 权限；无权限时建议回退 symlink
  if [[ "${EUID}" -ne 0 ]]; then
    echo "bind_mount requires root; fallback to symlink"
    ensure_link "$mount_point" "$source_path"
    return 0
  fi

  run mountpoint -q "$mount_point" || run mount --bind "$source_path" "$mount_point"
  if [[ "$READ_ONLY" == "true" ]]; then
    run mount -o remount,bind,ro "$mount_point"
  fi
}

run() {
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

if [[ "$MODE" == "symlink" ]]; then
  ensure_link "$LOCAL_DATA_DIR/documents" "$DOCS_TARGET"
  ensure_link "$LOCAL_DATA_DIR/images" "$IMAGES_TARGET"
  ensure_link "$LOCAL_CACHE_LINK" "$RAG_CACHE_ROOT"
  ensure_link "$LOCAL_LOGS_LINK" "$RAG_LOGS_ROOT"
elif [[ "$MODE" == "bind_mount" ]]; then
  ensure_bind_mount "$LOCAL_DATA_DIR/documents" "$DOCS_TARGET"
  ensure_bind_mount "$LOCAL_DATA_DIR/images" "$IMAGES_TARGET"
  ensure_bind_mount "$LOCAL_CACHE_LINK" "$RAG_CACHE_ROOT"
  ensure_bind_mount "$LOCAL_LOGS_LINK" "$RAG_LOGS_ROOT"
else
  echo "unsupported mode: $MODE"
  exit 1
fi

echo "workspace links initialized"
```

补充约定：

1. `--force` 仅覆盖链接或映射目标，不删除 `rag-server` 下真实数据目录。
2. `bind_mount + read_only=true` 优先用于生产环境；开发环境默认 `symlink`。
3. 每次部署前都应先执行一次 `sync_workspace_links.sh`，再启动任何服务进程。

### 5.4 模块说明（自顶向下分层）

本小节按系统调用链路自顶向下描述各层模块职责。设计约束为：上层只依赖下层公开接口，避免跨层直接调用具体实现。

#### 5.4.1 L1 交互与展示层（Client/UI）

| 模块                                                               | 职责                                           | 关键技术点                                                         |
| ------------------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------------ |
| `sgcc-report-audit-app/frontend/src/views/AuditResultView.vue`     | 展示单份报告 20 项审查结果、判定说明与证据入口 | Vue 3 组合式 API，按审查项分组渲染，证据定位跳转（页码/段落/截图） |
| `sgcc-report-audit-app/frontend/src/views/IngestionTracesView.vue` | 展示摄取链路追踪历史与单次详情                 | Trace 列表筛选，阶段耗时瀑布图联动详情面板                         |
| `sgcc-report-audit-app/frontend/src/views/QueryTracesView.vue`     | 展示查询链路追踪与召回/重排变化                | Dense/Sparse/Fusion/Rerank 分阶段对比，Top-K 结果可视化            |
| `sgcc-report-audit-app/frontend/src/router/index.ts`               | 管理七页面路由与导航守卫                       | Vue Router 路由表，页面级懒加载                                    |
| `sgcc-report-audit-app/frontend/src/stores/audit.ts`               | 管理审查任务与结果状态                         | Pinia 状态管理，请求状态机（idle/running/success/error）           |
| `sgcc-report-audit-app/frontend/src/api/http.ts`                   | 封装前端统一 HTTP 调用                         | Axios 拦截器、统一错误映射、请求超时控制                           |

#### 5.4.2 L2 接口接入层（FastAPI + MCP）

| 模块                                                                           | 职责                                  | 关键技术点                                                   |
| ------------------------------------------------------------------------------ | ------------------------------------- | ------------------------------------------------------------ |
| `sgcc-report-audit-app/backend/src/sgcc_audit/main.py`                         | 业务后端入口，注册路由和依赖          | FastAPI 应用装配，生命周期钩子，依赖注入                     |
| `sgcc-report-audit-app/backend/src/sgcc_audit/controllers/audit_controller.py` | 接收审查任务请求并返回任务状态        | 请求参数校验，异步任务触发，统一响应模型                     |
| `sgcc-report-audit-app/backend/src/sgcc_audit/controllers/trace_controller.py` | 提供追踪查询 API                      | trace_id 检索，分页与过滤条件解析                            |
| `rag-server/src/mcp_server/server.py`                                          | MCP Server 主入口，处理 JSON-RPC 交互 | Python 官方 MCP SDK，Stdio Transport，stdout/stderr 通道隔离 |
| `rag-server/src/mcp_server/tool_registry.py`                                   | 工具注册与能力暴露                    | `tools/list` 声明，输入输出 Schema 绑定                      |
| `rag-server/src/mcp_server/tools/query_knowledge_hub.py`                       | 对外主检索工具                        | Tool 参数解析，检索流水线编排，引用透明输出                  |

#### 5.4.3 L3 业务编排层（MVC Domain Service）

| 模块                                                                                     | 职责                                           | 关键技术点                                             |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------ |
| `sgcc-report-audit-app/backend/src/sgcc_audit/services/audit_orchestrator.py`            | 审查总编排，驱动 20 项规则执行                 | 流程编排（预处理 -> 分项审查 -> 汇总），失败隔离与回退 |
| `sgcc-report-audit-app/backend/src/sgcc_audit/services/check_dispatcher.py`              | 分发并调度各审查项规则                         | 规则注册表，按审查项 ID 动态路由实现                   |
| `sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_01_qualification.py` | 第 1 项“评估单位”规则实现（其余 02~20 同模式） | 模板化规则接口，证据抽取 + 判定输出标准化              |
| `sgcc-report-audit-app/backend/src/sgcc_audit/services/evidence_service.py`              | 聚合并规范化证据数据                           | 证据去重，来源定位结构化（source/page/chunk_id）       |
| `sgcc-report-audit-app/backend/src/sgcc_audit/services/result_merge_service.py`          | 合并 20 项结果并生成最终报告                   | 结果完整性检查，枚举值校验，排序与统计                 |
| `sgcc-report-audit-app/backend/src/sgcc_audit/clients/rag_mcp_client.py`                 | 业务侧 MCP 客户端调用封装                      | Stdio 子进程通信，超时/重试策略，错误码映射            |
| `sgcc-report-audit-app/backend/src/sgcc_audit/models/check_item.py`                      | 单项审查领域模型                               | Pydantic/ORM 双向约束，状态与证据结构统一              |
| `sgcc-report-audit-app/backend/src/sgcc_audit/views/audit_response_view.py`              | 输出 DTO 视图模型                              | 对外响应字段稳定性，向后兼容约束                       |

#### 5.4.4 L4 RAG 核心引擎层（Ingestion + Retrieval + Rerank）

| 模块                                                                 | 职责                                                            | 关键技术点                                               |
| -------------------------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------- |
| `rag-server/src/ingestion/pipeline.py`                               | 摄取主流程编排（load -> split -> transform -> embed -> upsert） | 阶段化流水线，进度回调，失败可观测                       |
| `rag-server/src/ingestion/file_integrity_checker.py`                 | 文档去重与增量判断                                              | SHA256 文件指纹，Early Exit 降本                         |
| `rag-server/src/ingestion/loaders/pdf_loader_markitdown.py`          | PDF 解析为标准 `Document`                                       | MarkItDown/MinerU 解析，图片引用抽取                     |
| `rag-server/src/ingestion/splitters/recursive_character_splitter.py` | 文本切块                                                        | LangChain `RecursiveCharacterTextSplitter`，语义边界优先 |
| `rag-server/src/ingestion/transforms/image_caption_transform.py`     | 图片转文本描述并注入 Chunk                                      | Vision LLM，Image-to-Text 策略，缓存与幂等               |
| `rag-server/src/ingestion/embedding/incremental_embedding.py`        | 增量向量化执行                                                  | Dense+Sparse 双路编码，批处理优化                        |
| `rag-server/src/retrieval/retrieval_pipeline.py`                     | 查询检索主流程编排                                              | Query Processing -> Dense/Sparse -> Fusion -> Rerank     |
| `rag-server/src/retrieval/hybrid_retriever.py`                       | 双路召回执行                                                    | BM25 + Dense 并行召回，候选集归一化                      |
| `rag-server/src/retrieval/rrf_fusion.py`                             | 融合排序                                                        | Reciprocal Rank Fusion 减少单路偏差                      |
| `rag-server/src/rerank/cross_encoder_reranker.py`                    | 精排（Cross-Encoder）                                           | 相关性重打分，超时回退到基础排序                         |
| `rag-server/src/retrieval/response_builder.py`                       | 构建带引用响应                                                  | `source_file/page/chunk_id/score` 结构化引用输出         |

#### 5.4.5 L5 可插拔与存储基础层（Factory + Repository）

| 模块                                                               | 职责                    | 关键技术点                                      |
| ------------------------------------------------------------------ | ----------------------- | ----------------------------------------------- |
| `rag-server/src/factories/llm_factory.py`                          | 按配置实例化 LLM 提供者 | 配置驱动路由，Provider 抽象解耦                 |
| `rag-server/src/factories/embedding_factory.py`                    | 选择 Embedding 实现     | OpenAI/BGE/Ollama 可切换，统一调用接口          |
| `rag-server/src/factories/vector_store_factory.py`                 | 选择向量存储实现        | 首期固定 PgVector，接口预留扩展                 |
| `rag-server/src/storage/vector/pgvector_store.py`                  | 向量数据读写            | PgVector 相似度检索，批量 upsert，metadata 过滤 |
| `rag-server/src/storage/bm25/bm25_indexer.py`                      | 稀疏索引构建维护        | BM25 倒排索引更新，统计量持久化                 |
| `rag-server/src/storage/image/image_storage.py`                    | 原图文件存储管理        | 本地文件系统持久化，按集合/文档哈希分层         |
| `rag-server/src/storage/integrity/ingestion_history_repository.py` | 摄取历史与幂等记录      | 历史版本追踪，增量重建判定                      |
| `rag-server/src/storage/cache/processing_cache_repository.py`      | 图片描述哈希缓存        | 内容哈希比对，Vision LLM 调用幂等，避免重复计算 |
| `rag-server/src/storage/db/engine.py`                              | 数据库连接与引擎创建    | SQLAlchemy Engine、连接池、超时参数             |

#### 5.4.6 L6 可观测与质量保障层（Observability + Test）

| 模块                                                                   | 职责                    | 关键技术点                                              |
| ---------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------- |
| `rag-server/src/observability/trace_context.py`                        | 请求级追踪上下文        | `trace_id`、`trace_type`、阶段耗时记录、`finish()` 汇总 |
| `rag-server/src/observability/trace_repository.py`                     | Trace 持久化到数据库    | `obs_traces`/`obs_trace_stages` 写入与查询              |
| `rag-server/src/observability/trace_exporter_jsonl.py`                 | Trace 镜像导出          | JSON Lines 结构化输出，离线排障友好                     |
| `rag-server/src/observability/trace_service.py`                        | Dashboard 读取服务      | 按类型/时间/关键词聚合查询                              |
| `rag-server/tests/integration/test_ingestion_pipeline.py`              | 验证摄取链路集成行为    | 真实样本文档 + 临时库，端到端阶段断言                   |
| `rag-server/tests/integration/test_hybrid_retrieval.py`                | 验证混合检索质量        | Dense/Sparse/Fusion 行为对照，Top-K 命中断言            |
| `sgcc-report-audit-app/backend/tests/e2e/test_a1_a4_business_cases.py` | 验证业务 A1~A4 关键场景 | 20 项结果完整性、证据可追溯、关键 fail 项稳定性         |
| `sgcc-report-audit-app/tests/e2e/audit-result.spec.ts`                 | 验证前端结果展示链路    | Playwright 页面渲染与证据跳转测试                       |

#### 5.4.7 跨层协作约定

| 模块                                                                      | 职责               | 关键技术点                                    |
| ------------------------------------------------------------------------- | ------------------ | --------------------------------------------- |
| `rag-server/src/core/settings.py`                                         | 统一加载并校验配置 | `settings.yaml` 分层配置，环境变量覆盖        |
| `rag-server/src/core/types.py`                                            | 定义跨层通用类型   | `Document/Chunk/RetrievalResult` 统一数据契约 |
| `sgcc-report-audit-app/backend/src/sgcc_audit/schemas/request_models.py`  | 入参契约           | Pydantic 强校验，请求字段约束                 |
| `sgcc-report-audit-app/backend/src/sgcc_audit/schemas/response_models.py` | 出参契约           | 对外响应 schema 固化，避免接口漂移            |

说明：本节表格用于开发分工、代码走查与面试讲解。实际实现时应以“接口稳定、实现可替换、证据可追溯、追踪可观测”为第一约束。

### 5.5 数据流说明

本小节描述系统四条核心数据流：离线数据摄取流（Ingestion Flow）、在线查询流（Query Flow）、管理操作流（Management Flow）与审查要点流（Audit Flow）。

#### 5.5.1 离线数据摄取流 (Ingestion Flow)

```text
原始报告文档 (PDF/WORD)
  │
  ▼
┌────────────────────────────┐
│ File Integrity Checker     │  SHA256 + 文件元信息比对
│ (file_integrity_checker.py)│
└──────────────┬─────────────┘
       │
       ├── 未变更 / 已处理 ───────────────► 记录 skipped Trace 并结束
       │
       └── 新文件 / 已变更
          ▼
┌────────────────────────────┐
│ Loader                     │  PDF/WORD -> Markdown
│ (MarkItDown / MinerU)      │  + 图片提取 + 元数据收集
└──────────────┬─────────────┘
       │ Document(text + metadata.images)
       ▼
┌────────────────────────────┐
│ Splitter                   │  RecursiveCharacterTextSplitter
│ (+ Parent-Child 可选)      │  保留 image_refs 与定位信息
└──────────────┬─────────────┘
       │ Chunks[]
       ▼
┌────────────────────────────┐
│ Transform                  │  Chunk 重写 + 元数据增强
│ (Refine/Enrich/Caption)    │  + Vision LLM 图片描述注入
└──────────────┬─────────────┘
       │ Enriched Chunks[]
       ▼
┌────────────────────────────┐
│ Embedding                  │  Dense Embedding + Sparse BM25
│ (incremental_embedding.py) │  批处理 + 增量跳过
└──────────────┬─────────────┘
       │ vectors + metadata
       ▼
┌────────────────────────────┐
│ Upsert & Storage           │  PgVector Upsert（幂等）
│ (upsert_service.py)        │  + BM25 索引更新 + 图片存储
└──────────────┬─────────────┘
       │
       ▼
   ingestion_history / obs_traces / obs_trace_stages 持久化
```

关键说明：

1. 幂等性由 `chunk_id` 与 `ingestion_history` 共同保证，重复摄取不产生重复数据。
2. 图片采用 Image-to-Text 策略，描述文本在 Transform 阶段注入 Chunk，用于后续统一文本检索。
3. 全阶段通过 `TraceContext` 记录耗时、输入输出规模与异常信息，支持 Dashboard 可视化追踪。

#### 5.5.2 在线查询流 (Query Flow)

```text
用户查询（Copilot / Claude Desktop / 业务后端）
  │
  ▼
┌────────────────────────────┐
│ MCP Server                 │  JSON-RPC 2.0 解析 + Tool 路由
│ (Stdio Transport)          │  stdout 消息 / stderr 日志
└──────────────┬─────────────┘
       │ query + top_k + filters
       ▼
┌────────────────────────────┐
│ Query Processor            │  查询改写、关键词提取、过滤解析
│ (query_processor.py)       │
└──────────────┬─────────────┘
       │ processed_query
       ▼
┌──────────────────────────────────────────────────────────────┐
│                     Hybrid Retrieval                         │
│  ┌──────────────────────┐      ┌──────────────────────────┐  │
│  │ Dense Retriever      │ 并行 │ Sparse Retriever         │  │
│  │ (vector similarity)  │ ◄──► │ (BM25 inverted index)    │  │
│  └──────────┬───────────┘      └────────────┬─────────────┘  │
│             │                                │                │
│             └───────────────┬────────────────┘                │
│                             ▼                                 │
│                    ┌──────────────────┐                       │
│                    │ RRF Fusion       │  融合排序             │
│                    └────────┬─────────┘                       │
└─────────────────────────────┼─────────────────────────────────┘
          │ Top-M
          ▼
┌────────────────────────────┐
│ Parent-Child Resolver      │  命中同父文档子块数 > k 时
│ (parent_child_resolver.py) │  提升为父文档上下文
└──────────────┬─────────────┘
       │ candidates
       ▼
┌────────────────────────────┐
│ Reranker (Optional)        │  Cross-Encoder / LLM / None
│ (rerank/*.py)              │  超时可回退
└──────────────┬─────────────┘
       │ Top-K
       ▼
┌────────────────────────────┐
│ Response Builder           │  引用生成 + 图片读取/编码
│ (response_builder.py)      │  MCP Content 格式化
└──────────────┬─────────────┘
       │ TextContent + ImageContent
       ▼
返回 MCP Client（可追溯引用结果）
```

关键说明：

1. 检索与重排全链路记录 Query Trace，支持追踪 Dense/Sparse/Fusion/Rerank 每阶段候选变化。
2. 返回结果必须携带 `source_file/page/chunk_id/score`，满足“引用透明”约束。
3. 当重排器不可用时允许降级到融合结果，保障可用性。

#### 5.5.3 管理操作流 (Management Flow)

```text
Dashboard (Vue3 + Vite)
  │
  ├── 页面 3: 数据浏览（Data Browser）
  │      │
  │      ▼
  │  backend/document_controller.py
  │      │
  │      ├── DataService / DocumentManager 读取文档与 Chunk
  │      ├── PgVectorStore 按 metadata 查询
  │      └── ImageStorage 返回图片预览路径
  │
  ├── 页面 4: Ingestion 管理（Ingestion Manager）
  │      │
  │      ├── 触发摄取: IngestionPipeline.run(..., on_progress)
  │      ├── 前端轮询任务状态，展示阶段进度
  │      └── 删除文档: DocumentManager.delete_document()
  │             ├── 删除 PgVector Chunk
  │             ├── 删除 BM25 索引记录
  │             ├── 删除 ImageStorage 文件
  │             └── 删除 ingestion_history 记录
  │
  └── 页面 5/6: Trace 查看（Ingestion/Query Traces）
     │
     ▼
     trace_controller.py -> trace_service.py
     ├── 查询 obs_traces / obs_trace_stages
     └── 可选读取 logs/traces.jsonl 镜像用于排障
```

关键说明：

1. 管理操作通过统一 API 层进入，避免前端绕过业务校验直接访问底层存储。
2. 文档删除遵循“跨存储一致性删除”原则，确保向量、稀疏索引、图片与完整性记录同步清理。
3. Trace 页面优先读 PostgreSQL 专表，JSONL 仅作为可选镜像与离线排障补充。

#### 5.5.4 审查要点流 (Audit Flow)

```text
用户提交审查任务（报告文件 + 集合 + 参数）
  │
  ▼
┌────────────────────────────┐
│ audit_controller.py        │  参数校验 + 创建任务
└──────────────┬─────────────┘
       ▼
┌────────────────────────────┐
│ audit_orchestrator.py      │  审查主编排
│                            │  (可先触发/校验摄取完成)
└──────────────┬─────────────┘
       ▼
┌──────────────────────────────────────────────────────────────┐
│ check_dispatcher.py                                          │
│  依次调度 check_01 ... check_20                              │
│  每个 check 通用流程：                                        │
│   1) prompt_service 加载该项提示词                           │
│   2) rag_mcp_client 调用 query_knowledge_hub / verify_answer │
│   3) evidence_service 归一化证据（source/page/chunk_id）      │
│   4) 输出判定：满足 / 不满足 / 需人工复核                     │
└──────────────┬───────────────────────────────────────────────┘
       ▼
┌────────────────────────────┐
│ result_merge_service.py    │  合并 20 项结果 + 完整性校验
│                            │  生成总评、风险项与建议
└──────────────┬─────────────┘
       ▼
audit_result_repository.py 持久化
       │
       ▼
AuditResultView.vue 展示 20 项结果 + 判定说明 + 证据跳转
```

关键说明：

1. 审查输出必须保证 20 项完整返回，不允许缺项。
2. 每项结论都必须绑定可追溯证据，满足“可解释优先”设计原则。
3. 对证据不足或冲突场景，输出 `需人工复核`，避免无依据强判。

### 5.6 配置驱动设计

系统通过配置文件统一管理组件实现与运行参数，目标是“改配置不改代码”。

核心原则：

1. 统一入口：RAG 能力以 `rag-server/config/settings.yaml` 为主配置源。
2. 业务隔离：业务侧独立维护 `sgcc-report-audit-app/config/settings.yaml`，不直接耦合 RAG 内部实现。
3. 环境覆盖：敏感参数通过环境变量注入，配置文件仅保留占位符。
4. 可插拔优先：LLM/Embedding/Reranker/Retrieval/Evaluator 均通过 `provider` 或 `backend` 字段切换。

#### 5.6.1 RAG Server 主配置示例（`rag-server/config/settings.yaml`）

系统通过 `rag-server/config/settings.yaml` 统一配置各组件实现，支持零代码切换：

> 待确认：rag-server 和 sgcc-audit-report-app 中，postgresql是否指向了同一个数据库下的同一个表？

```yaml
# rag-server/config/settings.yaml

app:
  env: local # local | test | prod
  log_level: INFO

# LLM 配置（生成/重写/解释）
llm:
  provider: azure # azure | openai | deepseek | ollama | openai-compatible
  model: gpt-4o
  temperature: 0.1
  max_tokens: 2000
  timeout_sec: 60
  # Azure
  endpoint: "${AZURE_OPENAI_ENDPOINT}"
  api_key: "${AZURE_OPENAI_API_KEY}"
  api_version: "2024-10-21"
  deployment_name: "${AZURE_OPENAI_DEPLOYMENT}"
  # OpenAI-compatible（用于 Qwen / vLLM 等）
  base_url: "${OPENAI_COMPAT_BASE_URL}"

# Embedding 配置
embedding:
  provider: openai # openai | azure | ollama | bge | openai-compatible
  model: text-embedding-3-small
  embedding_dim: 1536
  batch_size: 64
  timeout_sec: 30

# Vision LLM 配置（图片描述）
vision_llm:
  provider: qwen-vl # azure | qwen-vl | openai-compatible
  model: qwen-vl-max
  api_key: "${DASHSCOPE_API_KEY}"
  base_url: "${DASHSCOPE_BASE_URL}"
  timeout_sec: 60

# 切分配置
splitter:
  backend: recursive_character # recursive_character | parent_child
  chunk_size: 1000
  chunk_overlap: 150
  separators: ["\n\n", "\n", "。", "；", "，", " "]
  enable_parent_child: true
  parent_trigger_k: 3

# 向量存储配置（当前唯一实现为 PgVector）
vector_store:
  backend: pgvector # 当前仅实现 pgvector，保留扩展位
  table: rag_chunks
  embedding_dim: 1536
  distance_metric: cosine
  enable_sparse_fields: true
  metadata_jsonb: true

postgres:
  host: "${PG_HOST}"
  port: 5432
  database: "${PG_DATABASE}"
  user: "${PG_USER}"
  password: "${PG_PASSWORD}"
  schema: public
  sslmode: disable
  pool_size: 10
  pool_timeout_sec: 30
  statement_timeout_ms: 30000

# 检索配置
retrieval:
  mode: hybrid # dense | sparse | hybrid
  sparse_backend: bm25 # bm25
  dense_top_k: 30
  sparse_top_k: 30
  fusion_algorithm: rrf # rrf | weighted_sum(预留)
  fusion_k: 60
  final_top_k: 10
  score_threshold: 0.0

# 重排配置
rerank:
  backend: cross_encoder # none | cross_encoder | llm
  model: bge-reranker-v2-m3
  top_m: 30
  timeout_sec: 20
  fallback_to_fusion: true

# 评估配置
evaluation:
  enabled: true
  backends: [ragas, custom]
  golden_test_set: "./data/eval/golden_set.jsonl"
  custom_metrics: [hit_rate, mrr, ndcg, groundedness]

# 可观测性配置
observability:
  enabled: true
  sink: postgres # postgres | jsonl | both
  jsonl_mirror_enabled: true
  jsonl_file: "./logs/rag/traces.jsonl"
  detail_level: standard # minimal | standard | verbose

# MCP Server 配置
mcp:
  transport: stdio
  protocol_version: "2025-06-18"
  tool_timeout_sec: 60

# 路径配置
paths:
  documents_root: "./data/documents"
  images_root: "./data/images"
  cache_root: "./cache"
  logs_root: "./logs/rag"
```

#### 5.6.2 业务应用配置示例（`sgcc-report-audit-app/config/settings.yaml`）

```yaml
# sgcc-report-audit-app/config/settings.yaml

app:
  env: local
  api_host: 0.0.0.0
  api_port: 8080
  log_level: INFO

audit:
  enabled_check_ids:
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
  default_collection: sgcc_reports
  max_parallel_checks: 4
  allow_partial_success: false
  evidence_top_k: 5

result:
  require_all_20_checks: true
  missing_item_policy: fail_fast # fail_fast | mark_review
  evidence_required: true

dashboard:
  enabled: true
  frontend_dev_port: 5173
  auto_refresh: true
  refresh_interval: 5

postgres:
  host: "${PG_HOST}"
  port: 5432
  database: "${PG_DATABASE}"
  user: "${PG_USER}"
  password: "${PG_PASSWORD}"
  schema: public
  pool_size: 5
  pool_timeout_sec: 30

observability:
  enabled: true
  query_trace_api_enabled: true
  ingestion_trace_api_enabled: true
```

#### 5.6.3 MCP 客户端与目录映射配置示例

`sgcc-report-audit-app/config/mcp_client.yaml`：

```yaml
mcp_server:
  transport: stdio
  command: "uv"
  args:
    - "run"
    - "python"
    - "scripts/run_mcp_server.py"
    - "--config"
    - "config/settings.yaml"
  cwd: "../rag-server"
  timeout_sec: 60
  retry:
    max_attempts: 2
    backoff_sec: 1
```

`sgcc-report-audit-app/config/data_mapping.yaml`：

```yaml
rag_data_root: "../../rag-server/data"
documents_target: "${rag_data_root}/documents"
images_target: "${rag_data_root}/images"

local_data_dir: "./data"

rag_cache_root: "../rag-server/cache"
local_cache_link: "./cache"

rag_logs_root: "../rag-server/logs"
local_logs_link: "./logs"

mapping_mode: "symlink" # symlink | bind_mount
read_only: true
```

#### 5.6.4 配置加载优先级与校验

配置加载优先级（从低到高）：

1. 代码内默认值（Default）
2. `settings.yaml` 文件
3. `.env` 与系统环境变量（如 `AZURE_OPENAI_API_KEY`）
4. 启动命令参数（如 `--config` 指定路径）

分阶段实施约定：

1. **A4（配置加载底座）**：仅要求建立加载优先级链路与关键字段校验，允许以最小字段集实现可运行基线。
2. **D10（配置驱动校验）**：要求对齐本节 `5.6` 的全量关键配置语义，补齐配置模型并强化校验规则。
3. 如用户明确要求提前全量对齐，可跨阶段执行，但需在任务报告中显式说明偏离排期。

建议在启动阶段执行“配置完整性检查”：

1. LLM/Embedding/Vision 提供者必需字段校验（`provider`、`model`、凭据）。
2. PgVector 必需项校验（`backend=pgvector`、`embedding_dim`、`table`、PostgreSQL 连接信息）。
3. Retrieval/Rerank 参数范围校验（`top_k`、`top_m`、`timeout_sec` 等）。
4. 路径存在性与可写性校验（`data/`、`cache/`、`logs/`）。

#### 5.6.5 零代码切换示例

示例 A：将重排从 `cross_encoder` 切换到 `llm`

1. 修改 `rag-server/config/settings.yaml`：`rerank.backend: llm`
2. 填写对应 `rerank.model` 与凭据
3. 重启 RAG Server
4. 在 Query Trace 页面确认 `rerank.backend=llm` 生效

示例 B：将图片描述模型从 `qwen-vl` 切换到 `azure`

1. 修改 `vision_llm.provider: azure`
2. 配置 Azure endpoint/api_key/deployment
3. 执行增量重摄取（仅处理变更文档/图片）
4. 在 Ingestion Trace 中核对 `Transform` 阶段 provider

示例 C：将检索模式从 `hybrid` 临时切换到 `dense`

1. 修改 `retrieval.mode: dense`
2. 保持其余参数不变，重启服务
3. 在评估面板对比 HitRate/MRR 与延迟变化

说明：配置驱动的目标是支持教学演示、实验对比与面试展示。所有切换动作应保留 Trace 与评估记录，避免“只改参数无效果证据”的不可复现问题。

## 6. 项目排期

> **排期原则（严格对齐本 DEV_SPEC 的架构分层与目录结构）**
>
> - **只按本文档设计落地**：以第 5.2 节目录树为“交付清单”，每一步都要在文件系统上产生可见变化。
> - **1 小时一个可验收增量**：每个小阶段（≈1h）都必须同时给出“验收标准 + 测试方法”，尽量做到 TDD。
> - **先打通主闭环，再补齐默认实现**：优先做“可跑通的端到端路径（Ingestion → Retrieval → MCP Tool）”，并在 Libs 层补齐可运行的默认后端实现，避免出现“只有接口没有实现”的空转。
> - **外部依赖可替换/可 Mock**：LLM/Embedding/Vision/VectorStore 的真实调用在单元测试中一律用 Fake/Mock，集成测试再开真实后端（可选）。

### 6.1 阶段总览（大阶段 -> 目的）

1. **阶段 A：工程骨架与测试基座**

- 目的：先建立目录树、最小可运行入口、`pytest` 测试约定与 `Settings` 配置校验，为后续阶段提供统一工程底座。

2. **阶段 B：前端页面骨架优先落地（Vue3 + Vite）**

- 目的：遵循 `.github/skills/frontend-design` 设计准则，先完成 7 个页面的路由、布局骨架与视觉基线，形成可演示入口并提前冻结前后端交互契约。

3. **阶段 C：前端功能闭环与接口契约固化**

- 目的：在 Mock 数据驱动下打通“报告列表 -> 审查结果 20 项 -> 证据跳转 -> Trace/评估页导航”的核心交互闭环，输出稳定 API Schema。

4. **阶段 D：RAG Server 工程骨架与可插拔 Libs 默认实现**

- 目的：按第 5.2 节目录建立 `rag-server/` 基础工程，先补齐 Factory + Base 接口 + 可运行默认后端（LLM/Embedding/Vision/PgVector），避免“只有抽象没有实现”。

5. **阶段 E：Ingestion Pipeline 主链路打通**

- 目的：完成 `PDF/WORD -> Markdown -> Chunk -> Transform -> Dense+Sparse Embedding -> PgVector Upsert` 的离线摄取闭环，并落地 SHA256 增量跳过机制。

6. **阶段 F：Retrieval Pipeline 与两段式检索重排**

- 目的：完成 Dense + BM25 混合召回、RRF 融合、可选 Cross-Encoder/LLM Rerank，稳定输出含引用证据的 Top-K 结果并具备回退策略。

7. **阶段 G：MCP Server 与 Tools 落地（Stdio）**

- 目的：基于 Python 官方 MCP SDK 暴露 `query_knowledge_hub`、`list_collections`、`get_document_summary` 等工具，保证可被 Copilot/Claude 直接调用。

8. **阶段 H：可观测性与 Dashboard 联动增强**

- 目的：完善 Ingestion/Query 双链路 Trace（PostgreSQL + JSONL 可选镜像），并让 Dashboard 完整展示系统总览、数据浏览、摄取管理与追踪分析。

9. **阶段 I：SGCC 审查业务模块（FastAPI + MVC）**

- 目的：实现 `sgcc-report-audit-app/backend` 的控制器、服务编排与 20 项审查规则，输出“结论 + 判定说明 + 证据定位”的结构化审查结果。

10. **阶段 J：评估体系、端到端验收与文档收口**

- 目的：接入 Ragas + 自定义指标回归，完成 A1-A4 业务 E2E 与 MCP 兼容性验收，最终收口 README/操作文档，确保开箱即用与可复现。

11. **阶段 K：Docker 封装与可迁移部署**

- 目的：完成项目容器化封装与一键编排，沉淀可迁移、可复现的运行环境；在不改变 `Stdio` 传输约束前提下，实现跨机器快速部署。

### 6.2 进度跟踪表 (Progress Tracking)

> **状态说明**：`[ ]` 未开始 | `[~]` 进行中 | `[x]` 已完成
>
> **更新时间**：每完成一个子任务后，立即更新对应状态与完成日期

> **拆分口径**：严格映射第 5.2 节目录树，任务粒度下钻到“可直接编码的模块/文件/类”；默认每项对应一个可验收提交。

#### 阶段 A：工程骨架与测试基座

| 任务编号 | 任务名称                 | 状态 | 完成日期          | 备注                                                                                                                                                                                        |
| -------- | ------------------------ | ---- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A1       | 创建完整目录结构与空文件 | [x]  | 26-03-14 14:00:39 | 严格按 5.2 目录树，创建所有目录与空文件（含 `rag-server/`、`sgcc-report-audit-app/`、`docs/`、`docker/` 及其全部子目录和文件），`.py`/`.ts`/`.vue`/`.css`/`.sql`/`.md`/`.yaml` 等均为空文件 |
| A2       | 建立最小可运行入口       | [x]  | 26-03-14 14:49:11 | `rag-server/scripts/run_mcp_server.py`、`sgcc-report-audit-app/backend/src/sgcc_audit/main.py`、`frontend/src/main.ts`                                                                      |
| A3       | 初始化依赖与测试基线     | [x]  | 26-03-15 17:04:07 | `pyproject.toml`、`uv.lock`、`pytest.ini`、`tests/unit`、`tests/integration`、`tests/e2e` 目录约定                                                                                          |
| A4       | 配置加载与校验底座       | [x]  | 26-03-16 12:11:58 | `src/core/settings.py`、`sgcc_audit/core/config.py`，实现默认值/环境变量/文件优先级                                                                                                         |
| A5       | 基础日志与异常规范       | [x]  | 26-03-16 13:18:10 | `core/logging.py`、`core/exceptions.py`、`core/constants.py`，统一错误码与 JSON 日志格式                                                                                                    |

#### 阶段 B：前端页面骨架优先落地（Vue3 + Vite）

| 任务编号 | 任务名称                  | 状态 | 完成日期 | 备注                                                                                             |
| -------- | ------------------------- | ---- | -------- | ------------------------------------------------------------------------------------------------ |
| B1       | 初始化 Vue3+Vite 前端工程 | [ ]  | -        | `frontend/package.json`、`vite.config.ts`、`tsconfig.json`、`src/main.ts`                        |
| B2       | 路由与页面骨架            | [ ]  | -        | `src/router/index.ts` + `src/views/*` 7 页空骨架（审查结果/总览/数据/摄取/双 Trace/评估）        |
| B3       | 全局布局与导航框架        | [ ]  | -        | `src/layouts/AppShell.vue`、侧边栏、顶栏、面包屑、页面容器                                       |
| B4       | 设计变量与全局样式        | [ ]  | -        | `src/assets/styles/variables.css`、`src/assets/styles/global.css`，建立主题色/字号/间距/动效变量 |
| B5       | 前端状态管理基座          | [ ]  | -        | `src/stores/` 定义 app/trace/audit 基础 store                                                    |
| B6       | API 客户端与 Mock 适配    | [ ]  | -        | `src/api/http.ts`、`src/mock/mock.ts`、`src/types/index.ts`，保证离线可演示                      |
| B7       | 前端骨架冒烟测试          | [ ]  | -        | `tests/e2e/*.spec.ts` 验证 7 页可打开、路由跳转与基础渲染                                        |

#### 阶段 C：前端功能闭环与接口契约固化

| 任务编号 | 任务名称                 | 状态 | 完成日期 | 备注                                                                                         |
| -------- | ------------------------ | ---- | -------- | -------------------------------------------------------------------------------------------- |
| C1       | 审查结果列表与 20 项卡片 | [ ]  | -        | `views/AuditResultView.vue` + `components/audit/*`：展示 `status/reason/evidence` 与筛选排序 |
| C2       | 报告目录与详情联动       | [ ]  | -        | 左侧报告树 + 右侧审查详情联动，支持已完成/进行中状态切换                                     |
| C3       | 证据跳转与文档定位组件   | [ ]  | -        | `components/audit/EvidenceDrawer.vue`：页码、段落锚点、图片缩略图跳转                        |
| C4       | 系统总览页面真实指标卡   | [ ]  | -        | 读取配置与统计接口，展示 provider/model/vectorstore/健康状态                                 |
| C5       | 数据浏览器页面           | [ ]  | -        | 文档列表、chunk 明细、metadata 展开、图片预览                                                |
| C6       | Ingestion 管理页面       | [ ]  | -        | 上传/路径输入、任务启动、进度条、失败重试按钮                                                |
| C7       | Ingestion Trace 页面     | [ ]  | -        | stage 瀑布图、耗时分布、明细抽屉                                                             |
| C8       | Query Trace 页面         | [ ]  | -        | dense/sparse/fusion/rerank 对比与 Top-K 展示                                                 |
| C9       | 评估页面占位到可用切换   | [ ]  | -        | 未启用占位 + 启用后指标表格/趋势图占位容器                                                   |
| C10      | 前后端契约冻结           | [ ]  | -        | 产出 `docs/api/sgcc-backend-openapi.md` 与前端 `types.ts` 对齐                               |

#### 阶段 D：RAG Server 工程骨架与可插拔 Libs 默认实现

| 任务编号 | 任务名称                         | 状态 | 完成日期 | 备注                                                                                                                                       |
| -------- | -------------------------------- | ---- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| D1       | BaseLLM 与 Provider 适配接口     | [ ]  | -        | `src/libs/llm/base_llm.py` + 统一 `generate/chat` 契约                                                                                     |
| D2       | LLM 实现（全 Provider 适配）     | [ ]  | -        | `azure_openai_llm.py`、`openai_llm.py`、`qwen_llm.py`、`vllm_llm.py`、`deepseek_llm.py`、`ollama_llm.py`，openai-compatible 适配与参数校验 |
| D3       | Embedding 抽象与实现             | [ ]  | -        | `src/libs/embedding/base_embedding.py` + `openai_embedding.py`、`bge_embedding.py`、`ollama_embedding.py`                                  |
| D4       | Vision LLM 抽象与实现            | [ ]  | -        | `src/libs/vision/base_vision_llm.py` + `azure_vision_llm.py`、`qwen_vl_client.py`                                                          |
| D5       | Splitter 抽象与默认实现          | [ ]  | -        | `ingestion/splitters/base_splitter.py`、`recursive_character_splitter.py`、`parent_child_splitter.py`                                      |
| D6       | VectorStore 抽象与 PgVector 实现 | [ ]  | -        | `storage/vector/base_vector_store.py`、`pgvector_store.py`、`storage/db/engine.py`、`storage/db/session.py`                                |
| D7       | Reranker 抽象与实现              | [ ]  | -        | `rerank/base_reranker.py`、`none_reranker.py`、`cross_encoder_reranker.py`、`llm_reranker.py`                                              |
| D8       | Evaluator 抽象与工厂占位         | [ ]  | -        | `evaluation/base_evaluator.py` + `factories/evaluator_factory.py`，统一 `evaluate()` 接口                                                  |
| D9       | 全工厂路由联通                   | [ ]  | -        | `factories/*_factory.py` 按 `settings.yaml` 动态实例化                                                                                     |
| D10      | 配置驱动校验                     | [ ]  | -        | `config/settings.yaml` + Pydantic 校验（provider/model/api_key/timeout）                                                                   |
| D11      | Libs 层单元测试（Fake/Mock）     | [ ]  | -        | `tests/unit` 覆盖工厂路由、参数合法性、fallback 分支                                                                                       |

#### 阶段 E：Ingestion Pipeline 主链路打通

| 任务编号 | 任务名称                      | 状态 | 完成日期 | 备注                                                                                                                                        |
| -------- | ----------------------------- | ---- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| E1       | 核心类型定义                  | [ ]  | -        | `src/core/types.py`：`Document/Chunk/ChunkRecord/IngestionResult`                                                                           |
| E2       | 文件完整性检查                | [ ]  | -        | `ingestion/file_integrity_checker.py` + `storage/integrity/ingestion_history_repository.py` + `sql/002_ingestion_history.sql`               |
| E3       | Loader 抽象与 PDF/Word Loader | [ ]  | -        | `loaders/base_loader.py`、`pdf_loader_markitdown.py`、`word_loader_markitdown.py`                                                           |
| E4       | Splitter 集成与定位字段       | [ ]  | -        | 输出 `chunk_index/start_offset/end_offset/source/heading_path`                                                                              |
| E5       | Transform 基类与 ChunkRefine  | [ ]  | -        | `transforms/base_transform.py`、`chunk_refine_transform.py`                                                                                 |
| E6       | MetadataEnrich 实现           | [ ]  | -        | `metadata_enrich_transform.py` 注入行业、干扰源、指标等标签                                                                                 |
| E7       | ImageCaption Transform        | [ ]  | -        | `image_caption_transform.py` 调用 Vision LLM 并注入 chunk + `storage/cache/processing_cache_repository.py` + `sql/005_processing_cache.sql` |
| E8       | Dense 向量编码模块            | [ ]  | -        | `embedding/dense_embedder.py`、`embedding/incremental_embedding.py` 批处理与增量编码                                                        |
| E9       | Sparse 编码模块               | [ ]  | -        | `embedding/sparse_encoder_bm25.py` 关键词权重编码                                                                                           |
| E10      | Upsert 幂等写入               | [ ]  | -        | `upsert/chunk_id.py`、`upsert/upsert_service.py`、`upsert/dedup_service.py`                                                                 |
| E11      | 图片存储与索引                | [ ]  | -        | `storage/image/image_storage.py`、`image_index_repository.py` + `sql/003_image_index.sql`                                                   |
| E12      | BM25 索引持久化               | [ ]  | -        | `storage/bm25/bm25_indexer.py`、`bm25_repository.py` + `sql/004_bm25_meta.sql`                                                              |
| E13      | Pipeline 主编排与进度回调     | [ ]  | -        | `ingestion/pipeline.py`、`progress_callback.py`、异常重试                                                                                   |
| E14      | 文档生命周期管理              | [ ]  | -        | `ingestion/document_manager.py`：list/get/delete/stats                                                                                      |
| E15      | 摄取脚本与集成测试            | [ ]  | -        | `scripts/ingest_document.py`、`scripts/reindex_document.py`、`tests/integration/test_ingestion_pipeline.py`                                 |
| E16      | 图片描述提示词模板            | [ ]  | -        | `config/prompts/image_caption.md`，E7 图片描述注入所需模板                                                                                  |

#### 阶段 F：Retrieval Pipeline 与两段式检索重排

| 任务编号 | 任务名称             | 状态 | 完成日期 | 备注                                                                          |
| -------- | -------------------- | ---- | -------- | ----------------------------------------------------------------------------- |
| F1       | Query 预处理层       | [ ]  | -        | `query_processor.py`、`keyword_extractor.py`、`query_expander.py`             |
| F2       | 元数据过滤解析       | [ ]  | -        | `metadata_filter_parser.py` 支持 collection/source/tag 过滤                   |
| F3       | DenseRetriever 实现  | [ ]  | -        | `dense_retriever.py` 调用 `BaseVectorStore.query()`                           |
| F4       | SparseRetriever 实现 | [ ]  | -        | `sparse_retriever.py` 调用 BM25 repository                                    |
| F5       | Hybrid 并行召回编排  | [ ]  | -        | `hybrid_retriever.py` 合并双路候选                                            |
| F6       | RRF 融合模块         | [ ]  | -        | `rrf_fusion.py` 支持 `k` 参数与确定性输出                                     |
| F7       | 父子文档聚合策略     | [ ]  | -        | `parent_child_resolver.py` 实现阈值 `k=3` 召回父文档                          |
| F8       | 两段式 Rerank 编排   | [ ]  | -        | 接入 none/cross-encoder/llm 三模式与 fallback                                 |
| F9       | 响应构建与引用注释   | [ ]  | -        | `response_builder.py` 输出 `source/page/chunk_id/score`                       |
| F10      | 检索链路测试         | [ ]  | -        | `tests/unit/test_rrf_fusion.py`、`tests/integration/test_hybrid_retrieval.py` |
| F11      | 检索侧提示词模板     | [ ]  | -        | `config/prompts/query_rewrite.md`、`rerank_policy.md`，F1/F8 所需模板         |

#### 阶段 G：MCP Server 与 Tools 落地（Stdio）

| 任务编号 | 任务名称                                  | 状态 | 完成日期 | 备注                                                                      |
| -------- | ----------------------------------------- | ---- | -------- | ------------------------------------------------------------------------- |
| G1       | MCP Server 入口与 lifecycle               | [ ]  | -        | `mcp_server/server.py`、`lifecycle.py`，严格 `stdio` 通道约束             |
| G2       | Tool 注册与 Schema                        | [ ]  | -        | `tool_registry.py`、`schemas.py`，统一入参与返回类型                      |
| G3       | `query_knowledge_hub` 工具                | [ ]  | -        | 串联 Retrieval Pipeline，返回可引用结果                                   |
| G4       | `retrieve_context` 工具                   | [ ]  | -        | 支持 `top_k/filters` 的上下文检索                                         |
| G5       | `list_collections` 工具                   | [ ]  | -        | 返回集合名、统计、更新时间                                                |
| G6       | `get_document_summary` 工具               | [ ]  | -        | 文档摘要 + 元数据 + 章节概览                                              |
| G7       | `list_document_sections` 工具             | [ ]  | -        | 返回目录树，支持前端导航式检索                                            |
| G8       | `ingest_document`/`reindex_document` 工具 | [ ]  | -        | 摄取任务触发、重建索引、进度反馈                                          |
| G9       | `verify_answer` 工具                      | [ ]  | -        | 依据检索证据做事实支撑校验                                                |
| G10      | MCP 错误映射与兼容测试                    | [ ]  | -        | `tests/integration/test_mcp_tools.py`、`tests/e2e/test_stdio_workflow.py` |

#### 阶段 H：可观测性与 Dashboard 联动增强

| 任务编号 | 任务名称                         | 状态 | 完成日期 | 备注                                                           |
| -------- | -------------------------------- | ---- | -------- | -------------------------------------------------------------- |
| H1       | 可观测 SQL 脚本落地              | [ ]  | -        | `sql/001_observability.sql` 建立 `obs_traces/obs_trace_stages` |
| H2       | Trace 模型与仓储                 | [ ]  | -        | `observability/trace_models.py`、`trace_repository.py`         |
| H3       | TraceContext 增强                | [ ]  | -        | `trace_context.py` 支持 stage 记录、finish、总耗时             |
| H4       | Query 链路打点                   | [ ]  | -        | 在 query_processing/dense/sparse/fusion/rerank 注入 trace      |
| H5       | Ingestion 链路打点               | [ ]  | -        | 在 load/split/transform/embed/upsert 注入 trace                |
| H6       | JSONL 导出器                     | [ ]  | -        | `trace_exporter_jsonl.py` 输出 `logs/traces.jsonl`             |
| H7       | Trace 查询服务与 API             | [ ]  | -        | `observability/trace_service.py` + 后端 `trace_controller.py`  |
| H8       | Dashboard 总览页联通真实数据     | [ ]  | -        | provider 状态、资产统计、最近 trace 状态                       |
| H9       | Dashboard 数据浏览页联通         | [ ]  | -        | 文档/chunk/image 数据读取与筛选                                |
| H10      | Dashboard Ingestion 管理页联通   | [ ]  | -        | 上传触发 + 进度刷新 + 失败重试                                 |
| H11      | Dashboard Ingestion Trace 页联通 | [ ]  | -        | 摄取历史、瀑布图、阶段详情                                     |
| H12      | Dashboard Query Trace 页联通     | [ ]  | -        | 查询历史、重排对比、候选明细                                   |
| H13      | 联动回归测试                     | [ ]  | -        | `tests/integration/test_document_manager.py` + Dashboard 冒烟  |

#### 阶段 I：SGCC 审查业务模块（FastAPI + MVC）

| 任务编号 | 任务名称               | 状态 | 完成日期 | 备注                                                                   |
| -------- | ---------------------- | ---- | -------- | ---------------------------------------------------------------------- |
| I1       | MVC 后端骨架与依赖注入 | [ ]  | -        | `controllers/`、`models/`、`views/`、`core/dependencies.py`            |
| I2       | 请求响应 Schema 与枚举 | [ ]  | -        | `schemas/request_models.py`、`response_models.py`、`enums.py`          |
| I3       | RAG MCP 客户端封装     | [ ]  | -        | `clients/rag_mcp_client.py`、`rag_tool_adapter.py`                     |
| I4       | 审查主编排服务         | [ ]  | -        | `services/audit_orchestrator.py`、`check_dispatcher.py`                |
| I5       | Prompt 体系加载        | [ ]  | -        | `config/prompts/common/*` + `check_01..20_*.md` 管理与版本控制         |
| I6       | 审查规则 01-05         | [ ]  | -        | `services/checks/check_01` 到 `check_05`                               |
| I7       | 审查规则 06-10         | [ ]  | -        | `services/checks/check_06` 到 `check_10`                               |
| I8       | 审查规则 11-15         | [ ]  | -        | `services/checks/check_11` 到 `check_15`                               |
| I9       | 审查规则 16-20         | [ ]  | -        | `services/checks/check_16` 到 `check_20`                               |
| I10      | 证据聚合与结果合并     | [ ]  | -        | `evidence_service.py`、`result_merge_service.py`                       |
| I11      | 审查任务与结果仓储     | [ ]  | -        | `repositories/audit_task_repository.py`、`audit_result_repository.py`  |
| I12      | 控制器接口落地         | [ ]  | -        | `audit_controller.py`、`document_controller.py`、`trace_controller.py` |
| I13      | 结果页前后端联调       | [ ]  | -        | 前端审查结果页接入真实 API，支持 20 项证据跳转                         |
| I14      | 业务集成测试 A1-A4     | [ ]  | -        | `tests/integration/test_submit_audit_api.py`、`test_get_result_api.py` |
| I15      | 视图模型 View Models   | [ ]  | -        | `views/audit_response_view.py`、`error_view.py`，输出 DTO 与错误响应   |

#### 阶段 J：评估体系、端到端验收与文档收口

| 任务编号 | 任务名称                          | 状态 | 完成日期 | 备注                                                                   |
| -------- | --------------------------------- | ---- | -------- | ---------------------------------------------------------------------- |
| J1       | RagasEvaluator 与 CustomEvaluator | [ ]  | -        | 统一评估输出结构，支持 `hit_rate/MRR/faithfulness`                     |
| J2       | CompositeEvaluator 与 EvalRunner  | [ ]  | -        | 支持多评估器并行执行与结果汇总                                         |
| J3       | Golden Test Set 数据集            | [ ]  | -        | `data/eval/` 构建 query-ground_truth-citation 样本                     |
| J4       | 评估面板页面启用                  | [ ]  | -        | Dashboard 评估页支持运行评估、查看历史趋势                             |
| J5       | 阈值门禁与回归脚本                | [ ]  | -        | `scripts/run_eval.py`，指标低于阈值则失败                              |
| J6       | MCP E2E 验收                      | [ ]  | -        | 模拟客户端执行 tools/list + tools/call 全链路                          |
| J7       | Dashboard E2E 冒烟                | [ ]  | -        | 7 页面可用性、关键交互与错误态验证                                     |
| J8       | SGCC 审查 E2E 验收                | [ ]  | -        | 提交报告 -> 20 项结果 -> 证据跳转 -> trace 追踪                        |
| J9       | 文档收口                          | [ ]  | -        | 更新根 `README.md`、`docs/runbooks/local-dev.md`、`troubleshooting.md` |
| J10      | 发布与复现清单                    | [ ]  | -        | 产出版本号、配置快照、测试报告、演示脚本                               |

#### 阶段 K：Docker 封装与可迁移部署

| 任务编号 | 任务名称                       | 状态 | 完成日期 | 备注                                                                                  |
| -------- | ------------------------------ | ---- | -------- | ------------------------------------------------------------------------------------- |
| K1       | 容器化构建规范与镜像命名约定   | [ ]  | -        | 完善 `docker/` 目录内容、镜像命名规范、构建脚本约定                                   |
| K2       | `rag-server` 镜像封装          | [ ]  | -        | `docker/rag-server.Dockerfile` + `.dockerignore`，包含 `uv` 依赖安装与启动命令        |
| K3       | `sgcc-audit-backend` 镜像封装  | [ ]  | -        | `docker/backend.Dockerfile`，保留对 `rag-server` 的 `stdio` 调用兼容路径              |
| K4       | 前端生产镜像封装               | [ ]  | -        | `docker/frontend.Dockerfile` 多阶段构建（Node build + Nginx serve）                   |
| K5       | PostgreSQL + PgVector 容器接入 | [ ]  | -        | `docker-compose.yml` 增加 `postgres` 服务并挂载 `sql/*.sql` 初始化                    |
| K6       | 全栈 Compose 编排与健康检查    | [ ]  | -        | 编排 `frontend/backend/rag-server/postgres`，配置 `depends_on`、healthcheck、重启策略 |
| K7       | 数据卷与目录映射策略           | [ ]  | -        | 挂载 `data/`、`cache/`、`logs/` 与 Postgres volume，确保迁移后数据保留                |
| K8       | 容器环境变量与密钥模板         | [ ]  | -        | 新增 `.env.docker.example`，规范 API Key、数据库连接与模型参数注入                    |
| K9       | 一键启动与运维脚本             | [ ]  | -        | `scripts/docker_up.sh`、`scripts/docker_down.sh`、`scripts/docker_logs.sh`            |
| K10      | 容器化验收与迁移文档           | [ ]  | -        | 更新 `docs/runbooks/deployment.md`，补充 Docker 冒烟与迁移步骤                        |

### 6.3 总体进度

| 阶段     | 总任务数 | 已完成 | 进度   |
| -------- | -------- | ------ | ------ |
| 阶段 A   | 5        | 5      | 100%   |
| 阶段 B   | 7        | 0      | 0%     |
| 阶段 C   | 10       | 0      | 0%     |
| 阶段 D   | 11       | 0      | 0%     |
| 阶段 E   | 16       | 0      | 0%     |
| 阶段 F   | 11       | 0      | 0%     |
| 阶段 G   | 10       | 0      | 0%     |
| 阶段 H   | 13       | 0      | 0%     |
| 阶段 I   | 15       | 0      | 0%     |
| 阶段 J   | 10       | 0      | 0%     |
| 阶段 K   | 10       | 0      | 0%     |
| **总计** | **118**  | **5**  | **4%** |

### 6.4 分任务实现细则（按 6.2 全量展开）

> 说明：本小节为执行级任务说明。每个任务默认对应一个约 1 小时可验收增量，实施顺序与 6.2 保持一致。

#### 阶段 A：工程骨架与测试基座（实施细则）

| 任务编号 | 目标                                             | 修改文件（需在 5.2 中存在）                                                                                                                                                                                                                                                                                                                                             | 实现类/函数                                       | 验收标准                                                                         | 测试方法                                                                                    |
| -------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| A1       | 严格按 5.2 目录树创建全部目录与空文件。          | 5.2 目录树中全部 262 个文件（含 `rag-server/`、`sgcc-report-audit-app/`、`docs/`、`docker/` 及其全部子目录和文件）                                                                                                                                                                                                                                                      | 无（目录与空文件）                                | 目录结构与 5.2 完全一致；所有文件已创建；`__init__.py` 可导入。                  | `python -m compileall rag-server/src sgcc-report-audit-app/backend/src`                     |
| A2       | 打通三入口最小启动路径（MCP/Backend/Frontend）。 | `rag-server/scripts/run_mcp_server.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/main.py`<br>`sgcc-report-audit-app/frontend/src/main.ts`<br>`sgcc-report-audit-app/scripts/run_backend.sh`<br>`sgcc-report-audit-app/scripts/run_frontend.sh`                                                                                                                   | `main()`（脚本入口）<br>`create_app()`            | 三端入口可启动且返回健康响应或渲染首页。                                         | 后端 `uv run python -m sgcc_audit.main --help`；前端 `npm run dev -- --host 0.0.0.0` 冒烟。 |
| A3       | 固化依赖与测试基线，统一 Python/前端测试约定。   | `rag-server/pyproject.toml`<br>`rag-server/pytest.ini`<br>`sgcc-report-audit-app/backend/pyproject.toml`<br>`sgcc-report-audit-app/backend/pytest.ini`<br>`rag-server/tests/conftest.py`<br>`sgcc-report-audit-app/backend/tests/conftest.py`                                                                                                                           | 无（配置）                                        | `pytest` 能发现 `unit/integration/e2e`；依赖安装无冲突。                         | `uv sync` 后执行 `uv run pytest -q --collect-only`。                                        |
| A4       | 建立配置加载底座与优先级策略（文件+环境变量）。  | `rag-server/src/core/settings.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/core/config.py`<br>`rag-server/config/settings.yaml`<br>`sgcc-report-audit-app/config/settings.yaml`                                                                                                                                                                                 | `load_settings()`<br>`Settings`<br>`get_config()` | 默认配置可加载；环境变量可覆盖关键字段；缺失必填项时报错；以最小关键字段集为准。 | `tests/unit` 增加配置加载测试；用临时 env 覆盖断言。                                        |
| A5       | 建立统一日志与异常编码规范。                     | `rag-server/src/core/logging.py`<br>`rag-server/src/core/exceptions.py`<br>`rag-server/src/core/constants.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/core/logging.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/core/exceptions.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/core/constants.py`<br>`sgcc-report-audit-app/config/logging.yaml` | `setup_logging()`<br>`AppError`<br>`ErrorCode`    | 错误响应结构统一；日志输出 JSON Lines；异常可映射状态码。                        | 单元测试断言异常映射；运行示例请求检查日志字段。                                            |

#### 阶段 B：前端页面骨架优先落地（实施细则）

| 任务编号 | 目标                                     | 修改文件（需在 5.2 中存在）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 实现类/函数                                               | 验收标准                                         | 测试方法                                     |
| -------- | ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------- |
| B1       | 初始化 Vue3+Vite 工程并固定构建脚本。    | `sgcc-report-audit-app/frontend/package.json`<br>`sgcc-report-audit-app/frontend/vite.config.ts`<br>`sgcc-report-audit-app/frontend/tsconfig.json`<br>`sgcc-report-audit-app/frontend/index.html`<br>`sgcc-report-audit-app/frontend/env.d.ts`<br>`sgcc-report-audit-app/frontend/src/main.ts`<br>`sgcc-report-audit-app/scripts/run_frontend.sh`                                                                                                                                                                                            | `bootstrap()`（前端启动）                                 | 本地 `dev/build/preview` 命令可执行。            | `npm run build`、`npm run dev` 冒烟。        |
| B2       | 建立 7 页面路由骨架，保证导航可达。      | `sgcc-report-audit-app/frontend/src/router/index.ts`<br>`sgcc-report-audit-app/frontend/src/views/AuditResultView.vue`<br>`sgcc-report-audit-app/frontend/src/views/OverviewView.vue`<br>`sgcc-report-audit-app/frontend/src/views/DataBrowserView.vue`<br>`sgcc-report-audit-app/frontend/src/views/IngestionManagerView.vue`<br>`sgcc-report-audit-app/frontend/src/views/IngestionTracesView.vue`<br>`sgcc-report-audit-app/frontend/src/views/QueryTracesView.vue`<br>`sgcc-report-audit-app/frontend/src/views/EvaluationPanelView.vue` | 路由表 `routes`                                           | 7 个页面 URL 均可访问；刷新不 404。              | Playwright 路由跳转用例。                    |
| B3       | 形成统一壳层布局（侧栏+顶栏+内容容器）。 | `sgcc-report-audit-app/frontend/src/layouts/AppShell.vue`<br>`sgcc-report-audit-app/frontend/src/App.vue`<br>`sgcc-report-audit-app/frontend/src/components/common/EmptyState.vue`                                                                                                                                                                                                                                                                                                                                                           | `AppShell` 组件                                           | 所有页面共用壳层；移动端下布局不溢出。           | 浏览器手测 + Playwright 视口回归。           |
| B4       | 建立设计变量与全局样式基线。             | `sgcc-report-audit-app/frontend/src/assets/styles/variables.css`<br>`sgcc-report-audit-app/frontend/src/assets/styles/global.css`                                                                                                                                                                                                                                                                                                                                                                                                            | CSS 变量体系                                              | 颜色、字号、间距、动画变量可复用；页面风格统一。 | 样式快照检查；手测主题变量生效。             |
| B5       | 建立前端状态管理基础仓库。               | `sgcc-report-audit-app/frontend/src/stores/app.ts`<br>`sgcc-report-audit-app/frontend/src/stores/audit.ts`<br>`sgcc-report-audit-app/frontend/src/stores/trace.ts`                                                                                                                                                                                                                                                                                                                                                                           | `useAppStore()`<br>`useAuditStore()`<br>`useTraceStore()` | 页面共享状态可读写；刷新策略明确。               | Vitest/单测（或组件单测）覆盖 store action。 |
| B6       | 完成 API 客户端和离线 Mock 适配。        | `sgcc-report-audit-app/frontend/src/api/http.ts`<br>`sgcc-report-audit-app/frontend/src/mock/mock.ts`<br>`sgcc-report-audit-app/frontend/src/types/index.ts`                                                                                                                                                                                                                                                                                                                                                                                 | `createHttpClient()`<br>`mockAuditResult()`               | 断网条件下可演示主流程；类型定义可约束接口。     | 切换 mock 开关后执行页面冒烟。               |
| B7       | 建立前端骨架级自动化冒烟测试。           | `sgcc-report-audit-app/tests/playwright.config.ts`<br>`sgcc-report-audit-app/tests/e2e/audit-result.spec.ts`<br>`sgcc-report-audit-app/tests/e2e/traces.spec.ts`                                                                                                                                                                                                                                                                                                                                                                             | E2E 测试用例函数                                          | 至少覆盖首页加载、菜单跳转、页面标题渲染。       | `npx playwright test`。                      |

#### 阶段 C：前端功能闭环与接口契约固化（实施细则）

| 任务编号 | 目标                           | 修改文件（需在 5.2 中存在）                                                                                                                                                                                                                                                | 实现类/函数                                | 验收标准                                          | 测试方法                           |
| -------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------- | ---------------------------------- |
| C1       | 实现审查结果 20 项列表与筛选。 | `sgcc-report-audit-app/frontend/src/views/AuditResultView.vue`<br>`sgcc-report-audit-app/frontend/src/components/audit/CheckItemTable.vue`<br>`sgcc-report-audit-app/frontend/src/components/common/StatusTag.vue`<br>`sgcc-report-audit-app/frontend/src/stores/audit.ts` | `renderCheckItems()`<br>`filterByStatus()` | 展示每项 `status/reason/evidence`；支持排序筛选。 | 组件测试 + 页面手测。              |
| C2       | 报告树与详情联动。             | `sgcc-report-audit-app/frontend/src/views/AuditResultView.vue`<br>`sgcc-report-audit-app/frontend/src/api/documents.ts`<br>`sgcc-report-audit-app/frontend/src/stores/audit.ts`                                                                                            | `selectReport()`                           | 点击左侧报告后右侧详情同步更新。                  | E2E 用例验证联动状态。             |
| C3       | 证据定位与跳转。               | `sgcc-report-audit-app/frontend/src/components/audit/EvidenceDrawer.vue`<br>`sgcc-report-audit-app/frontend/src/components/data/ImagePreview.vue`<br>`sgcc-report-audit-app/frontend/src/views/AuditResultView.vue`                                                        | `openEvidence()`<br>`jumpToAnchor()`       | 支持页码/段落/图片证据跳转并高亮。                | E2E 点击证据定位断言。             |
| C4       | 系统总览页接入真实状态数据。   | `sgcc-report-audit-app/frontend/src/views/OverviewView.vue`<br>`sgcc-report-audit-app/frontend/src/api/trace.ts`<br>`sgcc-report-audit-app/frontend/src/stores/app.ts`                                                                                                     | `loadOverviewStats()`                      | 可展示 provider、模型、向量库与服务健康。         | Mock API 与真实 API 双模式测试。   |
| C5       | 数据浏览页面可用化。           | `sgcc-report-audit-app/frontend/src/views/DataBrowserView.vue`<br>`sgcc-report-audit-app/frontend/src/components/data/ChunkViewer.vue`<br>`sgcc-report-audit-app/frontend/src/api/documents.ts`                                                                            | `loadChunks()`<br>`renderMetadata()`       | 文档/Chunk/Metadata 可浏览和筛选。                | 页面手测 + 接口契约测试。          |
| C6       | 摄取管理页形成任务发起闭环。   | `sgcc-report-audit-app/frontend/src/views/IngestionManagerView.vue`<br>`sgcc-report-audit-app/frontend/src/api/documents.ts`<br>`sgcc-report-audit-app/frontend/src/stores/app.ts`                                                                                         | `startIngestion()`<br>`retryTask()`        | 可提交摄取任务、查看进度、失败重试。              | E2E 上传或路径输入流程测试。       |
| C7       | Ingestion Trace 可视化。       | `sgcc-report-audit-app/frontend/src/views/IngestionTracesView.vue`<br>`sgcc-report-audit-app/frontend/src/components/traces/WaterfallChart.vue`<br>`sgcc-report-audit-app/frontend/src/api/trace.ts`                                                                       | `loadIngestionTrace()`                     | 能展示阶段耗时瀑布图与详情。                      | E2E + 伪数据快照测试。             |
| C8       | Query Trace 对比页可用。       | `sgcc-report-audit-app/frontend/src/views/QueryTracesView.vue`<br>`sgcc-report-audit-app/frontend/src/components/traces/TraceDetailPanel.vue`<br>`sgcc-report-audit-app/frontend/src/api/trace.ts`                                                                         | `loadQueryTrace()`                         | dense/sparse/fusion/rerank 候选变化可视化。       | E2E 检查 Top-K 与阶段面板。        |
| C9       | 评估页从占位切到可交互。       | `sgcc-report-audit-app/frontend/src/views/EvaluationPanelView.vue`<br>`sgcc-report-audit-app/frontend/src/stores/app.ts`<br>`sgcc-report-audit-app/frontend/src/api/trace.ts`                                                                                              | `runEvaluation()`                          | 未启用态有明确提示；启用后可展示指标表。          | 页面状态切换单测与手测。           |
| C10      | 冻结前后端 API 契约。          | `docs/api/sgcc-backend-openapi.md`<br>`sgcc-report-audit-app/frontend/src/types/index.ts`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/schemas/response_models.py`                                                                                                     | DTO/Schema 定义                            | OpenAPI、前端类型、后端响应字段三者一致。         | 契约测试（schema diff）+ CI 校验。 |

#### 阶段 D：RAG Server 工程骨架与可插拔 Libs 默认实现（实施细则）

| 任务编号 | 目标                                   | 修改文件（需在 5.2 中存在）                                                                                                                                                                                                                                                                                | 实现类/函数                              | 验收标准                                                               | 测试方法                                   |
| -------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------ |
| D1       | 定义统一 LLM 抽象接口。                | `rag-server/src/libs/llm/base_llm.py`<br>`rag-server/src/utils/retry.py`                                                                                                                                                                                                                                   | `BaseLLM.generate()`<br>`BaseLLM.chat()` | 所有 LLM 适配器遵守同一协议；重试策略可用。                            | `tests/unit` 对抽象实现契约测试。          |
| D2       | 实现全 Provider LLM 适配。             | `rag-server/src/libs/llm/azure_openai_llm.py`<br>`rag-server/src/libs/llm/openai_llm.py`<br>`rag-server/src/libs/llm/qwen_llm.py`<br>`rag-server/src/libs/llm/vllm_llm.py`<br>`rag-server/src/libs/llm/deepseek_llm.py`<br>`rag-server/src/libs/llm/ollama_llm.py`                                         | 各 Provider Client 类                    | 配置切换 provider 后可完成最小调用。                                   | Fake transport 单测 + 可选真实联调。       |
| D3       | 完成 Embedding 抽象与实现。            | `rag-server/src/libs/embedding/base_embedding.py`<br>`rag-server/src/libs/embedding/openai_embedding.py`<br>`rag-server/src/libs/embedding/bge_embedding.py`<br>`rag-server/src/libs/embedding/ollama_embedding.py`                                                                                        | `BaseEmbedding.embed_texts()`            | Dense 编码接口稳定，可批量处理。                                       | 单测覆盖维度、批次、异常分支。             |
| D4       | 完成 Vision LLM 抽象与实现。           | `rag-server/src/libs/vision/base_vision_llm.py`<br>`rag-server/src/libs/vision/azure_vision_llm.py`<br>`rag-server/src/libs/vision/qwen_vl_client.py`                                                                                                                                                      | `caption_image()`                        | 输入图片路径可返回描述文本。                                           | Mock Vision 调用与超时回退测试。           |
| D5       | 建立 Splitter 抽象和默认实现。         | `rag-server/src/ingestion/splitters/base_splitter.py`<br>`rag-server/src/ingestion/splitters/recursive_character_splitter.py`<br>`rag-server/src/ingestion/splitters/parent_child_splitter.py`<br>`rag-server/tests/unit/test_splitter_recursive.py`                                                       | `split()`<br>`split_parent_child()`      | 支持语义切分与父子切分两模式。                                         | 样本文本切分断言（数量/边界）。            |
| D6       | 建立 VectorStore 抽象并实现 PgVector。 | `rag-server/src/storage/vector/base_vector_store.py`<br>`rag-server/src/storage/vector/pgvector_store.py`<br>`rag-server/src/storage/db/engine.py`<br>`rag-server/src/storage/db/session.py`                                                                                                               | `upsert()`<br>`query()`                  | 向量写入/检索可执行；支持 metadata 过滤。                              | 集成测试连接 PostgreSQL+PgVector。         |
| D7       | 建立 Reranker 抽象与三实现。           | `rag-server/src/rerank/base_reranker.py`<br>`rag-server/src/rerank/none_reranker.py`<br>`rag-server/src/rerank/cross_encoder_reranker.py`<br>`rag-server/src/rerank/llm_reranker.py`                                                                                                                       | `rerank()`                               | 三模式可切换，失败可回退 none。                                        | 单测覆盖 fallback 与排序稳定性。           |
| D8       | 评估器抽象与工厂占位。                 | `rag-server/src/evaluation/base_evaluator.py`<br>`rag-server/src/factories/evaluator_factory.py`                                                                                                                                                                                                           | `BaseEvaluator.evaluate()`               | 评估器可被统一实例化并返回标准结构。                                   | 单测验证工厂路由与未知类型报错。           |
| D9       | 打通所有工厂路由。                     | `rag-server/src/factories/llm_factory.py`<br>`rag-server/src/factories/vision_llm_factory.py`<br>`rag-server/src/factories/embedding_factory.py`<br>`rag-server/src/factories/splitter_factory.py`<br>`rag-server/src/factories/vector_store_factory.py`<br>`rag-server/src/factories/reranker_factory.py` | `create_*()` 系列                        | `settings.yaml` 切换可驱动实例变化。                                   | 参数化单测遍历 provider 组合。             |
| D10      | 完善配置模型校验并对齐 5.6 配置语义。  | `rag-server/config/settings.yaml`<br>`rag-server/src/core/settings.py`                                                                                                                                                                                                                                     | `validate_settings()`                    | provider/model/api_key/timeout 校验完整；补齐 5.6 关键配置项语义校验。 | 无效配置样例测试 + 正常样例回归。          |
| D11      | 完成 Libs 层单元测试基线。             | `rag-server/tests/unit/test_reranker_fallback.py`<br>`rag-server/tests/unit/test_rrf_fusion.py`<br>`rag-server/tests/unit/test_trace_context.py`                                                                                                                                                           | pytest 测试函数                          | 关键工厂与 fallback 分支覆盖到位。                                     | `uv run pytest rag-server/tests/unit -q`。 |

#### 阶段 E：Ingestion Pipeline 主链路打通（实施细则）

| 任务编号 | 目标                               | 修改文件（需在 5.2 中存在）                                                                                                                                                                                                                                                                 | 实现类/函数                                                | 验收标准                                                                | 测试方法                         |
| -------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------- |
| E1       | 定义摄取核心数据类型。             | `rag-server/src/core/types.py`                                                                                                                                                                                                                                                              | `Document`<br>`Chunk`<br>`IngestionResult`                 | 类型字段满足摄取链路全程传递。                                          | 类型构造单测与序列化测试。       |
| E2       | 建立 SHA256 完整性检查。           | `rag-server/src/ingestion/file_integrity_checker.py`<br>`rag-server/src/storage/integrity/ingestion_history_repository.py`<br>`rag-server/sql/002_ingestion_history.sql`<br>`rag-server/src/utils/hash_utils.py`                                                                            | `calc_sha256()`<br>`should_skip()`                         | 重复文件可跳过；变更文件可重建。                                        | 单测构造同名不同内容样例。       |
| E3       | 实现 PDF/Word Loader。             | `rag-server/src/ingestion/loaders/base_loader.py`<br>`rag-server/src/ingestion/loaders/pdf_loader_markitdown.py`<br>`rag-server/src/ingestion/loaders/word_loader_markitdown.py`<br>`rag-server/src/utils/file_utils.py`<br>`rag-server/tests/unit/test_loader_pdf.py`                      | `load()`                                                   | 能输出标准 Document 和图片引用。                                        | 小样本文档集成测试。             |
| E4       | 切分输出定位字段。                 | `rag-server/src/ingestion/splitters/recursive_character_splitter.py`<br>`rag-server/src/ingestion/splitters/parent_child_splitter.py`                                                                                                                                                       | `build_chunk_metadata()`                                   | chunk 含 `chunk_index/start_offset/end_offset`。                        | 断言切分定位字段完整。           |
| E5       | 建立 Transform 抽象与 Chunk 精炼。 | `rag-server/src/ingestion/transforms/base_transform.py`<br>`rag-server/src/ingestion/transforms/chunk_refine_transform.py`<br>`rag-server/src/utils/text_utils.py`                                                                                                                          | `transform()`                                              | 可对 chunk 做规范化重写。                                               | 单测验证输入输出一致性。         |
| E6       | 注入行业与干扰源元数据。           | `rag-server/src/ingestion/transforms/metadata_enrich_transform.py`                                                                                                                                                                                                                          | `enrich_metadata()`                                        | 可注入行业、指标、干扰源标签。                                          | 用典型干扰源样例断言标签。       |
| E7       | 图片描述注入流程落地。             | `rag-server/src/ingestion/transforms/image_caption_transform.py`<br>`rag-server/src/libs/vision/qwen_vl_client.py`<br>`rag-server/src/storage/cache/processing_cache_repository.py`<br>`rag-server/sql/005_processing_cache.sql`<br>`rag-server/tests/unit/test_transform_image_caption.py` | `caption_and_inject()`                                     | 图片描述可并入 chunk；失败可降级；结果可缓存。                          | Mock Vision 单测 + 集成回归。    |
| E8       | Dense 编码模块落地。               | `rag-server/src/ingestion/embedding/dense_embedder.py`<br>`rag-server/src/ingestion/embedding/incremental_embedding.py`                                                                                                                                                                     | `embed_chunks()`                                           | 批量编码成功，向量维度一致；支持增量编码。                              | 单测覆盖批大小和异常重试。       |
| E9       | Sparse(BM25) 编码模块落地。        | `rag-server/src/ingestion/embedding/sparse_encoder_bm25.py`                                                                                                                                                                                                                                 | `encode_sparse()`                                          | 稀疏向量或词项权重可生成。                                              | 单测断言关键词权重输出。         |
| E10      | 幂等 Upsert 与 Chunk ID。          | `rag-server/src/ingestion/upsert/chunk_id.py`<br>`rag-server/src/ingestion/upsert/upsert_service.py`<br>`rag-server/src/ingestion/upsert/dedup_service.py`                                                                                                                                  | `build_chunk_id()`<br>`upsert_chunks()`                    | 重复执行不产生重复记录。                                                | 集成测试重复导入同一文档。       |
| E11      | 图片存储与索引持久化。             | `rag-server/src/storage/image/image_storage.py`<br>`rag-server/src/storage/image/image_index_repository.py`<br>`rag-server/sql/003_image_index.sql`                                                                                                                                         | `save_image()`<br>`index_image()`                          | 图片文件与索引记录一致。                                                | 文件系统+数据库联合测试。        |
| E12      | BM25 索引持久化实现。              | `rag-server/src/storage/bm25/bm25_indexer.py`<br>`rag-server/src/storage/bm25/bm25_repository.py`<br>`rag-server/sql/004_bm25_meta.sql`                                                                                                                                                     | `build_index()`<br>`search()`                              | 索引可更新且可查询。                                                    | 构建后检索命中测试。             |
| E13      | 编排摄取主 Pipeline 与进度回调。   | `rag-server/src/ingestion/pipeline.py`<br>`rag-server/src/ingestion/progress_callback.py`                                                                                                                                                                                                   | `IngestionPipeline.run()`                                  | 各阶段串联可执行且可回调进度。                                          | 集成测试断言阶段顺序和耗时。     |
| E14      | 文档生命周期管理。                 | `rag-server/src/ingestion/document_manager.py`                                                                                                                                                                                                                                              | `list_documents()`<br>`delete_document()`<br>`get_stats()` | 文档列表、删除、统计可用。                                              | `test_document_manager.py`。     |
| E15      | 脚本化摄取与重建索引。             | `rag-server/scripts/ingest_document.py`<br>`rag-server/scripts/reindex_document.py`<br>`rag-server/tests/integration/test_ingestion_pipeline.py`                                                                                                                                            | `main()` 脚本入口                                          | CLI 可触发摄取和重建。                                                  | 通过脚本执行集成用例。           |
| E16      | 图片描述提示词模板编写。           | `rag-server/config/prompts/image_caption.md`                                                                                                                                                                                                                                                | 无（Prompt 模板）                                          | 模板含角色、任务、输出格式说明；E7 图片描述注入可正确加载并使用该模板。 | 集成测试验证模板加载与输出格式。 |

#### 阶段 F：Retrieval Pipeline 与两段式检索重排（实施细则）

| 任务编号 | 目标                       | 修改文件（需在 5.2 中存在）                                                                                                                      | 实现类/函数                                 | 验收标准                                                                       | 测试方法                                          |
| -------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------- |
| F1       | 查询预处理层可用。         | `rag-server/src/retrieval/query_processor.py`<br>`rag-server/src/retrieval/keyword_extractor.py`<br>`rag-server/src/retrieval/query_expander.py` | `normalize_query()`<br>`extract_keywords()` | 查询归一化、关键词提取、扩展可独立调用。                                       | 单测覆盖中英文、空输入、长查询。                  |
| F2       | 元数据过滤解析支持多条件。 | `rag-server/src/retrieval/metadata_filter_parser.py`                                                                                             | `parse_filters()`                           | 支持 collection/source/tag 过滤。                                              | 单测断言 DSL 到查询条件映射。                     |
| F3       | Dense 检索器落地。         | `rag-server/src/retrieval/dense_retriever.py`<br>`rag-server/src/storage/vector/pgvector_store.py`                                               | `retrieve_dense()`                          | Top-K 结果可返回评分与引用。                                                   | 集成测试验证召回数量与排序。                      |
| F4       | Sparse 检索器落地。        | `rag-server/src/retrieval/sparse_retriever.py`<br>`rag-server/src/storage/bm25/bm25_repository.py`                                               | `retrieve_sparse()`                         | BM25 召回稳定可复现。                                                          | 单测对比已知语料命中顺序。                        |
| F5       | 混合召回编排可并行。       | `rag-server/src/retrieval/hybrid_retriever.py`                                                                                                   | `retrieve_hybrid()`                         | dense+sparse 候选可并行合并。                                                  | 集成测试比较单路与双路命中。                      |
| F6       | RRF 融合模块实现。         | `rag-server/src/retrieval/rrf_fusion.py`                                                                                                         | `rrf_fuse()`                                | 融合结果确定性输出；支持参数 `k`。                                             | `test_rrf_fusion.py` 参数化测试。                 |
| F7       | 父子文档聚合策略实现。     | `rag-server/src/retrieval/parent_child_resolver.py`                                                                                              | `resolve_parent_if_needed()`                | 子块命中超阈值时召回父文档。                                                   | 构造 `k=3` 场景断言策略生效。                     |
| F8       | 两段式重排编排。           | `rag-server/src/retrieval/retrieval_pipeline.py`<br>`rag-server/src/rerank/cross_encoder_reranker.py`<br>`rag-server/src/rerank/llm_reranker.py` | `run_rerank_stage()`                        | 粗排到精排链路可开关；超时回退可用。                                           | 集成测试注入超时并验证 fallback。                 |
| F9       | 响应构建含证据引用。       | `rag-server/src/retrieval/response_builder.py`<br>`rag-server/src/core/types.py`                                                                 | `build_response()`                          | 输出含 `source/page/chunk_id/score`。                                          | 单测断言响应 schema。                             |
| F10      | 检索链路测试完善。         | `rag-server/tests/unit/test_rrf_fusion.py`<br>`rag-server/tests/integration/test_hybrid_retrieval.py`                                            | pytest 测试函数                             | 核心检索流程有单测+集成覆盖。                                                  | `uv run pytest rag-server/tests/integration -q`。 |
| F11      | 检索侧提示词模板编写。     | `rag-server/config/prompts/query_rewrite.md`<br>`rag-server/config/prompts/rerank_policy.md`                                                     | 无（Prompt 模板）                           | 查询改写与重排策略模板就绪；F1 查询预处理和 F8 LLM Reranker 可正确加载并使用。 | 集成测试验证模板加载与输出格式。                  |

#### 阶段 G：MCP Server 与 Tools 落地（Stdio，实施细则）

| 任务编号 | 目标                                   | 修改文件（需在 5.2 中存在）                                                                                                                             | 实现类/函数                                               | 验收标准                                | 测试方法                        |
| -------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------- | ------------------------------- |
| G1       | 搭建 MCP Server 入口与生命周期。       | `rag-server/src/mcp_server/server.py`<br>`rag-server/src/mcp_server/lifecycle.py`<br>`rag-server/scripts/run_mcp_server.py`                             | `serve_stdio()`<br>`initialize()`                         | 仅使用 stdio 通道；启动/关闭流程完整。  | `test_stdio_workflow.py` 冒烟。 |
| G2       | 完成 Tool 注册与 Schema 绑定。         | `rag-server/src/mcp_server/tool_registry.py`<br>`rag-server/src/mcp_server/schemas.py`                                                                  | `register_tools()`                                        | `tools/list` 可返回完整工具与参数定义。 | 集成测试校验 schema。           |
| G3       | 实现主检索工具 `query_knowledge_hub`。 | `rag-server/src/mcp_server/tools/query_knowledge_hub.py`<br>`rag-server/src/retrieval/retrieval_pipeline.py`                                            | `handle_query_knowledge_hub()`                            | 返回带引用的检索结果与说明。            | MCP tools/call 集成测试。       |
| G4       | 实现 `retrieve_context` 工具。         | `rag-server/src/mcp_server/tools/retrieve_context.py`<br>`rag-server/src/retrieval/hybrid_retriever.py`                                                 | `handle_retrieve_context()`                               | 支持 `top_k` 与过滤参数。               | 参数化测试不同 top_k。          |
| G5       | 实现 `list_collections` 工具。         | `rag-server/src/mcp_server/tools/list_collections.py`<br>`rag-server/src/ingestion/document_manager.py`                                                 | `handle_list_collections()`                               | 返回集合名、文档量、更新时间。          | 集成测试对空集合与非空集合。    |
| G6       | 实现 `get_document_summary` 工具。     | `rag-server/src/mcp_server/tools/get_document_summary.py`<br>`rag-server/src/mcp_server/tools/list_document_sections.py`                                | `handle_get_document_summary()`                           | 返回摘要、元数据、章节总览。            | 工具级单测 + MCP 集成测试。     |
| G7       | 实现章节浏览工具。                     | `rag-server/src/mcp_server/tools/list_document_sections.py`<br>`rag-server/src/ingestion/document_manager.py`                                           | `handle_list_document_sections()`                         | 可按文档返回目录树结构。                | 测试文档章节解析断言。          |
| G8       | 实现摄取触发工具。                     | `rag-server/src/mcp_server/tools/ingest_document.py`<br>`rag-server/src/mcp_server/tools/reindex_document.py`<br>`rag-server/src/ingestion/pipeline.py` | `handle_ingest_document()`<br>`handle_reindex_document()` | 可触发任务并返回进度/结果。             | MCP 工具调用集成测试。          |
| G9       | 实现答案核查工具。                     | `rag-server/src/mcp_server/tools/verify_answer.py`<br>`rag-server/src/retrieval/response_builder.py`                                                    | `handle_verify_answer()`                                  | 输出事实支撑度与证据列表。              | 单测覆盖支持/不支持两类结论。   |
| G10      | 完成 MCP 错误映射与兼容回归。          | `rag-server/tests/integration/test_mcp_tools.py`<br>`rag-server/tests/e2e/test_stdio_workflow.py`<br>`rag-server/src/mcp_server/server.py`              | 错误映射函数                                              | 非法参数、超时、内部异常都能稳定返回。  | MCP 全链路 E2E。                |

#### 阶段 H：可观测性与 Dashboard 联动增强（实施细则）

| 任务编号 | 目标                         | 修改文件（需在 5.2 中存在）                                                                                                                                                                                          | 实现类/函数                                    | 验收标准                                       | 测试方法                         |
| -------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | -------------------------------- |
| H1       | 建立 Trace 数据表 SQL。      | `rag-server/sql/001_observability.sql`<br>`rag-server/scripts/init_db.py`                                                                                                                                            | SQL 初始化函数                                 | 可创建 `obs_traces` 与 `obs_trace_stages`。    | 本地 DB 初始化并检查表结构。     |
| H2       | 建立 Trace 模型与仓储。      | `rag-server/src/observability/trace_models.py`<br>`rag-server/src/observability/trace_repository.py`                                                                                                                 | `save_trace()`<br>`list_traces()`              | Trace 可写入并查询。                           | 仓储层集成测试。                 |
| H3       | 增强 TraceContext 生命周期。 | `rag-server/src/observability/trace_context.py`                                                                                                                                                                      | `start_stage()`<br>`end_stage()`<br>`finish()` | 每阶段耗时与总耗时可记录。                     | 单测断言阶段时序和耗时字段。     |
| H4       | 查询链路全阶段打点。         | `rag-server/src/retrieval/retrieval_pipeline.py`<br>`rag-server/src/retrieval/dense_retriever.py`<br>`rag-server/src/retrieval/sparse_retriever.py`<br>`rag-server/src/retrieval/rrf_fusion.py`                      | `trace_stage()` 调用点                         | Query 每阶段都有 trace 记录。                  | 集成测试断言阶段集合完整。       |
| H5       | 摄取链路全阶段打点。         | `rag-server/src/ingestion/pipeline.py`<br>`rag-server/src/ingestion/loaders/pdf_loader_markitdown.py`<br>`rag-server/src/ingestion/upsert/upsert_service.py`                                                         | `trace_stage()` 调用点                         | load/split/transform/embed/upsert 全有 trace。 | 摄取集成测试断言阶段明细。       |
| H6       | JSONL 导出器落地。           | `rag-server/src/observability/trace_exporter_jsonl.py`<br>`rag-server/scripts/export_traces.py`                                                                                                                      | `export_jsonl()`                               | Trace 可镜像导出为 JSONL。                     | 单测写文件并校验 JSON schema。   |
| H7       | Trace 查询服务与后端接口。   | `rag-server/src/observability/trace_service.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/controllers/trace_controller.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/repositories/trace_repository.py` | `get_trace_detail()`                           | 前端可通过 API 拉取 trace 列表和详情。         | 后端集成测试覆盖分页与过滤。     |
| H8       | 总览页接入真实监控数据。     | `sgcc-report-audit-app/frontend/src/views/OverviewView.vue`<br>`sgcc-report-audit-app/frontend/src/api/trace.ts`                                                                                                     | `loadOverview()`                               | 显示服务健康、资产统计、最近任务。             | 前端 E2E 检查指标卡渲染。        |
| H9       | 数据浏览页接入真实数据。     | `sgcc-report-audit-app/frontend/src/views/DataBrowserView.vue`<br>`sgcc-report-audit-app/frontend/src/api/documents.ts`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/controllers/document_controller.py`         | `loadDocuments()`                              | 可筛选文档、Chunk、图片。                      | 前后端联调测试。                 |
| H10      | Ingestion 管理页联动后端。   | `sgcc-report-audit-app/frontend/src/views/IngestionManagerView.vue`<br>`sgcc-report-audit-app/frontend/src/api/documents.ts`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/controllers/document_controller.py`    | `submitIngestionTask()`                        | 任务创建、状态轮询、重试可用。                 | E2E 提交任务流程测试。           |
| H11      | Ingestion Trace 页联动。     | `sgcc-report-audit-app/frontend/src/views/IngestionTracesView.vue`<br>`sgcc-report-audit-app/frontend/src/components/traces/WaterfallChart.vue`                                                                      | `loadIngestionTraceList()`                     | 摄取历史与阶段详情可展示。                     | E2E 断言列表和瀑布图存在。       |
| H12      | Query Trace 页联动。         | `sgcc-report-audit-app/frontend/src/views/QueryTracesView.vue`<br>`sgcc-report-audit-app/frontend/src/components/traces/TraceDetailPanel.vue`                                                                        | `loadQueryTraceList()`                         | 查询追踪、重排前后对比可展示。                 | E2E 断言候选结果对比表。         |
| H13      | 完成联动回归测试。           | `rag-server/tests/integration/test_document_manager.py`<br>`sgcc-report-audit-app/tests/e2e/traces.spec.ts`                                                                                                          | pytest/Playwright 用例                         | 可观测链路在主路径下持续可用。                 | CI 执行 integration + e2e 套件。 |

#### 阶段 I：SGCC 审查业务模块（实施细则）

| 任务编号 | 目标                          | 修改文件（需在 5.2 中存在）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 实现类/函数                               | 验收标准                                                            | 测试方法                                                         |
| -------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------- |
| I1       | 建立 MVC 后端骨架与依赖注入。 | `sgcc-report-audit-app/backend/src/sgcc_audit/main.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/core/dependencies.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/controllers/health_controller.py`                                                                                                                                                                                                                                                                                                                                                                           | `create_app()`<br>`get_audit_service()`   | 路由装配与依赖注入可运行。                                          | FastAPI TestClient 冒烟。                                        |
| I2       | 定义请求响应 Schema 与枚举。  | `sgcc-report-audit-app/backend/src/sgcc_audit/schemas/request_models.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/schemas/response_models.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/schemas/enums.py`                                                                                                                                                                                                                                                                                                                                                                   | Pydantic 模型类                           | 入参与出参结构稳定且可校验。                                        | schema 单测 + 反序列化测试。                                     |
| I3       | 封装 RAG MCP 客户端。         | `sgcc-report-audit-app/backend/src/sgcc_audit/clients/rag_mcp_client.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/clients/rag_tool_adapter.py`<br>`sgcc-report-audit-app/config/mcp_client.yaml`                                                                                                                                                                                                                                                                                                                                                                                   | `call_tool()`<br>`query_knowledge_hub()`  | 后端可稳定调用 rag-server 工具。                                    | Mock MCP 子进程 + 超时重试测试。                                 |
| I4       | 审查主编排服务落地。          | `sgcc-report-audit-app/backend/src/sgcc_audit/services/audit_orchestrator.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/check_dispatcher.py`<br>`sgcc-report-audit-app/backend/tests/unit/test_check_dispatcher.py`                                                                                                                                                                                                                                                                                                                                                        | `run_audit()`<br>`dispatch_check()`       | 可编排 20 项审查并汇总。                                            | 集成测试断言全项输出。                                           |
| I5       | Prompt 体系与版本加载。       | `sgcc-report-audit-app/config/prompts/common/system.md`<br>`sgcc-report-audit-app/config/prompts/common/output_schema.md`<br>`sgcc-report-audit-app/config/prompts/check_01_qualification.md` 至 `check_20_monitoring.md`（共 20 个）<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/prompt_service.py`                                                                                                                                                                                                                                                                         | `load_prompt()`                           | 可按审查项加载对应 prompt。                                         | 单测覆盖 prompt 缺失与回退。                                     |
| I6       | 实现 01-05 审查规则。         | `sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_01_qualification.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_02_approval.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_03_basis.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_04_access_info.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_05_equipment_params.py`                                                                                                                               | `evaluate()`（每规则）                    | 前 5 项可返回结论、说明、证据。                                     | 规则单测（正例/反例/缺证据）。                                   |
| I7       | 实现 06-10 审查规则。         | `sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_06_disturbance_source.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_07_raw_materials.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_08_grid_equipment.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_09_grid_capacity.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_10_indicators.py`                                                                                                                | `evaluate()`（每规则）                    | 06-10 项规则可独立执行。                                            | 单测 + 编排集成测试。                                            |
| I8       | 实现 11-15 审查规则。         | `sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_11_limits.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_12_background_test.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_13_superposition.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_14_simulation_model.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_15_assessment_point.py`                                                                                                                  | `evaluate()`（每规则）                    | 11-15 项规则可独立执行。                                            | 单测 + 编排集成测试。                                            |
| I9       | 实现 16-20 审查规则。         | `sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_16_operation_mode.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_17_calculation_result.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_18_conclusion.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_19_governance.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/checks/check_20_monitoring.py`                                                                                                                      | `evaluate()`（每规则）                    | 16-20 项规则可独立执行。                                            | 单测 + 编排集成测试。                                            |
| I10      | 聚合证据并合并总结果。        | `sgcc-report-audit-app/backend/src/sgcc_audit/services/evidence_service.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/services/result_merge_service.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/models/evidence.py`<br>`sgcc-report-audit-app/backend/tests/unit/test_evidence_service.py`<br>`sgcc-report-audit-app/backend/tests/unit/test_result_merge_service.py`                                                                                                                                                                                                      | `collect_evidence()`<br>`merge_results()` | 输出总分、单项、证据可追溯。                                        | 单测断言去重和排序规则。                                         |
| I11      | 落地任务与结果仓储。          | `sgcc-report-audit-app/backend/src/sgcc_audit/repositories/audit_task_repository.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/repositories/audit_result_repository.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/models/audit_task.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/models/audit_result.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/models/check_item.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/models/report_profile.py`<br>`sgcc-report-audit-app/backend/sql/001_audit_tables.sql`<br>`sgcc-report-audit-app/scripts/init_db.py` | `save_task()`<br>`save_result()`          | 任务状态与结果可持久化查询。                                        | 仓储集成测试。                                                   |
| I12      | 完成控制器接口。              | `sgcc-report-audit-app/backend/src/sgcc_audit/controllers/audit_controller.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/controllers/document_controller.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/controllers/trace_controller.py`                                                                                                                                                                                                                                                                                                                                      | `submit_audit()`<br>`get_audit_result()`  | API 覆盖审查提交、文档、追踪查询。                                  | FastAPI 集成测试。                                               |
| I13      | 前后端联调审查结果页。        | `sgcc-report-audit-app/frontend/src/views/AuditResultView.vue`<br>`sgcc-report-audit-app/frontend/src/api/audit.ts`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/controllers/audit_controller.py`                                                                                                                                                                                                                                                                                                                                                                                      | `fetchAuditResult()`                      | 前端可展示真实 20 项结果并跳证据。                                  | E2E 审查结果链路测试。                                           |
| I14      | 完成业务 A1-A4 集成测试。     | `sgcc-report-audit-app/backend/tests/integration/test_submit_audit_api.py`<br>`sgcc-report-audit-app/backend/tests/integration/test_get_result_api.py`<br>`sgcc-report-audit-app/backend/tests/e2e/test_a1_a4_business_cases.py`                                                                                                                                                                                                                                                                                                                                                           | pytest 用例                               | A1-A4 核心业务场景全部通过。                                        | `uv run pytest backend/tests/integration backend/tests/e2e -q`。 |
| I15      | 落地视图模型（View Models）。 | `sgcc-report-audit-app/backend/src/sgcc_audit/views/audit_response_view.py`<br>`sgcc-report-audit-app/backend/src/sgcc_audit/views/error_view.py`                                                                                                                                                                                                                                                                                                                                                                                                                                          | `AuditResponseView`<br>`ErrorView`        | 输出 DTO 字段稳定；错误响应结构统一；与 `response_models.py` 对齐。 | schema 单测 + 序列化断言。                                       |

#### 阶段 J：评估体系、端到端验收与文档收口（实施细则）

| 任务编号 | 目标                        | 修改文件（需在 5.2 中存在）                                                                                                                                                                   | 实现类/函数                                           | 验收标准                                   | 测试方法                                           |
| -------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------ | -------------------------------------------------- |
| J1       | 落地 Ragas 与自定义评估器。 | `rag-server/src/evaluation/ragas_evaluator.py`<br>`rag-server/src/evaluation/custom_metrics_evaluator.py`<br>`rag-server/src/evaluation/base_evaluator.py`                                    | `evaluate_batch()`                                    | 支持 `hit_rate/MRR/faithfulness` 输出。    | 单测 + 小样本评估回归。                            |
| J2       | 实现组合评估与执行器。      | `rag-server/src/evaluation/composite_evaluator.py`<br>`rag-server/src/evaluation/eval_runner.py`<br>`rag-server/src/factories/evaluator_factory.py`                                           | `CompositeEvaluator.evaluate()`<br>`EvalRunner.run()` | 支持多评估器并行执行与聚合。               | 集成测试验证汇总结果。                             |
| J3       | 构建黄金测试集。            | `rag-server/data/eval/golden_set.jsonl`<br>`docs/runbooks/local-dev.md`                                                                                                                       | 无（数据集定义）                                      | 数据集包含 query、ground_truth、citation。 | 数据校验脚本 + 人工抽检。                          |
| J4       | 启用评估面板页面。          | `sgcc-report-audit-app/frontend/src/views/EvaluationPanelView.vue`<br>`sgcc-report-audit-app/frontend/src/stores/trace.ts`                                                                    | `loadEvaluationHistory()`                             | 页面可触发评估并展示历史趋势。             | 前端 E2E 与接口联调。                              |
| J5       | 建立阈值门禁脚本。          | `rag-server/scripts/run_eval.py`<br>`rag-server/config/settings.yaml`                                                                                                                         | `main()`<br>`check_thresholds()`                      | 指标低于阈值时脚本返回非零退出码。         | 在 CI 中执行 `uv run python scripts/run_eval.py`。 |
| J6       | 完成 MCP E2E 验收。         | `rag-server/tests/e2e/test_stdio_workflow.py`<br>`rag-server/tests/e2e/test_multimodal_response.py`<br>`rag-server/tests/integration/test_mcp_tools.py`                                       | E2E 测试函数                                          | `tools/list` 与关键 `tools/call` 全通过。  | pytest e2e 套件。                                  |
| J7       | 完成 Dashboard E2E 冒烟。   | `sgcc-report-audit-app/tests/e2e/audit-result.spec.ts`<br>`sgcc-report-audit-app/tests/e2e/traces.spec.ts`                                                                                    | Playwright 用例                                       | 7 页面加载、关键交互、错误态可用。         | `npx playwright test`。                            |
| J8       | 完成 SGCC 审查 E2E。        | `sgcc-report-audit-app/backend/tests/e2e/test_a1_a4_business_cases.py`<br>`sgcc-report-audit-app/frontend/src/views/AuditResultView.vue`                                                      | 端到端流程用例                                        | 提交报告到结果展示链路闭环通过。           | 联调环境执行 E2E。                                 |
| J9       | 文档收口。                  | `README.md`<br>`docs/runbooks/local-dev.md`<br>`docs/runbooks/troubleshooting.md`<br>`docs/architecture/context.md`<br>`docs/architecture/containers.md`<br>`docs/architecture/components.md` | 无（文档）                                            | 文档覆盖安装、运行、架构说明、常见问题。   | 按文档从零复现一次。                               |
| J10      | 发布与复现清单落地。        | `docs/runbooks/deployment.md`<br>`docs/api/mcp-tools.md`<br>`README.md`                                                                                                                       | 无（发布清单）                                        | 包含版本号、配置快照、测试报告入口。       | 发布前 checklist 逐项勾选。                        |

#### 阶段 K：Docker 封装与可迁移部署（实施细则）

| 任务编号 | 目标                            | 修改文件（需在 5.2 中存在）                                                                                                                                                                                                                    | 实现类/函数                      | 验收标准                                            | 测试方法                               |
| -------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | --------------------------------------------------- | -------------------------------------- |
| K1       | 完善容器化规范与构建约定。      | `docker/docker-compose.yml`<br>`docker/.dockerignore`<br>`docs/runbooks/deployment.md`                                                                                                                                                         | 无（编排约定）                   | 形成统一镜像命名和构建规范。                        | `docker compose config` 校验。         |
| K2       | 封装 rag-server 镜像。          | `docker/rag-server.Dockerfile`<br>`docker/.dockerignore`<br>`rag-server/README.md`                                                                                                                                                             | Dockerfile 启动命令              | 镜像可构建并启动 MCP Server。                       | `docker build` + 容器健康检查。        |
| K3       | 封装 backend 镜像。             | `docker/backend.Dockerfile`<br>`sgcc-report-audit-app/backend/README.md`                                                                                                                                                                       | Dockerfile 启动命令              | backend 镜像可连通 rag-server（stdio 子进程模式）。 | compose 联调请求 `/health`。           |
| K4       | 封装 frontend 生产镜像。        | `docker/frontend.Dockerfile`<br>`sgcc-report-audit-app/frontend/package.json`                                                                                                                                                                  | 多阶段构建脚本                   | 前端镜像可提供静态页面服务。                        | `docker run` 后访问首页。              |
| K5       | 接入 PostgreSQL+PgVector 容器。 | `docker/docker-compose.yml`<br>`rag-server/sql/001_observability.sql`<br>`rag-server/sql/002_ingestion_history.sql`<br>`rag-server/sql/003_image_index.sql`<br>`rag-server/sql/004_bm25_meta.sql`<br>`rag-server/sql/005_processing_cache.sql` | DB 初始化入口                    | Postgres 启动后自动初始化所需表。                   | compose 启动并执行 SQL 验证。          |
| K6       | 完成全栈 Compose 编排。         | `docker/docker-compose.yml`<br>`sgcc-report-audit-app/scripts/docker_up.sh`                                                                                                                                                                    | `docker_up.sh`                   | `frontend/backend/rag-server/postgres` 可一键拉起。 | `bash docker_up.sh` 后接口冒烟。       |
| K7       | 落地数据卷与映射策略。          | `docker/docker-compose.yml`<br>`sgcc-report-audit-app/config/data_mapping.yaml`<br>`sgcc-report-audit-app/scripts/sync_workspace_links.sh`                                                                                                     | 卷挂载配置                       | 重启容器后 `data/cache/logs` 保留。                 | 写入样本后重启验证持久化。             |
| K8       | 规范容器环境变量模板。          | `docker/.env.docker.example`<br>`rag-server/.env.example`<br>`sgcc-report-audit-app/.env.example`                                                                                                                                              | 无（模板）                       | 关键密钥与连接项均有模板说明。                      | `docker compose --env-file` 启动验证。 |
| K9       | 提供一键运维脚本。              | `sgcc-report-audit-app/scripts/docker_up.sh`<br>`sgcc-report-audit-app/scripts/docker_down.sh`<br>`sgcc-report-audit-app/scripts/docker_logs.sh`                                                                                               | `docker_up()`<br>`docker_down()` | 启停与日志查看可脚本化执行。                        | 脚本执行回归测试。                     |
| K10      | 完成容器化验收与迁移文档。      | `docs/runbooks/deployment.md`<br>`README.md`                                                                                                                                                                                                   | 无（验收文档）                   | 提供跨机器迁移步骤与冒烟清单。                      | 依据文档在新环境复现一次。             |
