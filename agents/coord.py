from typing import Dict, Any

from agents.budget_agent import budget_agent_executor
from agents.spending_agent import summarize_subscriptions
from agents.alert_agent import detect_anomalies


def route_query(query: str) -> Dict[str, Any]:
    q = (query or "").lower()

    if "budget" in q:
        result = budget_agent_executor.invoke({"input": query})
        return {"type": "budget", "output": result.get("output", str(result))}

    if "subscription" in q or "saas" in q:
        df = summarize_subscriptions()
        return {"type": "spending", "output": df.to_dict(orient="records")}

    if ("alert" in q) or ("anomaly" in q) or ("risk" in q):
        df = detect_anomalies()
        return {"type": "alert", "output": df.head(20).to_dict(orient="records")}

    # default
    result = budget_agent_executor.invoke({"input": query})
    return {"type": "budget", "output": result.get("output", str(result))}


