"""
Semantic Chunker for R1 Reasoning Engine

Intelligent document chunking optimized for reasoning tasks
with AAI confidence scoring and quality assessment.
"""
import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ChunkMetadata:
    """Metadata for a document chunk"""
    chunk_index: int
    start_position: int
    end_position: int
    word_count: int
    character_count: int
    chunk_type: str  # "text", "heading", "list", "code", "table"
    content_quality: float = 0.50
    reasoning_relevance: float = 0.50
    confidence_score: float = 0.70  # AAI compliant
    semantic_coherence: float = 0.50
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class DocumentChunk:
    """A semantically coherent chunk of document content"""
    content: str
    metadata: ChunkMetadata
    embedding: Optional[List[float]] = None
    parent_document_id: Optional[str] = None
    overlap_content: Optional[str] = None  # Content that overlaps with adjacent chunks
    

@dataclass
class ChunkingResult:
    """Result of document chunking process"""
    success: bool
    chunks: List[DocumentChunk]
    total_chunks: int = 0
    average_chunk_size: int = 0
    average_confidence: float = 0.70
    average_quality: float = 0.50
    processing_time_ms: int = 0
    chunking_strategy: str = "semantic"
    error_message: Optional[str] = None


class SemanticChunker:
    """
    Semantic document chunker optimized for reasoning tasks.
    
    Features:
    - Semantic boundary detection
    - Reasoning-optimized chunk sizing
    - Content type classification
    - Quality assessment and confidence scoring
    - Overlap handling for context preservation
    - AAI compliance throughout
    """
    
    def __init__(self,
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 min_chunk_size: int = 100,
                 max_chunk_size: int = 2000,
                 preserve_semantic_boundaries: bool = True):
        """Initialize semantic chunker"""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.preserve_semantic_boundaries = preserve_semantic_boundaries
        
        # Semantic boundary patterns
        self.boundary_patterns = self._initialize_boundary_patterns()
        
        # Content type patterns
        self.content_type_patterns = self._initialize_content_type_patterns()
        
        # Quality indicators
        self.quality_indicators = self._initialize_quality_indicators()
    
    def _initialize_boundary_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for detecting semantic boundaries"""
        return {
            "strong": [
                r'\n\s*#+\s+',  # Markdown headers
                r'\n\s*Chapter\s+\d+',  # Chapter headings
                r'\n\s*Section\s+\d+',  # Section headings
                r'\n\s*\d+\.\s+[A-Z]',  # Numbered sections
                r'\n\s*[A-Z][A-Z\s]+\n',  # All caps headings
                r'\n\s*---+\s*\n',  # Horizontal rules
                r'\n\s*===+\s*\n',  # Equals rules
            ],
            "medium": [
                r'\.\s*\n\s*[A-Z]',  # Sentence boundary followed by new paragraph
                r'\n\s*\n\s*[A-Z]',  # Double newline with capital letter
                r'\n\s*•\s+',  # Bullet points
                r'\n\s*-\s+',  # Dash points
                r'\n\s*\d+\)\s+',  # Numbered lists
                r'\n\s*[a-z]\)\s+',  # Lettered lists
            ],
            "weak": [
                r'\.\s+[A-Z]',  # Sentence boundaries
                r';\s+',  # Semicolon boundaries
                r':\s+',  # Colon boundaries
                r',\s+(?=and|but|or|however)',  # Conjunctions
            ]
        }
    
    def _initialize_content_type_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for content type classification"""
        return {
            "heading": [
                r'^#+\s+',  # Markdown headers
                r'^[A-Z][A-Z\s]+$',  # All caps lines
                r'^\d+\.\s+[A-Z]',  # Numbered headers
                r'^Chapter\s+\d+',  # Chapter headings
                r'^Section\s+\d+',  # Section headings
            ],
            "list": [
                r'^\s*•\s+',  # Bullet points
                r'^\s*-\s+',  # Dash points
                r'^\s*\d+\.\s+',  # Numbered lists
                r'^\s*[a-z]\)\s+',  # Lettered lists
                r'^\s*[ivx]+\.\s+',  # Roman numerals
            ],
            "code": [
                r'```',  # Code blocks
                r'^\s*def\s+',  # Function definitions
                r'^\s*class\s+',  # Class definitions
                r'^\s*import\s+',  # Import statements
                r'^\s*from\s+.*import',  # From imports
                r'[{}();]',  # Programming punctuation
            ],
            "table": [
                r'\|.*\|',  # Pipe-separated tables
                r'\t.*\t',  # Tab-separated tables
                r'^\s*\d+\s+\w+\s+\w+',  # Tabular data pattern
            ]
        }
    
    def _initialize_quality_indicators(self) -> Dict[str, List[str]]:
        """Initialize quality indicators for content assessment"""
        return {
            "high_quality": [
                "analysis", "research", "study", "methodology", "results",
                "conclusion", "evidence", "data", "experiment", "theory",
                "algorithm", "implementation", "framework", "architecture"
            ],
            "reasoning_relevant": [
                "because", "therefore", "thus", "consequently", "since",
                "due to", "as a result", "leads to", "causes", "implies",
                "suggests", "indicates", "demonstrates", "proves"
            ],
            "structure_indicators": [
                "introduction", "background", "overview", "summary",
                "discussion", "methodology", "approach", "solution"
            ]
        }
    
    async def chunk_document(self, 
                           content: str,
                           document_id: Optional[str] = None) -> ChunkingResult:
        """
        Chunk document content into semantically coherent pieces.
        
        Args:
            content: Document content to chunk
            document_id: Optional parent document identifier
            
        Returns:
            ChunkingResult with chunks and metadata
        """
        start_time = datetime.now()
        
        try:
            if not content or len(content.strip()) < self.min_chunk_size:
                return ChunkingResult(
                    success=False,
                    chunks=[],
                    error_message="Content too short for chunking"
                )
            
            # Preprocess content
            processed_content = self._preprocess_content(content)
            
            # Detect semantic boundaries
            boundaries = self._detect_semantic_boundaries(processed_content)
            
            # Create initial chunks based on boundaries
            initial_chunks = self._create_initial_chunks(processed_content, boundaries)
            
            # Optimize chunk sizes
            optimized_chunks = self._optimize_chunk_sizes(initial_chunks)
            
            # Add overlap for context preservation
            chunks_with_overlap = self._add_chunk_overlap(optimized_chunks)
            
            # Create DocumentChunk objects with metadata
            document_chunks = []
            for i, chunk_content in enumerate(chunks_with_overlap):
                chunk_metadata = await self._create_chunk_metadata(
                    chunk_content, i, processed_content
                )
                
                document_chunk = DocumentChunk(
                    content=chunk_content,
                    metadata=chunk_metadata,
                    parent_document_id=document_id
                )
                
                document_chunks.append(document_chunk)
            
            # Calculate result metrics
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            result = ChunkingResult(
                success=True,
                chunks=document_chunks,
                total_chunks=len(document_chunks),
                average_chunk_size=sum(len(chunk.content) for chunk in document_chunks) // len(document_chunks) if document_chunks else 0,
                average_confidence=sum(chunk.metadata.confidence_score for chunk in document_chunks) / len(document_chunks) if document_chunks else 0.70,
                average_quality=sum(chunk.metadata.content_quality for chunk in document_chunks) / len(document_chunks) if document_chunks else 0.50,
                processing_time_ms=int(processing_time),
                chunking_strategy="semantic"
            )
            
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"Document chunking failed: {e}")
            
            return ChunkingResult(
                success=False,
                chunks=[],
                processing_time_ms=int(processing_time),
                error_message=str(e)
            )
    
    def _preprocess_content(self, content: str) -> str:
        """Preprocess content for better chunking"""
        
        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Normalize line endings
        content = re.sub(r'\r\n|\r', '\n', content)
        
        # Clean up multiple newlines
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Remove page headers/footers (common patterns)
        content = re.sub(r'\n--- Page \d+ ---\n', '\n', content)
        
        return content.strip()
    
    def _detect_semantic_boundaries(self, content: str) -> List[Tuple[int, str]]:
        """Detect semantic boundaries in content"""
        
        boundaries = []
        
        # Find strong boundaries (high priority)
        for pattern in self.boundary_patterns["strong"]:
            for match in re.finditer(pattern, content, re.MULTILINE):
                boundaries.append((match.start(), "strong"))
        
        # Find medium boundaries if we need more split points
        if len(boundaries) < len(content) // (self.chunk_size * 2):
            for pattern in self.boundary_patterns["medium"]:
                for match in re.finditer(pattern, content, re.MULTILINE):
                    boundaries.append((match.start(), "medium"))
        
        # Find weak boundaries if still need more split points
        if len(boundaries) < len(content) // self.chunk_size:
            for pattern in self.boundary_patterns["weak"]:
                for match in re.finditer(pattern, content):
                    boundaries.append((match.start(), "weak"))
        
        # Sort by position and remove duplicates
        boundaries = sorted(list(set(boundaries)), key=lambda x: x[0])
        
        return boundaries
    
    def _create_initial_chunks(self, content: str, boundaries: List[Tuple[int, str]]) -> List[str]:
        """Create initial chunks based on semantic boundaries"""
        
        if not boundaries:
            # No boundaries found, create chunks by size
            return self._chunk_by_size(content)
        
        chunks = []
        start = 0
        
        for boundary_pos, boundary_type in boundaries:
            # Check if chunk would be appropriate size
            chunk_content = content[start:boundary_pos].strip()
            
            if len(chunk_content) >= self.min_chunk_size:
                chunks.append(chunk_content)
                start = boundary_pos
            elif len(chunk_content) > self.max_chunk_size:
                # Chunk too large, need to split further
                sub_chunks = self._chunk_by_size(chunk_content)
                chunks.extend(sub_chunks)
                start = boundary_pos
        
        # Handle remaining content
        remaining_content = content[start:].strip()
        if remaining_content and len(remaining_content) >= self.min_chunk_size:
            chunks.append(remaining_content)
        elif chunks and remaining_content:
            # Merge with last chunk if too small
            chunks[-1] += "\n" + remaining_content
        
        return [chunk for chunk in chunks if chunk.strip()]
    
    def _chunk_by_size(self, content: str) -> List[str]:
        """Fallback chunking by size when no semantic boundaries"""
        
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + self.chunk_size
            
            if end >= len(content):
                # Last chunk
                chunks.append(content[start:])
                break
            
            # Try to find a good break point near the target size
            break_point = self._find_good_break_point(content, start, end)
            
            chunks.append(content[start:break_point])
            start = break_point
        
        return chunks
    
    def _find_good_break_point(self, content: str, start: int, target_end: int) -> int:
        """Find a good break point near target position"""
        
        # Look for sentence boundaries within 100 characters of target
        search_start = max(start, target_end - 100)
        search_end = min(len(content), target_end + 100)
        
        search_text = content[search_start:search_end]
        
        # Look for sentence endings
        sentence_pattern = r'[.!?]\s+'
        matches = list(re.finditer(sentence_pattern, search_text))
        
        if matches:
            # Find the match closest to our target
            target_relative = target_end - search_start
            best_match = min(matches, key=lambda m: abs(m.end() - target_relative))
            return search_start + best_match.end()
        
        # No good break point found, use target
        return target_end
    
    def _optimize_chunk_sizes(self, chunks: List[str]) -> List[str]:
        """Optimize chunk sizes by merging small chunks or splitting large ones"""
        
        optimized = []
        i = 0
        
        while i < len(chunks):
            current_chunk = chunks[i]
            
            if len(current_chunk) < self.min_chunk_size and i < len(chunks) - 1:
                # Merge with next chunk if both are small
                next_chunk = chunks[i + 1]
                if len(current_chunk) + len(next_chunk) <= self.max_chunk_size:
                    merged = current_chunk + "\n\n" + next_chunk
                    optimized.append(merged)
                    i += 2  # Skip next chunk as it's been merged
                    continue
            
            if len(current_chunk) > self.max_chunk_size:
                # Split large chunk
                sub_chunks = self._chunk_by_size(current_chunk)
                optimized.extend(sub_chunks)
            else:
                optimized.append(current_chunk)
            
            i += 1
        
        return optimized
    
    def _add_chunk_overlap(self, chunks: List[str]) -> List[str]:
        """Add overlap between adjacent chunks for context preservation"""
        
        if self.chunk_overlap == 0 or len(chunks) <= 1:
            return chunks
        
        chunks_with_overlap = []
        
        for i, chunk in enumerate(chunks):
            chunk_with_overlap = chunk
            
            # Add overlap from previous chunk
            if i > 0:
                prev_chunk = chunks[i - 1]
                overlap_text = prev_chunk[-self.chunk_overlap:] if len(prev_chunk) > self.chunk_overlap else prev_chunk
                
                # Find a good break point in the overlap
                sentences = re.split(r'[.!?]\s+', overlap_text)
                if len(sentences) > 1:
                    overlap_text = '. '.join(sentences[-2:])
                
                chunk_with_overlap = overlap_text + "\n\n" + chunk
            
            chunks_with_overlap.append(chunk_with_overlap)
        
        return chunks_with_overlap
    
    async def _create_chunk_metadata(self, 
                                   chunk_content: str, 
                                   chunk_index: int,
                                   full_content: str) -> ChunkMetadata:
        """Create metadata for a chunk"""
        
        # Basic metrics
        word_count = len(chunk_content.split())
        character_count = len(chunk_content)
        
        # Determine chunk type
        chunk_type = self._classify_chunk_type(chunk_content)
        
        # Calculate quality metrics
        content_quality = self._assess_content_quality(chunk_content)
        reasoning_relevance = self._assess_reasoning_relevance(chunk_content)
        semantic_coherence = self._assess_semantic_coherence(chunk_content)
        
        # Calculate confidence score (AAI compliant)
        confidence_score = self._calculate_chunk_confidence(
            chunk_content, content_quality, reasoning_relevance, semantic_coherence
        )
        
        # Find position in full content
        start_position = full_content.find(chunk_content.split('\n\n')[-1][:100])
        if start_position == -1:
            start_position = chunk_index * 1000  # Rough estimate
        
        return ChunkMetadata(
            chunk_index=chunk_index,
            start_position=start_position,
            end_position=start_position + character_count,
            word_count=word_count,
            character_count=character_count,
            chunk_type=chunk_type,
            content_quality=content_quality,
            reasoning_relevance=reasoning_relevance,
            confidence_score=confidence_score,
            semantic_coherence=semantic_coherence
        )
    
    def _classify_chunk_type(self, content: str) -> str:
        """Classify the type of content in a chunk"""
        
        content_lower = content.lower()
        
        # Check each content type
        for content_type, patterns in self.content_type_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.MULTILINE):
                    return content_type
        
        # Default to text
        return "text"
    
    def _assess_content_quality(self, content: str) -> float:
        """Assess content quality of a chunk"""
        
        content_lower = content.lower()
        quality_score = 0.50  # Base quality
        
        # High-quality indicators
        high_quality_count = sum(1 for indicator in self.quality_indicators["high_quality"] 
                               if indicator in content_lower)
        quality_score += min(0.3, high_quality_count * 0.05)
        
        # Structure indicators
        structure_count = sum(1 for indicator in self.quality_indicators["structure_indicators"] 
                            if indicator in content_lower)
        quality_score += min(0.15, structure_count * 0.03)
        
        # Length factor
        if len(content) > 500:
            quality_score += 0.05
        if len(content) > 1000:
            quality_score += 0.05
        
        # Penalize very short or very long chunks
        if len(content) < 100:
            quality_score -= 0.15
        elif len(content) > 2000:
            quality_score -= 0.10
        
        return max(0.0, min(1.0, quality_score))
    
    def _assess_reasoning_relevance(self, content: str) -> float:
        """Assess relevance for reasoning tasks"""
        
        content_lower = content.lower()
        relevance_score = 0.50  # Base relevance
        
        # Reasoning-relevant indicators
        reasoning_count = sum(1 for indicator in self.quality_indicators["reasoning_relevant"] 
                            if indicator in content_lower)
        relevance_score += min(0.25, reasoning_count * 0.04)
        
        # Question and answer patterns
        if '?' in content:
            relevance_score += 0.05
        
        # Decision and analysis patterns
        decision_patterns = ['decision', 'choice', 'option', 'alternative', 'compare', 'versus']
        decision_count = sum(1 for pattern in decision_patterns if pattern in content_lower)
        relevance_score += min(0.15, decision_count * 0.03)
        
        return max(0.0, min(1.0, relevance_score))
    
    def _assess_semantic_coherence(self, content: str) -> float:
        """Assess semantic coherence of chunk content"""
        
        coherence_score = 0.50  # Base coherence
        
        # Check for topic consistency (simplified)
        sentences = re.split(r'[.!?]+', content)
        if len(sentences) > 1:
            # Check for repeated keywords (indicator of topic consistency)
            words = re.findall(r'\b\w+\b', content.lower())
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Only consider longer words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Calculate keyword consistency
            if words:
                repeated_words = sum(1 for freq in word_freq.values() if freq > 1)
                coherence_score += min(0.3, repeated_words / len(set(words)))
        
        # Check for transition words (indicators of logical flow)
        transition_words = [
            'furthermore', 'moreover', 'additionally', 'however', 'nevertheless',
            'therefore', 'thus', 'consequently', 'in contrast', 'similarly'
        ]
        
        transition_count = sum(1 for word in transition_words if word in content.lower())
        coherence_score += min(0.2, transition_count * 0.05)
        
        return max(0.0, min(1.0, coherence_score))
    
    def _calculate_chunk_confidence(self,
                                  content: str,
                                  content_quality: float,
                                  reasoning_relevance: float,
                                  semantic_coherence: float) -> float:
        """Calculate AAI-compliant confidence score for chunk"""
        
        base_confidence = 0.70  # AAI minimum
        
        # Weight the quality factors
        quality_contribution = (
            content_quality * 0.4 +
            reasoning_relevance * 0.35 +
            semantic_coherence * 0.25
        )
        
        # Scale to confidence range
        confidence_boost = (quality_contribution - 0.5) * 0.2
        confidence_score = base_confidence + confidence_boost
        
        # Ensure within AAI range
        return max(0.70, min(0.95, confidence_score))
    
    def get_chunker_status(self) -> Dict[str, Any]:
        """Get chunker configuration and status"""
        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "min_chunk_size": self.min_chunk_size,
            "max_chunk_size": self.max_chunk_size,
            "preserve_semantic_boundaries": self.preserve_semantic_boundaries,
            "boundary_patterns_count": sum(len(patterns) for patterns in self.boundary_patterns.values()),
            "content_type_patterns_count": sum(len(patterns) for patterns in self.content_type_patterns.values()),
            "ready": True
        }


