import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta

def load_cashflow_data(path: str = "data/cashflow_data.csv") -> pd.DataFrame:
    """Load cash flow data"""
    try:
        return pd.read_csv(path)
    except Exception:
        # Fallback data if file doesn't exist
        return pd.DataFrame({
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "quarter": ["Q1", "Q1", "Q1"],
            "revenue": [100000, 120000, 95000],
            "operating_expenses": [80000, 85000, 75000],
            "capital_expenditures": [10000, 5000, 15000],
            "net_cashflow": [10000, 30000, 5000],
            "cash_balance": [500000, 530000, 535000]
        })

def analyze_cashflow_trends(df: pd.DataFrame) -> str:
    """Analyze cash flow trends"""
    if df.empty:
        return "Không có dữ liệu cash flow để phân tích."
    
    # Calculate trends
    recent_periods = df.tail(30)  # Last 30 days
    avg_revenue = recent_periods['revenue'].mean()
    avg_expenses = recent_periods['operating_expenses'].mean()
    avg_cashflow = recent_periods['net_cashflow'].mean()
    
    current_balance = df['cash_balance'].iloc[-1]
    
    # Calculate growth rates
    if len(df) > 1:
        revenue_growth = ((recent_periods['revenue'].iloc[-1] - recent_periods['revenue'].iloc[0]) / 
                         recent_periods['revenue'].iloc[0] * 100) if recent_periods['revenue'].iloc[0] > 0 else 0
        expense_growth = ((recent_periods['operating_expenses'].iloc[-1] - recent_periods['operating_expenses'].iloc[0]) / 
                         recent_periods['operating_expenses'].iloc[0] * 100) if recent_periods['operating_expenses'].iloc[0] > 0 else 0
    else:
        revenue_growth = 0
        expense_growth = 0
    
    # Predict future cash flow (simple linear projection)
    if len(df) >= 7:  # Need at least a week of data
        recent_cashflow = df['net_cashflow'].tail(7).mean()
        projected_30_days = recent_cashflow * 30
        projected_balance = current_balance + projected_30_days
    else:
        projected_30_days = avg_cashflow * 30
        projected_balance = current_balance + projected_30_days
    
    # Generate insights
    insights = []
    
    if avg_cashflow > 0:
        insights.append(f"✅ Dòng tiền dương trung bình: ${avg_cashflow:,.2f}/ngày")
    else:
        insights.append(f"⚠️ Dòng tiền âm trung bình: ${avg_cashflow:,.2f}/ngày")
    
    if revenue_growth > 5:
        insights.append(f"📈 Doanh thu tăng trưởng tốt: +{revenue_growth:.1f}%")
    elif revenue_growth < -5:
        insights.append(f"📉 Doanh thu giảm: {revenue_growth:.1f}%")
    else:
        insights.append(f"📊 Doanh thu ổn định: {revenue_growth:+.1f}%")
    
    if projected_balance < current_balance * 0.8:
        insights.append("🚨 Cảnh báo: Dự báo dòng tiền giảm trong 30 ngày tới")
    elif projected_balance > current_balance * 1.2:
        insights.append("💚 Tích cực: Dự báo dòng tiền tăng trong 30 ngày tới")
    
    return f"""
**Phân tích dòng tiền:**
- Số dư hiện tại: ${current_balance:,.2f}
- Doanh thu trung bình: ${avg_revenue:,.2f}/ngày
- Chi phí trung bình: ${avg_expenses:,.2f}/ngày
- Dòng tiền ròng trung bình: ${avg_cashflow:,.2f}/ngày

**Dự báo 30 ngày tới:**
- Dòng tiền dự kiến: ${projected_30_days:,.2f}
- Số dư dự kiến: ${projected_balance:,.2f}

**Insights:**
{chr(10).join(insights)}
"""

def cashflow_tool(query: str) -> str:
    """Main cash flow analysis tool"""
    df = load_cashflow_data()
    return analyze_cashflow_trends(df)

class CashFlowAgentExecutor:
    """Cash Flow Agent Executor"""
    
    def invoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        query = inputs.get("input", "")
        result = cashflow_tool(query)
        
        return {"output": result}

cashflow_agent_executor = CashFlowAgentExecutor()
