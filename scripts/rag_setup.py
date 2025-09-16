import os
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document


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

    vectorstore = FAISS.from_documents(chunks, embeddings)

    index_dir = os.path.join(os.path.dirname(__file__), "..", "rag", "faiss_index")
    index_dir = os.path.abspath(index_dir)
    os.makedirs(index_dir, exist_ok=True)
    vectorstore.save_local(index_dir)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    test = retriever.get_relevant_documents("policy chi tiêu")
    print("Seeded docs. Sample retrieve:")
    for d in test:
        print("-", d.page_content)


if __name__ == "__main__":
    main()
