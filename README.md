Multi‑Agent Finance Demo (Windows‑friendly, simple, extensible)

Tổng quan
- Mục tiêu: Demo hệ thống nhiều tác nhân (agents) cho phân tích tài chính, chạy nhẹ trên Windows.
- Kiến trúc tối giản: orchestrator tự viết (không dùng `langgraph`), 3 agents + RAG JSON.

Agents
- Coordinator: định tuyến câu hỏi theo từ khoá, gom kết quả.
- Budget: xuất bảng ngân sách + variance (approved − actual), kèm RAG policy nếu câu hỏi liên quan.
- Spending: tổng hợp subscription theo vendor từ `data/transactions.csv`.
- Alert: phát hiện giao dịch bất thường (z‑score) trên cột `amount`.

Chạy nhanh
1) Yêu cầu
- Python 3.12 (Windows). Nếu dùng RAG embeddings local: `ollama pull nomic-embed-text`.

2) Cài đặt
```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

3) Seed RAG (tuỳ chọn, tạo `rag/simple_index.json`)
```powershell
python scripts\rag_setup.py
```

4) Chạy UI
```powershell
streamlit run app\demo.py
```

5) Chạy API (tuỳ chọn)
```powershell
python app\server.py
```

Ví dụ câu hỏi để test
- Budget:
  - "So sánh budget marketing tháng này?"
  - "Cho tôi bảng ngân sách và variance theo phòng ban"
- Subscription/Spending:
  - "Tổng chi phí subscription theo vendor?"
  - "Vendor nào tốn nhiều nhất?"
- Alert/Risk:
  - "Phát hiện giao dịch bất thường"
  - "Có giao dịch nào vượt ngưỡng bất thường không?"
- RAG (sau khi seed):
  - "Chính sách chi tiêu > 5000 USD cần ai duyệt?"

Thiết kế rút gọn
- Orchestrator: `orchestration/mas_graph.py` cung cấp `app.invoke({messages:[...]})`.
- Budget executor: không dùng `initialize_agent` để tránh deprecation/xung đột.
- RAG: `rag/vectorstore.py` dùng `OllamaEmbeddings` và file `rag/simple_index.json`.
- UI/API: `app/demo.py` (Streamlit), `app/server.py` (FastAPI).

Phát triển thêm
- Có thể thay Budget executor bằng agent ReAct mới của LangChain khi cần.
- Có thể chuyển retriever JSON sang vector DB khi scale.
