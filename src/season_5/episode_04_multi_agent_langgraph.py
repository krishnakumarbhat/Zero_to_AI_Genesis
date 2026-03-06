from typing import TypedDict

from langgraph.graph import END, StateGraph


class AgentState(TypedDict):
    task: str
    draft_code: str
    review: str
    final_output: str


def manager_node(state: AgentState) -> AgentState:
    task = state["task"]
    plan = f"Manager delegates coding + review for task: {task}"
    return {**state, "final_output": plan}


def coder_node(state: AgentState) -> AgentState:
    task = state["task"]
    code = f"def solve_task():\n    return 'Solved: {task}'"
    return {**state, "draft_code": code}


def reviewer_node(state: AgentState) -> AgentState:
    review = "Code is syntactically valid and task-aligned."
    final = f"{state['final_output']}\n\nDraft:\n{state['draft_code']}\n\nReview:\n{review}"
    return {**state, "review": review, "final_output": final}


def main():
    graph = StateGraph(AgentState)
    graph.add_node("manager", manager_node)
    graph.add_node("coder", coder_node)
    graph.add_node("reviewer", reviewer_node)

    graph.set_entry_point("manager")
    graph.add_edge("manager", "coder")
    graph.add_edge("coder", "reviewer")
    graph.add_edge("reviewer", END)

    app = graph.compile()
    result = app.invoke(
        {
            "task": "Build shipping calculator",
            "draft_code": "",
            "review": "",
            "final_output": "",
        }
    )

    print("\nSeason 1 / Ep 04 - Level 4 Multi-Agent LangGraph")
    print(result["final_output"])


if __name__ == "__main__":
    main()
