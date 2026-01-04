"""
Configuration module for Multi-Agent System
Centralizes all configuration settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Central configuration class
    """

    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

    # LLM Configuration
    DEFAULT_MODEL = "mixtral-8x7b-32768"  # Fast and capable
    ALTERNATIVE_MODELS = {
        "fast": "mixtral-8x7b-32768",
        "powerful": "llama-3.1-70b-versatile",
        "balanced": "llama-3.1-8b-instant"
    }

    # Temperature settings for different agents
    TEMPERATURES = {
        "research_coordinator": 0.3,  # Focused planning
        "web_searcher": 0.2,          # Factual search
        "data_analyst": 0.4,          # Balanced analysis
        "content_writer": 0.7,        # Creative writing
        "fact_checker": 0.2,          # Strict verification
        "editor": 0.5                 # Balanced editing
    }

    # Search Configuration
    SEARCH_RESULTS_PER_QUERY = 3
    MAX_SEARCH_QUERIES = {
        "shallow": 2,
        "medium": 5,
        "deep": 8
    }

    # Content Configuration
    TARGET_WORD_COUNT = {
        "shallow": 500,
        "medium": 1000,
        "deep": 1500
    }

    # Output Configuration
    OUTPUT_DIR = "outputs"

    # Workflow Configuration
    ENABLE_FACT_CHECKING = True
    ENABLE_EDITING = True

    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration is present

        Returns:
            bool: True if valid, False otherwise
        """
        if not cls.GROQ_API_KEY:
            print("ERROR: GROQ_API_KEY not found in environment")
            return False

        if not cls.SERPER_API_KEY:
            print("ERROR: SERPER_API_KEY not found in environment")
            return False

        return True

    @classmethod
    def get_model_for_agent(cls, agent_type: str) -> str:
        """
        Get the appropriate model for an agent

        Args:
            agent_type: Type of agent

        Returns:
            Model name
        """
        return cls.DEFAULT_MODEL

    @classmethod
    def get_temperature_for_agent(cls, agent_type: str) -> float:
        """
        Get the appropriate temperature for an agent

        Args:
            agent_type: Type of agent

        Returns:
            Temperature value
        """
        return cls.TEMPERATURES.get(agent_type, 0.5)


# Validate configuration on import
if __name__ != "__main__":
    Config.validate()
