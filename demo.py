#!/usr/bin/env python3
"""
Demo script for the Azra Bano AI Agent
Shows the functionality without requiring OpenAI API key
"""

import logging
from web_scraper import WebScraper
from knowledge_base import KnowledgeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def demo_web_scraping():
    """Demo web scraping functionality"""
    print("🌐 Demo: Web Scraping")
    print("=" * 40)
    
    scraper = WebScraper()
    
    # Test website scraping
    print("📄 Scraping personal website...")
    website_data = scraper.scrape_personal_website()
    
    if website_data:
        print(f"✅ Website scraped successfully!")
        print(f"   Title: {website_data.get('title', 'Not found')}")
        print(f"   Headings found: {len(website_data.get('headings', []))}")
        print(f"   Links found: {len(website_data.get('links', []))}")
        print(f"   Text content length: {len(website_data.get('text_content', ''))} characters")
        
        # Show first few headings
        headings = website_data.get('headings', [])
        if headings:
            print("   Sample headings:")
            for i, heading in enumerate(headings[:5]):
                print(f"     {i+1}. {heading}")
    else:
        print("❌ Failed to scrape website")
    
    # Test LinkedIn scraping
    print("\n🔗 Scraping LinkedIn profile...")
    linkedin_data = scraper.scrape_linkedin_profile("https://www.linkedin.com/in/meetazrabano/")
    
    if linkedin_data:
        print(f"✅ LinkedIn scraped successfully!")
        print(f"   Name: {linkedin_data.get('name', 'Not found')}")
        print(f"   Headline: {linkedin_data.get('headline', 'Not found')}")
        print(f"   About length: {len(linkedin_data.get('about', ''))} characters")
        print(f"   Experience entries: {len(linkedin_data.get('experience', []))}")
        print(f"   Education entries: {len(linkedin_data.get('education', []))}")
        
        # Show experience
        experience = linkedin_data.get('experience', [])
        if experience:
            print("   Sample experience:")
            for i, exp in enumerate(experience[:3]):
                print(f"     {i+1}. {exp}")
    else:
        print("❌ Failed to scrape LinkedIn")
    
    scraper.close_selenium()
    return website_data, linkedin_data

def demo_knowledge_base(website_data, linkedin_data):
    """Demo knowledge base functionality"""
    print("\n🧠 Demo: Knowledge Base")
    print("=" * 40)
    
    kb = KnowledgeBase()
    
    # Combine data
    scraped_data = {}
    if website_data:
        scraped_data['website'] = website_data
    if linkedin_data:
        scraped_data['linkedin'] = linkedin_data
    
    # Add data to knowledge base
    print("📚 Adding data to knowledge base...")
    success = kb.add_data_to_knowledge_base(scraped_data)
    
    if success:
        print("✅ Data added successfully!")
        
        # Get stats
        stats = kb.get_knowledge_base_stats()
        print(f"   Total documents: {stats.get('total_documents', 0)}")
        
        # Test search
        print("\n🔍 Testing search functionality...")
        test_queries = [
            "What does Azra do?",
            "Azra's experience",
            "education background",
            "skills and expertise"
        ]
        
        for query in test_queries:
            print(f"\n   Query: '{query}'")
            results = kb.search_knowledge_base(query, n_results=2)
            if results:
                print(f"   Found {len(results)} results:")
                for i, result in enumerate(results):
                    source = result['metadata'].get('source', 'unknown')
                    content_type = result['metadata'].get('type', 'unknown')
                    content_preview = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
                    print(f"     {i+1}. [{source}/{content_type}] {content_preview}")
            else:
                print("   No results found")
    else:
        print("❌ Failed to add data to knowledge base")

def demo_configuration():
    """Demo configuration"""
    print("\n⚙️  Demo: Configuration")
    print("=" * 40)
    
    from config import Config
    
    print(f"Personal Website: {Config.PERSONAL_WEBSITE}")
    print(f"LinkedIn URL: {Config.LINKEDIN_URL}")
    print(f"OpenAI Model: {Config.OPENAI_MODEL}")
    print(f"ChromaDB Directory: {Config.CHROMA_PERSIST_DIRECTORY}")
    print(f"Max Context Length: {Config.MAX_CONTEXT_LENGTH}")
    print(f"Temperature: {Config.TEMPERATURE}")
    print(f"OpenAI API Key configured: {'Yes' if Config.OPENAI_API_KEY else 'No'}")

def main():
    """Run the demo"""
    print("🤖 Azra Bano AI Agent - Demo")
    print("=" * 50)
    print("This demo shows the core functionality without requiring OpenAI API key")
    print()
    
    try:
        # Demo configuration
        demo_configuration()
        
        # Demo web scraping
        website_data, linkedin_data = demo_web_scraping()
        
        # Demo knowledge base
        demo_knowledge_base(website_data, linkedin_data)
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("\n📝 Next steps:")
        print("1. Set your OpenAI API key in the .env file")
        print("2. Run: python3 app.py")
        print("3. Open http://localhost:5000 in your browser")
        print("4. Start asking questions about Azra Bano!")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


