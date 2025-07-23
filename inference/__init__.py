"""
Inference Layer for R1 Reasoning Engine

Multi-backend inference with intelligent routing between
HuggingFace, Ollama, and OpenRouter services.
"""
from .model_router import ModelRouter, InferenceRequest, InferenceResponse
from .huggingface_client import HuggingFaceClient
from .ollama_client import OllamaClient

__version__ = "1.0.0"

__all__ = [
    "ModelRouter",
    "InferenceRequest", 
    "InferenceResponse",
    "HuggingFaceClient",
    "OllamaClient"
]