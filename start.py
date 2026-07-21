#!/usr/bin/env python3
"""
Startup script for the Azra Bano AI Agent
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8 or higher is required")
        return False
    logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import requests
        import beautifulsoup4
        import selenium
        import openai
        import flask
        import chromadb
        logger.info("✅ All dependencies are installed")
        return True
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        logger.info("💡 Run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    
    if not env_file.exists():
        logger.warning("⚠️  .env file not found")
        logger.info("💡 Copy env.example to .env and add your OpenAI API key")
        return False
    
    # Check if OpenAI API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=your_openai_api_key_here' in content:
            logger.warning("⚠️  OpenAI API key not configured")
            logger.info("💡 Add your OpenAI API key to the .env file")
            return False
    
    logger.info("✅ Environment configuration looks good")
    return True

def run_tests():
    """Run setup tests"""
    logger.info("🧪 Running setup tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_setup.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ All tests passed")
            return True
        else:
            logger.error("❌ Some tests failed")
            logger.error(result.stderr)
            return False
    except Exception as e:
        logger.error(f"❌ Error running tests: {e}")
        return False

def start_web_app():
    """Start the Flask web application"""
    logger.info("🚀 Starting web application...")
    
    try:
        # Set environment variables
        env = os.environ.copy()
        env['FLASK_APP'] = 'app.py'
        env['FLASK_ENV'] = 'development'
        
        # Start the Flask app
        subprocess.run([sys.executable, "app.py"], env=env)
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down...")
    except Exception as e:
        logger.error(f"❌ Error starting web app: {e}")

def main():
    """Main startup function"""
    print("🤖 Azra Bano AI Agent")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        logger.info("\n💡 To install dependencies, run:")
        logger.info("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check environment
    env_ok = check_env_file()
    
    # Run tests if environment is configured
    if env_ok:
        if not run_tests():
            logger.warning("⚠️  Tests failed, but continuing...")
    
    # Start the application
    print("\n" + "=" * 30)
    print("🎯 Choose an option:")
    print("1. Start web interface (recommended)")
    print("2. Start CLI interface")
    print("3. Run tests only")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                start_web_app()
                break
            elif choice == '2':
                logger.info("🚀 Starting CLI interface...")
                subprocess.run([sys.executable, "cli.py"])
                break
            elif choice == '3':
                run_tests()
                break
            elif choice == '4':
                logger.info("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            logger.info("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()


