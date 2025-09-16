from agents.budget_agent import budget_agent_executor


def test_budget_agent_runs():
    result = budget_agent_executor.invoke({"input": "Marketing budget?"})
    assert isinstance(result, dict)
