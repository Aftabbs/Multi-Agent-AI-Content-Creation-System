"""
Governance Orchestrator - Coordinates all AI governance guardrails
Implements comprehensive Responsible AI framework
"""
from typing import Dict, Any, Tuple
from .content_safety import ContentSafetyGuardrail
from .input_validator import InputValidator
from .bias_detector import BiasDetector
from .transparency import TransparencyLog


class GovernanceOrchestrator:
    """
    Central Governance System

    Coordinates all AI governance components:
    - Content Safety
    - Input Validation
    - Bias Detection
    - Transparency & Explainability
    """

    def __init__(self, enable_all: bool = True):
        """
        Initialize governance system

        Args:
            enable_all: Enable all guardrails (default: True)
        """
        self.content_safety = ContentSafetyGuardrail() if enable_all else None
        self.input_validator = InputValidator() if enable_all else None
        self.bias_detector = BiasDetector() if enable_all else None
        self.transparency_log = TransparencyLog() if enable_all else None

        self.governance_config = {
            "content_safety_enabled": enable_all,
            "input_validation_enabled": enable_all,
            "bias_detection_enabled": enable_all,
            "transparency_enabled": enable_all,
            "strict_mode": False  # If True, blocks content with any violations
        }

    def validate_input(self, topic: str, depth: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate user inputs before processing

        Args:
            topic: Research topic
            depth: Research depth

        Returns:
            Tuple of (is_valid, validation_results)
        """
        results = {
            "topic_validation": None,
            "depth_validation": None,
            "overall_valid": False
        }

        if not self.input_validator:
            results["overall_valid"] = True
            return True, results

        # Validate topic
        topic_result = self.input_validator.validate_topic(topic)
        results["topic_validation"] = topic_result

        # Validate depth
        depth_result = self.input_validator.validate_depth(depth)
        results["depth_validation"] = depth_result

        # Overall validation
        results["overall_valid"] = topic_result.is_valid and depth_result.is_valid

        return results["overall_valid"], results

    def check_content_safety(self, content: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Check content for safety violations

        Args:
            content: Content to check

        Returns:
            Tuple of (is_safe, safety_results)
        """
        results = {
            "is_safe": True,
            "violations": [],
            "sanitized_content": content,
            "report": ""
        }

        if not self.content_safety:
            return True, results

        # Check for violations
        is_safe, violations = self.content_safety.check_content(content)
        results["is_safe"] = is_safe
        results["violations"] = violations

        # Sanitize content
        sanitized = self.content_safety.sanitize_content(content)
        results["sanitized_content"] = sanitized

        # Generate report
        results["report"] = self.content_safety.generate_safety_report(violations)

        return is_safe, results

    def detect_bias(self, content: str) -> Dict[str, Any]:
        """
        Detect bias in content

        Args:
            content: Content to analyze

        Returns:
            Bias detection results
        """
        results = {
            "detections": [],
            "metrics": {},
            "mitigated_content": content,
            "report": ""
        }

        if not self.bias_detector:
            return results

        # Detect bias
        detections = self.bias_detector.detect_bias(content)
        results["detections"] = detections

        # Check representation
        metrics = self.bias_detector.check_representation(content)
        results["metrics"] = metrics

        # Attempt mitigation
        mitigated = self.bias_detector.mitigate_bias(content, detections)
        results["mitigated_content"] = mitigated

        # Generate report
        results["report"] = self.bias_detector.generate_bias_report(detections, metrics)

        return results

    def log_agent_decision(
        self,
        agent_name: str,
        input_data: Any,
        output_data: Any,
        reasoning: str,
        confidence: float = 0.8
    ):
        """
        Log agent decision for transparency

        Args:
            agent_name: Name of the agent
            input_data: Input received
            output_data: Output produced
            reasoning: Explanation
            confidence: Confidence score
        """
        if self.transparency_log:
            self.transparency_log.log_decision(
                agent_name=agent_name,
                input_data=input_data,
                output_data=output_data,
                reasoning=reasoning,
                confidence=confidence
            )

    def finalize_content(self, content: str, topic: str) -> str:
        """
        Apply final governance checks and add disclaimers

        Args:
            content: Generated content
            topic: Original topic

        Returns:
            Finalized content with all governance additions
        """
        finalized = content

        # Add AI disclaimer
        if self.content_safety:
            finalized = self.content_safety.add_content_disclaimer(finalized, topic)

        return finalized

    def generate_comprehensive_report(self) -> str:
        """
        Generate comprehensive governance report

        Returns:
            Complete governance report
        """
        report = "# AI Governance & Responsible AI Report\n\n"

        report += "## System Configuration\n\n"
        for key, value in self.governance_config.items():
            status = "✅ Enabled" if value else "❌ Disabled"
            report += f"- **{key.replace('_', ' ').title()}**: {status}\n"

        report += "\n---\n\n"

        # Transparency report
        if self.transparency_log:
            report += self.transparency_log.generate_transparency_report()
            report += "\n---\n\n"
            report += self.transparency_log.generate_source_attribution()
            report += "\n---\n\n"
            report += self.transparency_log.explain_workflow()

        return report

    def get_governance_metrics(self) -> Dict[str, Any]:
        """
        Get governance metrics

        Returns:
            Dictionary of metrics
        """
        metrics = {
            "governance_enabled": self.governance_config,
            "confidence_metrics": {},
            "safety_status": "enabled" if self.content_safety else "disabled",
            "bias_detection_status": "enabled" if self.bias_detector else "disabled"
        }

        if self.transparency_log:
            metrics["confidence_metrics"] = self.transparency_log.get_confidence_metrics()

        return metrics

    def create_governance_summary(self) -> Dict[str, Any]:
        """
        Create governance summary for user display

        Returns:
            Summary dictionary
        """
        return {
            "status": "✅ Governance Active",
            "guardrails": {
                "Content Safety": "enabled" if self.content_safety else "disabled",
                "Input Validation": "enabled" if self.input_validator else "disabled",
                "Bias Detection": "enabled" if self.bias_detector else "disabled",
                "Transparency": "enabled" if self.transparency_log else "disabled"
            },
            "responsible_ai_features": [
                "Automated content safety checks",
                "Input sanitization and validation",
                "Bias detection and mitigation",
                "Full transparency and audit trails",
                "Source attribution",
                "AI-generated content disclaimers"
            ]
        }
