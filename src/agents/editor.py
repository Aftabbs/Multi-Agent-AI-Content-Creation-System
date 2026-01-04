"""
Editor Agent - Reviews and polishes content for quality
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..skills.editing_skill import EditingSkill
from langchain.prompts import ChatPromptTemplate


class Editor(BaseAgent):
    """
    Editor Agent

    Responsibilities:
    - Review content for quality and clarity
    - Check grammar, style, and structure
    - Improve readability
    - Apply final polish to content
    """

    def __init__(self):
        editing_skill = EditingSkill()

        super().__init__(
            name="Editor",
            role="Content quality assurance and editing specialist",
            skills=[editing_skill],
            temperature=0.5
        )

        self.editing_skill = editing_skill

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review and improve content quality

        Args:
            input_data: Must contain 'content' to edit

        Returns:
            Dictionary with editing results and improved content
        """
        content = input_data.get('content', '')
        fact_check_assessment = input_data.get('fact_check_assessment', '')

        if not content:
            return {
                'error': 'No content provided for editing',
                'final_content': None
            }

        # Check readability
        readability = self.editing_skill.check_readability(content)

        # Check structure
        structure_suggestions = self.editing_skill.check_structure(content)

        # Check clarity
        clarity_suggestions = self.editing_skill.improve_clarity(content)

        # Generate editing report
        editing_report = self.editing_skill.generate_editing_report(content)

        # Use LLM to create the final polished version
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", """Review and improve this content:

{content}

Editing Report:
{editing_report}

Fact-Check Assessment:
{fact_check}

Tasks:
1. Fix any grammatical or structural issues
2. Improve clarity and flow
3. Ensure consistent tone and style
4. Address any fact-checking concerns
5. Polish the final presentation

Provide the complete, improved version of the article. Maintain all the key information while enhancing quality.""")
        ])

        chain = prompt | self.llm

        response = chain.invoke({
            'content': content,
            'editing_report': editing_report[:1000],
            'fact_check': fact_check_assessment[:500] if fact_check_assessment else "No issues found"
        })

        # Apply final polish
        final_content = self.editing_skill.apply_polish(response.content)

        # Calculate improvement metrics
        original_readability = readability['readability_score']
        final_readability = self.editing_skill.check_readability(final_content)

        return {
            'editing_report': editing_report,
            'readability_before': readability,
            'readability_after': final_readability,
            'structure_suggestions': structure_suggestions,
            'clarity_suggestions': clarity_suggestions,
            'final_content': final_content,
            'improvements_made': len(structure_suggestions) + len(clarity_suggestions)
        }
