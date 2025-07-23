"""
Memory Enhancement Configuration

Configuration settings for AAI memory enhancement system.
Integrates with existing AAI environment variables and patterns.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MemoryConfig:
    """Configuration for AAI memory enhancement system"""
    
    # Supabase configuration (using existing AAI patterns)
    supabase_url: str = None
    supabase_key: str = None
    
    # OpenRouter configuration (using existing AAI patterns)
    openrouter_api_key: str = None
    
    # Jina API configuration
    jina_api_key: str = None
    
    # Memory storage configuration
    memory_table_prefix: str = "aai_mem0_"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    
    # Memory quality thresholds (AAI standards)
    min_confidence: float = 0.70
    target_confidence: float = 0.85
    max_confidence: float = 0.95
    
    # Memory retention settings
    max_memory_age_days: int = 90
    max_memories_per_user: int = 10000
    cleanup_threshold: float = 0.5  # Quality score below which memories are cleaned
    
    # Performance settings
    memory_search_limit: int = 10
    memory_cache_ttl: int = 3600  # 1 hour in seconds
    vector_search_limit: int = 50
    
    # User preferences
    enable_user_learning: bool = True
    enable_pattern_capture: bool = True
    enable_cross_session_memory: bool = True
    
    # Integration settings
    enable_aai_brain_logging: bool = True
    enable_supabase_auto_offload: bool = True
    
    def __post_init__(self):
        """Initialize configuration from environment variables"""
        # Load from environment variables if not provided
        if not self.supabase_url:
            self.supabase_url = os.getenv('SUPABASE_URL')
        if not self.supabase_key:
            self.supabase_key = os.getenv('SUPABASE_KEY')
        if not self.openrouter_api_key:
            self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.jina_api_key:
            self.jina_api_key = os.getenv('JINA_API_KEY')
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        required_vars = [
            ('supabase_url', self.supabase_url),
            ('supabase_key', self.supabase_key),
            ('openrouter_api_key', self.openrouter_api_key)
        ]
        
        missing_vars = [var_name for var_name, value in required_vars if not value]
        
        if missing_vars:
            print(f"Missing required environment variables: {missing_vars}")
            return False
        
        return True
    
    def get_supabase_config(self) -> Dict[str, str]:
        """Get Supabase configuration dictionary"""
        return {
            'url': self.supabase_url,
            'key': self.supabase_key
        }
    
    def get_openrouter_config(self) -> Dict[str, Any]:
        """Get OpenRouter configuration dictionary"""
        return {
            'api_key': self.openrouter_api_key,
            'model': self.embedding_model,
            'dimensions': self.embedding_dimensions
        }
    
    def get_jina_config(self) -> Dict[str, str]:
        """Get Jina API configuration dictionary"""
        return {
            'api_key': self.jina_api_key
        }
    
    def get_memory_storage_config(self) -> Dict[str, Any]:
        """Get memory storage configuration"""
        return {
            'table_prefix': self.memory_table_prefix,
            'max_age_days': self.max_memory_age_days,
            'max_memories_per_user': self.max_memories_per_user,
            'cleanup_threshold': self.cleanup_threshold
        }
    
    def get_confidence_config(self) -> Dict[str, float]:
        """Get confidence scoring configuration"""
        return {
            'min_confidence': self.min_confidence,
            'target_confidence': self.target_confidence,
            'max_confidence': self.max_confidence
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'supabase_config': self.get_supabase_config(),
            'openrouter_config': self.get_openrouter_config(),
            'jina_config': self.get_jina_config(),
            'memory_storage': self.get_memory_storage_config(),
            'confidence': self.get_confidence_config(),
            'performance': {
                'search_limit': self.memory_search_limit,
                'cache_ttl': self.memory_cache_ttl,
                'vector_search_limit': self.vector_search_limit
            },
            'features': {
                'user_learning': self.enable_user_learning,
                'pattern_capture': self.enable_pattern_capture,
                'cross_session_memory': self.enable_cross_session_memory,
                'aai_brain_logging': self.enable_aai_brain_logging,
                'supabase_auto_offload': self.enable_supabase_auto_offload
            }
        }
    
    @classmethod
    def from_env(cls) -> 'MemoryConfig':
        """Create configuration from environment variables"""
        return cls(
            supabase_url=os.getenv('SUPABASE_URL'),
            supabase_key=os.getenv('SUPABASE_KEY'),
            openrouter_api_key=os.getenv('OPENROUTER_API_KEY'),
            jina_api_key=os.getenv('JINA_API_KEY'),
            # Override defaults with env vars if available
            memory_table_prefix=os.getenv('AAI_MEMORY_TABLE_PREFIX', 'aai_mem0_'),
            min_confidence=float(os.getenv('AAI_MIN_CONFIDENCE', '0.70')),
            target_confidence=float(os.getenv('AAI_TARGET_CONFIDENCE', '0.85')),
            max_confidence=float(os.getenv('AAI_MAX_CONFIDENCE', '0.95')),
            max_memory_age_days=int(os.getenv('AAI_MEMORY_MAX_AGE_DAYS', '90')),
            max_memories_per_user=int(os.getenv('AAI_MAX_MEMORIES_PER_USER', '10000')),
            cleanup_threshold=float(os.getenv('AAI_MEMORY_CLEANUP_THRESHOLD', '0.5'))
        )
    
    @classmethod
    def for_testing(cls) -> 'MemoryConfig':
        """Create configuration for testing"""
        return cls(
            supabase_url="test://localhost",
            supabase_key="test-key",
            openrouter_api_key="test-openrouter-key",
            jina_api_key="test-jina-key",
            memory_table_prefix="test_mem0_",
            max_memory_age_days=7,
            max_memories_per_user=100,
            memory_search_limit=5
        )


def load_memory_config() -> MemoryConfig:
    """Load memory configuration with fallbacks"""
    try:
        config = MemoryConfig.from_env()
        
        if not config.validate():
            print("Warning: Memory configuration incomplete, some features may be disabled")
        
        return config
        
    except Exception as e:
        print(f"Failed to load memory configuration: {e}")
        print("Using default configuration")
        return MemoryConfig()


def create_env_template() -> str:
    """Create environment variable template for memory configuration"""
    template = """
