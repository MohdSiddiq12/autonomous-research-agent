"""
LangGraph skeleton for the Autonomous Research Agent.

Milestone 2: nodes are stubs that just pass state through - real logic
gets filled in at Milestones 4-9. The point right now is to confirm the
graph topology (fan-out to Search + Paper agents, fan-in, conditional
loop back to supervisor, synthesis) compiles and routes correctly
before any AWS calls are wired in.

Run directly to smoke-test: python graph/graph.py
"""
from langgraph.graph import StateGraph, END
from graph.state import ResearchState


def supervisor_node(state: ResearchState) -> ResearchState:
    # Milestone 8: real routing logic goes here (Bedrock call)
    print(f"[supervisor] iteration {state['iteration_count']}")
    return state


def search_agent_node(state: ResearchState) -> ResearchState:
    # Milestone 4: invokes the search Lambda function via boto3
    print("[search_agent] stub - no Lambda call yet")
    return {**state, "search_results": []}


def paper_agent_node(state: ResearchState) -> ResearchState:
    # Milestone 5: invokes the paper Lambda function via boto3
    print("[paper_agent] stub - no Lambda call yet")
    return {**state, "paper_results": []}


def aggregate_node(state: ResearchState) -> ResearchState:
    # Milestone 6: merges search_results + paper_results into sources
    combined = state["search_results"] + state["paper_results"]
    return {**state, "sources": combined}


def analysis_node(state: ResearchState) -> ResearchState:
    # Milestone 7: Bedrock call to extract/rank findings
    print("[analysis] stub - no LLM call yet")
    return {**state, "analysis": ""}


def synthesis_node(state: ResearchState) -> ResearchState:
    # Milestone 9: Bedrock call to write the final cited report
    print("[synthesis] stub - no LLM call yet")
    return {**state, "final_report": ""}


def route_after_analysis(state: ResearchState) -> str:
    """Milestone 8: real 'enough evidence?' decision goes here."""
    if state["iteration_count"] >= state["max_iterations"]:
        return "synthesize"
    return "synthesize"  # stub always proceeds for now


def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("search_agent", search_agent_node)
    graph.add_node("paper_agent", paper_agent_node)
    graph.add_node("aggregate", aggregate_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("synthesis", synthesis_node)

    graph.set_entry_point("supervisor")

    # Fan-out: supervisor dispatches to both specialist agents in parallel
    graph.add_edge("supervisor", "search_agent")
    graph.add_edge("supervisor", "paper_agent")

    # Fan-in: both agents feed the same aggregation node
    graph.add_edge("search_agent", "aggregate")
    graph.add_edge("paper_agent", "aggregate")

    graph.add_edge("aggregate", "analysis")

    # Conditional edge: loop back to supervisor, or proceed to synthesis
    graph.add_conditional_edges(
        "analysis",
        route_after_analysis,
        {"supervisor": "supervisor", "synthesize": "synthesis"},
    )

    graph.add_edge("synthesis", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({
        "question": "test question",
        "search_results": [],
        "paper_results": [],
        "analysis": "",
        "sources": [],
        "final_report": "",
        "next_step": "search",
        "iteration_count": 0,
        "max_iterations": 3,
        "errors": [],
    })
    print(result)