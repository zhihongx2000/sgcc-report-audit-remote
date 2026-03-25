"""Unit tests for Embedding provider adapters using fake transports (mocks).

Each provider is tested for:
- embed_texts() encodes a batch and returns the correct number of vectors
- embed() convenience wrapper returns a single vector
- empty texts raises ValueError
- empty single text raises ValueError
- API errors are propagated (retry eventually re-raises)
- returned vector dimension is consistent across batch items
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from libs.embedding.base_embedding import BaseEmbedding
from libs.embedding.ollama_embedding import OllamaEmbedding
from libs.embedding.openai_embedding import OpenAIEmbedding
from utils.retry import RetryPolicy


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_NO_RETRY = RetryPolicy(max_attempts=1, base_delay_seconds=0)

_DIM = 4  # small dimension for test vectors


def _make_vectors(n: int, dim: int = _DIM) -> list[list[float]]:
	return [[float(i + j) for j in range(dim)] for i in range(n)]


# ---------------------------------------------------------------------------
# BaseEmbedding contract
# ---------------------------------------------------------------------------


class _ConcreteEmbedding(BaseEmbedding):
	"""Minimal concrete implementation for base-contract tests."""

	def __init__(self, vectors: list[list[float]]) -> None:
		super().__init__(retry_policy=_NO_RETRY)
		self._vectors = vectors

	def _embed_texts_once(self, texts: list[str]) -> list[list[float]]:
		return self._vectors[: len(texts)]


@pytest.mark.unit
def test_base_embed_texts_returns_one_vector_per_text() -> None:
	vecs = _make_vectors(3)
	emb = _ConcreteEmbedding(vecs)
	result = emb.embed_texts(["a", "b", "c"])
	assert len(result) == 3


@pytest.mark.unit
def test_base_embed_texts_empty_raises() -> None:
	emb = _ConcreteEmbedding(_make_vectors(1))
	with pytest.raises(ValueError, match="texts must not be empty"):
		emb.embed_texts([])


@pytest.mark.unit
def test_base_embed_single_text_convenience() -> None:
	vecs = _make_vectors(1)
	emb = _ConcreteEmbedding(vecs)
	result = emb.embed("hello")
	assert result == vecs[0]


@pytest.mark.unit
def test_base_embed_empty_text_raises() -> None:
	emb = _ConcreteEmbedding(_make_vectors(1))
	with pytest.raises(ValueError, match="text must not be empty"):
		emb.embed("")


@pytest.mark.unit
def test_base_embed_texts_error_propagates() -> None:
	class _FailingEmbedding(BaseEmbedding):
		def _embed_texts_once(self, texts: list[str]) -> list[list[float]]:
			raise RuntimeError("upstream failure")

	emb = _FailingEmbedding(retry_policy=_NO_RETRY)
	with pytest.raises(RuntimeError, match="upstream failure"):
		emb.embed_texts(["x"])


@pytest.mark.unit
def test_base_embed_texts_dimension_consistent() -> None:
	vecs = _make_vectors(3, dim=8)
	emb = _ConcreteEmbedding(vecs)
	result = emb.embed_texts(["a", "b", "c"])
	dims = {len(v) for v in result}
	assert dims == {8}


# ---------------------------------------------------------------------------
# OpenAIEmbedding
# ---------------------------------------------------------------------------


def _openai_embed_response(vectors: list[list[float]]) -> MagicMock:
	"""Build a minimal fake openai CreateEmbeddingResponse."""
	data_items = []
	for idx, vec in enumerate(vectors):
		item = MagicMock()
		item.index = idx
		item.embedding = vec
		data_items.append(item)
	resp = MagicMock()
	resp.data = data_items
	return resp


@pytest.mark.unit
@patch("libs.embedding.openai_embedding.openai.OpenAI")
def test_openai_embed_texts_returns_batch(mock_cls: MagicMock) -> None:
	vecs = _make_vectors(2)
	mock_create = mock_cls.return_value.embeddings.create
	mock_create.return_value = _openai_embed_response(vecs)

	emb = OpenAIEmbedding(api_key="k", model="text-embedding-3-small", retry_policy=_NO_RETRY)
	result = emb.embed_texts(["hello", "world"])

	assert result == vecs
	call_kwargs = mock_create.call_args.kwargs
	assert call_kwargs["model"] == "text-embedding-3-small"
	assert call_kwargs["input"] == ["hello", "world"]


@pytest.mark.unit
@patch("libs.embedding.openai_embedding.openai.OpenAI")
def test_openai_embed_single(mock_cls: MagicMock) -> None:
	vecs = _make_vectors(1)
	mock_cls.return_value.embeddings.create.return_value = _openai_embed_response(vecs)

	emb = OpenAIEmbedding(api_key="k", model="text-embedding-3-small", retry_policy=_NO_RETRY)
	result = emb.embed("hi")

	assert result == vecs[0]


@pytest.mark.unit
@patch("libs.embedding.openai_embedding.openai.OpenAI")
def test_openai_embed_error_propagates(mock_cls: MagicMock) -> None:
	mock_cls.return_value.embeddings.create.side_effect = RuntimeError("api error")

	emb = OpenAIEmbedding(api_key="k", model="text-embedding-3-small", retry_policy=_NO_RETRY)
	with pytest.raises(RuntimeError, match="api error"):
		emb.embed_texts(["x"])


@pytest.mark.unit
@patch("libs.embedding.openai_embedding.openai.OpenAI")
def test_openai_embed_sorts_by_index(mock_cls: MagicMock) -> None:
	"""Verify that vectors are returned in original text order even if API returns them shuffled."""
	vec_a = [1.0, 0.0]
	vec_b = [0.0, 1.0]
	# Return items in reverse order (index=1 first, then index=0)
	item0 = MagicMock(index=0, embedding=vec_a)
	item1 = MagicMock(index=1, embedding=vec_b)
	resp = MagicMock()
	resp.data = [item1, item0]  # shuffled
	mock_cls.return_value.embeddings.create.return_value = resp

	emb = OpenAIEmbedding(api_key="k", model="text-embedding-3-small", retry_policy=_NO_RETRY)
	result = emb.embed_texts(["first", "second"])

	assert result[0] == vec_a
	assert result[1] == vec_b


@pytest.mark.unit
@patch("libs.embedding.openai_embedding.openai.OpenAI")
def test_openai_embed_with_base_url(mock_cls: MagicMock) -> None:
	"""Custom base_url is forwarded to the OpenAI client constructor."""
	vecs = _make_vectors(1)
	mock_cls.return_value.embeddings.create.return_value = _openai_embed_response(vecs)

	emb = OpenAIEmbedding(
		api_key="k",
		model="bge-m3",
		base_url="http://my-server/v1",
		retry_policy=_NO_RETRY,
	)
	emb.embed_texts(["x"])

	call_kwargs = mock_cls.call_args.kwargs
	assert call_kwargs["base_url"] == "http://my-server/v1"


# ---------------------------------------------------------------------------
# OllamaEmbedding
# ---------------------------------------------------------------------------


def _ollama_embed_response(vectors: list[list[float]]) -> MagicMock:
	resp = MagicMock()
	resp.embeddings = vectors
	return resp


@pytest.mark.unit
@patch("libs.embedding.ollama_embedding._ollama.Client")
def test_ollama_embed_texts_returns_batch(mock_cls: MagicMock) -> None:
	vecs = _make_vectors(3)
	mock_embed = mock_cls.return_value.embed
	mock_embed.return_value = _ollama_embed_response(vecs)

	emb = OllamaEmbedding(model="nomic-embed-text", retry_policy=_NO_RETRY)
	result = emb.embed_texts(["a", "b", "c"])

	assert len(result) == 3
	assert result == vecs
	mock_embed.assert_called_once_with(model="nomic-embed-text", input=["a", "b", "c"])


@pytest.mark.unit
@patch("libs.embedding.ollama_embedding._ollama.Client")
def test_ollama_embed_single(mock_cls: MagicMock) -> None:
	vecs = _make_vectors(1)
	mock_cls.return_value.embed.return_value = _ollama_embed_response(vecs)

	emb = OllamaEmbedding(model="nomic-embed-text", retry_policy=_NO_RETRY)
	result = emb.embed("test")

	assert result == vecs[0]


@pytest.mark.unit
@patch("libs.embedding.ollama_embedding._ollama.Client")
def test_ollama_embed_error_propagates(mock_cls: MagicMock) -> None:
	mock_cls.return_value.embed.side_effect = ConnectionError("server down")

	emb = OllamaEmbedding(model="nomic-embed-text", retry_policy=_NO_RETRY)
	with pytest.raises(ConnectionError):
		emb.embed_texts(["x"])


@pytest.mark.unit
@patch("libs.embedding.ollama_embedding._ollama.Client")
def test_ollama_embed_base_url_forwarded(mock_cls: MagicMock) -> None:
	vecs = _make_vectors(1)
	mock_cls.return_value.embed.return_value = _ollama_embed_response(vecs)

	OllamaEmbedding(model="m", base_url="http://custom:11434", retry_policy=_NO_RETRY)

	call_kwargs = mock_cls.call_args.kwargs
	assert call_kwargs["host"] == "http://custom:11434"


# ---------------------------------------------------------------------------
# BGEEmbedding (mocking sentence_transformers to avoid model download)
# ---------------------------------------------------------------------------


def _make_numpy_like_rows(vecs: list[list[float]]) -> MagicMock:
	"""Return a mock that mimics a 2-D numpy array (iterable of rows with .tolist())."""
	rows = []
	for v in vecs:
		row = MagicMock()
		row.tolist.return_value = v
		rows.append(row)
	mock_array = MagicMock()
	mock_array.__iter__ = MagicMock(return_value=iter(rows))
	return mock_array


@pytest.mark.unit
@patch("libs.embedding.bge_embedding.sentence_transformers")
def test_bge_embed_texts_returns_batch(mock_st: MagicMock) -> None:
	from libs.embedding.bge_embedding import BGEEmbedding

	vecs = _make_vectors(2)
	mock_model = MagicMock()
	mock_model.encode.return_value = _make_numpy_like_rows(vecs)
	mock_st.SentenceTransformer.return_value = mock_model

	emb = BGEEmbedding(model_name_or_path="BAAI/bge-large-zh-v1.5", retry_policy=_NO_RETRY)
	result = emb.embed_texts(["text1", "text2"])

	assert len(result) == 2
	assert result == vecs


@pytest.mark.unit
@patch("libs.embedding.bge_embedding.sentence_transformers")
def test_bge_model_loaded_lazily(mock_st: MagicMock) -> None:
	from libs.embedding.bge_embedding import BGEEmbedding

	mock_model = MagicMock()
	mock_model.encode.return_value = _make_numpy_like_rows(_make_vectors(1))
	mock_st.SentenceTransformer.return_value = mock_model

	emb = BGEEmbedding(retry_policy=_NO_RETRY)
	# Model should not be loaded until first call
	mock_st.SentenceTransformer.assert_not_called()

	emb.embed_texts(["hi"])
	mock_st.SentenceTransformer.assert_called_once()


@pytest.mark.unit
@patch("libs.embedding.bge_embedding.sentence_transformers")
def test_bge_embed_error_propagates(mock_st: MagicMock) -> None:
	from libs.embedding.bge_embedding import BGEEmbedding

	mock_model = MagicMock()
	mock_model.encode.side_effect = RuntimeError("model error")
	mock_st.SentenceTransformer.return_value = mock_model

	emb = BGEEmbedding(retry_policy=_NO_RETRY)
	with pytest.raises(RuntimeError, match="model error"):
		emb.embed_texts(["x"])
