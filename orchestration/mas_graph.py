from typing import List, Dict
from agents.coord import route_query


class _SimpleApp:
    """Lightweight drop-in replacement exposing invoke({...}) like langgraph app.

    Expects state: {"messages": [{"role": str, "content": str}, ...]}
    Returns state with {"result": any} merged.
    """

    def invoke(self, state: Dict) -> Dict:
        messages: List[Dict] = state.get("messages", [])
        user_msg = (messages[-1] if messages else {}).get("content", "")
        out = route_query(user_msg)
        new_state = dict(state)
        new_state["result"] = out
        return new_state


app = _SimpleApp()
