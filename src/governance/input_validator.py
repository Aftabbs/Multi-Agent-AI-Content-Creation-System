"""
Input Validation Module - Validates and sanitizes user inputs
Prevents injection attacks and malicious inputs
"""
from typing import Tuple, List
from pydantic import BaseModel, validator
import re


class ValidationResult(BaseModel):
    """Model for validation results"""
    is_valid: bool
    sanitized_input: str
    errors: List[str]
    warnings: List[str]


class InputValidator:
    """
    Input Validation Guardrail

    Protects against:
    - Injection attacks
    - Malicious inputs
    - Inappropriate requests
    - System abuse
    """

    def __init__(self):
        # Prohibited input patterns
        self.prohibited_patterns = [
            r"<script",  # XSS attempts
            r"javascript:",  # JavaScript injection
            r"on\w+\s*=",  # Event handler injection
            r"eval\(",  # Code execution
            r"exec\(",  # Code execution
            r"system\(",  # System command
            r"__import__",  # Python imports
            r"\${",  # Template injection
            r"<!--",  # HTML comments (potential injection)
        ]

        # Maximum input lengths
        self.max_lengths = {
            "topic": 500,
            "depth": 20,
            "general": 10000
        }

        # Prohibited topics (illegal/harmful content)
        self.prohibited_topics = [
            "how to make explosives",
            "how to hack",
            "illegal drugs",
            "child exploitation",
            "bioweapons",
            "weapons of mass destruction",
            "terrorism",
            "suicide methods",
            "self-harm techniques"
        ]

    def validate_topic(self, topic: str) -> ValidationResult:
        """
        Validate research topic input

        Args:
            topic: User-provided topic

        Returns:
            ValidationResult with validation status
        """
        errors = []
        warnings = []

        # Check if empty
        if not topic or not topic.strip():
            errors.append("Topic cannot be empty")
            return ValidationResult(
                is_valid=False,
                sanitized_input="",
                errors=errors,
                warnings=warnings
            )

        # Check length
        if len(topic) > self.max_lengths["topic"]:
            errors.append(f"Topic too long (max {self.max_lengths['topic']} characters)")

        # Check for prohibited patterns
        for pattern in self.prohibited_patterns:
            if re.search(pattern, topic, re.IGNORECASE):
                errors.append(f"Prohibited pattern detected: {pattern}")

        # Check for prohibited topics
        topic_lower = topic.lower()
        for prohibited in self.prohibited_topics:
            if prohibited in topic_lower:
                errors.append(f"Prohibited topic: Cannot generate content about {prohibited}")

        # Sanitize input
        sanitized = self._sanitize_text(topic)

        # Check for excessive special characters
        special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\s]', sanitized)) / len(sanitized)
        if special_char_ratio > 0.3:
            warnings.append("Topic contains many special characters")

        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            sanitized_input=sanitized,
            errors=errors,
            warnings=warnings
        )

    def validate_depth(self, depth: str) -> ValidationResult:
        """
        Validate depth parameter

        Args:
            depth: Research depth

        Returns:
            ValidationResult
        """
        errors = []
        warnings = []

        valid_depths = ["shallow", "medium", "deep"]

        if depth not in valid_depths:
            errors.append(f"Invalid depth. Must be one of: {', '.join(valid_depths)}")
            sanitized = "medium"  # Default fallback
        else:
            sanitized = depth

        return ValidationResult(
            is_valid=len(errors) == 0,
            sanitized_input=sanitized,
            errors=errors,
            warnings=warnings
        )

    def _sanitize_text(self, text: str) -> str:
        """
        Sanitize text input

        Args:
            text: Text to sanitize

        Returns:
            Sanitized text
        """
        # Remove null bytes
        sanitized = text.replace('\x00', '')

        # Remove control characters (except newlines and tabs)
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\n\t')

        # Normalize whitespace
        sanitized = ' '.join(sanitized.split())

        # Remove potential HTML/script tags
        sanitized = re.sub(r'<[^>]+>', '', sanitized)

        # Remove potential SQL injection patterns
        sanitized = re.sub(r"([';]|--|\*|/\*|\*/)", '', sanitized)

        # Trim to reasonable length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]

        return sanitized.strip()

    def check_rate_limit(self, user_id: str, requests: int, time_window: int = 3600) -> Tuple[bool, str]:
        """
        Check if user has exceeded rate limits

        Args:
            user_id: User identifier
            requests: Number of requests in time window
            time_window: Time window in seconds (default: 1 hour)

        Returns:
            Tuple of (allowed, message)
        """
        # Simple rate limiting logic
        # In production, use Redis or similar
        max_requests_per_hour = 10

        if requests > max_requests_per_hour:
            return False, f"Rate limit exceeded. Max {max_requests_per_hour} requests per hour."

        return True, "Request allowed"

    def validate_api_usage(self, estimated_cost: float, user_tier: str = "free") -> Tuple[bool, str]:
        """
        Validate API usage against user tier limits

        Args:
            estimated_cost: Estimated cost in USD
            user_tier: User's subscription tier

        Returns:
            Tuple of (allowed, message)
        """
        tier_limits = {
            "free": 0.50,  # $0.50 per request
            "basic": 2.00,
            "pro": 10.00,
            "enterprise": 100.00
        }

        limit = tier_limits.get(user_tier, tier_limits["free"])

        if estimated_cost > limit:
            return False, f"Request exceeds tier limit of ${limit}"

        return True, f"Estimated cost: ${estimated_cost:.2f}"

    def generate_validation_report(self, result: ValidationResult) -> str:
        """
        Generate validation report

        Args:
            result: ValidationResult object

        Returns:
            Formatted report
        """
        report = "# Input Validation Report\n\n"

        if result.is_valid:
            report += "✅ **Status**: Valid\n\n"
        else:
            report += "❌ **Status**: Invalid\n\n"

        if result.errors:
            report += "## Errors\n\n"
            for error in result.errors:
                report += f"- ❌ {error}\n"
            report += "\n"

        if result.warnings:
            report += "## Warnings\n\n"
            for warning in result.warnings:
                report += f"- ⚠️ {warning}\n"
            report += "\n"

        if result.sanitized_input:
            report += f"## Sanitized Input\n\n```\n{result.sanitized_input}\n```\n"

        return report
