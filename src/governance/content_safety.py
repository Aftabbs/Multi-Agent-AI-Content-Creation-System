"""
Content Safety Module - Ensures generated content meets safety standards
Implements Responsible AI principles
"""
from typing import Dict, List, Tuple
from pydantic import BaseModel
import re


class SafetyViolation(BaseModel):
    """Model for safety violations"""
    category: str
    severity: str  # "low", "medium", "high", "critical"
    description: str
    flagged_content: str


class ContentSafetyGuardrail:
    """
    Content Safety Guardrail

    Implements responsible AI by:
    - Detecting harmful content
    - Preventing misinformation
    - Ensuring ethical standards
    - Protecting user safety
    """

    def __init__(self):
        # Prohibited content patterns
        self.prohibited_patterns = {
            "violence": [
                r"\b(kill|murder|assault|weapon|bomb|terrorist)\b",
                r"\b(violence|violent|attack|harm)\b"
            ],
            "hate_speech": [
                r"\b(hate|discriminat(e|ion)|racist|sexist)\b",
                r"\b(offensive|slur|derogatory)\b"
            ],
            "sexual_content": [
                r"\b(explicit|pornographic|sexual abuse)\b",
                r"\b(nsfw|adult content)\b"
            ],
            "personal_info": [
                r"\b\d{3}-\d{2}-\d{4}\b",  # SSN pattern
                r"\b\d{16}\b",  # Credit card pattern
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"  # Email
            ],
            "medical_advice": [
                r"\b(diagnose|treatment|cure|medication)\s+(for|of)\b",
                r"\b(take|use|consume)\s+\d+\s*(mg|ml|pills)\b"
            ],
            "financial_advice": [
                r"\b(invest in|buy|sell)\s+(stock|crypto|bitcoin)\b",
                r"\b(guaranteed|risk-free)\s+(profit|return)\b"
            ],
            "legal_advice": [
                r"\b(you should|must)\s+(sue|file|claim)\b",
                r"\b(legal advice|lawyer|attorney)\b"
            ]
        }

        # Warning patterns (less severe)
        self.warning_patterns = {
            "unverified_claims": [
                r"\b(definitely|certainly|absolutely)\s+(will|can|does)\b",
                r"\b(proven|scientific fact)\b"
            ],
            "conspiracy": [
                r"\b(conspiracy|cover-up|secret agenda)\b",
                r"\b(mainstream media|fake news)\b"
            ]
        }

    def check_content(self, content: str) -> Tuple[bool, List[SafetyViolation]]:
        """
        Check content for safety violations

        Args:
            content: Content to check

        Returns:
            Tuple of (is_safe, list of violations)
        """
        violations = []

        # Check prohibited content
        for category, patterns in self.prohibited_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    violations.append(SafetyViolation(
                        category=category,
                        severity="high",
                        description=f"Detected {category.replace('_', ' ')} content",
                        flagged_content=match.group()
                    ))

        # Check warning patterns
        for category, patterns in self.warning_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    violations.append(SafetyViolation(
                        category=category,
                        severity="medium",
                        description=f"Potential {category.replace('_', ' ')}",
                        flagged_content=match.group()
                    ))

        # Content is safe if no high/critical violations
        critical_violations = [v for v in violations if v.severity in ["high", "critical"]]
        is_safe = len(critical_violations) == 0

        return is_safe, violations

    def sanitize_content(self, content: str) -> str:
        """
        Remove or redact sensitive information

        Args:
            content: Content to sanitize

        Returns:
            Sanitized content
        """
        sanitized = content

        # Redact SSN patterns
        sanitized = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED-SSN]', sanitized)

        # Redact credit card patterns
        sanitized = re.sub(r'\b\d{16}\b', '[REDACTED-CC]', sanitized)

        # Redact email addresses (keep domain for context)
        sanitized = re.sub(
            r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b',
            r'[EMAIL]@\1',
            sanitized
        )

        # Redact phone numbers
        sanitized = re.sub(
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            '[REDACTED-PHONE]',
            sanitized
        )

        return sanitized

    def generate_safety_report(self, violations: List[SafetyViolation]) -> str:
        """
        Generate a human-readable safety report

        Args:
            violations: List of safety violations

        Returns:
            Formatted safety report
        """
        if not violations:
            return "✅ No safety violations detected."

        report = "# Content Safety Report\n\n"

        # Group by severity
        by_severity = {}
        for v in violations:
            if v.severity not in by_severity:
                by_severity[v.severity] = []
            by_severity[v.severity].append(v)

        for severity in ["critical", "high", "medium", "low"]:
            if severity in by_severity:
                report += f"\n## {severity.upper()} Severity Issues\n\n"
                for v in by_severity[severity]:
                    report += f"- **{v.category}**: {v.description}\n"
                    report += f"  - Flagged: `{v.flagged_content}`\n"

        return report

    def add_content_disclaimer(self, content: str, topic: str) -> str:
        """
        Add responsible AI disclaimer to content

        Args:
            content: Original content
            topic: Topic of the content

        Returns:
            Content with disclaimer
        """
        disclaimer = f"""
---

## ⚠️ AI-Generated Content Disclaimer

This article about "{topic}" was generated by an AI multi-agent system.

**Important Notes:**
- **Verify Information**: This content is for informational purposes only. Always verify facts from authoritative sources.
- **Not Professional Advice**: This is not medical, legal, financial, or professional advice. Consult qualified professionals for specific guidance.
- **Fact-Checking**: While automated fact-checking was performed, human verification is recommended.
- **Bias Awareness**: AI systems may reflect biases present in training data. Use critical thinking.
- **Time-Sensitive**: Information may become outdated. Check publication date and verify current relevance.

**Generated By**: Multi-Agent AI System
**Technology**: LangChain, LangGraph, Groq LLM
**Generation Date**: {self._get_timestamp()}

---
"""
        return content + disclaimer

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
