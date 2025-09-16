import os
from typing import List

from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document


def get_connection_string() -> str:
    user = os.getenv("PGUSER", "mas_user")
    password = os.getenv("PGPASSWORD", "mas_pass")
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    db = os.getenv("PGDATABASE", "mas_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def seed_policy_docs() -> List[Document]:
    texts = [
        "Policy: Chi tiêu > $5000 cần approve bởi CFO.",
        "GAAP: Báo cáo tài chính phải tuân thủ nguyên tắc dồn tích.",
        "Travel: Limit $2000 per employee per month, ngoại lệ cần phê duyệt.",
    ]
    return [Document(page_content=t) for t in texts]


def main() -> None:
    docs = seed_policy_docs()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="finance_docs",
        connection_string=get_connection_string(),
    )

    retriever = vectorstore.as_retriever(k=3)
    test = retriever.get_relevant_documents("policy chi tiêu")
    print("Seeded docs. Sample retrieve:")
    for d in test:
        print("-", d.page_content)


if __name__ == "__main__":
    main()
