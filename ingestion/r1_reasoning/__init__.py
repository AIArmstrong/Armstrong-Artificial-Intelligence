"""
Document Ingestion Pipeline for R1 Reasoning Engine

Enhanced document processing with AAI patterns including
PDF processing, semantic chunking, and quality assessment.
"""

__version__ = "1.0.0"

# Import components with fallback handling
try:
    from .pdf_processor import PDFProcessor
except ImportError:
    PDFProcessor = None

try:
    from .semantic_chunker import SemanticChunker
except ImportError:
    SemanticChunker = None

try:
    from .jina_research_ingester import JinaResearchIngester
except ImportError:
    JinaResearchIngester = None

__all__ = [
    "PDFProcessor",
    "SemanticChunker", 
    "JinaResearchIngester"
]