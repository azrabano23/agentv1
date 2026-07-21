#!/usr/bin/env python3
"""
Command-line interface for the Azra Bano AI Agent
"""

import argparse
import sys
import logging
from ai_agent import AzraBanoAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Azra Bano AI Agent CLI')
    parser.add_argument('--question', '-q', help='Ask a specific question')
    parser.add_argument('--initialize', '-i', action='store_true', help='Initialize the knowledge base')
    parser.add_argument('--refresh', '-r', action='store_true', help='Refresh the knowledge base')
    parser.add_argument('--status', '-s', action='store_true', help='Show agent status')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = AzraBanoAgent()
    
    try:
        if args.status:
            show_status(agent)
        elif args.initialize:
            initialize_agent(agent)
        elif args.refresh:
            refresh_agent(agent)
        elif args.question:
            ask_question(agent, args.question)
        elif args.interactive:
            interactive_mode(agent)
        else:
            # Default: show status and start interactive mode
            show_status(agent)
            print("\n" + "="*50)
            interactive_mode(agent)
            
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

def show_status(agent):
    """Show agent status"""
    print("🤖 Azra Bano AI Agent Status")
    print("="*30)
    
    status = agent.get_agent_status()
    
    print(f"Initialized: {'✅ Yes' if status.get('is_initialized') else '❌ No'}")
    print(f"OpenAI Configured: {'✅ Yes' if status.get('openai_configured') else '❌ No'}")
    print(f"Website URL: {status.get('website_url', 'Not set')}")
    print(f"LinkedIn URL: {status.get('linkedin_url', 'Not found')}")
    
    kb_stats = status.get('knowledge_base_stats', {})
    if 'total_documents' in kb_stats:
        print(f"Knowledge Base Documents: {kb_stats['total_documents']}")
    else:
        print("Knowledge Base: Not initialized")

def initialize_agent(agent):
    """Initialize the knowledge base"""
    print("🔄 Initializing knowledge base...")
    
    success = agent.initialize_knowledge_base()
    
    if success:
        print("✅ Knowledge base initialized successfully!")
        print("You can now ask questions about Azra Bano.")
    else:
        print("❌ Failed to initialize knowledge base.")
        print("Please check your configuration and try again.")

def refresh_agent(agent):
    """Refresh the knowledge base"""
    print("🔄 Refreshing knowledge base...")
    
    success = agent.refresh_knowledge_base()
    
    if success:
        print("✅ Knowledge base refreshed successfully!")
    else:
        print("❌ Failed to refresh knowledge base.")

def ask_question(agent, question):
    """Ask a single question"""
    print(f"❓ Question: {question}")
    print("🤖 Answer:")
    print("-" * 40)
    
    result = agent.answer_question(question)
    
    print(result['answer'])
    
    if result.get('sources'):
        print("\n📚 Sources:")
        for source in result['sources']:
            print(f"  - {source.get('source', 'Unknown')} ({source.get('type', 'Unknown')})")
    
    if result.get('confidence'):
        print(f"\n🎯 Confidence: {result['confidence']}")

def interactive_mode(agent):
    """Start interactive question-answer mode"""
    print("\n💬 Interactive Mode")
    print("Ask questions about Azra Bano (type 'quit' to exit)")
    print("="*50)
    
    # Show sample questions
    questions = agent.get_sample_questions()
    print("\n💡 Sample questions:")
    for i, q in enumerate(questions[:5], 1):
        print(f"  {i}. {q}")
    print()
    
    while True:
        try:
            question = input("❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not question:
                continue
            
            print("🤖 Thinking...")
            result = agent.answer_question(question)
            
            print(f"\n💬 Answer: {result['answer']}")
            
            if result.get('sources'):
                print("\n📚 Sources:")
                for source in result['sources']:
                    print(f"  - {source.get('source', 'Unknown')} ({source.get('type', 'Unknown')})")
            
            if result.get('confidence'):
                print(f"🎯 Confidence: {result['confidence']}")
            
            print("\n" + "-"*50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()


