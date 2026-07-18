"""
Shared state object passed between all LangGraph nodes.

Every agent reads from and writes to this single structure - this is
what makes the pipeline debuggable and testable node-by-node, rather
than a black box of chained function calls.
"""
from typing import TypedDict, Literal


class SourceResult(TypedDict):
    title: str
    url: str
    snippet: str
    source_type: Literal["web", "paper"]


class ResearchState(TypedDict):
    # Input
    question: str

    # Raw agent outputs (filled by search_agent / paper_agent nodes)
    search_results: list[SourceResult]
    paper_results: list[SourceResult]

    # Derived (filled by aggregate / analysis / synthesis nodes)
    analysis: str
    sources: list[SourceResult]        # deduped, used for citations
    final_report: str

    # Control flow (used by the supervisor's routing decisions)
    next_step: Literal["search", "analyze", "synthesize", "end"]
    iteration_count: int
    max_iterations: int

    # Observability - every node should append here on failure, not raise
    errors: list[str]