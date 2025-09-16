README.md: Hướng Dẫn Multi‑Agent System (MAS) cho Phân Tích Tài Chính – Bản Demo (Ollama + CSV + FAISS)

Giới thiệu hệ thống
Hệ thống gồm 5 agents phối hợp xử lý câu hỏi và tác vụ tài chính:
- Central Coordinator Agent: định tuyến câu hỏi tới agent phù hợp và tổng hợp kết quả.
- Ingest Data Agent: đọc dữ liệu từ CSV (đã có sẵn dữ liệu fake trong thư mục `data/`).
- Budget Agent: so sánh ngân sách với thực chi, tính variance và hiển thị bảng.
- Alert & Risk Agent: phát hiện giao dịch bất thường bằng z‑score.
- Spending Analyzer Agent: tổng hợp chi phí subscription theo vendor để tối ưu.

RAG chạy local in‑memory (DocArrayInMemorySearch) với embeddings từ Ollama (`nomic-embed-text`). Không cần bất kỳ DB hay thêm package hệ thống nào, phù hợp Windows.

Điểm chính của bản demo
- Không cần Docker/K8s, không cần PostgreSQL/pgvector.
- CSV data đã có sẵn trong `data/` – không cần thao tác thêm.
- Hai cách chạy: Streamlit UI hoặc API FastAPI.

Cấu trúc thư mục
```
MAS_Project/
  app/               # API/Streamlit demo
  agents/            # 5 agents
  orchestration/     # LangGraph workflow
  rag/               # FAISS vector store & retriever
  scripts/           # RAG seed (local)
  data/              # CSV synthetic (đã có sẵn)
  tests/             # Pytest
  requirements.txt
  README.md
```

1) Cài đặt yêu cầu
- Python 3.10+, RAM ≥ 8 GB
- Cài Ollama: https://ollama.com/
- Kéo model demo:
```bash
ollama pull llama3
```

2) Thiết lập môi trường Python
```bash
python -m venv venv
./venv/Scripts/activate  # Windows PowerShell
# Linux/macOS: source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3) Khởi tạo RAG local (in‑memory)
```bash
python scripts/rag_setup.py
```
- In‑memory, không tạo file index. Có thể chạy trực tiếp.

4) Chạy demo giao diện (Streamlit)
```bash
streamlit run app/demo.py
```
- Mở URL (mặc định http://localhost:8501).

5) Chạy API (tuỳ chọn)
```bash
python app/server.py
```

6) Test nhanh (pytest)
```bash
pytest -q
```

Ghi chú cấu hình
- Mặc định dùng Ollama, không cần API key.
- Chroma index: `rag/chroma_index/`.
- CSV đã có trong `data/`.

FAQ nhanh
- Không có API key? Không cần – dùng Ollama.
- Lỗi FAISS index? Chạy lại `python scripts/rag_setup.py`.

Giấy phép
MIT (có thể thay đổi tuỳ nhu cầu).
