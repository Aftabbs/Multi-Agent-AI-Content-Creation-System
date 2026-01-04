"""
Bias Detection Module - Detects and mitigates bias in AI-generated content
Implements Fairness and Responsible AI principles
"""
from typing import Dict, List
from pydantic import BaseModel
import re


class BiasDetection(BaseModel):
    """Model for bias detection results"""
    bias_type: str
    confidence: float
    description: str
    flagged_text: str
    suggestion: str


class BiasDetector:
    """
    Bias Detection Guardrail

    Detects various types of bias:
    - Gender bias
    - Racial/ethnic bias
    - Age bias
    - Disability bias
    - Cultural bias
    - Socioeconomic bias
    """

    def __init__(self):
        # Biased language patterns
        self.bias_patterns = {
            "gender": {
                "patterns": [
                    r"\b(he|him|his)\b(?!.*\b(she|her|they)\b)",  # Male-only pronouns
                    r"\bmankind\b",
                    r"\bmanpower\b",
                    r"\bfreshman\b",
                    r"\bchairman\b",
                    r"\bsalesman\b"
                ],
                "alternatives": {
                    "mankind": "humanity",
                    "manpower": "workforce",
                    "freshman": "first-year student",
                    "chairman": "chairperson",
                    "salesman": "salesperson"
                }
            },
            "age": {
                "patterns": [
                    r"\b(elderly|old people|aged)\b",
                    r"\byoung people are\b",
                    r"\bmillennials are\b"
                ],
                "alternatives": {
                    "elderly": "older adults",
                    "old people": "older adults",
                    "aged": "older"
                }
            },
            "disability": {
                "patterns": [
                    r"\b(handicapped|crippled|suffering from)\b",
                    r"\bwheelchair-bound\b",
                    r"\bafflicted with\b"
                ],
                "alternatives": {
                    "handicapped": "person with a disability",
                    "wheelchair-bound": "wheelchair user",
                    "suffering from": "living with"
                }
            },
            "socioeconomic": {
                "patterns": [
                    r"\b(poor people are|rich people are)\b",
                    r"\blow-income\s+\w+\s+are\b"
                ],
                "alternatives": {}
            }
        }

        # Stereotypical associations
        self.stereotypes = [
            r"\bwomen are\s+(emotional|nurturing|weak)\b",
            r"\bmen are\s+(aggressive|strong|logical)\b",
            r"\basians are\s+(good at|smart)\b",
            r"\bmuslims are\s+",
            r"\b(all|most)\s+\w+\s+people\s+are\b"
        ]

    def detect_bias(self, content: str) -> List[BiasDetection]:
        """
        Detect bias in content

        Args:
            content: Content to analyze

        Returns:
            List of BiasDetection objects
        """
        detections = []

        # Check for biased language
        for bias_type, data in self.bias_patterns.items():
            for pattern in data["patterns"]:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    flagged = match.group()
                    suggestion = data["alternatives"].get(
                        flagged.lower(),
                        "Consider using more inclusive language"
                    )

                    detections.append(BiasDetection(
                        bias_type=bias_type,
                        confidence=0.8,
                        description=f"{bias_type.capitalize()} bias detected",
                        flagged_text=flagged,
                        suggestion=suggestion
                    ))

        # Check for stereotypes
        for pattern in self.stereotypes:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                detections.append(BiasDetection(
                    bias_type="stereotype",
                    confidence=0.9,
                    description="Stereotypical statement detected",
                    flagged_text=match.group(),
                    suggestion="Avoid generalizations about groups of people"
                ))

        return detections

    def check_representation(self, content: str) -> Dict[str, any]:
        """
        Check for balanced representation in content

        Args:
            content: Content to analyze

        Returns:
            Dictionary with representation metrics
        """
        metrics = {
            "male_pronouns": len(re.findall(r"\b(he|him|his)\b", content, re.IGNORECASE)),
            "female_pronouns": len(re.findall(r"\b(she|her|hers)\b", content, re.IGNORECASE)),
            "neutral_pronouns": len(re.findall(r"\b(they|them|their)\b", content, re.IGNORECASE)),
            "person_first_language": len(re.findall(r"\bperson with\b", content, re.IGNORECASE)),
            "balance_score": 0.0
        }

        # Calculate balance score
        total_pronouns = sum([
            metrics["male_pronouns"],
            metrics["female_pronouns"],
            metrics["neutral_pronouns"]
        ])

        if total_pronouns > 0:
            # Ideal is balanced or neutral
            neutral_ratio = metrics["neutral_pronouns"] / total_pronouns
            gender_diff = abs(metrics["male_pronouns"] - metrics["female_pronouns"]) / total_pronouns

            # Higher score is better
            metrics["balance_score"] = (neutral_ratio * 0.7) + ((1 - gender_diff) * 0.3)

        return metrics

    def mitigate_bias(self, content: str, detections: List[BiasDetection]) -> str:
        """
        Attempt to automatically mitigate detected bias

        Args:
            content: Original content
            detections: List of bias detections

        Returns:
            Mitigated content
        """
        mitigated = content

        # Apply suggested replacements
        for detection in detections:
            if detection.suggestion and " " not in detection.suggestion:
                # Simple word replacement
                mitigated = re.sub(
                    r'\b' + re.escape(detection.flagged_text) + r'\b',
                    detection.suggestion,
                    mitigated,
                    flags=re.IGNORECASE
                )

        return mitigated

    def generate_bias_report(self, detections: List[BiasDetection], metrics: Dict) -> str:
        """
        Generate bias detection report

        Args:
            detections: List of bias detections
            metrics: Representation metrics

        Returns:
            Formatted report
        """
        report = "# Bias Detection Report\n\n"

        if not detections:
            report += "✅ No significant bias detected.\n\n"
        else:
            report += f"⚠️ Found {len(detections)} potential bias issues.\n\n"

            # Group by type
            by_type = {}
            for d in detections:
                if d.bias_type not in by_type:
                    by_type[d.bias_type] = []
                by_type[d.bias_type].append(d)

            for bias_type, items in by_type.items():
                report += f"## {bias_type.capitalize()} Bias\n\n"
                for item in items:
                    report += f"- **Flagged**: `{item.flagged_text}`\n"
                    report += f"  - **Suggestion**: {item.suggestion}\n"
                    report += f"  - **Confidence**: {item.confidence:.0%}\n\n"

        # Add representation metrics
        report += "## Representation Analysis\n\n"
        report += f"- Male pronouns: {metrics['male_pronouns']}\n"
        report += f"- Female pronouns: {metrics['female_pronouns']}\n"
        report += f"- Neutral pronouns: {metrics['neutral_pronouns']}\n"
        report += f"- Balance score: {metrics['balance_score']:.2f} (0-1, higher is better)\n\n"

        if metrics['balance_score'] < 0.5:
            report += "⚠️ **Recommendation**: Consider using more inclusive language and balanced representation.\n"
        else:
            report += "✅ **Good**: Content shows balanced representation.\n"

        return report

    def get_inclusive_language_suggestions(self) -> Dict[str, str]:
        """
        Get dictionary of inclusive language suggestions

        Returns:
            Dictionary mapping biased terms to inclusive alternatives
        """
        suggestions = {}

        for bias_type, data in self.bias_patterns.items():
            suggestions.update(data["alternatives"])

        # Additional suggestions
        suggestions.update({
            "guys": "everyone / folks / team",
            "manmade": "artificial / synthetic",
            "blacklist": "blocklist",
            "whitelist": "allowlist",
            "master/slave": "primary/replica",
            "crazy": "surprising / unexpected",
            "insane": "remarkable / extraordinary",
            "lame": "disappointing / inadequate"
        })

        return suggestions
