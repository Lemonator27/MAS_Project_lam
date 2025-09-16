import os
from functools import lru_cache
from typing import Any

from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings


def _conn_str() -> str:
    user = os.getenv("PGUSER", "mas_user")
    password = os.getenv("PGPASSWORD", "mas_pass")
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    db = os.getenv("PGDATABASE", "mas_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


@lru_cache(maxsize=1)
def get_vectorstore() -> PGVector:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return PGVector(
        embedding_function=embeddings,
        collection_name="finance_docs",
        connection_string=_conn_str(),
    )


def get_retriever(k: int = 4) -> Any:
    return get_vectorstore().as_retriever(k=k)
