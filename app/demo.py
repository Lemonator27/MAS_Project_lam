import os
import sys
import streamlit as st
import pandas as pd
import warnings

try:
    from langchain_core._api.deprecation import LangChainDeprecationWarning
    warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
except Exception:
    pass

# Ensure project root on PYTHONPATH when running via Streamlit
ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(ROOT, os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from orchestration.mas_graph import app as mas_app


st.title("MAS Finance Demo")
query = st.text_input("Nhập câu hỏi (ví dụ: 'So sánh budget marketing tháng này?')")
if st.button("Run") and query:
    state = mas_app.invoke({"messages": [{"role": "user", "content": query}]})
    out = state.get("result", {})
    st.write(out)
    if isinstance(out.get("output"), list):
        st.dataframe(pd.DataFrame(out["output"]))
