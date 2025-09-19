from typing import Dict, Any

from agents.budget_agent import budget_agent_executor
from agents.spending_agent import summarize_subscriptions
from agents.alert_agent import detect_anomalies
from agents.cashflow_agent import cashflow_agent_executor
from agents.invoice_agent import invoice_agent_executor


def route_query(query: str) -> Dict[str, Any]:
    q = (query or "").lower()

    # Cash Flow Agent
    if any(keyword in q for keyword in ["cash flow", "dòng tiền", "cashflow", "liquidity", "thanh khoản"]):
        result = cashflow_agent_executor.invoke({"input": query})
        return {"type": "cashflow", "output": result.get("output", str(result))}

    # Invoice Management Agent
    if any(keyword in q for keyword in ["invoice", "hóa đơn", "bill", "payment", "thanh toán", "overdue"]):
        result = invoice_agent_executor.invoke({"input": query})
        return {"type": "invoice", "output": result.get("output", str(result))}

    # Budget Agent
    if "budget" in q or "ngân sách" in q:
        result = budget_agent_executor.invoke({"input": query})
        return {"type": "budget", "output": result.get("output", str(result))}

    # Spending/Subscription Agent
    if "subscription" in q or "saas" in q or "spending" in q or "chi tiêu" in q:
        df = summarize_subscriptions()
        return {"type": "spending", "output": df.to_dict(orient="records")}

    # Alert/Risk Agent
    if any(keyword in q for keyword in ["alert", "anomaly", "risk", "bất thường", "cảnh báo"]):
        df = detect_anomalies()
        return {"type": "alert", "output": df.head(20).to_dict(orient="records")}

    # Default to budget agent
    result = budget_agent_executor.invoke({"input": query})
    return {"type": "budget", "output": result.get("output", str(result))}


