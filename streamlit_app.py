"""
Streamlit UI for Multi-Agent Research & Content Creation System
"""
import streamlit as st
import os
from dotenv import load_dotenv
import time
from datetime import datetime
import plotly.graph_objects as go

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Content Creator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .agent-card {
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #667eea;
        margin: 0.5rem 0;
        background-color: #f0f2f6;
    }
    .status-running {
        color: #ff9800;
        font-weight: bold;
    }
    .status-complete {
        color: #4caf50;
        font-weight: bold;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'workflow_state' not in st.session_state:
    st.session_state.workflow_state = None
if 'execution_log' not in st.session_state:
    st.session_state.execution_log = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Header
st.markdown('<h1 class="main-header">🤖 Multi-Agent Content Creator</h1>', unsafe_allow_html=True)
st.markdown("### Powered by 6 Specialized AI Agents with Agent Skills")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=AI+Agents")

    st.markdown("## ⚙️ Configuration")

    # API Key status
    groq_key = os.getenv("GROQ_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")

    col1, col2 = st.columns(2)
    with col1:
        if groq_key and groq_key != "your_groq_api_key_here":
            st.success("✅ Groq")
        else:
            st.error("❌ Groq")

    with col2:
        if serper_key and serper_key != "your_serper_api_key_here":
            st.success("✅ SERPER")
        else:
            st.error("❌ SERPER")

    st.markdown("---")

    # Model selection
    st.markdown("### 🧠 LLM Model")
    model_option = st.selectbox(
        "Select Model",
        ["mixtral-8x7b-32768 (Fast)", "llama-3.1-70b-versatile (Powerful)", "llama-3.1-8b-instant (Quick)"],
        index=0
    )

    st.markdown("---")

    # Agent Status
    st.markdown("### 🤖 Agent Status")

    agents = [
        ("Research Coordinator", "🎯", "Planning"),
        ("Web Searcher", "🔍", "Search"),
        ("Data Analyst", "📊", "Analysis"),
        ("Content Writer", "✍️", "Writing"),
        ("Fact Checker", "✅", "Verification"),
        ("Editor", "📝", "Editing")
    ]

    for idx, (name, icon, skill) in enumerate(agents):
        if st.session_state.current_step > idx:
            st.success(f"{icon} {name} ✓")
        elif st.session_state.current_step == idx:
            st.warning(f"{icon} {name} ⏳")
        else:
            st.info(f"{icon} {name}")

    st.markdown("---")

    # About
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Multi-Agent System Features:**
        - 6 Specialized AI Agents
        - Agent Skills Architecture
        - Internet Search Integration
        - Automated Fact-Checking
        - Quality Assurance
        - LangGraph Orchestration
        """)

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Create Content", "📊 Dashboard", "📚 Documentation", "⚙️ Settings"])

with tab1:
    st.markdown("## Create AI-Generated Content")

    col1, col2 = st.columns([2, 1])

    with col1:
        topic = st.text_input(
            "📝 Research Topic",
            placeholder="e.g., The Future of Artificial Intelligence in Healthcare",
            help="Enter any topic you want to research and create content about"
        )

    with col2:
        depth = st.selectbox(
            "🎚️ Research Depth",
            ["shallow", "medium", "deep"],
            index=1,
            help="Shallow: 2 searches, Medium: 5 searches, Deep: 8+ searches"
        )

    # Example topics
    st.markdown("### 💡 Example Topics")
    example_topics = [
        "The Future of Artificial Intelligence in Healthcare",
        "Sustainable Energy Solutions for Urban Cities",
        "Quantum Computing Applications in Cryptography",
        "The Impact of Blockchain on Supply Chain Management",
        "Climate Change Mitigation Strategies"
    ]

    cols = st.columns(5)
    for idx, example in enumerate(example_topics):
        with cols[idx]:
            if st.button(f"📌 {idx+1}", key=f"example_{idx}", help=example):
                st.session_state.selected_topic = example
                st.rerun()

    if 'selected_topic' in st.session_state:
        topic = st.session_state.selected_topic
        st.info(f"Selected: {topic}")

    st.markdown("---")

    # Generate button
    if st.button("🚀 Generate Content", type="primary"):
        if not topic:
            st.error("❌ Please enter a topic!")
        elif not (groq_key and serper_key):
            st.error("❌ Please configure API keys in .env file!")
        else:
            # Create progress placeholder
            progress_placeholder = st.empty()
            status_placeholder = st.empty()

            try:
                with st.spinner("Initializing multi-agent system..."):
                    from src.workflow.orchestrator import MultiAgentOrchestrator
                    orchestrator = MultiAgentOrchestrator()

                # Progress bar
                progress_bar = progress_placeholder.progress(0)

                # Run workflow with progress updates
                status_placeholder.info("🎯 **Step 1/6:** Research Coordinator - Planning strategy...")
                st.session_state.current_step = 0
                time.sleep(1)
                progress_bar.progress(16)

                status_placeholder.info("🔍 **Step 2/6:** Web Searcher - Gathering information...")
                st.session_state.current_step = 1
                time.sleep(1)
                progress_bar.progress(33)

                # Execute workflow
                with status_placeholder.container():
                    st.info("⚙️ Running multi-agent workflow...")
                    final_state = orchestrator.run(topic=topic, depth=depth)

                progress_bar.progress(100)

                # Store results
                st.session_state.workflow_state = final_state
                st.session_state.current_step = 6

                # Success message
                st.success("✅ **Content Generation Complete!**")

                # Save outputs
                os.makedirs("outputs", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                if final_state.get('final_content'):
                    filename = f"outputs/article_{timestamp}.md"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(final_state['final_content'])
                    st.success(f"💾 Saved to: {filename}")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)

    # Display results if available
    if st.session_state.workflow_state:
        st.markdown("---")
        st.markdown("## 📄 Generated Content")

        final_state = st.session_state.workflow_state

        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🔍 Searches", len(final_state.get('search_queries', [])))

        with col2:
            st.metric("📊 Key Points", len(final_state.get('key_points', [])))

        with col3:
            st.metric("✅ Claims Checked", final_state.get('claims_checked', 0))

        with col4:
            words = len(final_state.get('final_content', '').split())
            st.metric("📝 Word Count", words)

        st.markdown("---")

        # Content tabs
        content_tab1, content_tab2, content_tab3, content_tab4 = st.tabs([
            "📄 Final Article",
            "🔍 Research Plan",
            "✅ Fact Check",
            "📝 Editing Report"
        ])

        with content_tab1:
            if final_state.get('final_content'):
                st.markdown(final_state['final_content'])

                st.download_button(
                    "⬇️ Download Article",
                    final_state['final_content'],
                    file_name="article.md",
                    mime="text/markdown"
                )

        with content_tab2:
            if final_state.get('workflow_summary'):
                st.markdown(final_state['workflow_summary'])

        with content_tab3:
            if final_state.get('fact_check_report'):
                st.markdown(final_state['fact_check_report'])

        with content_tab4:
            if final_state.get('editing_report'):
                st.markdown(final_state['editing_report'])

with tab2:
    st.markdown("## 📊 System Dashboard")

    if st.session_state.workflow_state:
        final_state = st.session_state.workflow_state

        # Agent performance visualization
        st.markdown("### 🤖 Agent Workflow")

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["Input", "Coordinator", "Searcher", "Analyst", "Writer", "Fact Checker", "Editor", "Output"],
                color=["#667eea", "#764ba2", "#667eea", "#764ba2", "#667eea", "#764ba2", "#667eea", "#764ba2"]
            ),
            link=dict(
                source=[0, 1, 2, 3, 4, 5, 6],
                target=[1, 2, 3, 4, 5, 6, 7],
                value=[1, 1, 1, 1, 1, 1, 1]
            )
        )])

        fig.update_layout(title_text="Agent Workflow Flow", font_size=10, height=400)
        st.plotly_chart(fig)

        # Key Points
        st.markdown("### 🎯 Key Insights")
        if final_state.get('key_points'):
            for i, point in enumerate(final_state['key_points'], 1):
                st.info(f"**{i}.** {point}")

        # Themes
        st.markdown("### 🏷️ Identified Themes")
        if final_state.get('themes'):
            theme_cols = st.columns(len(final_state['themes']))
            for idx, theme in enumerate(final_state['themes']):
                with theme_cols[idx]:
                    st.success(f"🏷️ {theme}")
    else:
        st.info("👆 Generate content first to see the dashboard")

with tab3:
    st.markdown("## 📚 Documentation")

    st.markdown("""
    ### 🎯 How It Works

    This multi-agent system uses **6 specialized AI agents**, each equipped with unique skills:

    1. **🎯 Research Coordinator** (Planning Skill)
       - Creates research strategy
       - Generates search queries
       - Coordinates workflow

    2. **🔍 Web Searcher** (Search Skill)
       - Executes internet searches
       - Uses SERPER API
       - Gathers multiple sources

    3. **📊 Data Analyst** (Analysis Skill)
       - Analyzes search results
       - Extracts key insights
       - Identifies themes

    4. **✍️ Content Writer** (Writing Skill)
       - Creates article structure
       - Writes engaging content
       - Formats professionally

    5. **✅ Fact Checker** (Verification Skill)
       - Extracts claims
       - Verifies with web search
       - Provides confidence scores

    6. **📝 Editor** (Editing Skill)
       - Reviews quality
       - Improves readability
       - Final polish

    ---

    ### 🔧 Agent Skills Architecture

    Each agent possesses **specific, reusable skills**:
    - Skills are modular components
    - Agents can share skills
    - Easy to add new capabilities
    - Clear separation of concerns

    ---

    ### ⚡ Performance

    - **Execution Time:** 60-90 seconds
    - **API Calls:** ~15-30 per workflow
    - **Output:** Publication-ready article

    ---

    ### 📖 Documentation Files

    - **README.md** - Complete documentation
    - **QUICKSTART.md** - 5-minute setup
    - **ARCHITECTURE.md** - Technical details
    - **PROJECT_SUMMARY.md** - Overview
    """)

with tab4:
    st.markdown("## ⚙️ Settings")

    st.markdown("### 🔑 API Configuration")

    st.info("""
    API keys are loaded from the `.env` file in the project root.

    Required keys:
    - **GROQ_API_KEY** - Get from https://console.groq.com
    - **SERPER_API_KEY** - Get from https://serper.dev
    """)

    # Display current status
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Groq API")
        if groq_key and groq_key != "your_groq_api_key_here":
            st.success("✅ Configured")
            st.code(f"{groq_key[:10]}...{groq_key[-5:]}", language="text")
        else:
            st.error("❌ Not configured")

    with col2:
        st.markdown("#### SERPER API")
        if serper_key and serper_key != "your_serper_api_key_here":
            st.success("✅ Configured")
            st.code(f"{serper_key[:10]}...{serper_key[-5:]}", language="text")
        else:
            st.error("❌ Not configured")

    st.markdown("---")

    st.markdown("### 📁 Output Directory")
    st.info("Generated content is saved to: `outputs/`")

    if st.button("📂 Open Output Folder"):
        os.makedirs("outputs", exist_ok=True)
        st.success("✅ Output folder ready at: outputs/")

    st.markdown("---")

    st.markdown("### 🧹 Clear Cache")
    if st.button("🗑️ Clear Session Data"):
        st.session_state.workflow_state = None
        st.session_state.current_step = 0
        st.success("✅ Session cleared!")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using Multi-Agent AI | Powered by LangChain, LangGraph & Groq</p>
</div>
""", unsafe_allow_html=True)
