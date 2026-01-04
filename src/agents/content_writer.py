"""
Content Writer Agent - Creates well-structured content from research
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..skills.writing_skill import WritingSkill
from langchain.prompts import ChatPromptTemplate


class ContentWriter(BaseAgent):
    """
    Content Writer Agent

    Responsibilities:
    - Create engaging, well-structured content
    - Organize information into coherent articles
    - Apply proper formatting and style
    - Ensure content flows logically
    """

    def __init__(self):
        writing_skill = WritingSkill()

        super().__init__(
            name="Content Writer",
            role="Professional content creation specialist",
            skills=[writing_skill],
            temperature=0.7  # Higher temperature for creative writing
        )

        self.writing_skill = writing_skill

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create content based on analyzed data

        Args:
            input_data: Must contain 'topic', 'key_points', 'deep_analysis'

        Returns:
            Dictionary with created content
        """
        topic = input_data.get('topic', 'Research Topic')
        key_points = input_data.get('key_points', [])
        deep_analysis = input_data.get('deep_analysis', '')
        synthesized_data = input_data.get('synthesized_data', '')

        if not key_points and not deep_analysis:
            return {
                'error': 'Insufficient data for content creation',
                'content': None
            }

        # Create content outline
        outline = self.writing_skill.create_outline(topic, key_points)

        # Use LLM to create the full article
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", """Create a comprehensive, well-written article on: {topic}

Use this research and analysis:
{analysis}

Key points to cover:
{key_points}

Requirements:
- Write an engaging introduction
- Create 3-5 main sections with clear headings
- Use concrete examples and insights from the research
- Include a strong conclusion
- Aim for approximately 800-1000 words
- Use markdown formatting

Write the complete article now.""")
        ])

        chain = prompt | self.llm

        response = chain.invoke({
            'topic': topic,
            'analysis': deep_analysis[:2000],
            'key_points': '\n'.join([f"- {point}" for point in key_points[:5]])
        })

        # Get the generated content
        content = response.content

        # Apply basic formatting polish
        polished_content = self.writing_skill.apply_polish(content)

        return {
            'outline': outline,
            'draft_content': polished_content,
            'word_count': len(polished_content.split()),
            'sections_count': len(outline)
        }
