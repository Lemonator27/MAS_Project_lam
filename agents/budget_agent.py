from typing import Any, Dict

import pandas as pd
from langchain.agents import AgentExecutor, Tool
from langchain_openai import OpenAI
from langchain_community.llms import Ollama

from rag.vectorstore import get_retriever


def load_budgets(path: str = "data/budgets.csv") -> pd.DataFrame:
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
        df.assign(variance=df["approved_amount"] - df["actual_spent"])  # noqa: W503
        .to_string(index=False)
    )
    return f"Budget summary (variance = approved - actual):\n{summary}"


def rag_tool(query: str) -> str:
    docs = get_retriever().get_relevant_documents(query)
    return "\n".join(d.page_content for d in docs)


def build_budget_agent() -> AgentExecutor:
    # Prefer local Ollama if available; fallback to OpenAI if env key exists
    try:
        llm = Ollama(model="llama3")
    except Exception:
        llm = OpenAI()  # requires OPENAI_API_KEY

    tools = [
        Tool(name="budget_table", func=simple_budget_tool, description="Show budget table and variance"),
        Tool(name="rag_retrieve", func=rag_tool, description="Retrieve finance policy via RAG"),
    ]

    from langchain.agents import initialize_agent

    agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


budget_agent_executor = build_budget_agent()
