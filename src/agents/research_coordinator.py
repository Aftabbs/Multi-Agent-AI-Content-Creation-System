"""
Research Coordinator Agent - Plans and coordinates the research workflow
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..skills.planning_skill import PlanningSkill
from langchain.prompts import ChatPromptTemplate


class ResearchCoordinator(BaseAgent):
    """
    Research Coordinator Agent

    Responsibilities:
    - Create comprehensive research plans
    - Generate effective search queries
    - Coordinate the overall workflow
    """

    def __init__(self):
        planning_skill = PlanningSkill()

        super().__init__(
            name="Research Coordinator",
            role="Strategic planning and workflow coordination",
            skills=[planning_skill],
            temperature=0.3  # Lower temperature for more focused planning
        )

        self.planning_skill = planning_skill

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a research plan for the given topic

        Args:
            input_data: Must contain 'topic' and optionally 'depth'

        Returns:
            Dictionary with research plan
        """
        topic = input_data.get('topic', '')
        depth = input_data.get('depth', 'medium')

        if not topic:
            return {
                'error': 'No topic provided',
                'plan': None
            }

        # Create research plan using planning skill
        plan = self.planning_skill.create_research_plan(topic, depth)

        # Use LLM to enhance the plan
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", """Create an enhanced research strategy for the topic: {topic}

The initial plan includes:
- Objectives: {objectives}
- Search Queries: {queries}

Please provide:
1. Any additional important search queries
2. Key aspects to focus on
3. Potential challenges to be aware of

Be concise and strategic.""")
        ])

        chain = prompt | self.llm

        response = chain.invoke({
            'topic': topic,
            'objectives': ', '.join(plan.objectives),
            'queries': ', '.join(plan.search_queries)
        })

        # Generate workflow summary
        workflow_summary = self.planning_skill.create_workflow_summary(plan)

        return {
            'plan': plan,
            'workflow_summary': workflow_summary,
            'llm_enhancement': response.content,
            'search_queries': plan.search_queries
        }
