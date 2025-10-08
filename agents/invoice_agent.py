import pandas as pd
from typing import Dict, Any
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import os
from dotenv import load_dotenv

# Make sure to load your environment variables
load_dotenv()

# --- Data Loading and Analysis Functions (largely unchanged) ---

def load_invoice_data(path: str = "data/invoices_data.csv") -> pd.DataFrame:
    """Load invoice data from a CSV file."""
    try:
        df = pd.read_csv(path)
        df['invoice_date'] = pd.to_datetime(df['invoice_date'])
        df['due_date'] = pd.to_datetime(df['due_date'])
        return df
    except FileNotFoundError:
        # Fallback data if the file doesn't exist
        print("CSV file not found. Using fallback data.")
        return pd.DataFrame({
            "invoice_id": ["INV_001", "INV_002", "INV_003"],
            "vendor": ["Vendor A", "Vendor B", "Vendor A"],
            "amount": [1500.75, 2500.00, 850.50],
            "status": ["pending", "paid", "overdue"],
            "is_overdue": [False, False, True],
            "payment_terms": ["Net 30", "Net 60", "Net 30"],
            "invoice_date": [pd.to_datetime("2025-09-15"), pd.to_datetime("2025-09-20"), pd.to_datetime("2025-08-10")],
            "due_date": [pd.to_datetime("2025-10-15"), pd.to_datetime("2025-11-19"), pd.to_datetime("2025-09-09")]
        })

@tool
def analyze_all_invoices(query: str) -> str:
    """
    Analyzes the entire invoice dataset and provides a comprehensive summary.
    Use this tool when the user asks for a general overview, a report, or a full analysis of invoices.
    The 'query' argument is not used to filter data but is required by the agent.
    """
    df = load_invoice_data()
    if df.empty:
        return "Không có dữ liệu hóa đơn để phân tích."
    
    # --- Analysis logic (same as your original code) ---
    total_invoices = len(df)
    pending_invoices = df[df['status'].isin(['pending', 'overdue'])].shape[0]
    paid_invoices = df[df['status'] == 'paid'].shape[0]
    overdue_invoices = df[df['is_overdue'] == True].shape[0]
    
    total_amount = df['amount'].sum()
    pending_amount = df[df['status'].isin(['pending', 'overdue'])]['amount'].sum()
    paid_amount = df[df['status'] == 'paid']['amount'].sum()
    overdue_amount = df[df['is_overdue'] == True]['amount'].sum()
    
    vendor_summary = df.groupby('vendor').agg(
        total_amount=('amount', 'sum'),
        invoice_count=('invoice_id', 'count')
    ).sort_values('total_amount', ascending=False).round(2)
    
    payment_terms_analysis = df['payment_terms'].value_counts()
    
    insights = []
    if overdue_invoices > 0:
        insights.append(f"🚨 Có {overdue_invoices} hóa đơn đã quá hạn với tổng giá trị là {overdue_amount:,.2f} USD. Cần hành động ngay.")
    if pending_amount > total_amount * 0.5:
        insights.append(f"⚠️ Hơn 50% tổng giá trị hóa đơn ({pending_amount/total_amount:.1%}) đang chờ thanh toán.")

    return f"""
**Báo cáo tổng quan về hóa đơn:**

**Thống kê chính:**
- **Tổng số hóa đơn:** {total_invoices}
- **Đã thanh toán:** {paid_invoices} (Tổng: {paid_amount:,.2f} USD)
- **Chưa thanh toán:** {pending_invoices} (Tổng: {pending_amount:,.2f} USD)
- **Quá hạn:** {overdue_invoices} (Tổng: {overdue_amount:,.2f} USD)

**Top nhà cung cấp theo giá trị:**
{vendor_summary.head().to_string()}

**Phân tích điều khoản thanh toán:**
{payment_terms_analysis.to_string()}

**Thông tin chi tiết quan trọng:**
{''.join(f'- {i}\n' for i in insights) if insights else "✅ Mọi thứ đều ổn."}
"""
llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))

tools = [analyze_all_invoices]
prompt_template = """
You are an expert financial assistant specializing in invoice management, responding in Vietnamese.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question in Vietnamese.

Begin!

Question: {input}
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(prompt_template)

# 4. Create the ReAct Agent
agent = create_react_agent(llm, tools, prompt)

# 5. Create the Agent Executor
invoice_agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
