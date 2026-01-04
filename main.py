"""
Multi-Agent Research & Content Creation System
Main execution script

This system demonstrates a sophisticated multi-agent orchestration using:
- LangChain for agent framework
- LangGraph for workflow orchestration
- Groq for LLM inferencing
- Agent Skills (inspired by Claude's Agent Skills feature)
- SERPER API for web search capability
"""
import os
from dotenv import load_dotenv
from src.workflow.orchestrator import MultiAgentOrchestrator


def save_output(final_state: dict, output_dir: str = "outputs"):
    """
    Save the workflow outputs to files

    Args:
        final_state: Final state from the workflow
        output_dir: Directory to save outputs
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save final article
    if final_state.get('final_content'):
        with open(f"{output_dir}/final_article.md", 'w', encoding='utf-8') as f:
            f.write(final_state['final_content'])
        print(f"✓ Final article saved to: {output_dir}/final_article.md")

    # Save research plan
    if final_state.get('workflow_summary'):
        with open(f"{output_dir}/research_plan.md", 'w', encoding='utf-8') as f:
            f.write(final_state['workflow_summary'])
        print(f"✓ Research plan saved to: {output_dir}/research_plan.md")

    # Save fact-check report
    if final_state.get('fact_check_report'):
        with open(f"{output_dir}/fact_check_report.md", 'w', encoding='utf-8') as f:
            f.write(final_state['fact_check_report'])
        print(f"✓ Fact-check report saved to: {output_dir}/fact_check_report.md")

    # Save editing report
    if final_state.get('editing_report'):
        with open(f"{output_dir}/editing_report.md", 'w', encoding='utf-8') as f:
            f.write(final_state['editing_report'])
        print(f"✓ Editing report saved to: {output_dir}/editing_report.md")


def main():
    """
    Main execution function
    """
    # Load environment variables
    load_dotenv()

    # Verify API keys
    groq_key = os.getenv("GROQ_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")

    if not groq_key:
        print("ERROR: GROQ_API_KEY not found in .env file")
        return

    if not serper_key:
        print("ERROR: SERPER_API_KEY not found in .env file")
        return

    print("✓ API keys loaded successfully\n")

    # Example topics to research
    example_topics = [
        {
            "topic": "The Future of Artificial Intelligence in Healthcare",
            "depth": "medium"
        },
        {
            "topic": "Sustainable Energy Solutions for Urban Cities",
            "depth": "medium"
        },
        {
            "topic": "Quantum Computing Applications in Cryptography",
            "depth": "deep"
        }
    ]

    # Let user choose a topic or enter their own
    print("=" * 60)
    print("Multi-Agent Research & Content Creation System")
    print("=" * 60)
    print("\nExample topics:")
    for i, example in enumerate(example_topics, 1):
        print(f"{i}. {example['topic']} (depth: {example['depth']})")
    print(f"{len(example_topics) + 1}. Enter your own topic")

    try:
        choice = input(f"\nSelect an option (1-{len(example_topics) + 1}): ").strip()
        choice_num = int(choice)

        if 1 <= choice_num <= len(example_topics):
            selected = example_topics[choice_num - 1]
            topic = selected['topic']
            depth = selected['depth']
        else:
            topic = input("Enter your research topic: ").strip()
            depth_input = input("Enter research depth (shallow/medium/deep) [medium]: ").strip()
            depth = depth_input if depth_input in ['shallow', 'medium', 'deep'] else 'medium'

    except (ValueError, KeyboardInterrupt):
        print("\nUsing default topic...")
        topic = example_topics[0]['topic']
        depth = example_topics[0]['depth']

    # Initialize the orchestrator
    print("\nInitializing multi-agent system...")
    orchestrator = MultiAgentOrchestrator()

    # Run the workflow
    try:
        final_state = orchestrator.run(topic=topic, depth=depth)

        # Save outputs
        print("\n" + "=" * 60)
        print("Saving outputs...")
        print("=" * 60 + "\n")
        save_output(final_state)

        # Print summary
        print("\n" + "=" * 60)
        print("WORKFLOW SUMMARY")
        print("=" * 60)
        print(f"Topic: {topic}")
        print(f"Depth: {depth}")
        print(f"Search Queries Executed: {len(final_state.get('search_queries', []))}")
        print(f"Search Results: {len(final_state.get('search_results', []))}")
        print(f"Key Points Identified: {len(final_state.get('key_points', []))}")
        print(f"Claims Fact-Checked: {final_state.get('claims_checked', 0)}")
        print(f"\nFinal Article Preview:")
        print("-" * 60)
        if final_state.get('final_content'):
            preview = final_state['final_content'][:500]
            print(f"{preview}...")
        print("=" * 60)

        print("\n✓ All tasks completed successfully!")
        print(f"✓ Check the 'outputs/' directory for all generated files")

    except Exception as e:
        print(f"\n✗ Error during workflow execution: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
