"""
Multi-Dimensional Code Quality Scorer

Implements advanced quality scoring algorithms for comprehensive code analysis.
"""

import ast
import re
import math
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from collections import defaultdict
import subprocess
import json
import logging

from .models import QualityMetrics
from .config import QUALITY_THRESHOLDS, STATIC_ANALYSIS_TOOLS, get_config

logger = logging.getLogger(__name__)

class MultiDimensionalScorer:
    """
    Advanced quality scoring system that analyzes code across multiple dimensions.
    Integrates with enhanced-repository-analyzer.py for comprehensive assessment.
    """
    
    def __init__(self):
        self.thresholds = QUALITY_THRESHOLDS
        self.tools_config = STATIC_ANALYSIS_TOOLS
        self._init_scoring_weights()
    
    def _init_scoring_weights(self):
        """Initialize scoring weights for different metrics"""
        self.metric_weights = {
            "maintainability": {
                "cyclomatic_complexity": 0.3,
                "cognitive_complexity": 0.25,
                "lines_of_code": 0.15,
                "duplication": 0.15,
                "coupling": 0.15
            },
            "readability": {
                "naming_quality": 0.25,
                "comment_ratio": 0.20,
                "line_length": 0.15,
                "nesting_depth": 0.20,
                "consistency": 0.20
            },
            "security": {
                "vulnerability_count": 0.40,
                "unsafe_patterns": 0.30,
                "input_validation": 0.20,
                "crypto_usage": 0.10
            },
            "performance": {
                "algorithm_efficiency": 0.35,
                "memory_usage": 0.25,
                "io_operations": 0.20,
                "caching_usage": 0.20
            }
        }
    
    def score_file(self, file_path: str, content: Optional[str] = None) -> QualityMetrics:
        """
        Score a single file across all quality dimensions.
        
        Args:
            file_path: Path to the file
            content: Optional file content (will read if not provided)
            
        Returns:
            QualityMetrics with scores for all dimensions
        """
        # Read content if not provided
        if content is None:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # Calculate individual dimension scores
        scores = {
            "maintainability_score": self._score_maintainability(content, file_path),
            "complexity_score": self._score_complexity(content),
            "readability_score": self._score_readability(content),
            "test_coverage": self._get_test_coverage(file_path),
            "documentation_score": self._score_documentation(content),
            "security_score": self._score_security(content, file_path),
            "performance_score": self._score_performance(content)
        }
        
        # Create metrics object
        metrics = QualityMetrics(**scores, overall_score=0.0)
        metrics.calculate_overall()
        
        return metrics
    
    def score_project(self, project_path: str, 
                     file_patterns: List[str] = None) -> Dict[str, Any]:
        """
        Score an entire project.
        
        Args:
            project_path: Root path of the project
            file_patterns: File patterns to include (e.g., ["*.py", "*.js"])
            
        Returns:
            Dictionary with project-wide metrics and file-level scores
        """
        project_path = Path(project_path)
        
        # Default patterns
        if file_patterns is None:
            file_patterns = ["*.py", "*.js", "*.java", "*.cpp", "*.go"]
        
        # Collect all files
        files_to_analyze = []
        for pattern in file_patterns:
            files_to_analyze.extend(project_path.rglob(pattern))
        
        # Filter out excluded patterns
        excluded = get_config("excluded_patterns", [])
        files_to_analyze = [
            f for f in files_to_analyze
            if not any(excl in str(f) for excl in excluded)
        ]
        
        # Score each file
        file_scores = {}
        for file_path in files_to_analyze:
            try:
                score = self.score_file(str(file_path))
                file_scores[str(file_path)] = score
            except Exception as e:
                logger.warning(f"Failed to score {file_path}: {str(e)}")
        
        # Calculate aggregate metrics
        if file_scores:
            avg_metrics = self._calculate_average_metrics(list(file_scores.values()))
        else:
            avg_metrics = QualityMetrics(
                maintainability_score=0, complexity_score=0, readability_score=0,
                test_coverage=0, documentation_score=0, security_score=0,
                performance_score=0, overall_score=0
            )
        
        return {
            "project_metrics": avg_metrics,
            "file_scores": file_scores,
            "summary": self._generate_project_summary(file_scores),
            "recommendations": self._generate_project_recommendations(avg_metrics)
        }
    
    def _score_maintainability(self, content: str, file_path: str) -> float:
        """Calculate maintainability score"""
        scores = {}
        
        # Cyclomatic complexity
        complexity = self._calculate_cyclomatic_complexity(content)
        scores["cyclomatic_complexity"] = self._normalize_complexity_score(complexity)
        
        # Lines of code
        loc = len([line for line in content.splitlines() if line.strip()])
        scores["lines_of_code"] = self._normalize_loc_score(loc)
        
        # Code duplication (simplified check)
        duplication_ratio = self._estimate_duplication(content)
        scores["duplication"] = 100 * (1 - duplication_ratio)
        
        # Coupling (import analysis)
        coupling_score = self._analyze_coupling(content)
        scores["coupling"] = coupling_score
        
        # Cognitive complexity (simplified)
        cognitive_complexity = self._estimate_cognitive_complexity(content)
        scores["cognitive_complexity"] = self._normalize_complexity_score(cognitive_complexity)
        
        # Weighted average
        total_score = 0
        total_weight = 0
        
        for metric, score in scores.items():
            weight = self.metric_weights["maintainability"].get(metric, 0.2)
            total_score += score * weight
            total_weight += weight
        
        return round(total_score / total_weight if total_weight > 0 else 0, 2)
    
    def _score_complexity(self, content: str) -> float:
        """Calculate complexity score (inverse of complexity)"""
        try:
            tree = ast.parse(content)
            
            # Count different complexity factors
            complexity_factors = {
                "branches": 0,  # if, elif, else
                "loops": 0,     # for, while
                "exceptions": 0, # try, except
                "functions": 0,  # def
                "classes": 0,    # class
                "nested_levels": 0
            }
            
            max_nesting = 0
            
            class ComplexityVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.nesting_level = 0
                    
                def visit_If(self, node):
                    complexity_factors["branches"] += 1
                    self.nesting_level += 1
                    nonlocal max_nesting
                    max_nesting = max(max_nesting, self.nesting_level)
                    self.generic_visit(node)
                    self.nesting_level -= 1
                
                def visit_For(self, node):
                    complexity_factors["loops"] += 1
                    self.nesting_level += 1
                    nonlocal max_nesting
                    max_nesting = max(max_nesting, self.nesting_level)
                    self.generic_visit(node)
                    self.nesting_level -= 1
                
                def visit_While(self, node):
                    complexity_factors["loops"] += 1
                    self.nesting_level += 1
                    nonlocal max_nesting
                    max_nesting = max(max_nesting, self.nesting_level)
                    self.generic_visit(node)
                    self.nesting_level -= 1
                
                def visit_Try(self, node):
                    complexity_factors["exceptions"] += 1
                    self.generic_visit(node)
                
                def visit_FunctionDef(self, node):
                    complexity_factors["functions"] += 1
                    self.generic_visit(node)
                
                def visit_ClassDef(self, node):
                    complexity_factors["classes"] += 1
                    self.generic_visit(node)
            
            visitor = ComplexityVisitor()
            visitor.visit(tree)
            
            complexity_factors["nested_levels"] = max_nesting
            
            # Calculate complexity score
            # Lower complexity = higher score
            total_complexity = (
                complexity_factors["branches"] * 2 +
                complexity_factors["loops"] * 3 +
                complexity_factors["exceptions"] * 2 +
                complexity_factors["nested_levels"] * 4
            )
            
            # Normalize to 0-100 scale
            if total_complexity == 0:
                return 100.0
            elif total_complexity < 10:
                return 90.0
            elif total_complexity < 20:
                return 80.0
            elif total_complexity < 40:
                return 70.0
            elif total_complexity < 60:
                return 60.0
            else:
                return max(30.0, 100.0 - total_complexity)
            
        except:
            # If parsing fails, return moderate score
            return 50.0
    
    def _score_readability(self, content: str) -> float:
        """Calculate readability score"""
        scores = {}
        
        # Naming quality (simplified check for snake_case/camelCase consistency)
        naming_score = self._check_naming_consistency(content)
        scores["naming_quality"] = naming_score
        
        # Comment ratio
        comment_ratio = self._calculate_comment_ratio(content)
        scores["comment_ratio"] = min(100, comment_ratio * 200)  # Target 50% comments
        
        # Line length
        line_length_score = self._check_line_length(content)
        scores["line_length"] = line_length_score
        
        # Nesting depth
        nesting_score = self._check_nesting_depth(content)
        scores["nesting_depth"] = nesting_score
        
        # Consistency (indentation, spacing)
        consistency_score = self._check_consistency(content)
        scores["consistency"] = consistency_score
        
        # Weighted average
        total_score = 0
        total_weight = 0
        
        for metric, score in scores.items():
            weight = self.metric_weights["readability"].get(metric, 0.2)
            total_score += score * weight
            total_weight += weight
        
        return round(total_score / total_weight if total_weight > 0 else 0, 2)
    
    def _score_documentation(self, content: str) -> float:
        """Calculate documentation score"""
        try:
            tree = ast.parse(content)
            
            total_items = 0
            documented_items = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    total_items += 1
                    if ast.get_docstring(node):
                        documented_items += 1
            
            if total_items == 0:
                return 100.0  # No documentable items
            
            doc_ratio = documented_items / total_items
            
            # Also check for inline comments
            lines = content.splitlines()
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            comment_bonus = min(20, comment_lines * 2)  # Up to 20 bonus points
            
            return min(100, round(doc_ratio * 80 + comment_bonus, 2))
            
        except:
            # Fallback to simple comment counting
            lines = content.splitlines()
            comment_lines = sum(1 for line in lines if '#' in line or '"""' in line or "'''" in line)
            total_lines = len([l for l in lines if l.strip()])
            
            if total_lines == 0:
                return 0.0
            
            return min(100, round((comment_lines / total_lines) * 200, 2))
    
    def _score_security(self, content: str, file_path: str) -> float:
        """Calculate security score"""
        vulnerabilities = 0
        
        # Check for common security issues
        security_patterns = [
            (r'eval\s*\(', 5),  # eval usage
            (r'exec\s*\(', 5),  # exec usage
            (r'pickle\.loads', 3),  # unsafe deserialization
            (r'subprocess\.call.*shell=True', 4),  # shell injection
            (r'os\.system', 3),  # command injection
            (r'\.format\(.*request\.', 2),  # format string vulnerability
            (r'password\s*=\s*["\']', 2),  # hardcoded password
            (r'api_key\s*=\s*["\']', 2),  # hardcoded API key
        ]
        
        for pattern, severity in security_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            vulnerabilities += len(matches) * severity
        
        # Run bandit if available
        if self.tools_config.get("bandit", {}).get("enabled", False):
            try:
                bandit_score = self._run_bandit(file_path)
                vulnerabilities += bandit_score
            except:
                pass
        
        # Calculate score (fewer vulnerabilities = higher score)
        if vulnerabilities == 0:
            return 100.0
        elif vulnerabilities < 5:
            return 90.0
        elif vulnerabilities < 10:
            return 75.0
        elif vulnerabilities < 20:
            return 60.0
        else:
            return max(30.0, 100 - vulnerabilities * 2)
    
    def _score_performance(self, content: str) -> float:
        """Calculate performance score"""
        performance_issues = 0
        
        # Check for common performance anti-patterns
        perf_patterns = [
            (r'for .* in .*:\s*for .* in .*:', 3),  # Nested loops
            (r'\.append\(.*\)\s*for', 2),  # List comprehension opportunity
            (r're\.compile.*for', 2),  # Regex compilation in loop
            (r'open\(.*\)(?!.*with)', 2),  # File not using context manager
            (r'global\s+\w+', 1),  # Global variable usage
        ]
        
        for pattern, severity in perf_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            performance_issues += len(matches) * severity
        
        # Check for optimization opportunities
        optimization_score = self._check_optimization_opportunities(content)
        
        # Combine scores
        base_score = max(30, 100 - performance_issues * 5)
        final_score = (base_score * 0.7) + (optimization_score * 0.3)
        
        return round(final_score, 2)
    
    def _get_test_coverage(self, file_path: str) -> float:
        """Get test coverage for the file"""
        # This would integrate with coverage.py or similar tools
        # For now, return a placeholder
        
        # Simple heuristic: check if test file exists
        path = Path(file_path)
        test_file_patterns = [
            path.parent / f"test_{path.name}",
            path.parent / f"{path.stem}_test.py",
            path.parent.parent / "tests" / path.name,
        ]
        
        for test_path in test_file_patterns:
            if test_path.exists():
                return 80.0  # Assume good coverage if tests exist
        
        return 40.0  # Assume poor coverage if no tests found
    
    # Helper methods
    
    def _calculate_cyclomatic_complexity(self, content: str) -> int:
        """Calculate cyclomatic complexity"""
        try:
            tree = ast.parse(content)
            complexity = 1
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
                elif isinstance(node, ast.ExceptHandler):
                    complexity += 1
            
            return complexity
        except:
            return 10  # Default moderate complexity
    
    def _normalize_complexity_score(self, complexity: int) -> float:
        """Normalize complexity to 0-100 score"""
        if complexity <= 5:
            return 100.0
        elif complexity <= 10:
            return 90.0
        elif complexity <= 15:
            return 75.0
        elif complexity <= 20:
            return 60.0
        elif complexity <= 30:
            return 45.0
        else:
            return max(20.0, 100 - complexity)
    
    def _normalize_loc_score(self, loc: int) -> float:
        """Normalize lines of code to score"""
        if loc <= 50:
            return 100.0
        elif loc <= 100:
            return 90.0
        elif loc <= 200:
            return 75.0
        elif loc <= 500:
            return 60.0
        else:
            return max(30.0, 100 - (loc / 20))
    
    def _estimate_duplication(self, content: str) -> float:
        """Estimate code duplication ratio"""
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if not lines:
            return 0.0
        
        # Simple duplication check
        line_counts = defaultdict(int)
        for line in lines:
            if len(line) > 10:  # Ignore short lines
                line_counts[line] += 1
        
        duplicated_lines = sum(count - 1 for count in line_counts.values() if count > 1)
        return duplicated_lines / len(lines) if lines else 0.0
    
    def _analyze_coupling(self, content: str) -> float:
        """Analyze coupling based on imports"""
        import_lines = [line for line in content.splitlines() 
                       if line.strip().startswith(('import ', 'from '))]
        
        # Fewer imports = less coupling = higher score
        import_count = len(import_lines)
        
        if import_count <= 5:
            return 100.0
        elif import_count <= 10:
            return 85.0
        elif import_count <= 20:
            return 70.0
        else:
            return max(40.0, 100 - import_count * 2)
    
    def _estimate_cognitive_complexity(self, content: str) -> int:
        """Estimate cognitive complexity (simplified)"""
        complexity = 0
        
        # Count cognitive complexity factors
        patterns = [
            (r'\bif\b', 1),
            (r'\belif\b', 1),
            (r'\belse\b', 1),
            (r'\bfor\b', 1),
            (r'\bwhile\b', 1),
            (r'\btry\b', 2),
            (r'\bexcept\b', 1),
            (r'\band\b', 1),
            (r'\bor\b', 1),
            (r'\bnot\b', 1),
            (r'lambda', 2),
            (r'\breturn\b.*\bif\b', 2),  # Conditional return
        ]
        
        for pattern, weight in patterns:
            matches = len(re.findall(pattern, content))
            complexity += matches * weight
        
        return complexity
    
    def _check_naming_consistency(self, content: str) -> float:
        """Check naming consistency"""
        # Extract variable and function names
        snake_case = re.findall(r'\b[a-z_][a-z0-9_]*\b', content)
        camel_case = re.findall(r'\b[a-z][a-zA-Z0-9]*\b', content)
        
        if not snake_case and not camel_case:
            return 100.0
        
        # Check which style is dominant
        snake_ratio = len(snake_case) / (len(snake_case) + len(camel_case))
        
        # Consistency score (prefer one style)
        consistency = max(snake_ratio, 1 - snake_ratio)
        
        return round(consistency * 100, 2)
    
    def _calculate_comment_ratio(self, content: str) -> float:
        """Calculate ratio of comments to code"""
        lines = content.splitlines()
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        comment_lines = [l for l in lines if l.strip().startswith('#')]
        
        total_lines = len(code_lines) + len(comment_lines)
        if total_lines == 0:
            return 0.0
        
        return len(comment_lines) / total_lines
    
    def _check_line_length(self, content: str) -> float:
        """Check line length compliance"""
        lines = content.splitlines()
        long_lines = sum(1 for line in lines if len(line) > 80)
        
        if not lines:
            return 100.0
        
        compliance_ratio = 1 - (long_lines / len(lines))
        return round(compliance_ratio * 100, 2)
    
    def _check_nesting_depth(self, content: str) -> float:
        """Check nesting depth"""
        max_depth = 0
        current_depth = 0
        
        for line in content.splitlines():
            # Simple indentation-based check
            indent = len(line) - len(line.lstrip())
            depth = indent // 4  # Assuming 4-space indentation
            
            if depth > current_depth:
                current_depth = depth
                max_depth = max(max_depth, current_depth)
            elif depth < current_depth:
                current_depth = depth
        
        # Score based on max depth
        if max_depth <= 3:
            return 100.0
        elif max_depth <= 5:
            return 80.0
        elif max_depth <= 7:
            return 60.0
        else:
            return max(30.0, 100 - max_depth * 10)
    
    def _check_consistency(self, content: str) -> float:
        """Check code consistency (indentation, spacing)"""
        lines = content.splitlines()
        
        # Check indentation consistency
        indents = []
        for line in lines:
            if line and line[0] in ' \t':
                indent = len(line) - len(line.lstrip())
                indents.append(indent)
        
        if not indents:
            return 100.0
        
        # Check if indents are multiples of a common value (2 or 4)
        common_indent = 4  # Assume 4-space default
        consistent_indents = sum(1 for i in indents if i % common_indent == 0)
        
        consistency_score = (consistent_indents / len(indents)) * 100 if indents else 100
        
        return round(consistency_score, 2)
    
    def _check_optimization_opportunities(self, content: str) -> float:
        """Check for optimization opportunities"""
        opportunities = 0
        
        # Patterns that could be optimized
        optimization_patterns = [
            (r'list\(\)', 'Use [] instead of list()'),
            (r'dict\(\)', 'Use {} instead of dict()'),
            (r'== True', 'Use implicit truth checking'),
            (r'== False', 'Use "not" for false checking'),
            (r'len\(.*\) > 0', 'Use implicit truth checking for collections'),
        ]
        
        for pattern, _ in optimization_patterns:
            if re.search(pattern, content):
                opportunities += 1
        
        # Score based on opportunities found
        if opportunities == 0:
            return 100.0
        else:
            return max(60.0, 100 - opportunities * 10)
    
    def _run_bandit(self, file_path: str) -> int:
        """Run bandit security scanner"""
        try:
            result = subprocess.run(
                ['bandit', '-f', 'json', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                report = json.loads(result.stdout)
                # Count issues by severity
                issues = report.get('results', [])
                severity_weights = {'HIGH': 5, 'MEDIUM': 3, 'LOW': 1}
                
                total_score = sum(
                    severity_weights.get(issue['issue_severity'], 1)
                    for issue in issues
                )
                
                return total_score
        except:
            pass
        
        return 0
    
    def _calculate_average_metrics(self, metrics_list: List[QualityMetrics]) -> QualityMetrics:
        """Calculate average metrics from a list"""
        if not metrics_list:
            return QualityMetrics(
                maintainability_score=0, complexity_score=0, readability_score=0,
                test_coverage=0, documentation_score=0, security_score=0,
                performance_score=0, overall_score=0
            )
        
        avg_scores = {}
        for field in QualityMetrics.__fields__:
            if field != "overall_score":
                values = [getattr(m, field) for m in metrics_list]
                avg_scores[field] = sum(values) / len(values)
        
        avg_metrics = QualityMetrics(**avg_scores, overall_score=0)
        avg_metrics.calculate_overall()
        
        return avg_metrics
    
    def _generate_project_summary(self, file_scores: Dict[str, QualityMetrics]) -> Dict[str, Any]:
        """Generate project summary from file scores"""
        if not file_scores:
            return {"total_files": 0, "quality_distribution": {}}
        
        scores = [m.overall_score for m in file_scores.values()]
        
        return {
            "total_files": len(file_scores),
            "average_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "quality_distribution": {
                "excellent": sum(1 for s in scores if s >= self.thresholds["excellent"]),
                "good": sum(1 for s in scores if self.thresholds["good"] <= s < self.thresholds["excellent"]),
                "acceptable": sum(1 for s in scores if self.thresholds["acceptable"] <= s < self.thresholds["good"]),
                "critical": sum(1 for s in scores if s < self.thresholds["acceptable"])
            }
        }
    
    def _generate_project_recommendations(self, metrics: QualityMetrics) -> List[str]:
        """Generate recommendations based on project metrics"""
        recommendations = []
        
        # Check each dimension
        if metrics.maintainability_score < self.thresholds["acceptable"]:
            recommendations.append("Improve maintainability: reduce complexity and coupling")
        
        if metrics.complexity_score < self.thresholds["acceptable"]:
            recommendations.append("Reduce code complexity: break down large functions and reduce nesting")
        
        if metrics.readability_score < self.thresholds["good"]:
            recommendations.append("Enhance readability: improve naming and add comments")
        
        if metrics.test_coverage < 60:
            recommendations.append("Increase test coverage: add unit tests for critical functions")
        
        if metrics.documentation_score < self.thresholds["acceptable"]:
            recommendations.append("Add documentation: write docstrings for public APIs")
        
        if metrics.security_score < self.thresholds["good"]:
            recommendations.append("Address security issues: fix vulnerabilities and unsafe patterns")
        
        if metrics.performance_score < self.thresholds["acceptable"]:
            recommendations.append("Optimize performance: address algorithmic inefficiencies")
        
        return recommendations