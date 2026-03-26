# 03 Tech Stack Checklist

## Use When

- adding/changing dependencies,
- choosing runtime/framework integration patterns.

## Inputs

1. `DEV_SPEC.md` section `3`.
2. Selected task acceptance from `6.4`.

## Checklist

- [ ] Verify candidate change is allowed by section `3`.
- [ ] Verify command/toolchain version baseline before risky changes.
- [ ] Use `uv` for Python dependency and execution commands.
- [ ] Avoid new libraries unless required by selected task.

## Environment Baseline

1. `uv 0.8.10`
2. `nvm 0.39.3`
3. `npm 11.9.0`
4. `node v24.14.0`

## Multi-Host Python Environment Rule

1. Use `uv` to rebuild environments per host; do not assume `.venv` is portable across machines.
2. Dependency truth source is `pyproject.toml` (+ `uv.lock` when present), not checked-in virtualenv folders.
3. For this repository, run:

```bash
cd rag-server && uv sync
cd ../sgcc-report-audit-app/backend && uv sync
```

4. If `uv sync` fails due to Python version mismatch, install/select a compatible version (for example 3.12), then rerun sync.

## Configuration Staging Rule

1. `A4` builds config loading foundation with minimal key set.
2. `D10` aligns full section `5.6` schema and strict validation.
3. Do not force full `5.6` scope during `A4` unless user asks.

## Local Model Asset Rules

1. **Model storage path**: `rag-server/models/` — git-ignored, portable via `rsync`.
2. **Top-level config field**: `model_cache_dir: ./models` (relative to `rag-server/` working directory).
3. **Components that read `model_cache_dir`**: `BGEEmbedding` (`cache_folder` arg) and `CrossEncoderReranker` (`cache_folder` arg to `sentence_transformers.CrossEncoder`).
4. **RTX 4060 8GB recommended models**:

| Role      | Model                       | Dim  | VRAM   |
|-----------|-----------------------------|------|--------|
| Embedding | `BAAI/bge-large-zh-v1.5`    | 1024 | ~1.3 GB |
| Reranker  | `BAAI/bge-reranker-v2-m3`   | —    | ~1.1 GB |
| Total     | —                           | —    | ~2.5 GB |

5. **`embedding_dim` must be `1024`** for `bge-large-zh-v1.5`/`bge-m3`. Never use 1536 for BGE models.
6. For mainland China: use `ModelScope` SDK or set `MODELSCOPE_CACHE` env var instead of HuggingFace Hub.

## Output Record

1. Stack compatibility decision.
2. Dependency decision with spec justification.
3. Any version mismatch and risk note.
