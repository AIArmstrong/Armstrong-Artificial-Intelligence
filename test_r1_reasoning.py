"""
Test script for R1 Reasoning Engine components

Tests the core reasoning infrastructure without external dependencies.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all components can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from agents.r1_reasoning.models import (
            ReasoningStep, ReasoningChain, ReasoningResponse,
            DocumentAnalysisRequest, ConfidenceAnalysis
        )
        print("✅ R1 reasoning models imported successfully")
    except Exception as e:
        print(f"❌ Failed to import R1 reasoning models: {e}")
        return False
    
    try:
        from agents.r1_reasoning.config import R1ReasoningConfig
        print("✅ R1 reasoning config imported successfully")
    except Exception as e:
        print(f"❌ Failed to import R1 reasoning config: {e}")
        return False
    
    try:
        from inference.model_router import ModelRouter, InferenceRequest, InferenceResponse
        print("✅ Model router imported successfully")
    except Exception as e:
        print(f"❌ Failed to import model router: {e}")
        return False
    
    try:
        from inference.huggingface_client import HuggingFaceClient
        print("✅ HuggingFace client imported successfully")
    except Exception as e:
        print(f"❌ Failed to import HuggingFace client: {e}")
        return False
    
    try:
        from inference.ollama_client import OllamaClient
        print("✅ Ollama client imported successfully")
    except Exception as e:
        print(f"❌ Failed to import Ollama client: {e}")
        return False
    
    try:
        from agents.r1_reasoning.reasoning_engine import ReasoningEngine
        print("✅ Reasoning engine imported successfully")
    except Exception as e:
        print(f"❌ Failed to import reasoning engine: {e}")
        return False
    
    try:
        from agents.r1_reasoning.confidence_scorer import ConfidenceScorer
        print("✅ Confidence scorer imported successfully")
    except Exception as e:
        print(f"❌ Failed to import confidence scorer: {e}")
        return False
    
    return True

def test_config_validation():
    """Test configuration validation"""
    print("\n🔧 Testing configuration validation...")
    
    try:
        from agents.r1_reasoning.config import R1ReasoningConfig
        
        config = R1ReasoningConfig()
        validation = config.validate_config()
        
        print(f"Config validation result: {'✅ Valid' if validation['valid'] else '❌ Invalid'}")
        
        if validation['errors']:
            print("Errors:")
            for error in validation['errors']:
                print(f"  - {error}")
        
        if validation['warnings']:
            print("Warnings:")
            for warning in validation['warnings']:
                print(f"  - {warning}")
        
        if validation['missing_optional']:
            print("Missing optional configs:")
            for missing in validation['missing_optional']:
                print(f"  - {missing}")
        
        return validation['valid']
        
    except Exception as e:
        print(f"❌ Config validation failed: {e}")
        return False

def test_model_creation():
    """Test data model creation"""
    print("\n📊 Testing data model creation...")
    
    try:
        from agents.r1_reasoning.models import (
            ReasoningStep, ReasoningChain, ReasoningMethod,
            ConfidenceAnalysis, DocumentAnalysisRequest
        )
        
        # Test ReasoningStep creation
        step = ReasoningStep(
            step_number=1,
            description="Test reasoning step",
            reasoning="This is a test reasoning step with AAI compliance",
            confidence=0.85,
            evidence=["Test evidence 1", "Test evidence 2"],
            assumptions=["Test assumption"]
        )
        
        assert 0.70 <= step.confidence <= 0.95, "Confidence not in AAI range"
        print("✅ ReasoningStep created successfully")
        
        # Test ReasoningChain creation
        chain = ReasoningChain(
            query="Test query for reasoning",
            steps=[step],
            final_conclusion="Test conclusion with high confidence",
            overall_confidence=0.82,
            reasoning_method=ReasoningMethod.DEDUCTIVE
        )
        
        assert 0.70 <= chain.overall_confidence <= 0.95, "Overall confidence not in AAI range"
        print("✅ ReasoningChain created successfully")
        
        # Test ConfidenceAnalysis creation
        confidence = ConfidenceAnalysis(
            overall=0.80,
            reasoning_confidence=0.75,
            evidence_confidence=0.65,
            source_reliability=0.70,
            assumption_certainty=0.85,
            reasoning_coherence=0.78
        )
        
        assert 0.70 <= confidence.overall <= 0.95, "Overall confidence not in AAI range"
        print("✅ ConfidenceAnalysis created successfully")
        
        # Test DocumentAnalysisRequest creation
        request = DocumentAnalysisRequest(
            query="What are the benefits of using FastAPI?",
            user_id="test_user",
            confidence_threshold=0.75
        )
        
        assert 0.70 <= request.confidence_threshold <= 0.95, "Confidence threshold not in AAI range"
        print("✅ DocumentAnalysisRequest created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False

async def test_confidence_scorer():
    """Test confidence scoring functionality"""
    print("\n🎯 Testing confidence scorer...")
    
    try:
        from agents.r1_reasoning.confidence_scorer import ConfidenceScorer
        from agents.r1_reasoning.models import ReasoningStep, ReasoningChain, ReasoningMethod
        
        scorer = ConfidenceScorer()
        
        # Create test reasoning chain
        steps = [
            ReasoningStep(
                step_number=1,
                description="Analyze system requirements",
                reasoning="The system needs to handle 10,000 concurrent users with sub-200ms response times. Current architecture shows bottlenecks under load.",
                confidence=0.85,
                evidence=["Load testing results", "Performance monitoring data"],
                assumptions=["Traffic patterns remain consistent"]
            ),
            ReasoningStep(
                step_number=2,
                description="Evaluate solution options",
                reasoning="Three main options: horizontal scaling, vertical scaling, or architectural changes. Each has different cost and complexity implications.",
                confidence=0.80,
                evidence=["Industry benchmarks", "Cost analysis"],
                assumptions=["Budget constraints allow for infrastructure changes"]
            )
        ]
        
        test_chain = ReasoningChain(
            query="How should we improve system performance?",
            steps=steps,
            final_conclusion="Recommend horizontal scaling with caching layer for optimal cost-performance ratio",
            overall_confidence=0.82,
            reasoning_method=ReasoningMethod.COMPARATIVE
        )
        
        # Test confidence assessment
        confidence_analysis = await scorer.assess_reasoning_chain(test_chain)
        
        print(f"Overall confidence: {confidence_analysis.overall:.2%}")
        print(f"Reasoning confidence: {confidence_analysis.reasoning_confidence:.2%}")
        print(f"Evidence confidence: {confidence_analysis.evidence_confidence:.2%}")
        
        # Validate AAI compliance
        assert 0.70 <= confidence_analysis.overall <= 0.95, "Overall confidence not in AAI range"
        assert 0.70 <= confidence_analysis.reasoning_confidence <= 0.95, "Reasoning confidence not in AAI range"
        
        print("✅ Confidence scorer working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Confidence scorer test failed: {e}")
        return False

def test_model_router_init():
    """Test model router initialization"""
    print("\n🚦 Testing model router initialization...")
    
    try:
        from inference.model_router import ModelRouter, InferenceRequest
        from agents.r1_reasoning.models import InferenceBackend
        
        router = ModelRouter()
        
        # Test inference request creation
        request = InferenceRequest(
            prompt="Test prompt for reasoning analysis",
            model_type="reasoning",
            max_tokens=1024,
            temperature=0.3
        )
        
        print(f"Model router initialized with strategy: {router.selection_strategy}")
        print(f"Test request created for model type: {request.model_type}")
        
        # Test status method
        status = router.get_model_status()
        print(f"Model status retrieved: {len(status.get('models', {}))} models tracked")
        
        print("✅ Model router initialization successful")
        return True
        
    except Exception as e:
        print(f"❌ Model router initialization failed: {e}")
        return False

async def test_reasoning_engine_init():
    """Test reasoning engine initialization"""
    print("\n🧠 Testing reasoning engine initialization...")
    
    try:
        from agents.r1_reasoning.reasoning_engine import ReasoningEngine
        from agents.r1_reasoning.models import ReasoningDepth
        
        engine = ReasoningEngine()
        
        print(f"Reasoning engine initialized")
        print(f"Available templates: {list(engine.reasoning_templates.keys())}")
        print(f"Model router available: {engine.model_router is not None}")
        
        # Test metrics (should be empty initially)
        metrics = engine.get_reasoning_metrics()
        print(f"Initial metrics: {metrics}")
        
        print("✅ Reasoning engine initialization successful")
        return True
        
    except Exception as e:
        print(f"❌ Reasoning engine initialization failed: {e}")
        return False

async def run_all_tests():
    """Run all available tests"""
    print("🚀 Starting R1 Reasoning Engine Tests")
    print("=" * 50)
    
    test_results = []
    
    # Test imports
    test_results.append(("Imports", test_imports()))
    
    # Test configuration
    test_results.append(("Configuration", test_config_validation()))
    
    # Test data models
    test_results.append(("Data Models", test_model_creation()))
    
    # Test confidence scorer
    test_results.append(("Confidence Scorer", await test_confidence_scorer()))
    
    # Test model router
    test_results.append(("Model Router", test_model_router_init()))
    
    # Test reasoning engine
    test_results.append(("Reasoning Engine", await test_reasoning_engine_init()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} | {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! R1 Reasoning Engine components are working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(run_all_tests())