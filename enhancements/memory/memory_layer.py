#!/usr/bin/env python3
"""
AAI Memory Layer - Core Memory Management

Provides the core memory functionality for AAI command enhancement.
Integrates with Supabase for persistent storage and OpenRouter for embeddings.
"""

import os
import json
import asyncio
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path

# Third-party imports
try:
    import numpy as np
    from supabase import create_client, Client
    import requests
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Install with: pip install supabase numpy requests")

from .config import MemoryConfig


@dataclass
class MemoryItem:
    """Core memory item with AAI metadata"""
    id: str
    user_id: str
    content: str
    content_type: str  # 'prp', 'implementation', 'analysis', 'research', etc.
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = None
    confidence_score: float = 0.85  # AAI default confidence
    quality_score: float = 0.0
    usage_count: int = 0
    last_accessed: Optional[datetime] = None
    created_at: Optional[datetime] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_accessed is None:
            self.last_accessed = self.created_at


@dataclass
class MemoryContext:
    """Memory context for command enhancement"""
    similar_items: List[MemoryItem]
    user_preferences: Dict[str, Any]
    confidence_score: float
    query_context: str
    reasoning: str
    
    # Command-specific context attributes
    similar_prps: List[MemoryItem] = None
    implementation_patterns: List[MemoryItem] = None
    analysis_patterns: List[MemoryItem] = None
    research_patterns: List[MemoryItem] = None
    research_findings: List[MemoryItem] = None
    architectural_decisions: List[MemoryItem] = None
    technology_preferences: Dict[str, Any] = None
    successful_solutions: List[MemoryItem] = None
    testing_patterns: List[MemoryItem] = None
    error_patterns: List[MemoryItem] = None
    previous_insights: List[MemoryItem] = None
    successful_approaches: List[MemoryItem] = None
    domain_knowledge: List[MemoryItem] = None
    quality_sources: List[MemoryItem] = None
    scraping_patterns: List[MemoryItem] = None
    build_patterns: List[MemoryItem] = None
    successful_configurations: List[MemoryItem] = None
    successful_test_suites: List[MemoryItem] = None
    documentation_patterns: List[MemoryItem] = None
    successful_documentation: List[MemoryItem] = None
    design_patterns: List[MemoryItem] = None
    successful_designs: List[MemoryItem] = None
    general_patterns: List[MemoryItem] = None
    
    def __post_init__(self):
        # Initialize None fields with empty lists
        for field_name, field_type in self.__annotations__.items():
            if getattr(self, field_name) is None and hasattr(field_type, '__origin__') and field_type.__origin__ is list:
                setattr(self, field_name, [])


