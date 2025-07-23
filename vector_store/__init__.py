"""
Vector Storage Layer for R1 Reasoning Engine

Multi-backend vector storage with Supabase pgvector and Chroma support,
optimized for reasoning tasks with AAI patterns.
"""

__version__ = "1.0.0"

# Import classes with fallback handling
try:
    from .supabase_vector_store import SupabaseVectorStore
except ImportError:
    SupabaseVectorStore = None

try:
    from .chroma_manager import ChromaManager
except ImportError:
    ChromaManager = None

try:
    from .retrieval_ranker import RetrievalRanker, RankingStrategy, RankingWeights
except ImportError:
    RetrievalRanker = None
    RankingStrategy = None
    RankingWeights = None

# Import from models
try:
    from agents.r1_reasoning.models import VectorSearchResult, VectorSearchRequest
except ImportError:
    VectorSearchResult = None
    VectorSearchRequest = None

__all__ = [
    "SupabaseVectorStore",
    "ChromaManager", 
    "RetrievalRanker",
    "RankingStrategy",
    "RankingWeights",
    "VectorSearchResult",
    "VectorSearchRequest"
]