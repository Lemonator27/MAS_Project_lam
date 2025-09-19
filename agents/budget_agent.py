from typing import Any, Dict

import pandas as pd

from rag.vectorstore import get_retriever


def load_budgets(path: str = "data/budgets_extended.csv") -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame(
            {
                "dept": ["Marketing", "Sales"],
                "project_id": [1, 2],
                "approved_amount": [60000.0, 40000.0],
                "actual_spent": [50000.0, 25000.0],
            }
        )


def simple_budget_tool(_: str) -> str:
    df = load_budgets()
    summary = (
        df.assign(variance=df["approved_amount"] - df["actual_spent"])
        .to_string(index=False)
    )
    return f"Budget summary (variance = approved - actual):\n{summary}"


def rag_tool(query: str) -> str:
    docs = get_retriever().get_relevant_documents(query)
    return "\n".join(d.page_content for d in docs)


class BudgetAgentExecutor:
    """Lightweight executor to avoid LangChain Agent deprecations and incompatibilities.

    Exposes invoke({"input": str}) -> {"output": str}
    """

    def invoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        query = (inputs.get("input") or "").lower()
        outputs: list[str] = []

        if any(k in query for k in ["policy", "quy định", "gaap", "travel", "rag"]):
            rag = rag_tool(query)
            if rag:
                outputs.append(f"RAG:\n{rag}")

        outputs.append(simple_budget_tool(query))

        return {"output": "\n\n".join(outputs)}


budget_agent_executor = BudgetAgentExecutor()
