#!/usr/bin/env python3
"""
Test script to verify the AI agent setup
"""

import os
import sys
import logging
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import requests
        import bs4  # beautifulsoup4
        import selenium
        import openai
        import flask
        import chromadb
        import sentence_transformers
        import webdriver_manager
        logger.info("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        # Check if OpenAI API key is set
        if not Config.OPENAI_API_KEY:
            logger.warning("⚠️  OpenAI API key not set (this is required for full functionality)")
        else:
            logger.info("✅ OpenAI API key configured")
        
        # Check website URL
        logger.info(f"✅ Personal website URL: {Config.PERSONAL_WEBSITE}")
        
        # Check other config values
        logger.info(f"✅ OpenAI model: {Config.OPENAI_MODEL}")
        logger.info(f"✅ ChromaDB directory: {Config.CHROMA_PERSIST_DIRECTORY}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Configuration error: {e}")
        return False

def test_web_scraper():
    """Test web scraper functionality"""
    try:
        from web_scraper import WebScraper
        
        scraper = WebScraper()
        logger.info("✅ WebScraper initialized successfully")
        
        # Test basic scraping (without actually scraping)
        logger.info("✅ WebScraper module loaded successfully")
        return True
    except Exception as e:
        logger.error(f"❌ WebScraper error: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base functionality"""
    try:
        from knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase()
        logger.info("✅ KnowledgeBase initialized successfully")
        
        # Test basic operations
        stats = kb.get_knowledge_base_stats()
        logger.info(f"✅ Knowledge base stats: {stats}")
        
        return True
    except Exception as e:
        logger.error(f"❌ KnowledgeBase error: {e}")
        return False

def test_ai_agent():
    """Test AI agent functionality"""
    try:
        from ai_agent import AzraBanoAgent
        
        agent = AzraBanoAgent()
        logger.info("✅ AzraBanoAgent initialized successfully")
        
        # Test sample questions
        questions = agent.get_sample_questions()
        logger.info(f"✅ Sample questions loaded: {len(questions)} questions")
        
        return True
    except Exception as e:
        logger.error(f"❌ AI Agent error: {e}")
        return False

def test_flask_app():
    """Test Flask app functionality"""
    try:
        from app import app
        
        logger.info("✅ Flask app loaded successfully")
        
        # Test basic routes
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                logger.info("✅ Main route working")
            else:
                logger.warning(f"⚠️  Main route returned status {response.status_code}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Flask app error: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting AI Agent setup verification...")
    logger.info("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("Web Scraper", test_web_scraper),
        ("Knowledge Base", test_knowledge_base),
        ("AI Agent", test_ai_agent),
        ("Flask App", test_flask_app),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name} passed")
            else:
                logger.error(f"❌ {test_name} failed")
        except Exception as e:
            logger.error(f"❌ {test_name} failed with exception: {e}")
    
    logger.info("=" * 50)
    logger.info(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Your AI agent is ready to use.")
        logger.info("\n📝 Next steps:")
        logger.info("1. Set your OpenAI API key in the .env file")
        logger.info("2. Run: python app.py")
        logger.info("3. Open http://localhost:5000 in your browser")
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
