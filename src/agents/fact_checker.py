"""
Fact Checker Agent - Verifies claims and ensures accuracy
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..skills.fact_checking_skill import FactCheckingSkill
from ..skills.search_skill import SearchSkill
from langchain.prompts import ChatPromptTemplate


class FactChecker(BaseAgent):
    """
    Fact Checker Agent

    Responsibilities:
    - Extract verifiable claims from content
    - Verify facts using web searches
    - Identify potential inaccuracies
    - Provide confidence scores for claims
    """

    def __init__(self):
        search_skill = SearchSkill()
        fact_checking_skill = FactCheckingSkill(search_skill)

        super().__init__(
            name="Fact Checker",
            role="Fact verification and accuracy specialist",
            skills=[fact_checking_skill, search_skill],
            temperature=0.2  # Very low temperature for factual accuracy
        )

        self.fact_checking_skill = fact_checking_skill
        self.search_skill = search_skill

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify facts in the provided content

        Args:
            input_data: Must contain 'content' to fact-check

        Returns:
            Dictionary with fact-check results
        """
        content = input_data.get('content', '')

        if not content:
            return {
                'error': 'No content provided for fact-checking',
                'report': None
            }

        # Extract claims using the skill
        claims = self.fact_checking_skill.extract_claims(content)

        # Verify claims
        verification_results = self.fact_checking_skill.verify_multiple_claims(claims)

        # Generate fact-check report
        report = self.fact_checking_skill.generate_fact_check_report(content)

        # Use LLM to provide additional context and recommendations
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", """Review this fact-check report:

{report}

Content being checked:
{content}

Provide:
1. Overall Assessment: How accurate is the content?
2. Critical Issues: Any claims that need immediate attention
3. Recommendations: Suggested corrections or clarifications
4. Confidence Score: Rate the overall factual accuracy (0-100%)

Be precise and cite specific concerns.""")
        ])

        chain = prompt | self.llm

        response = chain.invoke({
            'report': report,
            'content': content[:2000]
        })

        # Count verification results by verdict
        verdict_counts = {}
        for result in verification_results:
            verdict_counts[result.verdict] = verdict_counts.get(result.verdict, 0) + 1

        return {
            'claims_checked': len(claims),
            'verification_results': verification_results,
            'verdict_summary': verdict_counts,
            'fact_check_report': report,
            'llm_assessment': response.content
        }
