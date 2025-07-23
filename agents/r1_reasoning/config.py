"""
Configuration management for R1 Reasoning Engine

Handles environment variables, model settings, and AAI integration.
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path

# Load environment variables (fallback if dotenv not available)
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).resolve().parent.parent.parent
    dotenv_path = project_root / '.env'
    load_dotenv(dotenv_path, override=True)
except ImportError:
    # Fallback: just use os.getenv without dotenv
    pass


class R1ReasoningConfig:
    """Configuration for R1 Reasoning Engine with AAI patterns"""
    
    # Model Configuration
    REASONING_MODEL = os.getenv("R1_REASONING_MODEL", "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B")
    TOOL_MODEL = os.getenv("R1_TOOL_MODEL", "meta-llama/Llama-3.3-70B-Instruct")
    EMBEDDING_MODEL = os.getenv("R1_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Inference Configuration
    DEFAULT_BACKEND = os.getenv("R1_INFERENCE_BACKEND", "huggingface")
    HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # AAI Configuration
    AAI_MIN_CONFIDENCE = float(os.getenv("AAI_MIN_CONFIDENCE", "0.70"))
    AAI_MAX_CONFIDENCE = float(os.getenv("AAI_MAX_CONFIDENCE", "0.95"))
    AAI_TARGET_CONFIDENCE = float(os.getenv("AAI_TARGET_CONFIDENCE", "0.85"))
    
    # Vector Store Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "data/chroma_db")
    VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", "384"))
    
    # Research Configuration
    JINA_API_KEY = os.getenv("JINA_API_KEY")
    JINA_BASE_URL = os.getenv("JINA_BASE_URL", "https://r.jina.ai")
    
    # Processing Configuration
    MAX_TOKENS = int(os.getenv("R1_MAX_TOKENS", "4096"))
    REASONING_TEMPERATURE = float(os.getenv("R1_REASONING_TEMPERATURE", "0.3"))
    TOOL_TEMPERATURE = float(os.getenv("R1_TOOL_TEMPERATURE", "0.1"))
    TIMEOUT_SECONDS = int(os.getenv("R1_TIMEOUT_SECONDS", "60"))
    MAX_RETRIES = int(os.getenv("R1_MAX_RETRIES", "3"))
    
    # Document Processing
    CHUNK_SIZE = int(os.getenv("R1_CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("R1_CHUNK_OVERLAP", "200"))
    MIN_CHUNK_SIZE = int(os.getenv("R1_MIN_CHUNK_SIZE", "100"))
    MAX_DOCUMENTS_PER_QUERY = int(os.getenv("R1_MAX_DOCUMENTS", "20"))
    
    # API Configuration
    API_HOST = os.getenv("R1_API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("R1_API_PORT", "8000"))
    API_WORKERS = int(os.getenv("R1_API_WORKERS", "1"))
    
    # UI Configuration
    GRADIO_HOST = os.getenv("R1_GRADIO_HOST", "0.0.0.0")
    GRADIO_PORT = int(os.getenv("R1_GRADIO_PORT", "7860"))
    GRADIO_SHARE = os.getenv("R1_GRADIO_SHARE", "false").lower() == "true"
    
    # Logging and Monitoring
    LOG_LEVEL = os.getenv("R1_LOG_LEVEL", "INFO")
    ENABLE_METRICS = os.getenv("R1_ENABLE_METRICS", "true").lower() == "true"
    METRICS_INTERVAL = int(os.getenv("R1_METRICS_INTERVAL", "300"))  # 5 minutes
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "missing_optional": []
        }
        
        # Required configurations
        required_configs = [
            ("HUGGINGFACE_API_TOKEN", cls.HUGGINGFACE_API_TOKEN, "HuggingFace API access")
        ]
        
        for config_name, config_value, description in required_configs:
            if not config_value:
                validation_results["errors"].append(f"Missing required config: {config_name} ({description})")
                validation_results["valid"] = False
        
        # Optional but recommended configurations
        optional_configs = [
            ("OPENROUTER_API_KEY", cls.OPENROUTER_API_KEY, "Alternative model access"),
            ("SUPABASE_URL", cls.SUPABASE_URL, "Cloud vector storage"),
            ("JINA_API_KEY", cls.JINA_API_KEY, "Research content discovery")
        ]
        
        for config_name, config_value, description in optional_configs:
            if not config_value:
                validation_results["missing_optional"].append(f"Optional config missing: {config_name} ({description})")
        
        # Validate numeric ranges
        if not (0.70 <= cls.AAI_MIN_CONFIDENCE <= 0.95):
            validation_results["errors"].append("AAI_MIN_CONFIDENCE must be between 0.70 and 0.95")
            validation_results["valid"] = False
            
        if not (0.70 <= cls.AAI_MAX_CONFIDENCE <= 0.95):
            validation_results["errors"].append("AAI_MAX_CONFIDENCE must be between 0.70 and 0.95")
            validation_results["valid"] = False
            
        if cls.AAI_MIN_CONFIDENCE > cls.AAI_MAX_CONFIDENCE:
            validation_results["errors"].append("AAI_MIN_CONFIDENCE cannot be greater than AAI_MAX_CONFIDENCE")
            validation_results["valid"] = False
        
        # Validate temperature ranges
        if not (0.0 <= cls.REASONING_TEMPERATURE <= 1.0):
            validation_results["warnings"].append("REASONING_TEMPERATURE outside recommended range 0.0-1.0")
            
        if not (0.0 <= cls.TOOL_TEMPERATURE <= 1.0):
            validation_results["warnings"].append("TOOL_TEMPERATURE outside recommended range 0.0-1.0")
        
        return validation_results
    
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """Get model configuration for inference"""
        return {
            "reasoning_model": cls.REASONING_MODEL,
            "tool_model": cls.TOOL_MODEL,
            "embedding_model": cls.EMBEDDING_MODEL,
            "max_tokens": cls.MAX_TOKENS,
            "reasoning_temperature": cls.REASONING_TEMPERATURE,
            "tool_temperature": cls.TOOL_TEMPERATURE,
            "timeout_seconds": cls.TIMEOUT_SECONDS,
            "max_retries": cls.MAX_RETRIES
        }
    
    @classmethod
    def get_vector_config(cls) -> Dict[str, Any]:
        """Get vector store configuration"""
        return {
            "supabase_url": cls.SUPABASE_URL,
            "supabase_key": cls.SUPABASE_SERVICE_ROLE_KEY,
            "chroma_persist_directory": cls.CHROMA_PERSIST_DIRECTORY,
            "vector_dimension": cls.VECTOR_DIMENSION,
            "chunk_size": cls.CHUNK_SIZE,
            "chunk_overlap": cls.CHUNK_OVERLAP,
            "min_chunk_size": cls.MIN_CHUNK_SIZE
        }
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Get API server configuration"""
        return {
            "host": cls.API_HOST,
            "port": cls.API_PORT,
            "workers": cls.API_WORKERS,
            "log_level": cls.LOG_LEVEL
        }
    
    @classmethod
    def get_ui_config(cls) -> Dict[str, Any]:
        """Get UI configuration"""
        return {
            "host": cls.GRADIO_HOST,
            "port": cls.GRADIO_PORT,
            "share": cls.GRADIO_SHARE
        }
    
    @classmethod
    def get_aai_config(cls) -> Dict[str, Any]:
        """Get AAI-specific configuration"""
        return {
            "min_confidence": cls.AAI_MIN_CONFIDENCE,
            "max_confidence": cls.AAI_MAX_CONFIDENCE,
            "target_confidence": cls.AAI_TARGET_CONFIDENCE,
            "enable_metrics": cls.ENABLE_METRICS,
            "metrics_interval": cls.METRICS_INTERVAL
        }


