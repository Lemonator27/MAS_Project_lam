import os
import sys
from typing import List

from langchain_community.embeddings import OllamaEmbeddings

# Ensure project root is on sys.path when running as a script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from rag.vectorstore import add_texts, get_retriever
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

    # Use local Ollama embeddings to avoid heavy torch installs on Windows
    # Make sure to: ollama pull nomic-embed-text
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    texts = [d.page_content for d in chunks]
    add_texts(texts)
    retriever = get_retriever(k=3)
    test = retriever.get_relevant_documents("policy chi tiêu")
    print("Seeded docs. Sample retrieve:")
    for d in test:
        print("-", d.page_content)


if __name__ == "__main__":
    main()
