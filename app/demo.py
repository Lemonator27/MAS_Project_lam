import os
import sys
import streamlit as st
import pandas as pd
ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(ROOT, os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from orchestration.mas_graph import app as mas_app


st.title("MAS Finance Demo")
st.markdown("### Hệ thống Multi-Agent Finance với Synthetic Data")

# Display available agents
st.markdown("**Các Agent có sẵn:**")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    **💰 Budget Agent**
    - Quản lý ngân sách
    - So sánh approved vs actual
    """)
with col2:
    st.markdown("""
    **💸 Spending Agent**
    - Phân tích chi tiêu
    - Tổng hợp subscription
    """)
with col3:
    st.markdown("""
    **🚨 Alert Agent**
    - Phát hiện giao dịch bất thường
    - Cảnh báo rủi ro
    """)

col4, col5 = st.columns(2)
with col4:
    st.markdown("""
    **💧 Cash Flow Agent**
    - Phân tích dòng tiền
    - Dự báo thanh khoản
    """)
with col5:
    st.markdown("""
    **📄 Invoice Agent**
    - Quản lý hóa đơn
    - Theo dõi thanh toán
    """)

# Example queries
st.markdown("**Ví dụ câu hỏi để test:**")
example_queries = [
    "Phân tích dòng tiền hiện tại",
    "Hóa đơn nào đang quá hạn?",
    "So sánh budget marketing tháng này",
    "Chi tiêu subscription theo vendor",
    "Phát hiện giao dịch bất thường"
]

selected_query = st.selectbox("Hoặc chọn câu hỏi mẫu:", [""] + example_queries)

query = st.text_input("Nhập câu hỏi của bạn:", value=selected_query if selected_query else "")
if st.button("Run") and query:
    state = mas_app.invoke({"messages": [{"role": "user", "content": query}]})
    out = state.get("result", {})
    st.write(out)
    if isinstance(out.get("output"), list):
        st.dataframe(pd.DataFrame(out["output"]))
