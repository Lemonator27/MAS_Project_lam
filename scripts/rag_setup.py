import os
import sys

# Ensure project root is on sys.path when running as a script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from rag.vectorstore import add_texts, get_retriever


def main() -> None:
    import json
    
    rag_file = os.path.join(os.path.dirname(__file__), "..", "data", "rag_documents.json")
    if os.path.exists(rag_file):
        with open(rag_file, "r", encoding="utf-8") as f:
            rag_docs = json.load(f)
        texts = [doc["text"] for doc in rag_docs]
        print(f"Loaded {len(texts)} documents from {rag_file}")
    else:
        texts = [
            "Policy: Chi tiêu > $5000 cần approve bởi CFO.",
            "GAAP: Báo cáo tài chính phải tuân thủ nguyên tắc dồn tích.",
            "Travel: Limit $2000 per employee per month, ngoại lệ cần phê duyệt.",
        ]
        print("Using fallback texts")
    
    add_texts(texts)
    retriever = get_retriever(k=3)
    sample = retriever.get_relevant_documents("policy chi tiêu")
    print("Seeded docs. Sample retrieve:")
    for d in sample:
        print("-", d.page_content)


if __name__ == "__main__":
    main()