def validate_environment() -> bool:
    """Validate environment setup for R1 reasoning engine"""
    print("🔧 Validating R1 Reasoning Engine Environment...")
    
    validation = R1ReasoningConfig.validate_config()
    
    if validation["valid"]:
        print("✅ Configuration validation passed")
    else:
        print("❌ Configuration validation failed:")
        for error in validation["errors"]:
            print(f"   - {error}")
        return False
    
    if validation["warnings"]:
        print("⚠️ Configuration warnings:")
        for warning in validation["warnings"]:
            print(f"   - {warning}")
    
    if validation["missing_optional"]:
        print("📝 Missing optional configurations:")
        for missing in validation["missing_optional"]:
            print(f"   - {missing}")
    
    # Test critical dependencies
    try:
        import transformers
        print(f"✅ Transformers available: {transformers.__version__}")
    except ImportError:
        print("❌ Transformers not available - install with: pip install transformers")
        return False
    
    try:
        import requests
        # Test HuggingFace API if token provided
        if R1ReasoningConfig.HUGGINGFACE_API_TOKEN:
            response = requests.get(
                "https://huggingface.co/api/whoami",
                headers={"Authorization": f"Bearer {R1ReasoningConfig.HUGGINGFACE_API_TOKEN}"},
                timeout=10
            )
            if response.status_code == 200:
                print("✅ HuggingFace API access validated")
            else:
                print("⚠️ HuggingFace API token may be invalid")
    except Exception as e:
        print(f"⚠️ Could not validate HuggingFace API: {e}")
    
    print("🚀 Environment validation complete")
    return True


if __name__ == "__main__":
    validate_environment()