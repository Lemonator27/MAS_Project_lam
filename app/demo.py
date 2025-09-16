import streamlit as st
import pandas as pd

from orchestration.mas_graph import app as mas_app


st.title("MAS Finance Demo")
query = st.text_input("Nhập câu hỏi (ví dụ: 'So sánh budget marketing tháng này?')")
if st.button("Run") and query:
    state = mas_app.invoke({"messages": [{"role": "user", "content": query}]})
    out = state.get("result", {})
    st.write(out)
    if isinstance(out.get("output"), list):
        st.dataframe(pd.DataFrame(out["output"]))
