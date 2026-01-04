#  Multi-Agent AI Content Creation System

<img width="1158" height="617" alt="image" src="https://github.com/user-attachments/assets/a2fccf09-d114-4177-9c84-8f02ab420933" />
 
  
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.0+-green.svg)](https://github.com/langchain-ai/langchain)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0+-red.svg)](https://streamlit.io/)

> **Production-ready multi-agent AI system with comprehensive governance framework**

A sophisticated AI system where **6 specialized agents** collaborate to research topics, verify facts, and create publication-ready content autonomously. Built with enterprise-grade AI governance and responsible AI principles.

![Multi-Agent Workflow](https://via.placeholder.com/800x300/667eea/ffffff?text=Multi-Agent+AI+Content+Creation)

---

## ✨ Key Features

### 🤖 Multi-Agent Collaboration
- **6 Specialized AI Agents** working together
- **Agent Skills Architecture** (inspired by Claude's Agent Skills)
- **LangGraph Orchestration** for stateful workflows
- **Groq LLM** for ultra-fast inference

### 🛡️ AI Governance & Safety
- **Content Safety** - Harmful content detection & PII protection
- **Input Validation** - Injection attack prevention
- **Bias Detection** - Fair and inclusive content
- **Transparency** - Full audit trails & explainability

### 🎨 Dual Interface
- **Streamlit Web UI** - Beautiful, interactive interface
- **Command Line** - Terminal-based operation

### 🔍 Internet Search Integration
- Real-time web search via **SERPER API**
- Multi-source research
- Automated fact-checking

---

## 🏗️ Architecture

### The 6 AI Agents

```mermaid
graph LR
    A[Research Coordinator] -->|Search Queries| B[Web Searcher]
    B -->|Raw Data| C[Data Analyst]
    C -->|Key Insights| D[Content Writer]
    D -->|Draft Article| E[Fact Checker]
    E -->|Verified Content| F[Editor]
    F -->|Final Article| G[Output]

    style A fill:#667eea
    style B fill:#764ba2
    style C fill:#667eea
    style D fill:#764ba2
    style E fill:#667eea
    style F fill:#764ba2
    style G fill:#4caf50
```

| Agent | Skill | Role |
|-------|-------|------|
| 🎯 **Research Coordinator** | Planning | Creates research strategy |
| 🔍 **Web Searcher** | Search | Gathers information from internet |
| 📊 **Data Analyst** | Analysis | Extracts insights & patterns |
| ✍️ **Content Writer** | Writing | Creates structured articles |
| ✅ **Fact Checker** | Verification | Verifies claims with sources |
| 📝 **Editor** | Editing | Polishes & improves quality |

### Agent Skills

Each agent is equipped with **specific, reusable skills**:
- `PlanningSkill` - Strategic planning and query generation
- `SearchSkill` - Web search and information retrieval
- `AnalysisSkill` - Data analysis and synthesis
- `WritingSkill` - Content creation and structuring
- `FactCheckingSkill` - Claim verification
- `EditingSkill` - Quality assurance

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- [Groq API Key](https://console.groq.com) (free tier available)
- [SERPER API Key](https://serper.dev) (1000 free searches/month)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/multi-agent-orchestration.git
cd multi-agent-orchestration

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### Run

**Option 1: Streamlit Web UI (Recommended)**
```bash
streamlit run streamlit_app.py
```
Opens at `http://localhost:8501`

**Option 2: Command Line**
```bash
python main.py
```

### Verify Setup

```bash
python test_setup.py
```

---

## 📖 Usage

### Web Interface

1. **Launch Streamlit**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Enter a topic** or click an example

3. **Select research depth**:
   - `shallow` - Quick (30s, 2 searches)
   - `medium` - Balanced (90s, 5 searches)
   - `deep` - Comprehensive (3min, 8+ searches)

4. **Click "Generate Content"**

5. **View results** in organized tabs:
   - Final Article
   - Research Plan
   - Fact Check Report
   - Editing Report

### Programmatic Usage

```python
from src.workflow.orchestrator import MultiAgentOrchestrator

# Initialize
orchestrator = MultiAgentOrchestrator()

# Generate content
final_state = orchestrator.run(
    topic="The Future of AI in Healthcare",
    depth="medium"
)

# Access results
article = final_state['final_content']
fact_check = final_state['fact_check_report']
```

### With AI Governance

```python
from src.governance.governance_orchestrator import GovernanceOrchestrator

# Enable governance
governance = GovernanceOrchestrator(enable_all=True)

# Validate input
is_valid, results = governance.validate_input(topic, depth)

# Check content safety
is_safe, safety_results = governance.check_content_safety(content)

# Detect bias
bias_results = governance.detect_bias(content)

# Finalize with disclaimers
final_content = governance.finalize_content(content, topic)
```

---

## 🛡️ AI Governance Framework

### Content Safety Guardrail

✅ **Protects Against:**
- Violence & harmful content
- Hate speech & discrimination
- Personal information leaks (PII)
- Inappropriate advice (medical/legal/financial)

✅ **Features:**
- Automatic PII redaction
- Content sanitization
- Safety violation detection

**Example:**
```
Input:  "Call 555-123-4567 or email john@email.com"
Output: "Call [REDACTED-PHONE] or email [EMAIL]@email.com"
```

### Input Validation Guardrail

✅ **Prevents:**
- XSS attacks
- SQL injection
- Code execution
- Prohibited topics

✅ **Features:**
- Input sanitization
- Rate limiting (10/hour free tier)
- Topic filtering

### Bias Detection Guardrail

✅ **Detects:**
- Gender bias ("mankind" → "humanity")
- Age bias ("elderly" → "older adults")
- Disability bias
- Stereotypes

✅ **Features:**
- Multiple bias types
- Representation analysis
- Automatic mitigation

### Transparency & Explainability

✅ **Provides:**
- Decision logging
- Source attribution
- Confidence scores
- Audit trails

---

## 📊 Example Output

### Input
```
Topic: "The Benefits of Renewable Energy"
Depth: medium
```

### Process (60-90 seconds)
```
✓ Research Coordinator → Plans strategy (5 searches)
✓ Web Searcher → Gathers information (15 results)
✓ Data Analyst → Extracts 7 key insights
✓ Content Writer → Creates 1,247-word article
✓ Fact Checker → Verifies 12 claims
✓ Editor → Polishes & improves quality
```

### Output Files
```
outputs/
├── final_article.md           # 1,200-word article
├── research_plan.md          # Research strategy
├── fact_check_report.md      # Verification results
└── editing_report.md         # Quality analysis

outputs/governance/           # If governance enabled
├── governance_report.md      # Transparency log
├── safety_report.md         # Safety checks
└── bias_report.md           # Bias analysis
```

---

## 🎨 Streamlit UI Features

- 🎯 **Example Topics** - Quick-start templates
- 📊 **Live Progress** - Real-time agent status
- 📈 **Visual Dashboard** - Workflow diagrams
- ⬇️ **One-Click Download** - Export to Markdown
- 🎨 **Professional Design** - Modern, clean interface
- 📱 **Responsive** - Works on all devices

---

## 📁 Project Structure

```
MultiAgentOrchestration/
├── src/
│   ├── agents/              # 6 AI agents
│   │   ├── research_coordinator.py
│   │   ├── web_searcher.py
│   │   ├── data_analyst.py
│   │   ├── content_writer.py
│   │   ├── fact_checker.py
│   │   └── editor.py
│   ├── skills/              # Agent skills
│   │   ├── planning_skill.py
│   │   ├── search_skill.py
│   │   ├── analysis_skill.py
│   │   ├── writing_skill.py
│   │   ├── fact_checking_skill.py
│   │   └── editing_skill.py
│   ├── governance/          # AI governance
│   │   ├── content_safety.py
│   │   ├── input_validator.py
│   │   ├── bias_detector.py
│   │   ├── transparency.py
│   │   └── governance_orchestrator.py
│   ├── workflow/            # Orchestration
│   │   └── orchestrator.py
│   └── config.py            # Configuration
├── examples/                # Usage examples
│   └── governance_integration_example.py
├── streamlit_app.py         # Web UI
├── main.py                  # CLI interface
├── test_setup.py           # Setup verification
├── requirements.txt        # Dependencies
└── .env.example           # Environment template
```

---

## 🔧 Configuration

### LLM Model Selection

Edit `src/config.py`:
```python
DEFAULT_MODEL = "mixtral-8x7b-32768"  # Fast
# or
DEFAULT_MODEL = "llama-3.1-70b-versatile"  # More powerful
```

### Research Depth

```python
MAX_SEARCH_QUERIES = {
    "shallow": 2,
    "medium": 5,
    "deep": 8
}
```

### Governance Settings

```python
governance = GovernanceOrchestrator(enable_all=True)

# Enable strict mode (blocks any violations)
governance.governance_config["strict_mode"] = True
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical deep-dive |
| [AI_GOVERNANCE.md](AI_GOVERNANCE.md) | Governance framework |
| [GOVERNANCE_SUMMARY.md](GOVERNANCE_SUMMARY.md) | Governance quick reference |
| [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) | UI walkthrough |
| [FIX_AND_RUN.md](FIX_AND_RUN.md) | Troubleshooting guide |

---

## 🧪 Testing

### Run Tests
```bash
python test_setup.py
```

### Test Governance
```bash
cd examples
python governance_integration_example.py
```

### Expected Output
```
✅ 8/8 tests passed
✅ API keys configured
✅ All imports working
✅ Groq connection successful
✅ SERPER connection successful
```

---

## 🎯 Use Cases

### Content Marketing
- Research trending topics
- Generate SEO-optimized articles
- Fact-checked content
- Ready for publication

### Academic Research
- Gather information from multiple sources
- Synthesize findings
- Create structured reports
- Source attribution

### News Analysis
- Multi-source coverage
- Fact verification
- Comprehensive reporting
- Bias-aware content

### Product Research
- Market trend analysis
- Competitor research
- Feature comparisons
- Data-driven insights

---

## 🌟 What Makes This Special

### 1. Agent Skills Architecture
Inspired by Claude's Agent Skills feature:
- ✅ Modular, reusable skills
- ✅ Clear separation of concerns
- ✅ Easy to extend
- ✅ Composable capabilities

### 2. Production-Ready Governance
Enterprise-grade guardrails:
- ✅ Content safety
- ✅ Bias detection
- ✅ Transparency
- ✅ Compliance support

### 3. Complete Implementation
Not just a demo:
- ✅ Full workflow orchestration
- ✅ Error handling
- ✅ Type safety (Pydantic)
- ✅ Comprehensive docs

### 4. Dual Interface
Flexibility for all users:
- ✅ Beautiful Streamlit UI
- ✅ CLI for automation
- ✅ Programmatic API

---

## 🔒 Security & Privacy

- 🛡️ **PII Protection** - Automatic redaction
- 🔐 **Input Sanitization** - Injection prevention
- 🚫 **Content Filtering** - Harmful content blocked
- 📝 **Audit Trails** - Complete logging
- ⚖️ **Bias Mitigation** - Fair content

---

## 📈 Performance

| Depth | Time | Searches | Output |
|-------|------|----------|--------|
| Shallow | ~30s | 2 | ~500 words |
| Medium | ~90s | 5 | ~1000 words |
| Deep | ~180s | 8+ | ~1500 words |

**Requirements:**
- Internet connection
- ~100-200MB RAM
- API quotas (Groq + SERPER)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
pip install -r requirements-dev.txt
pytest tests/
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

### Technologies
- [LangChain](https://github.com/langchain-ai/langchain) - Agent framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Workflow orchestration
- [Groq](https://groq.com) - Ultra-fast LLM inference
- [SERPER](https://serper.dev) - Google Search API
- [Streamlit](https://streamlit.io) - Web interface

### Inspiration
- Claude's Agent Skills feature
- Multi-agent systems research
- Responsible AI principles

---

## 🗺️ Roadmap

- [ ] RAG (Retrieval Augmented Generation)
- [ ] Additional LLM providers (OpenAI, Anthropic)
- [ ] Agent memory and learning
- [ ] Multi-language support
- [ ] PDF/DOCX export
- [ ] Custom skill marketplace
- [ ] API endpoints (FastAPI)
- [ ] Docker deployment


---

## 🎉 Quick Commands

```bash
# Clone & Setup
git clone https://github.com/yourusername/multi-agent-orchestration.git
cd multi-agent-orchestration
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Test
python test_setup.py

# Run Streamlit UI
streamlit run streamlit_app.py

# Run CLI
python main.py

```

---

