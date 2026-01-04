"""
Web Search Skill - Enables agents to search the internet using SERPER API
This skill is inspired by Claude's Agent Skills feature
"""
import os
import requests
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """Model for a single search result"""
    title: str
    link: str
    snippet: str


class SearchSkill:
    """
    Agent Skill: Web Search Capability

    This skill enables agents to search the internet and retrieve relevant information.
    It uses the SERPER API for high-quality search results.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError("SERPER_API_KEY not found in environment variables")
        self.base_url = "https://google.serper.dev/search"

    def search(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """
        Perform a web search and return structured results

        Args:
            query: The search query
            num_results: Number of results to return (default: 5)

        Returns:
            List of SearchResult objects
        """
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        payload = {
            'q': query,
            'num': num_results
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            results = []
            if 'organic' in data:
                for item in data['organic'][:num_results]:
                    results.append(SearchResult(
                        title=item.get('title', ''),
                        link=item.get('link', ''),
                        snippet=item.get('snippet', '')
                    ))

            return results
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []

    def search_as_text(self, query: str, num_results: int = 5) -> str:
        """
        Perform a search and return results as formatted text

        Args:
            query: The search query
            num_results: Number of results to return

        Returns:
            Formatted string with search results
        """
        results = self.search(query, num_results)

        if not results:
            return "No results found."

        output = f"Search Results for: '{query}'\n\n"
        for i, result in enumerate(results, 1):
            output += f"{i}. {result.title}\n"
            output += f"   URL: {result.link}\n"
            output += f"   {result.snippet}\n\n"

        return output
