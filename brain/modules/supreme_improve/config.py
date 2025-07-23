"""
Configuration for Supreme Improve module
"""

import os
from typing import Dict, List, Any

# Quality thresholds for different aspects
QUALITY_THRESHOLDS = {
    "critical": 60.0,
    "acceptable": 70.0, 
    "good": 80.0,
    "excellent": 90.0
}

# Analysis timeout settings
ANALYSIS_TIMEOUT = {
    "file_analysis": 30,  # seconds per file
    "project_analysis": 600,  # seconds for entire project
    "recommendation_generation": 120,  # seconds
    "risk_assessment": 60  # seconds
}

# Safety mechanism settings
SAFETY_CHECKS = {
    "enable_preview": True,
    "require_approval_for_high_risk": True,
    "backup_before_changes": True,
    "max_changes_per_file": 50,
    "rollback_on_test_failure": True,
    "risk_threshold_for_approval": 0.7
}

# Machine learning model paths
ML_MODEL_PATHS = {
    "risk_prediction": "brain/models/risk_prediction_model.pkl",
    "quality_scoring": "brain/models/quality_scoring_model.pkl",
    "recommendation_ranking": "brain/models/recommendation_ranking_model.pkl"
}

# Static analysis tool configurations
STATIC_ANALYSIS_TOOLS = {
    "pylint": {
        "enabled": True,
        "config_file": ".pylintrc",
        "min_score": 7.0
    },
    "mypy": {
        "enabled": True,
        "config_file": "mypy.ini",
        "strict_mode": False
    },
    "bandit": {
        "enabled": True,
        "severity_threshold": "medium",
        "confidence_threshold": "medium"
    },
    "radon": {
        "enabled": True,
        "complexity_threshold": 10,
        "maintainability_threshold": "B"
    }
}

# Improvement categories and their weights
IMPROVEMENT_CATEGORIES = {
    "quality": {
        "weight": 0.25,
        "subcategories": ["readability", "consistency", "best_practices"]
    },
    "performance": {
        "weight": 0.20,
        "subcategories": ["optimization", "caching", "algorithm_efficiency"]
    },
    "security": {
        "weight": 0.25,
        "subcategories": ["vulnerability_fixes", "input_validation", "authentication"]
    },
    "maintainability": {
        "weight": 0.20,
        "subcategories": ["modularity", "documentation", "test_coverage"]
    },
    "architecture": {
        "weight": 0.10,
        "subcategories": ["design_patterns", "scalability", "extensibility"]
    }
}

# Risk assessment factors
RISK_FACTORS = {
    "api_changes": 0.8,
    "database_schema_changes": 0.9,
    "core_functionality_changes": 0.7,
    "configuration_changes": 0.5,
    "dependency_updates": 0.6,
    "refactoring_complexity": 0.4,
    "test_coverage_impact": 0.3
}

# Learning system configuration
LEARNING_CONFIG = {
    "min_samples_for_update": 10,
    "success_threshold": 0.8,
    "feedback_weight": 0.3,
    "outcome_weight": 0.7,
    "model_update_frequency": "weekly",
    "data_retention_days": 90
}

# Integration patterns with existing modules
MODULE_INTEGRATION = {
    "enhanced_repository_analyzer": {
        "import_path": "brain.modules.enhanced-repository-analyzer",
        "class_name": "EnhancedRepositoryAnalyzer",
        "methods": ["analyze_repository", "_identify_key_files"]
    },
    "github_analyzer": {
        "import_path": "brain.modules.github-analyzer", 
        "class_name": "GitHubRepositoryAnalyzer",
        "methods": ["analyze_repository", "generate_integration_stubs"]
    },
    "tech_stack_expert": {
        "import_path": "brain.modules.tech_stack_expert",
        "class_name": "TechStackExpertModule",
        "methods": ["provide_expertise", "analyze_architecture"]
    },
    "seamless_orchestrator": {
        "import_path": "brain.modules.seamless-orchestrator",
        "class_name": "SeamlessOrchestrator",
        "methods": ["process_idea", "_evaluate_idea"]
    },
    "unified_analytics": {
        "import_path": "brain.modules.unified-analytics",
        "class_name": "UnifiedAnalytics", 
        "methods": ["track_improvement", "get_success_patterns"]
    }
}

# Logging configuration
LOGGING_CONFIG = {
    "log_level": os.getenv("SUPREME_IMPROVE_LOG_LEVEL", "INFO"),
    "log_file": "brain/logs/improvements/supreme_improve.log",
    "max_log_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# Performance optimization settings
PERFORMANCE_CONFIG = {
    "enable_caching": True,
    "cache_ttl": 3600,  # 1 hour
    "max_cache_size": 100 * 1024 * 1024,  # 100MB
    "parallel_analysis": True,
    "max_workers": min(4, os.cpu_count() or 1),
    "chunk_size": 1000  # lines per chunk for large files
}

# Validation settings
VALIDATION_CONFIG = {
    "run_tests_after_changes": True,
    "test_command": "pytest",
    "lint_after_changes": True,
    "type_check_after_changes": True,
    "security_scan_after_changes": True
}

# Get configuration value with environment override
def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value with environment variable override"""
    env_key = f"SUPREME_IMPROVE_{key.upper()}"
    env_value = os.getenv(env_key)
    
    if env_value is not None:
        # Try to parse as JSON for complex types
        try:
            import json
            return json.loads(env_value)
        except:
            return env_value
    
    # Return from config dictionaries
    for config_dict in [
        QUALITY_THRESHOLDS, ANALYSIS_TIMEOUT, SAFETY_CHECKS,
        ML_MODEL_PATHS, STATIC_ANALYSIS_TOOLS, IMPROVEMENT_CATEGORIES,
        RISK_FACTORS, LEARNING_CONFIG, MODULE_INTEGRATION,
        LOGGING_CONFIG, PERFORMANCE_CONFIG, VALIDATION_CONFIG
    ]:
        if key in config_dict:
            return config_dict[key]
    
    return default