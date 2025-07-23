"""
Risk Assessment Engine for Code Changes

Provides breaking change prediction and risk assessment for code improvements.
"""

import ast
import re
import json
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass
import logging

from .models import ImprovementRecommendation
from .config import RISK_FACTORS, get_config

logger = logging.getLogger(__name__)

@dataclass
class RiskAssessment:
    """Risk assessment result for a code change"""
    breaking_change_probability: float
    impact_analysis: Dict[str, Any]
    risk_factors: Dict[str, float]
    mitigation_steps: List[str]
    confidence_score: float

class RiskAssessor:
    """
    Assesses risk of code changes and predicts breaking change probability.
    Integrates with r1-reasoning for advanced analysis.
    """
    
    def __init__(self):
        self.risk_factors = RISK_FACTORS
        self.risk_threshold = get_config("risk_threshold_for_approval", 0.7)
        self._init_patterns()
    
    def _init_patterns(self):
        """Initialize risk detection patterns"""
        self.breaking_patterns = {
            # API changes
            "function_signature": re.compile(r"def\s+(\w+)\s*\([^)]*\)"),
            "class_definition": re.compile(r"class\s+(\w+)"),
            "method_removal": re.compile(r"^-\s*def\s+(\w+)", re.MULTILINE),
            "parameter_change": re.compile(r"def\s+\w+\s*\(([^)]+)\)"),
            
            # Import changes
            "import_change": re.compile(r"^[+-]\s*(from\s+\S+\s+)?import\s+", re.MULTILINE),
            
            # Database/Schema
            "schema_change": re.compile(r"(ALTER|CREATE|DROP)\s+(TABLE|INDEX|COLUMN)", re.IGNORECASE),
            "model_field": re.compile(r"(\w+)\s*=\s*(models\.|Column\(|Field\()"),
            
            # Configuration
            "config_change": re.compile(r"(CONFIG|SETTINGS|ENV)\[[\'\"](\w+)[\'\"]\]"),
            "constant_change": re.compile(r"^[A-Z_]+\s*=", re.MULTILINE),
            
            # Dependencies
            "dependency_change": re.compile(r"(requirements\.txt|package\.json|Cargo\.toml|go\.mod)")
        }
    
    def assess_change(self, 
                     file_path: str,
                     original_content: str,
                     modified_content: str,
                     recommendation: Optional[ImprovementRecommendation] = None) -> RiskAssessment:
        """
        Assess risk of a code change.
        
        Args:
            file_path: Path to the file being modified
            original_content: Original file content
            modified_content: Modified file content
            recommendation: Optional improvement recommendation
            
        Returns:
            RiskAssessment with breaking change probability and analysis
        """
        try:
            # Analyze different risk factors
            api_risk = self._assess_api_changes(original_content, modified_content)
            dependency_risk = self._assess_dependency_risk(file_path, modified_content)
            complexity_risk = self._assess_complexity_risk(original_content, modified_content)
            test_impact = self._assess_test_impact(file_path)
            
            # Calculate risk scores
            risk_scores = {
                "api_changes": api_risk * self.risk_factors.get("api_changes", 0.8),
                "dependency_risk": dependency_risk * self.risk_factors.get("dependency_updates", 0.6),
                "complexity": complexity_risk * self.risk_factors.get("refactoring_complexity", 0.4),
                "test_coverage": test_impact * self.risk_factors.get("test_coverage_impact", 0.3)
            }
            
            # Add recommendation-specific risks
            if recommendation:
                if recommendation.category == "architecture":
                    risk_scores["architecture"] = 0.7
                elif recommendation.category == "security":
                    risk_scores["security"] = 0.5
            
            # Calculate overall breaking change probability
            breaking_probability = self._calculate_breaking_probability(risk_scores)
            
            # Generate impact analysis
            impact_analysis = self._analyze_impact(file_path, risk_scores)
            
            # Generate mitigation steps
            mitigation_steps = self._generate_mitigation_steps(risk_scores, breaking_probability)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(original_content, modified_content)
            
            return RiskAssessment(
                breaking_change_probability=breaking_probability,
                impact_analysis=impact_analysis,
                risk_factors=risk_scores,
                mitigation_steps=mitigation_steps,
                confidence_score=confidence
            )
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {str(e)}")
            # Return conservative risk assessment on error
            return RiskAssessment(
                breaking_change_probability=0.8,
                impact_analysis={"error": str(e)},
                risk_factors={"unknown": 0.8},
                mitigation_steps=["Manual review required due to assessment error"],
                confidence_score=0.3
            )
    
    def _assess_api_changes(self, original: str, modified: str) -> float:
        """Assess risk of API changes"""
        risk_score = 0.0
        
        # Check function signature changes
        orig_functions = self.breaking_patterns["function_signature"].findall(original)
        mod_functions = self.breaking_patterns["function_signature"].findall(modified)
        
        # Removed functions = high risk
        removed_functions = set(orig_functions) - set(mod_functions)
        if removed_functions:
            risk_score += 0.9 * len(removed_functions)
        
        # Check parameter changes
        orig_params = self.breaking_patterns["parameter_change"].findall(original)
        mod_params = self.breaking_patterns["parameter_change"].findall(modified)
        
        if orig_params != mod_params:
            risk_score += 0.7
        
        # Check class changes
        orig_classes = self.breaking_patterns["class_definition"].findall(original)
        mod_classes = self.breaking_patterns["class_definition"].findall(modified)
        
        if set(orig_classes) != set(mod_classes):
            risk_score += 0.8
        
        return min(risk_score, 1.0)
    
    def _assess_dependency_risk(self, file_path: str, content: str) -> float:
        """Assess risk of dependency changes"""
        path = Path(file_path)
        
        # Check if it's a dependency file
        if self.breaking_patterns["dependency_change"].search(str(path)):
            return 0.9
        
        # Check import changes
        import_changes = self.breaking_patterns["import_change"].findall(content)
        if import_changes:
            return 0.6
        
        return 0.0
    
    def _assess_complexity_risk(self, original: str, modified: str) -> float:
        """Assess risk based on complexity of changes"""
        try:
            # Calculate cyclomatic complexity difference
            orig_complexity = self._calculate_complexity(original)
            mod_complexity = self._calculate_complexity(modified)
            
            complexity_increase = mod_complexity - orig_complexity
            
            if complexity_increase > 10:
                return 0.8
            elif complexity_increase > 5:
                return 0.5
            elif complexity_increase > 0:
                return 0.3
            else:
                return 0.1
                
        except:
            # If we can't parse, assume moderate risk
            return 0.5
    
    def _calculate_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity of code"""
        try:
            tree = ast.parse(code)
            complexity = 1  # Base complexity
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
                elif isinstance(node, ast.ExceptHandler):
                    complexity += 1
                    
            return complexity
        except:
            return 0
    
    def _assess_test_impact(self, file_path: str) -> float:
        """Assess impact on test coverage"""
        # Check if modifying test files
        if "test" in file_path.lower():
            return 0.2
        
        # Check if modifying core modules
        if any(core in file_path for core in ["models", "api", "core", "utils"]):
            return 0.7
        
        return 0.4
    
    def _calculate_breaking_probability(self, risk_scores: Dict[str, float]) -> float:
        """Calculate overall breaking change probability"""
        if not risk_scores:
            return 0.0
        
        # Weighted average with higher weight for critical factors
        weights = {
            "api_changes": 0.35,
            "dependency_risk": 0.25,
            "complexity": 0.20,
            "test_coverage": 0.10,
            "architecture": 0.05,
            "security": 0.05
        }
        
        total_weight = 0.0
        weighted_sum = 0.0
        
        for factor, score in risk_scores.items():
            weight = weights.get(factor, 0.1)
            weighted_sum += score * weight
            total_weight += weight
        
        if total_weight > 0:
            probability = weighted_sum / total_weight
        else:
            probability = sum(risk_scores.values()) / len(risk_scores)
        
        return round(min(probability, 1.0), 3)
    
    def _analyze_impact(self, file_path: str, risk_scores: Dict[str, float]) -> Dict[str, Any]:
        """Analyze the impact of changes"""
        impact = {
            "affected_modules": self._find_affected_modules(file_path),
            "risk_scores": risk_scores,
            "critical_risks": [k for k, v in risk_scores.items() if v > 0.7],
            "file_type": self._classify_file(file_path)
        }
        
        # Add specific impacts based on file type
        if impact["file_type"] == "api":
            impact["api_compatibility_risk"] = risk_scores.get("api_changes", 0.0)
        elif impact["file_type"] == "model":
            impact["database_migration_required"] = risk_scores.get("api_changes", 0.0) > 0.5
        
        return impact
    
    def _find_affected_modules(self, file_path: str) -> List[str]:
        """Find modules that might be affected by changes to this file"""
        path_parts = Path(file_path).parts
        
        # Simple heuristic - files in same directory and parent
        affected = []
        if len(path_parts) > 1:
            affected.append(path_parts[-2])  # Parent directory
        
        # Add common dependent modules
        if "models" in file_path:
            affected.extend(["api", "serializers", "views"])
        elif "api" in file_path:
            affected.extend(["frontend", "tests", "clients"])
        elif "utils" in file_path:
            affected.append("*")  # Utils affect everything
        
        return list(set(affected))
    
    def _classify_file(self, file_path: str) -> str:
        """Classify the type of file"""
        path_lower = file_path.lower()
        
        if "test" in path_lower:
            return "test"
        elif "api" in path_lower or "view" in path_lower:
            return "api"
        elif "model" in path_lower:
            return "model"
        elif "util" in path_lower or "helper" in path_lower:
            return "utility"
        elif "config" in path_lower or "settings" in path_lower:
            return "configuration"
        else:
            return "general"
    
    def _generate_mitigation_steps(self, risk_scores: Dict[str, float], 
                                  breaking_probability: float) -> List[str]:
        """Generate mitigation steps based on risks"""
        steps = []
        
        if breaking_probability > self.risk_threshold:
            steps.append("⚠️ High risk change - require manual approval")
        
        if risk_scores.get("api_changes", 0) > 0.5:
            steps.extend([
                "Run full API test suite",
                "Update API documentation",
                "Notify API consumers of changes"
            ])
        
        if risk_scores.get("dependency_risk", 0) > 0.5:
            steps.extend([
                "Update dependency lock files",
                "Run dependency security audit",
                "Test in isolated environment first"
            ])
        
        if risk_scores.get("test_coverage", 0) > 0.3:
            steps.extend([
                "Run complete test suite",
                "Check test coverage metrics",
                "Add tests for modified functionality"
            ])
        
        if not steps:
            steps.append("Standard validation: run tests and linting")
        
        return steps
    
    def _calculate_confidence(self, original: str, modified: str) -> float:
        """Calculate confidence in risk assessment"""
        # Base confidence
        confidence = 0.7
        
        # Increase confidence if we can parse the code
        try:
            ast.parse(original)
            ast.parse(modified)
            confidence += 0.1
        except:
            confidence -= 0.2
        
        # Increase confidence based on change size
        lines_changed = abs(len(original.splitlines()) - len(modified.splitlines()))
        if lines_changed < 50:
            confidence += 0.1
        elif lines_changed > 200:
            confidence -= 0.1
        
        return round(max(0.3, min(0.95, confidence)), 2)
    
    def batch_assess(self, changes: List[Tuple[str, str, str]]) -> Dict[str, RiskAssessment]:
        """
        Assess multiple changes in batch.
        
        Args:
            changes: List of (file_path, original_content, modified_content) tuples
            
        Returns:
            Dictionary mapping file paths to risk assessments
        """
        results = {}
        
        for file_path, original, modified in changes:
            results[file_path] = self.assess_change(file_path, original, modified)
        
        return results