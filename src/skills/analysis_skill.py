"""
Data Analysis Skill - Enables agents to analyze and synthesize information
This skill is inspired by Claude's Agent Skills feature
"""
from typing import List, Dict
from pydantic import BaseModel


class AnalyzedData(BaseModel):
    """Model for analyzed data output"""
    key_points: List[str]
    themes: List[str]
    summary: str


class AnalysisSkill:
    """
    Agent Skill: Data Analysis & Synthesis Capability

    This skill enables agents to analyze raw information, extract key points,
    identify themes, and create structured summaries.
    """

    def extract_key_points(self, text: str, max_points: int = 5) -> List[str]:
        """
        Extract key points from text (helper method)
        In a real implementation, this could use NLP techniques

        Args:
            text: Input text to analyze
            max_points: Maximum number of key points

        Returns:
            List of key points
        """
        # Simple implementation - in production, use NLP or LLM
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        return sentences[:max_points]

    def identify_themes(self, text: str) -> List[str]:
        """
        Identify main themes in the text

        Args:
            text: Input text to analyze

        Returns:
            List of identified themes
        """
        # Simple keyword-based theme extraction
        # In production, this would use more sophisticated NLP
        keywords = ['technology', 'business', 'research', 'development',
                   'innovation', 'market', 'customer', 'product']

        text_lower = text.lower()
        themes = [kw for kw in keywords if kw in text_lower]

        return themes if themes else ['general']

    def synthesize_information(self, data_sources: List[str]) -> str:
        """
        Synthesize information from multiple sources

        Args:
            data_sources: List of text data from different sources

        Returns:
            Synthesized summary
        """
        if not data_sources:
            return "No data to synthesize."

        combined = "\n\n".join(data_sources)

        # Create a structured synthesis prompt
        synthesis = f"Combined information from {len(data_sources)} sources:\n\n"
        synthesis += combined[:2000]  # Limit length

        return synthesis

    def create_structured_analysis(self, text: str) -> AnalyzedData:
        """
        Create a complete structured analysis of the text

        Args:
            text: Input text to analyze

        Returns:
            AnalyzedData object with key points, themes, and summary
        """
        key_points = self.extract_key_points(text)
        themes = self.identify_themes(text)

        # Create summary (first 200 chars)
        summary = text[:200] + "..." if len(text) > 200 else text

        return AnalyzedData(
            key_points=key_points,
            themes=themes,
            summary=summary
        )
