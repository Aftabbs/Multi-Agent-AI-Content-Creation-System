"""
Planning & Coordination Skill - Enables agents to plan and coordinate research
This skill is inspired by Claude's Agent Skills feature
"""
from typing import List, Dict
from pydantic import BaseModel


class ResearchPlan(BaseModel):
    """Model for research plan"""
    topic: str
    objectives: List[str]
    search_queries: List[str]
    required_steps: List[str]


class PlanningSkill:
    """
    Agent Skill: Planning & Coordination Capability

    This skill enables agents to create research plans,
    coordinate workflows, and manage multi-step processes.
    """

    def create_research_plan(self, topic: str, depth: str = "medium") -> ResearchPlan:
        """
        Create a structured research plan for a topic

        Args:
            topic: The research topic
            depth: Research depth ("shallow", "medium", "deep")

        Returns:
            ResearchPlan object
        """
        # Define objectives based on depth
        objectives_map = {
            "shallow": [
                f"Understand the basics of {topic}",
                "Identify key concepts and definitions"
            ],
            "medium": [
                f"Understand the fundamentals of {topic}",
                "Explore current trends and developments",
                "Identify key players and experts",
                "Understand practical applications"
            ],
            "deep": [
                f"Comprehensive analysis of {topic}",
                "Historical context and evolution",
                "Current state and trends",
                "Future implications and predictions",
                "Critical analysis and expert opinions"
            ]
        }

        objectives = objectives_map.get(depth, objectives_map["medium"])

        # Generate search queries
        search_queries = self.generate_search_queries(topic, depth)

        # Define required steps
        required_steps = [
            "Execute web searches for each query",
            "Analyze and synthesize gathered information",
            "Create structured content draft",
            "Verify facts and claims",
            "Review and polish final content"
        ]

        return ResearchPlan(
            topic=topic,
            objectives=objectives,
            search_queries=search_queries,
            required_steps=required_steps
        )

    def generate_search_queries(self, topic: str, depth: str = "medium") -> List[str]:
        """
        Generate effective search queries for the topic

        Args:
            topic: The research topic
            depth: Research depth

        Returns:
            List of search queries
        """
        base_queries = [
            f"{topic} overview",
            f"what is {topic}",
            f"{topic} latest trends 2024"
        ]

        medium_queries = [
            f"{topic} applications",
            f"{topic} benefits and challenges",
            f"{topic} expert insights"
        ]

        deep_queries = [
            f"{topic} history and evolution",
            f"{topic} future predictions",
            f"{topic} research papers",
            f"{topic} industry analysis"
        ]

        if depth == "shallow":
            return base_queries[:2]
        elif depth == "medium":
            return base_queries + medium_queries[:2]
        else:  # deep
            return base_queries + medium_queries + deep_queries

    def prioritize_tasks(self, tasks: List[str]) -> List[Dict[str, any]]:
        """
        Prioritize and structure tasks

        Args:
            tasks: List of tasks

        Returns:
            List of prioritized task dictionaries
        """
        priorities = {
            'search': 1,
            'analyze': 2,
            'write': 3,
            'verify': 4,
            'edit': 5
        }

        prioritized = []
        for task in tasks:
            task_lower = task.lower()
            priority = 3  # default medium priority

            for key, val in priorities.items():
                if key in task_lower:
                    priority = val
                    break

            prioritized.append({
                'task': task,
                'priority': priority,
                'status': 'pending'
            })

        return sorted(prioritized, key=lambda x: x['priority'])

    def create_workflow_summary(self, plan: ResearchPlan) -> str:
        """
        Create a human-readable workflow summary

        Args:
            plan: ResearchPlan object

        Returns:
            Formatted workflow summary
        """
        summary = f"# Research Workflow for: {plan.topic}\n\n"

        summary += "## Objectives\n"
        for i, obj in enumerate(plan.objectives, 1):
            summary += f"{i}. {obj}\n"

        summary += "\n## Search Strategy\n"
        summary += "The following queries will be executed:\n"
        for i, query in enumerate(plan.search_queries, 1):
            summary += f"{i}. \"{query}\"\n"

        summary += "\n## Execution Steps\n"
        for i, step in enumerate(plan.required_steps, 1):
            summary += f"{i}. {step}\n"

        return summary
