"""
Transparency & Explainability Module
Provides transparency about AI system decisions and processes
"""
from typing import Dict, List, Any
from datetime import datetime
from pydantic import BaseModel


class AgentDecision(BaseModel):
    """Model for tracking agent decisions"""
    agent_name: str
    timestamp: str
    input_summary: str
    output_summary: str
    reasoning: str
    confidence: float
    sources_used: List[str]


class TransparencyLog:
    """
    Transparency & Explainability Guardrail

    Provides:
    - Decision tracking
    - Source attribution
    - Process transparency
    - Audit trails
    """

    def __init__(self):
        self.decisions: List[AgentDecision] = []
        self.metadata = {
            "system_version": "1.0.0",
            "model_used": "groq/mixtral-8x7b",
            "start_time": datetime.now().isoformat()
        }

    def log_decision(
        self,
        agent_name: str,
        input_data: Any,
        output_data: Any,
        reasoning: str,
        confidence: float,
        sources: List[str] = None
    ):
        """
        Log an agent decision for transparency

        Args:
            agent_name: Name of the agent
            input_data: Input received
            output_data: Output produced
            reasoning: Explanation of decision
            confidence: Confidence score (0-1)
            sources: List of sources used
        """
        decision = AgentDecision(
            agent_name=agent_name,
            timestamp=datetime.now().isoformat(),
            input_summary=str(input_data)[:200],
            output_summary=str(output_data)[:200],
            reasoning=reasoning,
            confidence=confidence,
            sources_used=sources or []
        )

        self.decisions.append(decision)

    def generate_transparency_report(self) -> str:
        """
        Generate comprehensive transparency report

        Returns:
            Formatted transparency report
        """
        report = "# AI System Transparency Report\n\n"

        report += "## System Information\n\n"
        report += f"- **System Version**: {self.metadata['system_version']}\n"
        report += f"- **Model**: {self.metadata['model_used']}\n"
        report += f"- **Session Start**: {self.metadata['start_time']}\n"
        report += f"- **Total Decisions**: {len(self.decisions)}\n\n"

        report += "## Agent Decision Trail\n\n"

        for i, decision in enumerate(self.decisions, 1):
            report += f"### {i}. {decision.agent_name}\n\n"
            report += f"- **Time**: {decision.timestamp}\n"
            report += f"- **Confidence**: {decision.confidence:.0%}\n"
            report += f"- **Reasoning**: {decision.reasoning}\n"

            if decision.sources_used:
                report += f"- **Sources Used**: {len(decision.sources_used)}\n"
                for source in decision.sources_used[:3]:  # Show top 3
                    report += f"  - {source}\n"

            report += "\n"

        return report

    def generate_source_attribution(self) -> str:
        """
        Generate source attribution report

        Returns:
            Formatted source attribution
        """
        report = "# Source Attribution\n\n"

        all_sources = []
        for decision in self.decisions:
            all_sources.extend(decision.sources_used)

        # Remove duplicates while preserving order
        unique_sources = list(dict.fromkeys(all_sources))

        if not unique_sources:
            report += "No external sources used.\n"
        else:
            report += f"This content was generated using information from {len(unique_sources)} sources:\n\n"

            for i, source in enumerate(unique_sources, 1):
                report += f"{i}. {source}\n"

            report += "\n## Citation Note\n\n"
            report += "All sources were accessed via web search and fact-checking processes. "
            report += "Users should independently verify information from original sources.\n"

        return report

    def get_confidence_metrics(self) -> Dict[str, float]:
        """
        Get confidence metrics across all decisions

        Returns:
            Dictionary of confidence metrics
        """
        if not self.decisions:
            return {
                "average_confidence": 0.0,
                "min_confidence": 0.0,
                "max_confidence": 0.0
            }

        confidences = [d.confidence for d in self.decisions]

        return {
            "average_confidence": sum(confidences) / len(confidences),
            "min_confidence": min(confidences),
            "max_confidence": max(confidences),
            "total_decisions": len(confidences)
        }

    def explain_workflow(self) -> str:
        """
        Explain the AI workflow to users

        Returns:
            Human-readable workflow explanation
        """
        explanation = """# How This Content Was Created

## Multi-Agent AI System

This content was generated by a multi-agent AI system, where specialized agents work together:

### 1. Research Coordinator Agent
- **Role**: Plans the research strategy
- **Process**: Analyzes the topic and creates search queries
- **Skill**: Strategic Planning

### 2. Web Search Agent
- **Role**: Gathers information from the internet
- **Process**: Executes searches using SERPER API (Google Search)
- **Skill**: Information Retrieval

### 3. Data Analyst Agent
- **Role**: Analyzes and synthesizes information
- **Process**: Extracts key insights and identifies themes
- **Skill**: Data Analysis

### 4. Content Writer Agent
- **Role**: Creates the article
- **Process**: Structures information into coherent content
- **Skill**: Content Creation

### 5. Fact Checker Agent
- **Role**: Verifies claims
- **Process**: Cross-references facts with additional searches
- **Skill**: Fact Verification

### 6. Editor Agent
- **Role**: Improves quality
- **Process**: Reviews readability, structure, and polish
- **Skill**: Quality Assurance

## Transparency Principles

✅ **Source Attribution**: All sources are documented
✅ **Decision Logging**: Every agent decision is recorded
✅ **Confidence Scores**: Each decision has a confidence level
✅ **Human Oversight**: Content should be reviewed by humans
✅ **Bias Detection**: Automated bias checking is performed

## Limitations

⚠️ AI-generated content may:
- Contain inaccuracies or outdated information
- Reflect biases in training data
- Lack nuance on complex topics
- Require human fact-checking

**Always verify important information from authoritative sources.**
"""
        return explanation

    def generate_audit_log(self) -> Dict[str, Any]:
        """
        Generate machine-readable audit log

        Returns:
            Audit log as dictionary
        """
        return {
            "metadata": self.metadata,
            "decisions": [d.dict() for d in self.decisions],
            "metrics": self.get_confidence_metrics(),
            "timestamp": datetime.now().isoformat()
        }
