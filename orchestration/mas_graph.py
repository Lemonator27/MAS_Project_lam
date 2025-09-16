from typing import TypedDict, Annotated, List, Dict
import operator

from langgraph.graph import StateGraph, END

from agents.coordinator_agent import route_query


class AgentState(TypedDict):
    messages: Annotated[List[Dict], operator.add]
    result: Dict


def coordinator_node(state: AgentState) -> AgentState:
    user_msg = state["messages"][-1]["content"]
    out = route_query(user_msg)
    state["result"] = out
    return state


graph = StateGraph(AgentState)
graph.add_node("coordinator", coordinator_node)
graph.set_entry_point("coordinator")
graph.add_edge("coordinator", END)

app = graph.compile()
