import os
import json
from functools import lru_cache
from typing import Any, List, Tuple

import numpy as np
from langchain_community.embeddings import OllamaEmbeddings


INDEX_PATH = os.path.join(os.path.dirname(__file__), "simple_index.json")
_EMBEDDER: OllamaEmbeddings | None = None
_INDEX: List[Tuple[str, List[float]]] | None = None


@lru_cache(maxsize=1)
def _get_embedder() -> OllamaEmbeddings:
    global _EMBEDDER
    if _EMBEDDER is None:
        _EMBEDDER = OllamaEmbeddings(model="nomic-embed-text")
    return _EMBEDDER


def _load_index() -> List[Tuple[str, List[float]]]:
    global _INDEX
    if _INDEX is not None:
        return _INDEX
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        _INDEX = [(d["text"], d["embedding"]) for d in data]
    else:
        _INDEX = []
    return _INDEX


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    if a.size == 0 or b.size == 0:
        return 0.0
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def add_texts(texts: List[str]) -> None:
    index = _load_index()
    emb = _get_embedder()
    vectors = emb.embed_documents(texts)
    for t, v in zip(texts, vectors):
        index.append((t, v))
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump([{"text": t, "embedding": v} for t, v in index], f, ensure_ascii=False)


def get_retriever(k: int = 4) -> Any:
    def retrieve(query: str) -> List[str]:
        index = _load_index()
        if not index:
            return []
        qv = np.array(_get_embedder().embed_query(query), dtype=float)
        scored = [
            (txt, _cosine(qv, np.array(vec, dtype=float))) for txt, vec in index
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [txt for txt, _ in scored[:k]]

    class SimpleRetriever:
        def get_relevant_documents(self, query: str) -> List[Any]:
            return [type("Doc", (), {"page_content": t})() for t in retrieve(query)]

    return SimpleRetriever()
