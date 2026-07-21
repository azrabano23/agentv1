from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import logging
import os
from ai_agent import AzraBanoAgent
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY
CORS(app)

# Initialize the AI agent
agent = AzraBanoAgent()

@app.route('/')
def index():
    """Main page with chat interface"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get agent status"""
    try:
        status = agent.get_agent_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/initialize', methods=['POST'])
def initialize_agent():
    """Initialize the knowledge base"""
    try:
        force_refresh = request.json.get('force_refresh', False)
        success = agent.initialize_knowledge_base(force_refresh=force_refresh)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Knowledge base initialized successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to initialize knowledge base'
            }), 500
            
    except Exception as e:
        logger.error(f"Error initializing agent: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask a question to the AI agent"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'success': False,
                'message': 'Question cannot be empty'
            }), 400
        
        # Get answer from agent
        result = agent.answer_question(question)
        
        return jsonify({
            'success': True,
            'answer': result['answer'],
            'sources': result.get('sources', []),
            'confidence': result.get('confidence', 'low'),
            'context_used': result.get('context_used', 0)
        })
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return jsonify({
            'success': False,
            'message': 'Error processing your question',
            'error': str(e)
        }), 500

@app.route('/api/sample-questions')
def get_sample_questions():
    """Get sample questions"""
    try:
        questions = agent.get_sample_questions()
        return jsonify({
            'success': True,
            'questions': questions
        })
    except Exception as e:
        logger.error(f"Error getting sample questions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh', methods=['POST'])
def refresh_knowledge_base():
    """Refresh the knowledge base"""
    try:
        success = agent.refresh_knowledge_base()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Knowledge base refreshed successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to refresh knowledge base'
            }), 500
            
    except Exception as e:
        logger.error(f"Error refreshing knowledge base: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=Config.FLASK_DEBUG
    )


