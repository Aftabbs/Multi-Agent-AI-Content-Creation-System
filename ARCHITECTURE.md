# Architecture Documentation

## System Overview

The Multi-Agent Research & Content Creation System is built on a modular, skill-based architecture where specialized AI agents collaborate to research topics and create high-quality content.

## Core Concepts

### 1. Agent Skills Architecture

Inspired by Claude's Agent Skills feature, this system implements a **skill-based agent architecture** where:

- **Skills are first-class citizens**: Each skill is a separate, reusable module
- **Agents possess skills**: Agents are equipped with one or more skills
- **Skills define capabilities**: What an agent can do is determined by its skills
- **Skills are composable**: New capabilities can be added by adding skills

### 2. Agent-Skill Relationship

```
┌─────────────────────────────────────────────────────────────┐
│                         Agent                                │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Skill 1   │  │  Skill 2   │  │  Skill 3   │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                              │
│  + LLM (Groq)                                               │
│  + System Prompt                                            │
│  + Execute Logic                                            │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Architecture

### Layer 1: Skills (Capabilities)

Skills are the foundational building blocks. Each skill encapsulates a specific capability.

#### Skill Structure

```python
class SomeSkill:
    """
    Agent Skill: Description
    """

    def __init__(self):
        # Initialize skill-specific resources
        pass

    def capability_method(self, input_data):
        # Implement specific capability
        return result
```

#### Implemented Skills

| Skill | File | Purpose | Key Methods |
|-------|------|---------|-------------|
| PlanningSkill | `planning_skill.py` | Strategic planning | `create_research_plan()`, `generate_search_queries()` |
| SearchSkill | `search_skill.py` | Web search | `search()`, `search_as_text()` |
| AnalysisSkill | `analysis_skill.py` | Data analysis | `synthesize_information()`, `extract_key_points()` |
| WritingSkill | `writing_skill.py` | Content creation | `compile_article()`, `create_outline()` |
| FactCheckingSkill | `fact_checking_skill.py` | Verification | `verify_claim()`, `extract_claims()` |
| EditingSkill | `editing_skill.py` | Quality assurance | `check_readability()`, `apply_polish()` |

### Layer 2: Agents (Executors)

Agents combine skills with LLM reasoning to execute complex tasks.

#### Agent Structure

```python
class SpecializedAgent(BaseAgent):
    def __init__(self):
        # Equip with skills
        skill1 = SomeSkill()
        skill2 = AnotherSkill()

        super().__init__(
            name="Agent Name",
            role="Agent's role",
            skills=[skill1, skill2],
            temperature=0.7
        )

    def execute(self, input_data):
        # 1. Use skills to gather/process data
        result = self.skill.some_method(input_data)

        # 2. Use LLM for reasoning/generation
        llm_output = self.llm.invoke(prompt)

        # 3. Return combined output
        return output
```

#### Agent Implementations

| Agent | Skills | Temperature | Role |
|-------|--------|-------------|------|
| ResearchCoordinator | PlanningSkill | 0.3 (focused) | Strategic planning |
| WebSearcher | SearchSkill | 0.2 (factual) | Information retrieval |
| DataAnalyst | AnalysisSkill | 0.4 (balanced) | Data synthesis |
| ContentWriter | WritingSkill | 0.7 (creative) | Content creation |
| FactChecker | FactCheckingSkill, SearchSkill | 0.2 (factual) | Verification |
| Editor | EditingSkill | 0.5 (balanced) | Quality assurance |

### Layer 3: Workflow Orchestration (LangGraph)

LangGraph coordinates agent execution in a stateful workflow.

#### Workflow State

```python
class AgentState(TypedDict):
    # Input
    topic: str
    depth: str

    # Intermediate outputs from each agent
    research_plan: Any
    search_results: list
    key_points: list
    draft_content: str
    fact_check_report: str

    # Final output
    final_content: str
```

#### Workflow Graph

```
Entry Point
    ↓
┌───────────────────┐
│ Research          │
│ Coordinator       │ Creates plan & queries
└────────┬──────────┘
         ↓
┌───────────────────┐
│ Web Searcher      │ Executes searches
└────────┬──────────┘
         ↓
┌───────────────────┐
│ Data Analyst      │ Analyzes results
└────────┬──────────┘
         ↓
┌───────────────────┐
│ Content Writer    │ Creates draft
└────────┬──────────┘
         ↓
┌───────────────────┐
│ Fact Checker      │ Verifies claims
└────────┬──────────┘
         ↓
┌───────────────────┐
│ Editor            │ Polishes content
└────────┬──────────┘
         ↓
      END
```

## Data Flow

### 1. Input Phase
```
User Input → Orchestrator
{
  topic: "AI in Healthcare",
  depth: "medium"
}
```

### 2. Research Phase
```
Orchestrator → Research Coordinator
{
  topic: "AI in Healthcare",
  depth: "medium"
}

Research Coordinator → State
{
  research_plan: ResearchPlan(...),
  search_queries: [
    "AI in Healthcare overview",
    "AI healthcare applications",
    ...
  ]
}
```

### 3. Search Phase
```
State → Web Searcher
{
  search_queries: [...]
}

Web Searcher → State
{
  search_results: [SearchResult(...)],
  search_summary: "Key findings..."
}
```

### 4. Analysis Phase
```
State → Data Analyst
{
  search_summary: "...",
  search_results: [...]
}

