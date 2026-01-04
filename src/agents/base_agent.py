"""
Base Agent Class - Foundation for all specialized agents
"""
from typing import Dict, Any, Optional
from langchain_groq import ChatGroq
import os


class BaseAgent:
    """
    Base class for all agents in the multi-agent system.
    Each agent has a specific role and set of skills.
    """

    def __init__(
        self,
        name: str,
        role: str,
        skills: list,
        model: str = "openai/gpt-oss-120b",
        temperature: float = 0.7
    ):
        """
        Initialize the base agent

        Args:
            name: Agent name
            role: Agent's role/purpose
            skills: List of skill objects this agent possesses
            model: Groq model to use
            temperature: LLM temperature
        """
        self.name = name
        self.role = role
        self.skills = skills

        # Initialize Groq LLM
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.llm = ChatGroq(
            api_key=api_key,
            model=model,
            temperature=temperature
        )

    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent

        Returns:
            System prompt string
        """
        skills_description = ", ".join([
            skill.__class__.__name__.replace('Skill', '')
            for skill in self.skills
        ])

        return f"""You are {self.name}, a specialized AI agent.

Role: {self.role}

Skills: You have access to the following capabilities: {skills_description}

Your task is to use your skills effectively to accomplish your specific role in the research and content creation workflow.
Be concise, accurate, and focused on your designated responsibilities.
"""

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's primary function.
        This should be overridden by subclasses.

        Args:
            input_data: Input data dictionary

        Returns:
            Output data dictionary
        """
        raise NotImplementedError("Subclasses must implement execute method")

    def __repr__(self) -> str:
        return f"{self.name} ({self.role})"
