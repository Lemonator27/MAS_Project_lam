from typing import Dict, Any, Callable
from agents.budget_agent import budget_agent_executor
from agents.spending_agent import summarize_subscriptions
from agents.alert_agent import detect_anomalies
from agents.cashflow_agent import cashflow_agent_executor
from agents.invoice_agent import invoice_agent_executor
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
import os
from dotenv import load_dotenv

load_dotenv()

def wrap_agent_executor(agent_executor):
    """Wrap LangChain AgentExecutor to return dict with 'response' key."""
    def wrapped(query: str) -> Dict[str, Any]:
        try:
            result = agent_executor.run(query)
            return {"response": result}
        except Exception as e:
            return {"response": f"Error in agent: {str(e)}"}
    return wrapped

def wrap_function_agent(func: Callable) -> Callable:
    """Wrap simple functions to match expected signature."""
    def wrapped(query: str) -> Dict[str, Any]:
        try:
            result = func(query)
            # Ensure result is a dict with 'response'
            if isinstance(result, dict):
                return result
            else:
                return {"response": str(result)}
        except Exception as e:
            return {"response": f"Error in agent: {str(e)}"}
    return wrapped

class AgentRouter:
    def __init__(self):
        # Ensure all agents are wrapped to return Dict[str, Any]
        self.agents: Dict[str, Callable[[str], Dict[str, Any]]] = {
            "budget": wrap_agent_executor(budget_agent_executor),
            "spending": wrap_function_agent(summarize_subscriptions),
            "anomalies": wrap_function_agent(detect_anomalies),
            "cashflow": wrap_agent_executor(cashflow_agent_executor),
            "invoice": wrap_agent_executor(invoice_agent_executor)
        }

        self.prompt_template = """
    You are a precise financial query router. Your **only** job is to classify the user's query into one of the predefined agent categories below.

**Available agents:**
- `budget`: Questions about creating, reviewing, adjusting, or analyzing budgets, allocations, or financial plans.
- `spending`: Requests about recurring expenses, subscription summaries, expense categorization, or spending trends.
- `anomalies`: Queries about detecting unusual transactions, outliers, fraud indicators, or unexpected financial activity.
- `cashflow`: Inquiries about cash inflows/outflows, liquidity forecasts, cash position, runway, or short-term financial health.
- `invoice`: Tasks involving invoice creation, status checks, payment tracking, due dates, or invoice data extraction.

**Instructions:**
1. Read the user query carefully.
2. Choose **exactly one** agent that best matches the primary intent.
3. If the query is unrelated to finance or none of the agents apply, choose `none`.
4. Respond with **only** the agent name in lowercase (e.g., `cashflow`, `none`).  
   → Do **not** add explanations, punctuation, or extra text.

User Query: {query}
    """

        self.prompt = PromptTemplate(input_variables=["query"], template=self.prompt_template)
        self.llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))
        agent = create_react_agent(self.llm, tool_names=list(self.agents.keys()), verbose=False)
        agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)
        

    def route(self, query: str) -> Dict[str, Any]:
        prompt_text = self.prompt.format(query=query)
        response = self.agent_executor.invoke({"input":prompt_text}).strip().lower()
        return response

# Convenience function
def route_query(query: str) -> Dict[str, Any]:
    router = AgentRouter()
    return router.route(query)