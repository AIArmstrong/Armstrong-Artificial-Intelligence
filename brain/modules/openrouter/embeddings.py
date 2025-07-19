"""
Semantic Embeddings Engine for Intent Similarity and Pattern Recognition
"""

import json
import asyncio
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from .router_client import get_openrouter_client
from ..supabase_cache import SupabaseCache, cache_intent_pattern

class EmbeddingsEngine:
    """
    Semantic intelligence for intent matching and pattern recognition
    """
    
    def __init__(self):
        self.client = get_openrouter_client()
        self.cache = SupabaseCache()
        self.similarity_threshold = 0.85
        self.vector_dimension = 1536  # OpenAI ada-002 embedding size
        
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        np_vec1 = np.array(vec1)
        np_vec2 = np.array(vec2)
        
        dot_product = np.dot(np_vec1, np_vec2)
        magnitude1 = np.linalg.norm(np_vec1)
        magnitude2 = np.linalg.norm(np_vec2)
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    async def generate_intent_embedding(self, intent_text: str) -> Optional[List[float]]:
        """
        Generate embedding vector for intent text
        Preprocesses text for better semantic matching
        """
        # Preprocess intent text for better embeddings
        processed_text = self._preprocess_intent(intent_text)
        
        embeddings = await self.client.generate_embeddings([processed_text])
        
        if embeddings and len(embeddings) > 0:
            return embeddings[0]
        
        return None
    
    def _preprocess_intent(self, intent_text: str) -> str:
        """
        Preprocess intent text to improve embedding quality
        """
        # Remove timestamps and IDs
        text = intent_text.lower()
        
        # Extract key terms for better semantic matching
        key_terms = []
        
        # Architecture terms
        if any(term in text for term in ["architecture", "design", "structure", "system"]):
            key_terms.append("system architecture")
        
        # Action terms
        if any(term in text for term in ["implement", "create", "build", "add"]):
            key_terms.append("implementation")
        elif any(term in text for term in ["fix", "correct", "resolve", "debug"]):
            key_terms.append("error resolution")
        elif any(term in text for term in ["enhance", "improve", "optimize", "upgrade"]):
            key_terms.append("enhancement")
        
        # Technology terms
        if any(term in text for term in ["cache", "storage", "database", "supabase"]):
            key_terms.append("data storage")
        
        # Combine original text with key terms
        enhanced_text = f"{intent_text} {' '.join(key_terms)}"
        
        return enhanced_text
    
    async def find_similar_intents(self, current_intent: str, confidence_threshold: float = None) -> List[Dict]:
        """
        Find similar past intents using semantic similarity
        Returns list of similar intents with similarity scores
        """
        threshold = confidence_threshold or self.similarity_threshold
        
        # Generate embedding for current intent
        current_embedding = await self.generate_intent_embedding(current_intent)
        if not current_embedding:
            return []
        
        # Query cached intent patterns
        cached_intents = self.cache.query_by_tags(["#intent", "#pattern"])
        
        similar_intents = []
        
        for cached_intent in cached_intents:
            try:
                cached_value = cached_intent['value']
                
                if 'embedding' in cached_value:
                    cached_embedding = cached_value['embedding']
                    similarity = self.cosine_similarity(current_embedding, cached_embedding)
                    
                    if similarity >= threshold:
                        similar_intents.append({
                            "intent": cached_value.get('intent', ''),
                            "similarity": similarity,
                            "confidence": cached_value.get('confidence', 0.0),
                            "pattern_data": cached_value.get('pattern_data', {}),
                            "timestamp": cached_intent.get('created_at', ''),
                            "cache_id": cached_intent.get('id', '')
                        })
                        
            except Exception as e:
                print(f"Error processing cached intent: {e}")
                continue
        
        # Sort by similarity score (highest first)
        similar_intents.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similar_intents
    
    async def cache_intent_with_embedding(self, intent: str, pattern_data: Dict, confidence: float, tags: List[str] = None) -> str:
        """
        Cache intent pattern with semantic embedding for future similarity matching
        """
        # Generate embedding
        embedding = await self.generate_intent_embedding(intent)
        if not embedding:
            print(f"Failed to generate embedding for intent: {intent}")
            return ""
        
        # Prepare value with embedding
        value = {
            "intent": intent,
            "pattern_data": pattern_data,
            "confidence": confidence,
            "embedding": embedding,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Cache with default intent tags
        default_tags = ["#intent", "#pattern", "#embedding"]
        if tags:
            default_tags.extend(tags)
        
        return self.cache.add_to_batch(f"intent_embedding_{intent}", value, default_tags)
    
    async def analyze_intent_clusters(self) -> Dict[str, List[Dict]]:
        """
        Analyze cached intents to identify clusters and patterns
        """
        cached_intents = self.cache.query_by_tags(["#intent", "#embedding"])
        
        if len(cached_intents) < 2:
            return {}
        
        clusters = {}
        processed_intents = set()
        
        for intent_item in cached_intents:
            intent_id = intent_item.get('id', '')
            
            if intent_id in processed_intents:
                continue
            
            intent_value = intent_item['value']
            current_embedding = intent_value.get('embedding', [])
            
            if not current_embedding:
                continue
            
            # Find similar intents for clustering
            cluster_members = [intent_item]
            processed_intents.add(intent_id)
            
            for other_intent in cached_intents:
                other_id = other_intent.get('id', '')
                
                if other_id == intent_id or other_id in processed_intents:
                    continue
                
                other_embedding = other_intent['value'].get('embedding', [])
                if not other_embedding:
                    continue
                
                similarity = self.cosine_similarity(current_embedding, other_embedding)
                
                if similarity >= 0.75:  # Cluster threshold (lower than similarity threshold)
                    cluster_members.append(other_intent)
                    processed_intents.add(other_id)
            
            # Create cluster if we have multiple members
            if len(cluster_members) > 1:
                cluster_name = self._generate_cluster_name(cluster_members)
                clusters[cluster_name] = cluster_members
        
        return clusters
    
    def _generate_cluster_name(self, cluster_members: List[Dict]) -> str:
        """Generate descriptive name for intent cluster"""
        intents = [member['value'].get('intent', '') for member in cluster_members]
        
        # Analyze common terms
        all_text = ' '.join(intents).lower()
        
        if 'architecture' in all_text or 'system' in all_text:
            return "Architecture & System Design"
        elif 'cache' in all_text or 'storage' in all_text:
            return "Cache & Storage Management"
        elif 'error' in all_text or 'fix' in all_text:
            return "Error Resolution & Debugging"
        elif 'enhance' in all_text or 'improve' in all_text:
            return "Enhancement & Optimization"
        elif 'protocol' in all_text or 'security' in all_text:
            return "Protocol & Security"
        else:
            return f"General Pattern ({len(cluster_members)} items)"
    
    async def get_recommendation_for_intent(self, current_intent: str) -> Optional[Dict]:
        """
        Get AI recommendation based on similar past intents
        """
        similar_intents = await self.find_similar_intents(current_intent)
        
        if not similar_intents:
            return None
        
        best_match = similar_intents[0]
        
        return {
            "recommendation": "Similar intent pattern found",
            "similarity_score": best_match['similarity'],
            "suggested_approach": best_match['pattern_data'],
            "confidence": best_match['confidence'],
            "reference_intent": best_match['intent'],
            "success_indicators": "Based on past success with similar patterns"
        }

# Convenience functions for brain system integration
async def find_similar_patterns(intent_text: str) -> List[Dict]:
    """Find similar intent patterns for current task"""
    engine = EmbeddingsEngine()
    return await engine.find_similar_intents(intent_text)

async def cache_current_intent(intent: str, success_data: Dict, confidence: float, tags: List[str] = None):
    """Cache current intent pattern for future similarity matching"""
    engine = EmbeddingsEngine()
    return await engine.cache_intent_with_embedding(intent, success_data, confidence, tags)

async def get_intent_recommendation(intent: str) -> Optional[Dict]:
    """Get AI recommendation for handling current intent"""
    engine = EmbeddingsEngine()
    return await engine.get_recommendation_for_intent(intent)

if __name__ == "__main__":
    # Test embeddings functionality
    async def test_embeddings():
        engine = EmbeddingsEngine()
        
        # Test embedding generation
        embedding = await engine.generate_intent_embedding("implement cache integration")
        if embedding:
            print(f"Generated embedding with {len(embedding)} dimensions")
        
        # Test caching intent with embedding
        cache_id = await engine.cache_intent_with_embedding(
            "implement cache integration",
            {"approach": "supabase", "tags": ["#cache"]},
            0.9,
            ["#test"]
        )
        print(f"Cached intent with ID: {cache_id}")
        
        # Test similarity search
        similar = await engine.find_similar_intents("build database connection")
        print(f"Found {len(similar)} similar intents")
        
        # Test clustering
        clusters = await engine.analyze_intent_clusters()
        print(f"Identified {len(clusters)} intent clusters")
    
    asyncio.run(test_embeddings())