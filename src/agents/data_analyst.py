"""
Data Analyst Agent - Analyzes and synthesizes gathered information
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..skills.analysis_skill import AnalysisSkill
from langchain.prompts import ChatPromptTemplate


class DataAnalyst(BaseAgent):
    """
    Data Analyst Agent

    Responsibilities:
    - Analyze raw search results
    - Extract key insights and patterns
    - Synthesize information from multiple sources
    - Create structured data for content creation
    """

    def __init__(self):
        analysis_skill = AnalysisSkill()

        super().__init__(
            name="Data Analyst",
            role="Information analysis and synthesis specialist",
            skills=[analysis_skill],
            temperature=0.4
        )

        self.analysis_skill = analysis_skill

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze search results and create structured insights

        Args:
            input_data: Must contain 'search_summary' or 'results_text'

        Returns:
            Dictionary with analyzed data
        """
        search_summary = input_data.get('search_summary', '')
        results_text = input_data.get('results_text', [])

        if not search_summary and not results_text:
            return {
                'error': 'No data provided for analysis',
                'analysis': None
            }

        # Synthesize information from multiple sources
        if results_text:
            synthesized = self.analysis_skill.synthesize_information(results_text)
        else:
            synthesized = search_summary

        # Create structured analysis
        structured_analysis = self.analysis_skill.create_structured_analysis(synthesized)

        # Use LLM for deeper analysis
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", """Analyze this research data in depth:

{data}

Provide:
1. Core Insights: The 5-7 most important insights
2. Data Patterns: Key patterns or trends identified
3. Knowledge Gaps: What information might be missing
4. Recommendations: What aspects should the content emphasize

Format your response clearly with headings.""")
        ])

        chain = prompt | self.llm

        response = chain.invoke({
            'data': synthesized[:4000]
        })

        return {
            'structured_analysis': structured_analysis,
            'key_points': structured_analysis.key_points,
            'themes': structured_analysis.themes,
            'deep_analysis': response.content,
            'synthesized_data': synthesized
        }
