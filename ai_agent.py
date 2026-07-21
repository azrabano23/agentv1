import openai
import logging
from typing import Dict, List, Any, Optional
from web_scraper import WebScraper
from knowledge_base import KnowledgeBase
from config import Config

logger = logging.getLogger(__name__)

class AzraBanoAgent:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.web_scraper = WebScraper()
        self.knowledge_base = KnowledgeBase()
        self.is_initialized = False
        
    def initialize_knowledge_base(self, force_refresh: bool = False) -> bool:
        """Initialize the knowledge base by scraping data"""
        try:
            if not force_refresh and self.knowledge_base.get_knowledge_base_stats().get('total_documents', 0) > 0:
                logger.info("Knowledge base already initialized")
                self.is_initialized = True
                return True
            
            logger.info("Initializing knowledge base...")
            
            # Scrape data from all sources
            scraped_data = self.web_scraper.scrape_all_sources()
            
            if not scraped_data:
                logger.error("No data scraped from sources")
                return False
            
            # Clear existing knowledge base if force refresh
            if force_refresh:
                self.knowledge_base.clear_knowledge_base()
            
            # Add data to knowledge base
            success = self.knowledge_base.add_data_to_knowledge_base(scraped_data)
            
            if success:
                self.is_initialized = True
                logger.info("Knowledge base initialized successfully")
                return True
            else:
                logger.error("Failed to add data to knowledge base")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing knowledge base: {e}")
            return False
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question about Azra Bano using the knowledge base"""
        try:
            if not self.is_initialized:
                logger.warning("Knowledge base not initialized. Initializing now...")
                if not self.initialize_knowledge_base():
                    return {
                        'answer': 'Sorry, I am unable to access information about Azra Bano at the moment. Please try again later.',
                        'sources': [],
                        'error': 'Knowledge base initialization failed'
                    }
            
            # Search knowledge base for relevant information
            search_results = self.knowledge_base.search_knowledge_base(question, n_results=5)
            
            if not search_results:
                return {
                    'answer': 'I don\'t have enough information to answer that question about Azra Bano. Please try asking something else.',
                    'sources': [],
                    'confidence': 'low'
                }
            
            # Prepare context for AI
            context = self._prepare_context(search_results)
            
            # Generate answer using OpenAI
            answer = self._generate_answer(question, context, search_results)
            
            return {
                'answer': answer,
                'sources': [result['metadata'] for result in search_results],
                'confidence': self._calculate_confidence(search_results),
                'context_used': len(search_results)
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                'answer': 'Sorry, I encountered an error while processing your question. Please try again.',
                'sources': [],
                'error': str(e)
            }
    
    def _prepare_context(self, search_results: List[Dict[str, Any]]) -> str:
        """Prepare context from search results for AI processing"""
        context_parts = []
        
        for result in search_results:
            source = result['metadata'].get('source', 'unknown')
            content_type = result['metadata'].get('type', 'content')
            content = result['content']
            
            context_parts.append(f"Source: {source} ({content_type})\nContent: {content}\n")
        
        return "\n".join(context_parts)
    
    def _generate_answer(self, question: str, context: str, search_results: List[Dict[str, Any]]) -> str:
        """Generate answer using OpenAI API"""
        try:
            system_prompt = """You are Azra Bano's AI assistant - think GenZ meets YC startup energy. You're badass, fire, and protecting privacy like a boss.

Your vibe:
- GenZ/YC college dropout energy - confident, direct, slightly rebellious
- Use casual, modern language but stay professional
- Drop some tech/startup slang when appropriate
- Be protective of Azra's privacy like you're her ride-or-die
- Sound like you're from the future but grounded

Your role:
1. Give fire answers based on the context provided
2. Be conversational and real - no corporate BS
3. If you don't have the info, be honest about it
4. Cite sources when you can (website/LinkedIn)
5. Keep it concise but informative
6. PRIVACY FIRST: For questions about specific employers, companies, or personal details, acknowledge but redirect to public info only
7. For questions like "Does Azra work at ___" or "Provide proof Azra works here" or "How did Azra get ___", be like "Yo, I can only share what's publicly available on her website and LinkedIn. For anything else, hit her up directly."
8. Never spill specific employment details, company names, or personal info that could be used for verification

Context information:
{context}

Answer this question about Azra Bano with that GenZ/YC energy:"""

            user_prompt = f"{question}"

            response = self.openai_client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt.format(context=context)},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=Config.MAX_CONTEXT_LENGTH,
                temperature=Config.TEMPERATURE
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating answer with OpenAI: {e}")
            return "I'm sorry, I'm having trouble generating an answer right now. Please try again later."
    
    def _calculate_confidence(self, search_results: List[Dict[str, Any]]) -> str:
        """Calculate confidence level based on search results"""
        if not search_results:
            return 'low'
        
        # Calculate average distance (lower is better)
        avg_distance = sum(result.get('distance', 1.0) for result in search_results) / len(search_results)
        
        # Adjust confidence thresholds for better scoring
        if avg_distance < 0.4:
            return 'high'
        elif avg_distance < 0.7:
            return 'medium'
        else:
            return 'low'
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get the current status of the agent"""
        try:
            kb_stats = self.knowledge_base.get_knowledge_base_stats()
            
            return {
                'is_initialized': self.is_initialized,
                'knowledge_base_stats': kb_stats,
                'openai_configured': bool(Config.OPENAI_API_KEY),
                'website_url': Config.PERSONAL_WEBSITE,
                'linkedin_url': Config.LINKEDIN_URL
            }
        except Exception as e:
            logger.error(f"Error getting agent status: {e}")
            return {'error': str(e)}
    
    def refresh_knowledge_base(self) -> bool:
        """Refresh the knowledge base with fresh data"""
        logger.info("Refreshing knowledge base...")
        return self.initialize_knowledge_base(force_refresh=True)
    
    def get_sample_questions(self) -> List[str]:
        """Get sample questions that the agent can answer"""
        return [
            "What does Azra do?",
            "What's Azra's background?",
            "What's Azra's vibe?",
            "How can I reach Azra?",
            "What's Azra building?",
            "What's Azra's story?",
            "What's Azra into?",
            "How do I connect with Azra?",
            "What's Azra's current hustle?",
            "What's Azra's superpower?"
        ]