Data Analyst → State
{
  key_points: [...],
  themes: [...],
  deep_analysis: "..."
}
```

### 5. Writing Phase
```
State → Content Writer
{
  topic: "...",
  key_points: [...],
  deep_analysis: "..."
}

Content Writer → State
{
  draft_content: "# Article...",
  outline: [...]
}
```

### 6. Verification Phase
```
State → Fact Checker
{
  content: "..."
}

Fact Checker → State
{
  fact_check_report: "...",
  claims_checked: 12
}
```

### 7. Editing Phase
```
State → Editor
{
  content: "...",
  fact_check_assessment: "..."
}

Editor → State
{
  final_content: "# Final Article..."
}
```

## Technology Stack

### Core Frameworks

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Agent Framework | LangChain | Agent abstraction & LLM integration |
| Workflow Engine | LangGraph | Stateful multi-agent orchestration |
| LLM Provider | Groq | Fast inference with Mixtral/Llama |
| Search API | SERPER | Google Search results |
| Validation | Pydantic | Type-safe data models |

### LangChain Components Used

- `ChatGroq` - Groq LLM integration
- `ChatPromptTemplate` - Prompt management
- `BaseAgent` pattern - Agent structure

### LangGraph Components Used

- `StateGraph` - Workflow definition
- `TypedDict` - State typing
- Edge management - Workflow routing

## Design Patterns

### 1. Strategy Pattern (Skills)
Skills implement different strategies for the same interface.

```python
# Different strategies for content creation
writing_skill.create_outline()
writing_skill.compile_article()
```

### 2. Decorator Pattern (Agent Skills)
Agents are decorated with skills to enhance capabilities.

```python
agent = BaseAgent(name="Agent")
agent.skills = [Skill1(), Skill2()]  # Decorated with skills
```

### 3. Chain of Responsibility (Workflow)
Each agent processes state and passes to next agent.

```python
state → Agent1 → Agent2 → Agent3 → ... → Final State
```

### 4. State Pattern (LangGraph State)
Workflow state changes as it progresses through agents.

```python
initial_state → researched_state → analyzed_state → ... → final_state
```

## Scalability Considerations

### Horizontal Scaling
- Add more agents in parallel for different aspects
- Example: Multiple search agents for different sources

### Vertical Scaling
- Enhance individual skills with more sophisticated algorithms
- Example: Better NLP in AnalysisSkill

### Extensibility
- New skills can be added without changing core architecture
- New agents can be composed from existing skills

## Example: Adding a New Agent

### Step 1: Create a Skill
```python
# src/skills/translation_skill.py
class TranslationSkill:
    def translate(self, text, target_language):
        # Implementation
        return translated_text
```

### Step 2: Create an Agent
```python
# src/agents/translator.py
class Translator(BaseAgent):
    def __init__(self):
        translation_skill = TranslationSkill()
        super().__init__(
            name="Translator",
            role="Language translation",
            skills=[translation_skill]
        )

    def execute(self, input_data):
        # Use skill + LLM
        return output
```

### Step 3: Add to Workflow
```python
# src/workflow/orchestrator.py
workflow.add_node("translate", self._translate)
workflow.add_edge("edit", "translate")
workflow.add_edge("translate", END)
```

## Performance Characteristics

### Timing (Approximate)

| Phase | Agent | Time | Operations |
|-------|-------|------|------------|
| 1 | Research Coordinator | 5-10s | LLM call, planning |
| 2 | Web Searcher | 10-15s | 3-8 API calls |
| 3 | Data Analyst | 10-15s | LLM call, analysis |
| 4 | Content Writer | 15-20s | LLM call, generation |
| 5 | Fact Checker | 10-15s | 5-10 verification searches |
| 6 | Editor | 10-15s | LLM call, polishing |

**Total: 60-90 seconds** for medium depth

### Resource Usage

- **API Calls**: ~15-30 per workflow
- **Tokens**: ~50k-100k total
- **Memory**: ~100-200MB
- **Network**: ~5-10MB data transfer

## Security Considerations

### API Key Management
- Keys stored in `.env` (not committed)
- Loaded via `python-dotenv`
- Never logged or exposed

### Input Validation
- Pydantic models validate all data structures
- Type hints throughout codebase
- Error handling at each stage

### Rate Limiting
- SERPER: 1,000 calls/month (free tier)
- Groq: Depends on tier
- Implement delays if needed

## Future Architecture Enhancements

### 1. Agent Memory
```python
class MemorySkill:
    def remember(self, key, value):
        # Store in vector DB
        pass

    def recall(self, query):
        # Retrieve relevant memories
        pass
```

### 2. Parallel Agent Execution
```python
# Execute multiple agents concurrently
workflow.add_parallel_nodes([
    "agent1",
    "agent2",
    "agent3"
])
```

### 3. Dynamic Agent Selection
```python
# Choose agent based on task
workflow.add_conditional_edges(
    "router",
    route_to_agent,
    {
        "technical": "technical_writer",
        "creative": "creative_writer"
    }
)
```

### 4. Agent Learning
```python
class LearningSkill:
    def learn_from_feedback(self, feedback):
        # Update agent behavior
        pass
```

## Conclusion

This architecture provides:
- ✅ Modularity through skills
- ✅ Reusability of components
- ✅ Clear separation of concerns
- ✅ Easy extensibility
- ✅ Type safety with Pydantic
- ✅ Stateful orchestration with LangGraph
- ✅ Production-ready error handling

The skill-based approach inspired by Claude's Agent Skills enables powerful, composable AI agents that can be easily extended and modified.
