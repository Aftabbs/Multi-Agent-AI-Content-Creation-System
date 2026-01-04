"""
Multi-Agent Orchestrator using LangGraph
Coordinates the workflow between all agents
"""
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import operator

from ..agents.research_coordinator import ResearchCoordinator
from ..agents.web_searcher import WebSearcher
from ..agents.data_analyst import DataAnalyst
from ..agents.content_writer import ContentWriter
from ..agents.fact_checker import FactChecker
from ..agents.editor import Editor


class AgentState(TypedDict):
    """
    State shared between all agents in the workflow
    """
    # Input
    topic: str
    depth: str

    # Research Coordinator outputs
    research_plan: Any
    workflow_summary: str
    search_queries: list

    # Web Searcher outputs
    search_results: list
    search_summary: str

    # Data Analyst outputs
    key_points: list
    themes: list
    deep_analysis: str
    synthesized_data: str

    # Content Writer outputs
    draft_content: str
    outline: list

    # Fact Checker outputs
    fact_check_report: str
    fact_check_assessment: str
    claims_checked: int

    # Editor outputs
    final_content: str
    editing_report: str

    # Workflow control
    current_step: str
    messages: Annotated[list, add_messages]


class MultiAgentOrchestrator:
    """
    Orchestrates the multi-agent research and content creation workflow
    """

    def __init__(self):
        # Initialize all agents
        self.research_coordinator = ResearchCoordinator()
        self.web_searcher = WebSearcher()
        self.data_analyst = DataAnalyst()
        self.content_writer = ContentWriter()
        self.fact_checker = FactChecker()
        self.editor = Editor()

        # Build the workflow graph
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow

        Returns:
            Compiled StateGraph
        """
        # Create the graph
        workflow = StateGraph(AgentState)

        # Add nodes for each agent
        workflow.add_node("coordinate", self._coordinate_research)
        workflow.add_node("search", self._search_web)
        workflow.add_node("analyze", self._analyze_data)
        workflow.add_node("write", self._write_content)
        workflow.add_node("fact_check", self._check_facts)
        workflow.add_node("edit", self._edit_content)

        # Define the workflow edges
        workflow.set_entry_point("coordinate")

        workflow.add_edge("coordinate", "search")
        workflow.add_edge("search", "analyze")
        workflow.add_edge("analyze", "write")
        workflow.add_edge("write", "fact_check")
        workflow.add_edge("fact_check", "edit")
        workflow.add_edge("edit", END)

        # Compile the workflow
        return workflow.compile()

    def _coordinate_research(self, state: AgentState) -> AgentState:
        """
        Research Coordinator node

        Args:
            state: Current workflow state

        Returns:
            Updated state
        """
        print(f"\n{'='*60}")
        print(f"STEP 1: Research Coordination")
        print(f"{'='*60}")

        result = self.research_coordinator.execute({
            'topic': state['topic'],
            'depth': state.get('depth', 'medium')
        })

        state['research_plan'] = result['plan']
        state['workflow_summary'] = result['workflow_summary']
        state['search_queries'] = result['search_queries']
        state['current_step'] = 'coordinate'

        print(f"\n✓ Research plan created")
        print(f"  - Queries to execute: {len(result['search_queries'])}")

        return state

    def _search_web(self, state: AgentState) -> AgentState:
        """
        Web Searcher node

        Args:
            state: Current workflow state

        Returns:
            Updated state
        """
        print(f"\n{'='*60}")
        print(f"STEP 2: Web Search")
        print(f"{'='*60}")

        result = self.web_searcher.execute({
            'search_queries': state['search_queries']
        })

        state['search_results'] = result['raw_results']
        state['search_summary'] = result['summary']
        state['current_step'] = 'search'

        print(f"\n✓ Search completed")
        print(f"  - Total results gathered: {result['total_results']}")

        return state

    def _analyze_data(self, state: AgentState) -> AgentState:
        """
        Data Analyst node

        Args:
            state: Current workflow state

        Returns:
            Updated state
        """
        print(f"\n{'='*60}")
        print(f"STEP 3: Data Analysis")
        print(f"{'='*60}")

        result = self.data_analyst.execute({
            'search_summary': state['search_summary'],
            'results_text': [str(r) for r in state['search_results'][:5]]
        })

        state['key_points'] = result['key_points']
        state['themes'] = result['themes']
        state['deep_analysis'] = result['deep_analysis']
        state['synthesized_data'] = result['synthesized_data']
        state['current_step'] = 'analyze'

        print(f"\n✓ Analysis completed")
        print(f"  - Key points identified: {len(result['key_points'])}")
        print(f"  - Themes found: {', '.join(result['themes'])}")

        return state

    def _write_content(self, state: AgentState) -> AgentState:
        """
        Content Writer node

        Args:
            state: Current workflow state

        Returns:
            Updated state
        """
        print(f"\n{'='*60}")
        print(f"STEP 4: Content Writing")
        print(f"{'='*60}")

        result = self.content_writer.execute({
            'topic': state['topic'],
            'key_points': state['key_points'],
            'deep_analysis': state['deep_analysis'],
            'synthesized_data': state['synthesized_data']
        })

        state['draft_content'] = result['draft_content']
        state['outline'] = result['outline']
        state['current_step'] = 'write'

        print(f"\n✓ Content created")
        print(f"  - Word count: {result['word_count']}")
        print(f"  - Sections: {result['sections_count']}")

        return state

    def _check_facts(self, state: AgentState) -> AgentState:
        """
        Fact Checker node

        Args:
            state: Current workflow state

        Returns:
            Updated state
        """
        print(f"\n{'='*60}")
        print(f"STEP 5: Fact Checking")
        print(f"{'='*60}")

        result = self.fact_checker.execute({
            'content': state['draft_content']
        })

        state['fact_check_report'] = result['fact_check_report']
        state['fact_check_assessment'] = result['llm_assessment']
        state['claims_checked'] = result['claims_checked']
        state['current_step'] = 'fact_check'

        print(f"\n✓ Fact checking completed")
        print(f"  - Claims verified: {result['claims_checked']}")
        print(f"  - Verdict summary: {result['verdict_summary']}")

        return state

    def _edit_content(self, state: AgentState) -> AgentState:
        """
        Editor node

        Args:
            state: Current workflow state

        Returns:
            Updated state
        """
        print(f"\n{'='*60}")
        print(f"STEP 6: Final Editing")
        print(f"{'='*60}")

        result = self.editor.execute({
            'content': state['draft_content'],
            'fact_check_assessment': state['fact_check_assessment']
        })

        state['final_content'] = result['final_content']
        state['editing_report'] = result['editing_report']
        state['current_step'] = 'edit'

        print(f"\n✓ Editing completed")
        print(f"  - Improvements made: {result['improvements_made']}")
        print(f"  - Readability: {result['readability_after']['readability_score']}")

        return state

    def run(self, topic: str, depth: str = "medium") -> Dict[str, Any]:
        """
        Execute the complete multi-agent workflow

        Args:
            topic: Research topic
            depth: Research depth ("shallow", "medium", "deep")

        Returns:
            Final workflow state with all outputs
        """
        print(f"\n{'#'*60}")
        print(f"# Multi-Agent Research & Content Creation System")
        print(f"# Topic: {topic}")
        print(f"# Depth: {depth}")
        print(f"{'#'*60}\n")

        # Initialize state
        initial_state = {
            'topic': topic,
            'depth': depth,
            'messages': [],
            'current_step': 'start'
        }

        # Run the workflow
        final_state = self.workflow.invoke(initial_state)

        print(f"\n{'#'*60}")
        print(f"# Workflow Complete!")
        print(f"{'#'*60}\n")

        return final_state
