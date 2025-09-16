import os
from functools import lru_cache
from typing import Any

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


INDEX_DIR = os.path.join(os.path.dirname(__file__), "faiss_index")


@lru_cache(maxsize=1)
def get_vectorstore() -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if os.path.isdir(INDEX_DIR):
        return FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    # if not seeded yet, caller should run scripts/rag_setup.py first
    return FAISS.from_texts(["Policy: run rag_setup.py to seed index."], embeddings)


def get_retriever(k: int = 4) -> Any:
    return get_vectorstore().as_retriever(search_kwargs={"k": k})
