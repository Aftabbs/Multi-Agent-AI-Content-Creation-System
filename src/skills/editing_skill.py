"""
Editing Skill - Enables agents to review and improve content quality
This skill is inspired by Claude's Agent Skills feature
"""
from typing import List, Dict
from pydantic import BaseModel


class EditingSuggestion(BaseModel):
    """Model for editing suggestions"""
    issue_type: str
    location: str
    suggestion: str


class EditingSkill:
    """
    Agent Skill: Editing & Quality Assurance Capability

    This skill enables agents to review content for quality,
    clarity, grammar, and structure.
    """

    def check_readability(self, text: str) -> Dict[str, any]:
        """
        Check text readability metrics

        Args:
            text: Text to analyze

        Returns:
            Dictionary with readability metrics
        """
        words = text.split()
        sentences = [s for s in text.split('.') if s.strip()]

        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0

        return {
            'total_words': len(words),
            'total_sentences': len(sentences),
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'readability_score': 'Good' if avg_sentence_length < 20 else 'Needs Improvement'
        }

    def check_structure(self, text: str) -> List[EditingSuggestion]:
        """
        Check content structure and organization

        Args:
            text: Text to analyze

        Returns:
            List of structural suggestions
        """
        suggestions = []

        # Check for headings
        if '##' not in text and '#' not in text:
            suggestions.append(EditingSuggestion(
                issue_type="Structure",
                location="Document",
                suggestion="Consider adding section headings for better organization"
            ))

        # Check for introduction
        lines = text.split('\n')
        if len(lines) > 0 and len(lines[0]) < 50:
            suggestions.append(EditingSuggestion(
                issue_type="Structure",
                location="Introduction",
                suggestion="Consider adding a more comprehensive introduction"
            ))

        # Check paragraph length
        paragraphs = text.split('\n\n')
        long_paragraphs = [p for p in paragraphs if len(p.split()) > 150]

        if long_paragraphs:
            suggestions.append(EditingSuggestion(
                issue_type="Structure",
                location="Paragraphs",
                suggestion=f"Found {len(long_paragraphs)} paragraphs that may be too long. Consider breaking them up."
            ))

        return suggestions

    def improve_clarity(self, text: str) -> List[EditingSuggestion]:
        """
        Identify areas where clarity can be improved

        Args:
            text: Text to analyze

        Returns:
            List of clarity suggestions
        """
        suggestions = []

        # Check for passive voice indicators
        passive_indicators = ['was', 'were', 'been', 'being']
        text_lower = text.lower()

        passive_count = sum(text_lower.count(word) for word in passive_indicators)

        if passive_count > len(text.split()) * 0.05:
            suggestions.append(EditingSuggestion(
                issue_type="Clarity",
                location="Voice",
                suggestion="Consider using more active voice to improve clarity"
            ))

        # Check for jargon
        jargon_words = ['utilize', 'leverage', 'synergy', 'paradigm']
        found_jargon = [word for word in jargon_words if word in text_lower]

        if found_jargon:
            suggestions.append(EditingSuggestion(
                issue_type="Clarity",
                location="Word Choice",
                suggestion=f"Consider simplifying terms: {', '.join(found_jargon)}"
            ))

        return suggestions

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
        polished = '\n\n'.join(p.strip() for p in polished.split('\n\n'))

        return polished

    def generate_editing_report(self, text: str) -> str:
        """
        Generate a comprehensive editing report

        Args:
            text: Text to review

        Returns:
            Formatted editing report
        """
        readability = self.check_readability(text)
        structure_suggestions = self.check_structure(text)
        clarity_suggestions = self.improve_clarity(text)

        report = "# Content Review Report\n\n"

        report += "## Readability Metrics\n"
        for key, value in readability.items():
            report += f"- **{key.replace('_', ' ').title()}:** {value}\n"

        report += "\n## Suggestions for Improvement\n\n"

        all_suggestions = structure_suggestions + clarity_suggestions

        if all_suggestions:
            for i, suggestion in enumerate(all_suggestions, 1):
                report += f"{i}. **{suggestion.issue_type}** ({suggestion.location})\n"
                report += f"   {suggestion.suggestion}\n\n"
        else:
            report += "No major issues found. Content quality is good!\n"

        return report
