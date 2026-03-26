目前 rag_server/models 目录中的模型还没有下载完，联网时运行以下命令继续下载：

```bash
cd rag-server
SENTENCE_TRANSFORMERS_HOME=./models \
  python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-large-zh-v1.5')"

SENTENCE_TRANSFORMERS_HOME=./models \
  python -c "from sentence_transformers import CrossEncoder; CrossEncoder('BAAI/bge-reranker-v2-m3')"
```