class MemoryLayer:
    """
    Core memory management layer for AAI commands.
    
    Provides persistent, cross-session memory capabilities with confidence scoring
    and integration with existing AAI infrastructure (Supabase, OpenRouter).
    """
    
    def __init__(self, config: MemoryConfig):
        self.config = config
        self.supabase_client = None
        self.embedding_cache = {}
        
        # Initialize connections
        self._initialize_supabase()
    
    def _initialize_supabase(self):
        """Initialize Supabase client using existing AAI patterns"""
        try:
            if self.config.supabase_url and self.config.supabase_key:
                self.supabase_client = create_client(
                    self.config.supabase_url,
                    self.config.supabase_key
                )
                print("✅ Supabase client initialized for memory layer")
            else:
                print("⚠️ Supabase not configured, memory will be limited to session-only")
        except Exception as e:
            print(f"❌ Failed to initialize Supabase: {e}")
            self.supabase_client = None
    
    async def store_memory(self, user_id: str, content: str, content_type: str, 
                          metadata: Dict[str, Any] = None, tags: List[str] = None) -> MemoryItem:
        """
        Store a memory item with embedding and metadata.
        
        Args:
            user_id: User identifier for personalized memory
            content: Content to store
            content_type: Type of content (prp, implementation, analysis, etc.)
            metadata: Additional metadata
            tags: Content tags for categorization
        
        Returns:
            MemoryItem with generated ID and embedding
        """
        try:
            # Generate content hash for deduplication
            content_hash = hashlib.md5(content.encode()).hexdigest()
            memory_id = f"{user_id}_{content_type}_{content_hash[:12]}"
            
            # Generate embedding
            embedding = await self._generate_embedding(content)
            
            # Assess memory quality
            quality_score = self._assess_memory_quality(content, metadata, tags)
            
            # Create memory item
            memory_item = MemoryItem(
                id=memory_id,
                user_id=user_id,
                content=content,
                content_type=content_type,
                embedding=embedding,
                metadata=metadata or {},
                confidence_score=self._calculate_storage_confidence(content, metadata),
                quality_score=quality_score,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                tags=tags or []
            )
            
            # Store in Supabase if available
            if self.supabase_client:
                await self._store_in_supabase(memory_item)
            
            return memory_item
            
        except Exception as e:
            print(f"Failed to store memory: {e}")
            # Return minimal memory item even if storage fails
            return MemoryItem(
                id=f"temp_{hashlib.md5(content.encode()).hexdigest()[:8]}",
                user_id=user_id,
                content=content,
                content_type=content_type,
                confidence_score=self.config.min_confidence
            )
    
    async def search_memories(self, user_id: str, query: str, content_type: str = None,
                            limit: int = 10, min_confidence: float = None) -> List[MemoryItem]:
        """
        Search memories using vector similarity and metadata filtering.
        
        Args:
            user_id: User identifier
            query: Search query
            content_type: Filter by content type
            limit: Maximum results to return
            min_confidence: Minimum confidence score
        
        Returns:
            List of relevant memory items sorted by relevance
        """
        try:
            # Use config default if not specified
            if min_confidence is None:
                min_confidence = self.config.min_confidence
            
            # Generate query embedding
            query_embedding = await self._generate_embedding(query)
            
            if self.supabase_client and query_embedding:
                # Vector similarity search in Supabase
                memories = await self._search_supabase_memories(
                    user_id, query_embedding, content_type, limit, min_confidence
                )
            else:
                # Fallback to in-memory search (limited functionality)
                memories = self._search_session_memories(user_id, query, content_type, limit)
            
            # Update access tracking
            for memory in memories:
                await self._update_memory_access(memory)
            
            return memories
            
        except Exception as e:
            print(f"Memory search failed: {e}")
            return []
    
    async def get_command_context(self, command_type: str, query_context: str, user_id: str) -> Optional[MemoryContext]:
        """
        Get comprehensive memory context for command enhancement.
        
        Args:
            command_type: Type of AAI command
            query_context: Context extracted from command arguments
            user_id: User identifier
        
        Returns:
            MemoryContext with relevant memories and user preferences
        """
        try:
            # Get user preferences
            user_preferences = await self._get_user_preferences(user_id)
            
            # Get similar items based on query context
            similar_items = await self.search_memories(
                user_id=user_id,
                query=query_context,
                limit=self.config.memory_search_limit
            )
            
            # Get command-specific context
            command_context = await self._get_command_specific_context(
                command_type, query_context, user_id
            )
            
            # Calculate overall confidence
            confidence_score = self._calculate_context_confidence(
                similar_items, user_preferences, command_context
            )
            
            # Generate reasoning for memory selection
            reasoning = self._generate_context_reasoning(
                similar_items, user_preferences, command_type
            )
            
            # Build comprehensive memory context
            memory_context = MemoryContext(
                similar_items=similar_items,
                user_preferences=user_preferences,
                confidence_score=confidence_score,
                query_context=query_context,
                reasoning=reasoning,
                **command_context  # Unpack command-specific context
            )
            
            return memory_context
            
        except Exception as e:
            print(f"Failed to get command context: {e}")
            return None
    
    async def _get_command_specific_context(self, command_type: str, query_context: str, user_id: str) -> Dict[str, Any]:
        """Get command-specific memory context"""
        context = {}
        
        if command_type == 'generate-prp':
            context['similar_prps'] = await self.search_memories(user_id, query_context, 'prp', 5)
            context['implementation_patterns'] = await self.search_memories(user_id, query_context, 'implementation', 3)
            context['architectural_decisions'] = await self.search_memories(user_id, query_context, 'architecture', 3)
            context['technology_preferences'] = await self._get_technology_preferences(user_id)
        
        elif command_type == 'implement':
            context['implementation_patterns'] = await self.search_memories(user_id, query_context, 'implementation', 5)
            context['successful_solutions'] = await self.search_memories(user_id, query_context, 'solution', 3)
            context['testing_patterns'] = await self.search_memories(user_id, f"{query_context} testing", 'testing', 3)
            context['error_patterns'] = await self.search_memories(user_id, f"{query_context} error", 'error', 2)
        
        elif command_type == 'analyze':
            context['analysis_patterns'] = await self.search_memories(user_id, query_context, 'analysis', 5)
            context['previous_insights'] = await self.search_memories(user_id, query_context, 'insight', 3)
            context['successful_approaches'] = await self.search_memories(user_id, query_context, 'approach', 3)
            context['domain_knowledge'] = await self.search_memories(user_id, query_context, 'knowledge', 3)
        
        elif command_type == 'research':
            context['research_patterns'] = await self.search_memories(user_id, query_context, 'research', 5)
            context['research_findings'] = await self.search_memories(user_id, query_context, 'finding', 5)
            context['quality_sources'] = await self.search_memories(user_id, f"{query_context} source", 'source', 3)
            context['scraping_patterns'] = await self.search_memories(user_id, f"{query_context} scraping", 'scraping', 2)
        
        return context
    
    async def _get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences from stored memories"""
        try:
            if self.supabase_client:
                # Query user preferences from Supabase
                result = self.supabase_client.table(f"{self.config.memory_table_prefix}user_preferences") \
                    .select("*") \
                    .eq("user_id", user_id) \
                    .execute()
                
                if result.data:
                    return result.data[0].get('preferences', {})
            
            # Fallback: extract preferences from recent memories
            recent_memories = await self.search_memories(user_id, "preferences", limit=20)
            return self._extract_preferences_from_memories(recent_memories)
            
        except Exception as e:
            print(f"Failed to get user preferences: {e}")
            return {}
    
    async def _get_technology_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user's technology and tool preferences"""
        tech_memories = await self.search_memories(user_id, "technology preferences", 'preference', 10)
        
        preferences = {
            'languages': [],
            'frameworks': [],
            'tools': [],
            'architectures': []
        }
        
        for memory in tech_memories:
            metadata = memory.metadata
            if 'preferred_language' in metadata:
                preferences['languages'].append(metadata['preferred_language'])
            if 'preferred_framework' in metadata:
                preferences['frameworks'].append(metadata['preferred_framework'])
            if 'preferred_tool' in metadata:
                preferences['tools'].append(metadata['preferred_tool'])
            if 'preferred_architecture' in metadata:
                preferences['architectures'].append(metadata['preferred_architecture'])
        
        return preferences
    
    def _extract_preferences_from_memories(self, memories: List[MemoryItem]) -> Dict[str, Any]:
        """Extract user preferences from memory patterns"""
        preferences = {
            'coding': {},
            'libraries': {},
            'testing': {},
            'documentation': {},
            'analysis': {},
            'architecture': {}
        }
        
        for memory in memories:
            metadata = memory.metadata
            content_type = memory.content_type
            
            # Extract preferences based on content type and metadata
            if content_type == 'implementation' and 'coding_style' in metadata:
                preferences['coding'].update(metadata['coding_style'])
            elif content_type == 'testing' and 'testing_framework' in metadata:
                preferences['testing']['framework'] = metadata['testing_framework']
            elif content_type == 'architecture' and 'architectural_pattern' in metadata:
                preferences['architecture']['pattern'] = metadata['architectural_pattern']
        
        return preferences
    
    async def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using OpenRouter (following AAI patterns)"""
        try:
            # Check cache first
            text_hash = hashlib.md5(text.encode()).hexdigest()
            if text_hash in self.embedding_cache:
                return self.embedding_cache[text_hash]
            
            if not self.config.openrouter_api_key:
                print("OpenRouter API key not configured, embeddings disabled")
                return None
            
            # Use OpenRouter API (following existing AAI patterns)
            headers = {
                'Authorization': f'Bearer {self.config.openrouter_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.config.embedding_model,
                'input': text
            }
            
            response = requests.post(
                'https://openrouter.ai/api/v1/embeddings',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                embedding = data['data'][0]['embedding']
                
                # Cache the embedding
                self.embedding_cache[text_hash] = embedding
                
                return embedding
            else:
                print(f"OpenRouter embedding failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Embedding generation failed: {e}")
            return None
    
    async def _store_in_supabase(self, memory_item: MemoryItem):
        """Store memory item in Supabase following AAI patterns"""
        try:
            table_name = f"{self.config.memory_table_prefix}memories"
            
            # Prepare data for storage
            storage_data = {
                'id': memory_item.id,
                'user_id': memory_item.user_id,
                'content': memory_item.content,
                'content_type': memory_item.content_type,
                'embedding': memory_item.embedding,
                'metadata': memory_item.metadata,
                'confidence_score': memory_item.confidence_score,
                'quality_score': memory_item.quality_score,
                'usage_count': memory_item.usage_count,
                'tags': memory_item.tags,
                'created_at': memory_item.created_at.isoformat(),
                'last_accessed': memory_item.last_accessed.isoformat()
            }
            
            # Use upsert to handle duplicates
            result = self.supabase_client.table(table_name).upsert(storage_data).execute()
            
            if result.data:
                print(f"✅ Memory stored: {memory_item.id}")
            else:
                print(f"⚠️ Memory storage result unclear: {memory_item.id}")
                
        except Exception as e:
            print(f"Failed to store memory in Supabase: {e}")
    
    async def _search_supabase_memories(self, user_id: str, query_embedding: List[float], 
                                      content_type: str, limit: int, min_confidence: float) -> List[MemoryItem]:
        """Search memories in Supabase using vector similarity"""
        try:
            table_name = f"{self.config.memory_table_prefix}memories"
            
            # Build query
            query = self.supabase_client.table(table_name) \
                .select("*") \
                .eq("user_id", user_id) \
                .gte("confidence_score", min_confidence) \
                .limit(limit)
            
            # Add content type filter if specified
            if content_type:
                query = query.eq("content_type", content_type)
            
            result = query.execute()
            
            if not result.data:
                return []
            
            # Convert to MemoryItem objects and calculate similarities
            memories = []
            for item in result.data:
                memory = self._dict_to_memory_item(item)
                
                # Calculate similarity if embeddings available
                if memory.embedding and query_embedding:
                    similarity = self._calculate_cosine_similarity(memory.embedding, query_embedding)
                    memory.metadata['similarity'] = similarity
                
                memories.append(memory)
            
            # Sort by similarity if available, otherwise by confidence
            if any(m.metadata.get('similarity') for m in memories):
                memories.sort(key=lambda m: m.metadata.get('similarity', 0), reverse=True)
            else:
                memories.sort(key=lambda m: m.confidence_score, reverse=True)
            
            return memories[:limit]
            
        except Exception as e:
            print(f"Supabase memory search failed: {e}")
            return []
    
    def _search_session_memories(self, user_id: str, query: str, content_type: str, limit: int) -> List[MemoryItem]:
        """Fallback search for session-only memories"""
        # This would search in-memory storage for current session
        # For now, return empty list as this requires session storage implementation
        return []
    
    def _dict_to_memory_item(self, data: Dict[str, Any]) -> MemoryItem:
        """Convert database dictionary to MemoryItem"""
        return MemoryItem(
            id=data['id'],
            user_id=data['user_id'],
            content=data['content'],
            content_type=data['content_type'],
            embedding=data.get('embedding'),
            metadata=data.get('metadata', {}),
            confidence_score=data.get('confidence_score', self.config.min_confidence),
            quality_score=data.get('quality_score', 0.0),
            usage_count=data.get('usage_count', 0),
            tags=data.get('tags', []),
            created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00')),
            last_accessed=datetime.fromisoformat(data['last_accessed'].replace('Z', '+00:00'))
        )
    
    def _calculate_cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            import numpy as np
            
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Calculate cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
            
        except Exception as e:
            print(f"Similarity calculation failed: {e}")
            return 0.0
    
    def _assess_memory_quality(self, content: str, metadata: Dict[str, Any], tags: List[str]) -> float:
        """Assess the quality of memory content"""
        quality_score = 0.0
        
        # Content length and detail
        if len(content) > 500:
            quality_score += 0.25
        elif len(content) > 100:
            quality_score += 0.15
        
        # Structured content (code, patterns, decisions)
        if any(marker in content.lower() for marker in ['```', 'def ', 'class ', 'function']):
            quality_score += 0.20
        
        # Rich metadata
        if metadata and len(metadata) > 2:
            quality_score += 0.15
        
        # Useful tags
        if tags and len(tags) > 0:
            quality_score += 0.10
        
        # Technical content indicators
        tech_indicators = ['api', 'implementation', 'pattern', 'solution', 'error', 'fix']
        if any(indicator in content.lower() for indicator in tech_indicators):
            quality_score += 0.15
        
        # Success/outcome indicators
        success_indicators = ['success', 'working', 'solved', 'completed', 'effective']
        if any(indicator in content.lower() for indicator in success_indicators):
            quality_score += 0.15
        
        return min(quality_score, 1.0)
    
    def _calculate_storage_confidence(self, content: str, metadata: Dict[str, Any]) -> float:
        """Calculate confidence score for stored memory (AAI 70-95% range)"""
        confidence = self.config.min_confidence  # Start with minimum
        
        # Add confidence based on content richness
        if len(content) > 200:
            confidence += 0.05
        if len(content) > 1000:
            confidence += 0.05
        
        # Add confidence based on metadata richness
        if metadata:
            confidence += min(len(metadata) * 0.02, 0.10)
        
        # Add confidence for structured content
        if any(marker in content for marker in ['```', 'def ', 'class ']):
            confidence += 0.05
        
        # Ensure within AAI range
        return max(self.config.min_confidence, min(confidence, self.config.max_confidence))
    
    def _calculate_context_confidence(self, similar_items: List[MemoryItem], 
                                    user_preferences: Dict[str, Any], 
                                    command_context: Dict[str, Any]) -> float:
        """Calculate confidence for memory context (AAI standards)"""
        confidence = self.config.min_confidence
        
        # Add confidence based on similar items
        if similar_items:
            avg_item_confidence = sum(item.confidence_score for item in similar_items) / len(similar_items)
            confidence += (avg_item_confidence - self.config.min_confidence) * 0.5
        
        # Add confidence based on user preferences
        if user_preferences:
            confidence += min(len(user_preferences) * 0.02, 0.10)
        
        # Add confidence based on command-specific context
        if command_context:
            context_items = sum(len(items) for items in command_context.values() if isinstance(items, list))
            confidence += min(context_items * 0.01, 0.10)
        
        return max(self.config.min_confidence, min(confidence, self.config.max_confidence))
    
    def _generate_context_reasoning(self, similar_items: List[MemoryItem], 
                                  user_preferences: Dict[str, Any], 
                                  command_type: str) -> str:
        """Generate WHY reasoning for memory context selection"""
        reasoning_parts = []
        
        if similar_items:
            reasoning_parts.append(f"Found {len(similar_items)} relevant memories")
            
            # Add quality information
            high_quality = [item for item in similar_items if item.quality_score > 0.7]
            if high_quality:
                reasoning_parts.append(f"including {len(high_quality)} high-quality items")
        
        if user_preferences:
            pref_count = sum(len(prefs) if isinstance(prefs, dict) else 1 for prefs in user_preferences.values())
            reasoning_parts.append(f"{pref_count} user preferences identified")
        
        # Command-specific reasoning
        if command_type == 'generate-prp':
            reasoning_parts.append("for PRP enhancement with implementation patterns")
        elif command_type == 'implement':
            reasoning_parts.append("for implementation with coding patterns and solutions")
        elif command_type == 'analyze':
            reasoning_parts.append("for analysis with previous insights and methodologies")
        
        if reasoning_parts:
            return "Memory context includes: " + ", ".join(reasoning_parts) + "."
        else:
            return "Limited memory context available for enhancement."
    
    async def _update_memory_access(self, memory: MemoryItem):
        """Update memory access tracking"""
        try:
            memory.usage_count += 1
            memory.last_accessed = datetime.now()
            
            if self.supabase_client:
                table_name = f"{self.config.memory_table_prefix}memories"
                self.supabase_client.table(table_name) \
                    .update({
                        'usage_count': memory.usage_count,
                        'last_accessed': memory.last_accessed.isoformat()
                    }) \
                    .eq('id', memory.id) \
                    .execute()
                    
        except Exception as e:
            print(f"Failed to update memory access: {e}")
    
    async def store_enhancement_event(self, enhancement):
        """Store command enhancement event for learning"""
        try:
            enhancement_content = f"Command: {enhancement.command_type}, Confidence: {enhancement.confidence_score:.2f}"
            
            await self.store_memory(
                user_id=enhancement.original_args.get('user_id', 'system'),
                content=enhancement_content,
                content_type='enhancement_event',
                metadata={
                    'command_type': enhancement.command_type,
                    'confidence_score': enhancement.confidence_score,
                    'had_memory_context': enhancement.memory_context is not None,
                    'timestamp': enhancement.enhancement_timestamp.isoformat()
                },
                tags=['enhancement', 'learning', enhancement.command_type]
            )
            
        except Exception as e:
            print(f"Failed to store enhancement event: {e}")
    
    async def update_user_preferences(self, user_id: str, preference_updates: Dict[str, Any]):
        """Update user preferences based on successful outcomes"""
        try:
            if self.supabase_client:
                table_name = f"{self.config.memory_table_prefix}user_preferences"
                
                # Try to update existing preferences
                result = self.supabase_client.table(table_name) \
                    .select("preferences") \
                    .eq("user_id", user_id) \
                    .execute()
                
                if result.data:
                    # Update existing preferences
                    current_prefs = result.data[0].get('preferences', {})
                    current_prefs.update(preference_updates)
                    
                    self.supabase_client.table(table_name) \
                        .update({'preferences': current_prefs}) \
                        .eq('user_id', user_id) \
                        .execute()
                else:
                    # Create new preferences record
                    self.supabase_client.table(table_name) \
                        .insert({
                            'user_id': user_id,
                            'preferences': preference_updates,
                            'created_at': datetime.now().isoformat(),
                            'updated_at': datetime.now().isoformat()
                        }) \
                        .execute()
                        
        except Exception as e:
            print(f"Failed to update user preferences: {e}")


def test_memory_layer():
    """Test memory layer functionality"""
    import asyncio
    
    async def test_operations():
        config = MemoryConfig.for_testing()
        memory_layer = MemoryLayer(config)
        
        print("Testing Memory Layer")
        print("=" * 30)
        
        # Test memory storage
        memory_item = await memory_layer.store_memory(
            user_id="test_user",
            content="User prefers FastAPI for API development with PostgreSQL database",
            content_type="preference",
            metadata={"domain": "web_development", "confidence": 0.85},
            tags=["fastapi", "postgresql", "api"]
        )
        
        print(f"✅ Memory stored: {memory_item.id}")
        print(f"   Quality score: {memory_item.quality_score:.2f}")
        print(f"   Confidence: {memory_item.confidence_score:.2f}")
        
        # Test memory search
        search_results = await memory_layer.search_memories(
            user_id="test_user",
            query="API development preferences",
            limit=5
        )
        
        print(f"\n🔍 Search results: {len(search_results)} items")
        for item in search_results:
            print(f"   - {item.content_type}: {item.content[:50]}...")
        
        # Test command context
        context = await memory_layer.get_command_context(
            command_type="generate-prp",
            query_context="API authentication system",
            user_id="test_user"
        )
        
        if context:
            print(f"\n🧠 Command context generated:")
            print(f"   Confidence: {context.confidence_score:.2f}")
            print(f"   Similar items: {len(context.similar_items)}")
            print(f"   Reasoning: {context.reasoning}")
        else:
            print("\n⚠️ No command context generated")
    
    asyncio.run(test_operations())


if __name__ == "__main__":
    test_memory_layer()