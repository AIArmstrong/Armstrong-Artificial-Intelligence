#!/usr/bin/env python3
"""
Command Module Configurations - Defines contextual modules and AI models for each enhanced command
Part of the AAI Supreme Enhancement Framework
"""

from typing import Dict, Any, List, Optional

class CommandModuleConfig:
    """Configuration for command module selection and AI model assignments"""
    
    @staticmethod
    def get_analyze_config() -> Dict[str, Any]:
        """Configuration for /analyze command"""
        return {
            "selected_modules": {
                "MEMORY": {
                    "criteria": ["Pattern History", "Codebase Learning", "Previous Analysis"],
                    "confidence": 0.92
                },
                "HYBRID_RAG": {
                    "criteria": ["Knowledge Synthesis", "Best Practices", "Documentation"],
                    "confidence": 0.89
                },
                "REASONING": {
                    "criteria": ["Complex Logic", "Multi-Step Analysis", "Decision Chains"],
                    "confidence": 0.94
                },
                "RESEARCH": {
                    "criteria": ["Security Research", "Framework Updates", "Vulnerability Scan"],
                    "confidence": 0.87
                },
                "FOUNDATION": {
                    "criteria": ["Quality Baseline", "Compliance Check", "Architecture Validation"],
                    "confidence": 0.91
                }
            },
            "model_assignments": {
                "MEMORY": "Claude-3.5-Sonnet",
                "HYBRID_RAG": "text-embedding-ada-002 (OR)",
                "REASONING": "Claude-3.5-Sonnet", 
                "RESEARCH": "gpt-4o-mini (OR)",
                "FOUNDATION": "Claude-3.5-Haiku",
                "SEMANTIC_INTELLIGENCE": "text-embedding-ada-002 (OR)",
                "CONTRADICTION_DETECTION": "openai/gpt-4o-mini (OR)"
            },
            "creative_cortex_modules": [
                "Code_Health_Timeline",
                "Bug_DNA_Pattern_Mining",
                "Multi_Perspective_Synthesis",
                "Ecosystem_Aware_Integration",
                "Modular_Risk_Ledger"
            ]
        }
    
    @staticmethod
    def get_test_config() -> Dict[str, Any]:
        """Configuration for /test command"""
        return {
            "selected_modules": {
                "MEMORY": {
                    "criteria": ["Test Patterns", "Flaky History", "Coverage Learning"],
                    "confidence": 0.93
                },
                "FOUNDATION": {
                    "criteria": ["Test Coverage", "Quality Gates", "Framework Standards"],
                    "confidence": 0.91
                },
                "REASONING": {
                    "criteria": ["Test Strategy", "Failure Analysis", "Quality Logic"],
                    "confidence": 0.89
                },
                "RESEARCH": {
                    "criteria": ["Testing Best Practices", "Framework Testing", "Tool Research"],
                    "confidence": 0.86
                },
                "ORCHESTRATION": {
                    "criteria": ["Multi-Agent Testing", "Parallel Execution", "Test Coordination"],
                    "confidence": 0.92
                }
            },
            "model_assignments": {
                "MEMORY": "Test-Memory-Engine",
                "FOUNDATION": "Quality-Gate-Pro",
                "REASONING": "Test-Logic-AI",
                "RESEARCH": "Testing-Research-Bot",
                "ORCHESTRATION": "Multi-Agent-Coordinator"
            },
            "creative_cortex_modules": [
                "Flaky_Test_Predictor",
                "User_Flow_Aware_Coverage", 
                "Evolutionary_Test_Generation",
                "Predictive_Quality_Assurance",
                "Test_Intelligence_Analytics"
            ]
        }
    
    @staticmethod
    def get_generate_prp_config() -> Dict[str, Any]:
        """Configuration for /generate-prp command"""
        return {
            "selected_modules": {
                "MEMORY": {
                    "criteria": ["PRP Patterns", "Success History", "Template Learning"],
                    "confidence": 0.95
                },
                "RESEARCH": {
                    "criteria": ["Domain Research", "Technical Documentation", "Industry Standards"],
                    "confidence": 0.91
                },
                "HYBRID_RAG": {
                    "criteria": ["Knowledge Integration", "Best Practice Synthesis", "Reference Compilation"],
                    "confidence": 0.88
                },
                "REASONING": {
                    "criteria": ["Planning Logic", "Risk Assessment", "Strategy Formation"],
                    "confidence": 0.93
                },
                "TOOL_SELECTION": {
                    "criteria": ["Implementation Tools", "Framework Selection", "Technology Stack"],
                    "confidence": 0.87
                }
            },
            "model_assignments": {
                "MEMORY": "PRP-Memory-Bank",
                "RESEARCH": "Deep-Research-Pro",
                "HYBRID_RAG": "Knowledge-Fusion-AI",
                "REASONING": "Strategic-Planner-GPT",
                "TOOL_SELECTION": "Tech-Stack-Advisor"
            },
            "creative_cortex_modules": [
                "Smart_PRP_DNA",
                "Authority_Weighted_Research",
                "Complexity_Aware_Planning", 
                "Auto_Prerequisite_Provisioner",
                "Bias_Gap_Auditor"
            ]
        }
    
    @staticmethod
    def get_build_config() -> Dict[str, Any]:
        """Configuration for /build command (Stage 2)"""
        return {
            "selected_modules": {
                "Memory": {
                    "criteria": ["Build History", "Error Patterns", "Optimization Learning"],
                    "confidence": 0.90
                },
                "Foundation": {
                    "criteria": ["Build Standards", "Quality Gates", "Dependency Management"],
                    "confidence": 0.88
                },
                "Tool Selection": {
                    "criteria": ["Build Tools", "Compiler Selection", "Pipeline Optimization"],
                    "confidence": 0.85
                },
                "Architecture": {
                    "criteria": ["Build Architecture", "Module Dependencies", "System Design"],
                    "confidence": 0.87
                },
                "Research": {
                    "criteria": ["Build Best Practices", "Tool Updates", "Performance Optimization"],
                    "confidence": 0.82
                },
                "Reasoning": {
                    "criteria": ["Build Strategy", "Error Resolution", "Optimization Logic"],
                    "confidence": 0.86
                }
            },
            "model_assignments": {
                "Memory": "Build-Memory-AI",
                "Foundation": "Quality-Foundation",
                "Tool Selection": "Tool-Selector-Pro",
                "Architecture": "Build-Architect",
                "Research": "Dev-Research-Bot",
                "Reasoning": "Build-Logic-Engine"
            }
        }
    
    @staticmethod
    def get_config_for_command(command_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific command"""
        config_map = {
            "/analyze": CommandModuleConfig.get_analyze_config,
            "/test": CommandModuleConfig.get_test_config,
            "/generate-prp": CommandModuleConfig.get_generate_prp_config,
            "/build": CommandModuleConfig.get_build_config,
        }
        
        config_func = config_map.get(command_name)
        return config_func() if config_func else None
    
    @staticmethod
    def get_smart_selection_reasons() -> Dict[str, List[str]]:
        """Common reasons why modules are selected by the smart loader"""
        return {
            "complexity_triggers": [
                "High Complexity Code",
                "Multi-File Analysis", 
                "Large Codebase",
                "Complex Dependencies"
            ],
            "context_triggers": [
                "Security Keywords",
                "Performance Keywords",
                "Architecture Keywords",
                "Testing Keywords"
            ],
            "historical_triggers": [
                "Previous Success Pattern",
                "User Preference Learning",
                "Error Prevention Pattern",
                "Optimization History"
            ],
            "confidence_triggers": [
                "Low Initial Confidence",
                "Uncertain Context",
                "Ambiguous Requirements",
                "Novel Problem Domain"
            ]
        }