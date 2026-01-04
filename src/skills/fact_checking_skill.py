"""
Fact Checking Skill - Enables agents to verify claims and facts
This skill is inspired by Claude's Agent Skills feature
"""
from typing import List, Dict, Optional
from pydantic import BaseModel
from .search_skill import SearchSkill


class FactCheckResult(BaseModel):
    """Model for fact check results"""
    claim: str
    verdict: str  # "Verified", "Disputed", "Unverified"
    confidence: float
    supporting_sources: List[str]


class FactCheckingSkill:
    """
    Agent Skill: Fact Verification & Validation Capability

    This skill enables agents to verify claims by cross-referencing
    with search results and multiple sources.
    """

    def __init__(self, search_skill: Optional[SearchSkill] = None):
        self.search_skill = search_skill or SearchSkill()

    def extract_claims(self, text: str) -> List[str]:
        """
        Extract factual claims from text

        Args:
            text: Input text to analyze

        Returns:
            List of extracted claims
        """
        # Simple sentence-based extraction
        # In production, use NLP to identify factual statements
        sentences = [s.strip() for s in text.split('.') if s.strip()]

        # Filter for sentences that look like claims
        claims = [
            s for s in sentences
            if len(s.split()) > 5 and any(
                keyword in s.lower()
                for keyword in ['is', 'are', 'has', 'have', 'will', 'can']
            )
        ]

        return claims[:5]  # Return top 5 claims

    def verify_claim(self, claim: str) -> FactCheckResult:
        """
        Verify a single claim using search

        Args:
            claim: The claim to verify

        Returns:
            FactCheckResult object
        """
        # Search for the claim
        search_results = self.search_skill.search(claim, num_results=3)

        if not search_results:
            return FactCheckResult(
                claim=claim,
                verdict="Unverified",
                confidence=0.0,
                supporting_sources=[]
            )

        # Analyze search results
        sources = [result.link for result in search_results]
        snippets = [result.snippet.lower() for result in search_results]

        # Simple verification logic
        claim_lower = claim.lower()
        matching_count = sum(
            1 for snippet in snippets
            if any(word in snippet for word in claim_lower.split()[:3])
        )

        confidence = matching_count / len(snippets) if snippets else 0.0

        if confidence >= 0.6:
            verdict = "Verified"
        elif confidence >= 0.3:
            verdict = "Partially Verified"
        else:
            verdict = "Disputed"

        return FactCheckResult(
            claim=claim,
            verdict=verdict,
            confidence=confidence,
            supporting_sources=sources
        )

    def verify_multiple_claims(self, claims: List[str]) -> List[FactCheckResult]:
        """
        Verify multiple claims

        Args:
            claims: List of claims to verify

        Returns:
            List of FactCheckResult objects
        """
        results = []
        for claim in claims:
            result = self.verify_claim(claim)
            results.append(result)

        return results

    def generate_fact_check_report(self, text: str) -> str:
        """
        Generate a complete fact-check report for a piece of text

        Args:
            text: Text to fact-check

        Returns:
            Formatted fact-check report
        """
        claims = self.extract_claims(text)

        if not claims:
            return "No verifiable claims found in the text."

        results = self.verify_multiple_claims(claims)

        report = "# Fact Check Report\n\n"

        for i, result in enumerate(results, 1):
            report += f"## Claim {i}\n"
            report += f"**Statement:** {result.claim}\n\n"
            report += f"**Verdict:** {result.verdict}\n"
            report += f"**Confidence:** {result.confidence:.2%}\n"

            if result.supporting_sources:
                report += f"**Sources:**\n"
                for source in result.supporting_sources:
                    report += f"- {source}\n"

            report += "\n"

        return report
