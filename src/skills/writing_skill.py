"""
Content Writing Skill - Enables agents to create well-structured content
This skill is inspired by Claude's Agent Skills feature
"""
from typing import Dict, List, Optional
from pydantic import BaseModel


class ContentStructure(BaseModel):
    """Model for structured content output"""
    title: str
    introduction: str
    main_sections: List[Dict[str, str]]
    conclusion: str


class WritingSkill:
    """
    Agent Skill: Content Creation & Writing Capability

    This skill enables agents to create well-structured, engaging content
    based on research and analysis.
    """

    def create_outline(self, topic: str, key_points: List[str]) -> List[str]:
        """
        Create a content outline from key points

        Args:
            topic: Main topic of the content
            key_points: List of key points to cover

        Returns:
            List of section headings
        """
        outline = [
            f"Introduction to {topic}",
            *[f"Key Aspect: {point[:50]}" for point in key_points[:4]],
            "Implications and Future Outlook",
            "Conclusion"
        ]
        return outline

    def format_section(self, heading: str, content: str) -> str:
        """
        Format a content section with proper structure

        Args:
            heading: Section heading
            content: Section content

        Returns:
            Formatted section string
        """
        return f"\n## {heading}\n\n{content}\n"

    def create_introduction(self, topic: str, context: str) -> str:
        """
        Create an engaging introduction

        Args:
            topic: Main topic
            context: Background context

        Returns:
            Introduction text
        """
        intro = f"# {topic}\n\n"
        intro += f"In today's rapidly evolving landscape, understanding {topic.lower()} "
        intro += f"has become increasingly important. {context[:200]}..."
        return intro

    def create_conclusion(self, main_points: List[str]) -> str:
        """
        Create a conclusion summarizing main points

        Args:
            main_points: List of main points to summarize

        Returns:
            Conclusion text
        """
        conclusion = "\n## Conclusion\n\n"
        conclusion += "To summarize, we've explored several key aspects:\n\n"
        for i, point in enumerate(main_points[:3], 1):
            conclusion += f"{i}. {point[:100]}\n"
        conclusion += "\nThese insights provide a comprehensive understanding of the topic."
        return conclusion

    def compile_article(
        self,
        title: str,
        sections: List[Dict[str, str]],
        introduction: Optional[str] = None,
        conclusion: Optional[str] = None
    ) -> str:
        """
        Compile all sections into a complete article

        Args:
            title: Article title
            sections: List of section dictionaries with 'heading' and 'content'
            introduction: Optional introduction text
            conclusion: Optional conclusion text

        Returns:
            Complete article as string
        """
        article = f"# {title}\n\n"

        if introduction:
            article += f"{introduction}\n\n"

        for section in sections:
            article += self.format_section(
                section.get('heading', 'Section'),
                section.get('content', '')
            )

        if conclusion:
            article += f"{conclusion}\n"

        return article

    def apply_polish(self, text: str) -> str:
        """
        Apply final polish to the text

        Args:
            text: Text to polish

        Returns:
            Polished text
        """
        # Remove multiple spaces
        polished = ' '.join(text.split())

        # Ensure proper spacing after periods
        polished = polished.replace('.', '. ').replace('  ', ' ')

        # Ensure proper paragraph spacing
        polished = '\n\n'.join(p.strip() for p in polished.split('\n\n') if p.strip())

        return polished