async def test_semantic_chunker():
    """Test semantic chunker functionality"""
    
    chunker = SemanticChunker()
    
    print("🧪 Testing Semantic Chunker")
    print("=" * 30)
    
    # Show chunker status
    status = chunker.get_chunker_status()
    print(f"Chunk size: {status['chunk_size']}")
    print(f"Overlap: {status['chunk_overlap']}")
    print(f"Semantic boundaries: {status['preserve_semantic_boundaries']}")
    print(f"Ready: {status['ready']}")
    
    # Test with sample content
    test_content = """
# Introduction to AI Reasoning Systems

Artificial Intelligence reasoning systems represent a fundamental advancement in computational thinking. These systems are designed to process information, analyze patterns, and draw logical conclusions similar to human cognitive processes.

## Core Components

The architecture of an AI reasoning system typically includes several key components:

1. **Knowledge Base**: A structured repository of facts, rules, and relationships that form the foundation of reasoning.

2. **Inference Engine**: The computational component responsible for applying logical rules to derive new conclusions from existing knowledge.

3. **Working Memory**: A temporary storage area where intermediate results and reasoning steps are maintained during the problem-solving process.

## Reasoning Methods

Different reasoning approaches can be employed depending on the problem domain:

### Deductive Reasoning
Deductive reasoning starts with general principles and applies them to specific cases. This approach guarantees that if the premises are true, the conclusion must also be true.

### Inductive Reasoning  
Inductive reasoning works in the opposite direction, starting with specific observations and building toward general principles. This method is particularly useful for pattern recognition and hypothesis formation.

### Abductive Reasoning
Abductive reasoning involves finding the best explanation for a set of observations. This approach is commonly used in diagnostic systems and fault detection.

## Implementation Considerations

When implementing AI reasoning systems, several factors must be considered:

- **Scalability**: The system must handle increasing amounts of data and complexity
- **Efficiency**: Reasoning processes should be optimized for performance
- **Accuracy**: The system must produce reliable and correct results
- **Maintainability**: The knowledge base and rules should be easy to update and modify

## Conclusion

AI reasoning systems continue to evolve and improve, offering powerful capabilities for automated decision-making and problem-solving across various domains.
"""
    
    print(f"\n📄 Testing with sample content ({len(test_content)} characters)")
    
    result = await chunker.chunk_document(test_content, "test_document")
    
    print(f"\n📊 Chunking Results:")
    print(f"Success: {result.success}")
    print(f"Total chunks: {result.total_chunks}")
    print(f"Average chunk size: {result.average_chunk_size}")
    print(f"Average confidence: {result.average_confidence:.2%}")
    print(f"Average quality: {result.average_quality:.2%}")
    print(f"Processing time: {result.processing_time_ms}ms")
    
    if result.success:
        print(f"\n📝 Chunk Details:")
        for i, chunk in enumerate(result.chunks[:3]):  # Show first 3 chunks
            print(f"\nChunk {i+1}:")
            print(f"  Type: {chunk.metadata.chunk_type}")
            print(f"  Words: {chunk.metadata.word_count}")
            print(f"  Confidence: {chunk.metadata.confidence_score:.2%}")
            print(f"  Quality: {chunk.metadata.content_quality:.2%}")
            print(f"  Content preview: {chunk.content[:100]}...")
        
        if len(result.chunks) > 3:
            print(f"\n... and {len(result.chunks) - 3} more chunks")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_semantic_chunker())