import chromadb
from chromadb.config import Settings
import json
import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import os
from config import Config

logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="azra_bano_knowledge",
            metadata={"description": "Knowledge base about Azra Bano"}
        )
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def process_website_data(self, website_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process website data into chunks for vector storage"""
        chunks = []
        
        if not website_data:
            return chunks
            
        # Process title
        if website_data.get('title'):
            chunks.append({
                'content': f"Website Title: {website_data['title']}",
                'source': 'website',
                'type': 'title'
            })
        
        # Process meta description
        if website_data.get('meta_description'):
            chunks.append({
                'content': f"Website Description: {website_data['meta_description']}",
                'source': 'website',
                'type': 'description'
            })
        
        # Process headings
        if website_data.get('headings'):
            for i, heading in enumerate(website_data['headings']):
                if heading.strip():
                    chunks.append({
                        'content': f"Website Section: {heading}",
                        'source': 'website',
                        'type': 'heading',
                        'order': i
                    })
        
        # Process main text content in chunks
        if website_data.get('text_content'):
            text = website_data['text_content']
            # Split into sentences and create chunks
            sentences = text.split('. ')
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < 500:  # Max chunk size
                    current_chunk += sentence + ". "
                else:
                    if current_chunk.strip():
                        chunks.append({
                            'content': current_chunk.strip(),
                            'source': 'website',
                            'type': 'content'
                        })
                    current_chunk = sentence + ". "
            
            # Add remaining chunk
            if current_chunk.strip():
                chunks.append({
                    'content': current_chunk.strip(),
                    'source': 'website',
                    'type': 'content'
                })
        
        return chunks
    
    def process_linkedin_data(self, linkedin_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process LinkedIn data into chunks for vector storage"""
        chunks = []
        
        if not linkedin_data:
            return chunks
        
        # Process name
        if linkedin_data.get('name'):
            chunks.append({
                'content': f"LinkedIn Name: {linkedin_data['name']}",
                'source': 'linkedin',
                'type': 'name'
            })
        
        # Process headline
        if linkedin_data.get('headline'):
            chunks.append({
                'content': f"LinkedIn Headline: {linkedin_data['headline']}",
                'source': 'linkedin',
                'type': 'headline'
            })
        
        # Process about section
        if linkedin_data.get('about'):
            chunks.append({
                'content': f"LinkedIn About: {linkedin_data['about']}",
                'source': 'linkedin',
                'type': 'about'
            })
        
        # Process experience
        if linkedin_data.get('experience'):
            experience_text = "LinkedIn Experience: " + "; ".join(linkedin_data['experience'])
            chunks.append({
                'content': experience_text,
                'source': 'linkedin',
                'type': 'experience'
            })
        
        # Process education
        if linkedin_data.get('education'):
            education_text = "LinkedIn Education: " + "; ".join(linkedin_data['education'])
            chunks.append({
                'content': education_text,
                'source': 'linkedin',
                'type': 'education'
            })
        
        # Process full text in chunks
        if linkedin_data.get('full_text'):
            text = linkedin_data['full_text']
            sentences = text.split('. ')
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < 500:
                    current_chunk += sentence + ". "
                else:
                    if current_chunk.strip():
                        chunks.append({
                            'content': current_chunk.strip(),
                            'source': 'linkedin',
                            'type': 'full_content'
                        })
                    current_chunk = sentence + ". "
            
            if current_chunk.strip():
                chunks.append({
                    'content': current_chunk.strip(),
                    'source': 'linkedin',
                    'type': 'full_content'
                })
        
        return chunks
    
    def add_data_to_knowledge_base(self, scraped_data: Dict[str, Any]):
        """Add scraped data to the knowledge base"""
        try:
            all_chunks = []
            
            # Process website data
            if 'website' in scraped_data:
                website_chunks = self.process_website_data(scraped_data['website'])
                all_chunks.extend(website_chunks)
            
            # Process LinkedIn data
            if 'linkedin' in scraped_data:
                linkedin_chunks = self.process_linkedin_data(scraped_data['linkedin'])
                all_chunks.extend(linkedin_chunks)
            
            # Add chunks to vector database
            if all_chunks:
                documents = [chunk['content'] for chunk in all_chunks]
                metadatas = [
                    {
                        'source': chunk['source'],
                        'type': chunk['type'],
                        'order': chunk.get('order', 0)
                    }
                    for chunk in all_chunks
                ]
                ids = [f"{chunk['source']}_{chunk['type']}_{i}" for i, chunk in enumerate(all_chunks)]
                
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                
                logger.info(f"Added {len(all_chunks)} chunks to knowledge base")
                return True
            else:
                logger.warning("No data chunks to add to knowledge base")
                return False
                
        except Exception as e:
            logger.error(f"Error adding data to knowledge base: {e}")
            return False
    
    def search_knowledge_base(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search the knowledge base for relevant information"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                        'distance': results['distances'][0][i] if results['distances'] and results['distances'][0] else 0
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': self.collection.name
            }
        except Exception as e:
            logger.error(f"Error getting knowledge base stats: {e}")
            return {'error': str(e)}
    
    def clear_knowledge_base(self):
        """Clear all data from the knowledge base"""
        try:
            self.client.delete_collection(self.collection.name)
            self.collection = self.client.create_collection(
                name="azra_bano_knowledge",
                metadata={"description": "Knowledge base about Azra Bano"}
            )
            logger.info("Knowledge base cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing knowledge base: {e}")
            return False


