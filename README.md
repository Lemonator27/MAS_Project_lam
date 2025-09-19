Multi‑Agent Finance Demo (Windows‑friendly, simple, extensible)

Tổng quan
- Mục tiêu: Demo hệ thống nhiều tác nhân (agents) cho phân tích tài chính, chạy nhẹ trên Windows.
- Kiến trúc tối giản: orchestrator tự viết (không dùng `langgraph`), 5 agents + RAG JSON.
- Dữ liệu: Sử dụng synthetic data realistic để demo và test các agents.

Agents
- Coordinator: định tuyến câu hỏi theo từ khoá, gom kết quả từ các agents khác.
- Budget: xuất bảng ngân sách + variance (approved − actual), kèm RAG policy nếu câu hỏi liên quan.
- Spending: tổng hợp subscription theo vendor từ synthetic transaction data.
- Alert: phát hiện giao dịch bất thường (z‑score) trên cột `amount`.
- Cash Flow: phân tích dòng tiền, dự báo thanh khoản và xu hướng.
- Invoice: quản lý hóa đơn, theo dõi thanh toán và phát hiện quá hạn.

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

3) Generate Synthetic Data & Seed RAG
```powershell
python scripts\generate_synthetic_data.py
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
- Cash Flow:
  - "Phân tích dòng tiền hiện tại"
  - "Dự báo cash flow 30 ngày tới"
- Invoice Management:
  - "Hóa đơn nào đang quá hạn?"
  - "Tình trạng thanh toán hóa đơn"
- RAG (sau khi seed):
  - "Chính sách chi tiêu > 5000 USD cần ai duyệt?"
  - "Quy định travel policy như thế nào?"

Thiết kế rút gọn
- Orchestrator: `orchestration/mas_graph.py` cung cấp `app.invoke({messages:[...]})`.
- 5 Agents: Budget, Spending, Alert, Cash Flow, Invoice - mỗi agent có executor riêng.
- RAG: `rag/vectorstore.py` dùng `OllamaEmbeddings` và file `rag/simple_index.json`.
- Synthetic Data: 100 mẫu cho mỗi loại data (budget, transaction, cashflow, invoice, policies).
- UI/API: `app/demo.py` (Streamlit), `app/server.py` (FastAPI).

Dữ liệu
- `data/budgets_extended.csv`: 100 ngân sách phòng ban/dự án
- `data/transactions_extended.csv`: 100 giao dịch với patterns bất thường
- `data/cashflow_data.csv`: 100 ngày dữ liệu dòng tiền
- `data/invoices_data.csv`: 100 hóa đơn với payment tracking
- `data/rag_documents.json`: 100 policy documents cho RAG
