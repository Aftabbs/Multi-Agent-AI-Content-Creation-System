"""
Web Search Agent - Performs internet searches to gather information
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..skills.search_skill import SearchSkill
from langchain.prompts import ChatPromptTemplate


class WebSearcher(BaseAgent):
    """
    Web Search Agent

    Responsibilities:
    - Execute web searches using SERPER API
    - Gather relevant information from multiple sources
    - Organize and present search results
    """

    def __init__(self):
        search_skill = SearchSkill()

        super().__init__(
            name="Web Search Agent",
            role="Information retrieval and web search specialist",
            skills=[search_skill],
            temperature=0.2  # Low temperature for factual search
        )

        self.search_skill = search_skill

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute searches for given queries

        Args:
            input_data: Must contain 'search_queries' (list of strings)

        Returns:
            Dictionary with search results
        """
        queries = input_data.get('search_queries', [])

        if not queries:
            return {
                'error': 'No search queries provided',
                'results': []
            }

        # Execute all searches
        all_results = []
        raw_results_text = []

        for query in queries:
            results = self.search_skill.search(query, num_results=3)
            all_results.extend(results)

            # Create text summary of results
            results_text = self.search_skill.search_as_text(query, num_results=3)
            raw_results_text.append(results_text)

        # Use LLM to summarize and organize findings
        combined_results = "\n\n".join(raw_results_text)

        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", """Review these search results and create a structured summary:

{results}

Provide:
1. Key findings (top 5-7 most important points)
2. Common themes across sources
3. Notable sources and their main contributions

Be concise and focus on the most relevant information.""")
        ])

        chain = prompt | self.llm

        response = chain.invoke({
            'results': combined_results[:4000]  # Limit to avoid token limits
        })

        return {
            'raw_results': all_results,
            'results_text': raw_results_text,
            'summary': response.content,
            'total_results': len(all_results)
        }
