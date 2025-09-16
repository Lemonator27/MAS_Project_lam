README.md: Hướng Dẫn Xây Dựng Multi-Agent System (MAS) Cho Phân Tích Tài Chính MVP

Giới thiệu
Dự án này dựng một Multi‑Agent System (MAS) dùng LangChain/LangGraph để xử lý tác vụ tài chính cơ bản. Hệ thống gồm 5 agents (1 Coordinator + 4 chuyên biệt) và RAG với PostgreSQL + pgvector. Bạn có thể chạy demo end‑to‑end trên máy local (Docker/Minikube tuỳ chọn).

Tính năng chính
- CFO/Operations Q&A qua các agent chuyên biệt.
- Tự động hoá: ingest dữ liệu, phân tích ngân sách, cảnh báo rủi ro, phân loại chi tiêu.
- RAG tránh hallucination: truy xuất policy/quy định từ vector store.
- Output: văn bản, bảng Pandas, PDF, giao diện demo Streamlit.

Yêu cầu hệ thống
- Ubuntu 20.04+ (khuyến nghị; Windows WSL2 được). Python 3.10+
- Docker 20.10+, (tuỳ chọn) Minikube 1.25+, kubectl
- RAM ≥ 8 GB, 4 CPU
- Tài khoản Kaggle (tải dataset), (tuỳ chọn) OpenAI/Groq API key; hoặc dùng Ollama local.

Cấu trúc thư mục
```
MAS_Project/
  app/               # API/Streamlit demo
  agents/            # 5 agents (coordinator + 4)
  orchestration/     # LangGraph workflow (MAS graph)
  rag/               # Vector store, retriever, embeddings
  scripts/           # Tiện ích: init DB, seed data, RAG setup
  data/              # CSV synthetic (transactions, budgets, risks, ...)
  k8s/               # Manifests cho Minikube/Kubernetes
  tests/             # Pytest
  Dockerfile
  docker-compose.yml
  requirements.txt
  README.md
```

1) Thiết lập môi trường (Python + deps)
Chạy lần lượt các lệnh sau:
```bash
python -m venv venv
./venv/Scripts/activate  # Windows PowerShell
# Trên Linux/macOS: source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) Tạo/generate synthetic data (tối thiểu 3 CSV)
Bạn có thể dùng notebook hoặc script. Bản đơn giản (script Pandas) sẽ được thêm sau, còn hiện tại bạn có thể tạo file trống để test luồng.
```bash
mkdir -p data
```
- Gợi ý tên file: `data/transactions.csv`, `data/budgets.csv`, `data/risks.csv`.

3) Chạy Postgres + pgvector bằng Docker Compose
```bash
docker-compose up -d
docker ps  # kiểm tra service db đang chạy
```

4) Khởi tạo database và schema
```bash
python scripts/init_db.py
```
- Script sẽ bật extension pgvector và tạo bảng cơ bản.

5) Thiết lập RAG (nhúng policy mẫu vào pgvector)
```bash
python scripts/rag_setup.py
```
- Lưu ý: Script dùng embeddings từ HuggingFace mặc định; có thể đổi sang OpenAI nếu có API key.

6) Chạy demo giao diện (Streamlit)
```bash
streamlit run app/demo.py
```
- Mở URL hiển thị trong terminal (mặc định http://localhost:8501).

7) Chạy API server (tuỳ chọn)
```bash
python app/server.py
```

8) Test nhanh (pytest)
```bash
pytest -q
```

Triển khai nâng cao (tuỳ chọn)
- Docker image ứng dụng:
```bash
docker build -t mas-finance:latest .
```
- Minikube/K8s:
```bash
kubectl apply -f k8s/deployment.yaml
minikube service mas-service --url
```

Ghi chú cấu hình
- Biến môi trường (nếu dùng OpenAI/Groq): đặt trong môi trường shell trước khi chạy.
  - `OPENAI_API_KEY`, `GROQ_API_KEY` (tuỳ chọn)
- Kết nối Postgres mặc định: `postgresql+psycopg2://mas_user:mas_pass@localhost:5432/mas_db`

Lộ trình thực thi chi tiết (dành cho người mới)
1. Cài Python môi trường và phụ thuộc bằng `requirements.txt`.
2. `docker-compose up -d` để chạy Postgres với pgvector.
3. `python scripts/init_db.py` tạo schema + extension.
4. Chuẩn bị CSV vào thư mục `data/` như đã nêu.
5. `python scripts/rag_setup.py` để nhúng policy mẫu vào vector store.
6. `streamlit run app/demo.py` để mở giao diện demo, thử câu hỏi về budget/spending.
7. (Tuỳ chọn) `python app/server.py` chạy API.
8. (Tuỳ chọn) Build Docker image và triển khai Minikube.

FAQ nhanh
- Không có OpenAI key? Dùng mặc định HuggingFace embeddings; LLM có thể chuyển sang Ollama.
- Lỗi kết nối DB? Kiểm tra `docker ps`, cổng 5432, và chuỗi kết nối.
- CSV rỗng? Tạo file mẫu vài dòng để kiểm thử và thay sau.

Giấy phép
MIT (có thể thay đổi tuỳ nhu cầu).