# AAI Memory Enhancement Configuration
# Add these to your .env file

# Required: Supabase configuration (should already exist in AAI)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Required: OpenRouter configuration (should already exist in AAI)
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional: Jina API for research content scraping
JINA_API_KEY=your_jina_api_key

# Optional: Memory system tuning
AAI_MEMORY_TABLE_PREFIX=aai_mem0_
AAI_MIN_CONFIDENCE=0.70
AAI_TARGET_CONFIDENCE=0.85
AAI_MAX_CONFIDENCE=0.95
AAI_MEMORY_MAX_AGE_DAYS=90
AAI_MAX_MEMORIES_PER_USER=10000
AAI_MEMORY_CLEANUP_THRESHOLD=0.5
"""
    return template.strip()


def validate_environment() -> Dict[str, bool]:
    """Validate environment setup for memory enhancement"""
    config = MemoryConfig.from_env()
    
    validation_results = {
        'supabase_configured': bool(config.supabase_url and config.supabase_key),
        'openrouter_configured': bool(config.openrouter_api_key),
        'jina_configured': bool(config.jina_api_key),
        'config_valid': config.validate()
    }
    
    return validation_results


if __name__ == "__main__":
    # Test configuration
    print("AAI Memory Enhancement Configuration Test")
    print("=" * 50)
    
    config = load_memory_config()
    print(f"Configuration loaded: {config.validate()}")
    
    validation = validate_environment()
    print("\nEnvironment Validation:")
    for check, status in validation.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {check}: {status}")
    
    if not all(validation.values()):
        print("\nEnvironment Template:")
        print(create_env_template())