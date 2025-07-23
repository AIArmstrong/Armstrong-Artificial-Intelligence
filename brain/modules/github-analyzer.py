#!/usr/bin/env python3
"""
GitHub Repository Analyzer & Integrator
Intelligent analysis and integration of external repositories into AAI ecosystem
"""

import asyncio
import ast
import json
import logging
import os
import shlex
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import hashlib
import sqlite3

# Core dependencies
import docker
import git
from git import Repo
import tree_sitter
from tree_sitter import Language, Parser
import requests

# Security scanning
import bandit

# AAI module imports
from brain.modules.analyze_orchestrator import AnalyzeOrchestrator, AnalysisTask
from brain.modules.integration_aware_prp_enhancer import IntegrationAwarePRPEnhancer
from brain.modules.research_prp_integration import ResearchPRPIntegration
from brain.modules.unified_analytics import UnifiedAnalytics

@dataclass
class ExtractedFeature:
    """Represents a feature extracted from repository analysis"""
    name: str
    type: str  # function, class, module, api, pattern
    description: str
    file_path: str
    line_start: int
    line_end: int
    dependencies: List[str]
    api_surface: Dict[str, Any]
    complexity_score: float
    documentation: Optional[str] = None

@dataclass
class SecurityFinding:
    """Security vulnerability or concern found in code"""
    severity: str  # critical, high, medium, low
    type: str
    description: str
    file_path: str
    line_number: int
    remediation: Optional[str] = None

@dataclass
class CompatibilityScore:
    """Compatibility assessment for integration"""
    relevance_score: float      # 0.0-1.0
    quality_score: float        # 0.0-1.0
    complexity_score: float     # 0.0-1.0 (inverse - lower is better)
    reusability_score: float    # 0.0-1.0
    security_score: float       # 0.0-1.0
    overall_score: float        # Weighted average
    rationale: str

@dataclass
class AnalysisReport:
    """Comprehensive repository analysis report"""
    repo_url: str
    repo_name: str
    analysis_id: str
    timestamp: str
    
    # Repository metadata
    language_distribution: Dict[str, float]
    total_lines: int
    file_count: int
    commit_count: int
    last_commit: str
    license: Optional[str]
    
    # Extracted features
    features: List[ExtractedFeature]
    
    # Quality metrics
    test_coverage: Optional[float]
    documentation_score: float
    code_quality_score: float
    
    # Security assessment
    security_findings: List[SecurityFinding]
    security_score: float
    
    # Compatibility assessment
    compatibility_scores: List[CompatibilityScore]
    
    # Integration recommendations
    recommended_features: List[str]
    integration_stubs: Dict[str, str]  # feature_name -> stub_code
    
    # Metadata
    analysis_duration: float
    success: bool
    error_message: Optional[str] = None

class GitCloner:
    """Handles secure repository cloning and management"""
    
    def __init__(self, base_dir: str = "/tmp/aai_repo_analysis"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def clone_repository(self, repo_url: str, max_size_mb: int = 500) -> Path:
        """Clone repository to isolated directory with size limits"""
        # Generate unique directory name
        repo_hash = hashlib.md5(repo_url.encode()).hexdigest()[:8]
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        clone_dir = self.base_dir / f"{repo_name}_{repo_hash}"
        
        # Remove if already exists
        if clone_dir.exists():
            shutil.rmtree(clone_dir)
        
        try:
            logging.info(f"Cloning {repo_url} to {clone_dir}")
            # Clone with depth and size limits
            repo = Repo.clone_from(
                repo_url, 
                clone_dir, 
                depth=1,  # Shallow clone
                single_branch=True,  # Only main branch
                progress=lambda op_code, cur_count, max_count=None, message='': None
            )
            
            # Check repository size
            repo_size_mb = sum(f.stat().st_size for f in clone_dir.rglob('*') if f.is_file()) / (1024 * 1024)
            if repo_size_mb > max_size_mb:
                shutil.rmtree(clone_dir)
                raise Exception(f"Repository too large: {repo_size_mb:.1f}MB > {max_size_mb}MB limit")
            
            logging.info(f"Successfully cloned repository ({repo_size_mb:.1f}MB)")
            return clone_dir
        except Exception as e:
            if clone_dir.exists():
                shutil.rmtree(clone_dir, ignore_errors=True)
            raise Exception(f"Failed to clone repository: {e}")
    
    def cleanup(self, repo_path: Path):
        """Clean up cloned repository"""
        if repo_path.exists():
            shutil.rmtree(repo_path)

class DockerSandbox:
    """Docker-based isolation for safe code analysis"""
    
    def __init__(self):
        self.client = docker.from_env()
        self.image_name = "aai-repo-analyzer:latest"
    
    def build_analysis_image(self):
        """Build Docker image for analysis if not exists"""
        try:
            self.client.images.get(self.image_name)
        except docker.errors.ImageNotFound:
            # Build minimal analysis image
            dockerfile = """
            FROM python:3.11-slim
            RUN apt-get update && apt-get install -y git
            RUN pip install tree-sitter bandit safety
            WORKDIR /analysis
            """
            with tempfile.NamedTemporaryFile(mode='w', suffix='.dockerfile', delete=False) as f:
                f.write(dockerfile)
                dockerfile_path = f.name
            
            self.client.images.build(path=str(Path(dockerfile_path).parent), 
                                   dockerfile=dockerfile_path, 
                                   tag=self.image_name)
            os.unlink(dockerfile_path)
    
    def run_analysis(self, repo_path: Path, analysis_script: str) -> Dict[str, Any]:
        """Run analysis in Docker container"""
        self.build_analysis_image()
        
        try:
            container = self.client.containers.run(
                self.image_name,
                command=f"python -c '{analysis_script}'",
                volumes={str(repo_path): {'bind': '/analysis/repo', 'mode': 'ro'}},
                working_dir='/analysis',
                mem_limit='512m',
                cpu_quota=50000,  # 50% CPU
                network_mode='none',  # No network access
                detach=True,
                remove=True
            )
            
            # Wait for completion with timeout
            result = container.wait(timeout=300)  # 5 minute timeout
            logs = container.logs().decode('utf-8')
            
            return {
                'exit_code': result['StatusCode'],
                'logs': logs,
                'success': result['StatusCode'] == 0
            }
            
        except Exception as e:
            return {
                'exit_code': -1,
                'logs': str(e),
                'success': False
            }

class CodeStructureAnalyzer:
    """AST-based code structure analysis"""
    
    def __init__(self):
        self.parsers = {}
        self._initialize_parsers()
    
    def _initialize_parsers(self):
        """Initialize tree-sitter parsers for supported languages"""
        # Note: In production, these would be properly installed
        # For now, we'll use Python's built-in AST for Python files
        pass
    
    def analyze_structure(self, repo_path: Path) -> List[ExtractedFeature]:
        """Analyze code structure and extract features"""
        features = []
        
        # Analyze Python files using built-in AST
        for py_file in repo_path.rglob("*.py"):
            try:
                features.extend(self._analyze_python_file(py_file))
            except Exception as e:
                logging.warning(f"Error analyzing {py_file}: {e}")
        
        # TODO: Add support for other languages via tree-sitter
        return features
    
    def _analyze_python_file(self, file_path: Path) -> List[ExtractedFeature]:
        """Analyze Python file using AST"""
        features = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    features.append(ExtractedFeature(
                        name=node.name,
                        type="function",
                        description=ast.get_docstring(node) or f"Function {node.name}",
                        file_path=str(file_path),
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        dependencies=self._extract_dependencies(node),
                        api_surface=self._extract_function_api(node),
                        complexity_score=self._calculate_complexity(node)
                    ))
                
                elif isinstance(node, ast.ClassDef):
                    features.append(ExtractedFeature(
                        name=node.name,
                        type="class",
                        description=ast.get_docstring(node) or f"Class {node.name}",
                        file_path=str(file_path),
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        dependencies=self._extract_dependencies(node),
                        api_surface=self._extract_class_api(node),
                        complexity_score=self._calculate_complexity(node)
                    ))
            
        except Exception as e:
            logging.warning(f"Error parsing {file_path}: {e}")
        
        return features
    
    def _extract_dependencies(self, node) -> List[str]:
        """Extract dependencies from AST node"""
        # Simplified dependency extraction
        return []
    
    def _extract_function_api(self, node) -> Dict[str, Any]:
        """Extract function API information"""
        return {
            "args": [arg.arg for arg in node.args.args],
            "returns": getattr(node.returns, 'id', None) if node.returns else None,
            "decorators": [d.id for d in node.decorator_list if hasattr(d, 'id')]
        }
    
    def _extract_class_api(self, node) -> Dict[str, Any]:
        """Extract class API information"""
        methods = []
        attributes = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
        
        return {
            "methods": methods,
            "attributes": attributes,
            "bases": [base.id for base in node.bases if hasattr(base, 'id')]
        }
    
    def _calculate_complexity(self, node) -> float:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return min(complexity / 10.0, 1.0)  # Normalize to 0-1

class SecurityAuditAnalyzer:
    """Security vulnerability analysis"""
    
    async def analyze_security(self, repo_path: Path) -> Tuple[List[SecurityFinding], float]:
        """Analyze repository for security issues"""
        findings = []
        
        # Use bandit for Python security analysis
        try:
            findings.extend(await self._run_bandit(repo_path))
        except Exception as e:
            logging.error(f"Bandit analysis failed: {e}")
        
        # Calculate security score
        security_score = self._calculate_security_score(findings)
        
        return findings, security_score
    
    async def _run_bandit(self, repo_path: Path) -> List[SecurityFinding]:
        """Run bandit security scanner with safe subprocess execution"""
        findings = []
        
        try:
            # Sanitize path to prevent command injection
            safe_path = shlex.quote(str(repo_path))
            
            proc = await asyncio.create_subprocess_exec(
                'bandit', '-r', safe_path, '-f', 'json',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
                if proc.returncode == 0 and stdout:
                    bandit_results = json.loads(stdout.decode('utf-8'))
                    
                    for result_item in bandit_results.get('results', []):
                        findings.append(SecurityFinding(
                            severity=result_item['issue_severity'].lower(),
                            type=result_item['test_name'],
                            description=result_item['issue_text'],
                            file_path=result_item['filename'],
                            line_number=result_item['line_number'],
                            remediation=result_item.get('more_info', '')
                        ))
                elif stderr:
                    logging.warning(f"Bandit stderr: {stderr.decode('utf-8')}")
            except asyncio.TimeoutError:
                logging.error(f"Bandit scan timed out for {repo_path}")
                try:
                    proc.terminate()
                    await proc.wait()
                except (ProcessLookupError, asyncio.CancelledError):
                    # Process already terminated or task cancelled
                    pass
                except Exception as e:
                    logging.warning(f"Failed to terminate bandit process: {e}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse Bandit JSON output: {e}")
        except Exception as e:
            logging.error(f"Bandit execution failed: {e}")
        
        return findings
    
    def _calculate_security_score(self, findings: List[SecurityFinding]) -> float:
        """Calculate overall security score"""
        if not findings:
            return 1.0
        
        severity_weights = {
            'critical': -0.8,
            'high': -0.4,
            'medium': -0.2,
            'low': -0.1
        }
        
        total_penalty = sum(severity_weights.get(f.severity, -0.1) for f in findings)
        return max(0.0, 1.0 + total_penalty)

class GitHubRepositoryAnalyzer:
    """Main orchestrator for GitHub repository analysis"""
    
    def __init__(self, base_path: str = "/mnt/c/Users/Brandon/AAI"):
        self.base_path = Path(base_path)
        self.cloner = GitCloner()
        self.sandbox = DockerSandbox()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # Initialize analyzers
        self.structure_analyzer = CodeStructureAnalyzer()
        self.security_analyzer = SecurityAuditAnalyzer()
        
        # Initialize integrations
        self.prp_enhancer = IntegrationAwarePRPEnhancer(str(base_path))
        self.research_integration = ResearchPRPIntegration(str(base_path))
        self.analytics = UnifiedAnalytics(str(base_path))
        
        # Analysis database
        self.db_path = self.base_path / "brain" / "github_analysis.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize analysis results database"""
        self.db_path.parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id TEXT PRIMARY KEY,
                    repo_url TEXT NOT NULL,
                    repo_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    overall_score REAL,
                    report_json TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS features (
                    id TEXT PRIMARY KEY,
                    analysis_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    compatibility_score REAL,
                    integrated BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (analysis_id) REFERENCES analyses (id)
                )
            """)
    
    async def analyze_repository(self, repo_url: str) -> AnalysisReport:
        """Perform comprehensive repository analysis"""
        start_time = datetime.now()
        analysis_id = hashlib.md5(f"{repo_url}_{start_time}".encode()).hexdigest()
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        try:
            # Clone repository
            self.logger.info(f"Starting analysis of repository: {repo_url}")
            repo_path = self.cloner.clone_repository(repo_url)
            
            # Perform multi-stage analysis
            report = await self._perform_analysis(
                repo_url, repo_name, analysis_id, repo_path
            )
            
            # Store results
            await self._store_analysis_results(report)
            
            # Cleanup
            self.cloner.cleanup(repo_path)
            
            report.analysis_duration = (datetime.now() - start_time).total_seconds()
            report.success = True
            
            return report
            
        except Exception as e:
            error_report = AnalysisReport(
                repo_url=repo_url,
                repo_name=repo_name,
                analysis_id=analysis_id,
                timestamp=start_time.isoformat(),
                language_distribution={},
                total_lines=0,
                file_count=0,
                commit_count=0,
                last_commit="",
                license=None,
                features=[],
                test_coverage=None,
                documentation_score=0.0,
                code_quality_score=0.0,
                security_findings=[],
                security_score=0.0,
                compatibility_scores=[],
                recommended_features=[],
                integration_stubs={},
                analysis_duration=(datetime.now() - start_time).total_seconds(),
                success=False,
                error_message=str(e)
            )
            
            return error_report
    
    async def _perform_analysis(
        self, repo_url: str, repo_name: str, analysis_id: str, repo_path: Path
    ) -> AnalysisReport:
        """Perform the actual analysis steps"""
        
        # 1. Basic repository metadata
        metadata = self._extract_repo_metadata(repo_path)
        
        # 2. Code structure analysis
        features = self.structure_analyzer.analyze_structure(repo_path)
        
        # 3. Security analysis
        security_findings, security_score = await self.security_analyzer.analyze_security(repo_path)
        
        # 4. Compatibility scoring
        compatibility_scores = await self._calculate_compatibility_scores(features)
        
        # 5. Generate integration recommendations
        recommended_features, integration_stubs = await self._generate_integration_recommendations(
            features, compatibility_scores
        )
        
        return AnalysisReport(
            repo_url=repo_url,
            repo_name=repo_name,
            analysis_id=analysis_id,
            timestamp=datetime.now().isoformat(),
            **metadata,
            features=features,
            security_findings=security_findings,
            security_score=security_score,
            compatibility_scores=compatibility_scores,
            recommended_features=recommended_features,
            integration_stubs=integration_stubs,
            analysis_duration=0.0,  # Will be set later
            success=True
        )
    
    def _extract_repo_metadata(self, repo_path: Path) -> Dict[str, Any]:
        """Extract basic repository metadata"""
        repo = Repo(repo_path)
        
        # Language distribution (simplified)
        language_dist = self._calculate_language_distribution(repo_path)
        
        # File and line counts
        total_lines = 0
        file_count = 0
        
        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                file_count += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        total_lines += len(f.readlines())
                except (UnicodeDecodeError, IOError, OSError) as e:
                    logging.debug(f"Could not read file {file_path} for line counting: {e}")
                    pass
        
        return {
            "language_distribution": language_dist,
            "total_lines": total_lines,
            "file_count": file_count,
            "commit_count": len(list(repo.iter_commits())),
            "last_commit": repo.head.commit.hexsha[:8],
            "license": self._detect_license(repo_path),
            "test_coverage": self._estimate_test_coverage(repo_path),
            "documentation_score": self._calculate_documentation_score(repo_path),
            "code_quality_score": self._calculate_code_quality_score(repo_path)
        }
    
    def _calculate_language_distribution(self, repo_path: Path) -> Dict[str, float]:
        """Calculate language distribution by file extensions"""
        extensions = {}
        total_files = 0
        
        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix:
                ext = file_path.suffix.lower()
                extensions[ext] = extensions.get(ext, 0) + 1
                total_files += 1
        
        # Convert to percentages
        if total_files > 0:
            return {ext: count/total_files for ext, count in extensions.items()}
        return {}
    
    def _detect_license(self, repo_path: Path) -> Optional[str]:
        """Detect repository license"""
        license_files = ['LICENSE', 'LICENSE.txt', 'LICENSE.md', 'COPYING']
        
        for license_file in license_files:
            license_path = repo_path / license_file
            if license_path.exists():
                try:
                    with open(license_path, 'r', encoding='utf-8') as f:
                        content = f.read()[:500]  # First 500 chars
                        if 'MIT' in content:
                            return 'MIT'
                        elif 'Apache' in content:
                            return 'Apache-2.0'
                        elif 'GPL' in content:
                            return 'GPL'
                        else:
                            return 'Custom'
                except (UnicodeDecodeError, IOError, OSError) as e:
                    logging.debug(f"Could not read license file {license_path}: {e}")
                    pass
        
        return None
    
    def _estimate_test_coverage(self, repo_path: Path) -> Optional[float]:
        """Estimate test coverage based on test files"""
        test_files = list(repo_path.rglob("*test*.py")) + list(repo_path.rglob("test_*.py"))
        source_files = list(repo_path.rglob("*.py"))
        
        # Filter out test files from source files
        source_files = [f for f in source_files if 'test' not in f.name.lower()]
        
        if len(source_files) == 0:
            return None
        
        # Rough estimation: test files to source files ratio
        coverage_estimate = min(len(test_files) / len(source_files), 1.0)
        return coverage_estimate
    
    def _calculate_documentation_score(self, repo_path: Path) -> float:
        """Calculate documentation score"""
        score = 0.0
        
        # Check for README
        if any((repo_path / name).exists() for name in ['README.md', 'README.txt', 'README']):
            score += 0.4
        
        # Check for docs directory
        if (repo_path / 'docs').exists():
            score += 0.3
        
        # Check for docstrings in Python files
        python_files = list(repo_path.rglob("*.py"))
        documented_files = 0
        
        for py_file in python_files[:10]:  # Sample first 10 files
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '"""' in content or "'''" in content:
                        documented_files += 1
            except (UnicodeDecodeError, IOError, OSError) as e:
                logging.debug(f"Could not read Python file {py_file} for documentation check: {e}")
                pass
        
        if python_files:
            score += 0.3 * (documented_files / min(len(python_files), 10))
        
        return min(score, 1.0)
    
    def _calculate_code_quality_score(self, repo_path: Path) -> float:
        """Calculate code quality score"""
        # Simplified quality metrics
        score = 0.5  # Base score
        
        # Check for common quality indicators
        quality_files = [
            'pyproject.toml', 'setup.py', 'requirements.txt',
            '.gitignore', '.pre-commit-config.yaml'
        ]
        
        for qf in quality_files:
            if (repo_path / qf).exists():
                score += 0.1
        
        return min(score, 1.0)
    
    async def _calculate_compatibility_scores(
        self, features: List[ExtractedFeature]
    ) -> List[CompatibilityScore]:
        """Calculate compatibility scores for each feature"""
        scores = []
        
        for feature in features:
            # Simplified scoring algorithm
            relevance = self._calculate_relevance_score(feature)
            quality = min(1.0 - feature.complexity_score, 1.0)
            complexity = feature.complexity_score
            reusability = self._calculate_reusability_score(feature)
            security = 0.8  # Default good security score
            
            # Weighted average
            weights = {
                'relevance': 0.30,
                'quality': 0.20,
                'complexity': 0.20,
                'reusability': 0.15,
                'security': 0.15
            }
            
            overall = (
                weights['relevance'] * relevance +
                weights['quality'] * quality +
                weights['complexity'] * (1.0 - complexity) +  # Inverse
                weights['reusability'] * reusability +
                weights['security'] * security
            )
            
            scores.append(CompatibilityScore(
                relevance_score=relevance,
                quality_score=quality,
                complexity_score=complexity,
                reusability_score=reusability,
                security_score=security,
                overall_score=overall,
                rationale=f"Feature {feature.name} scored {overall:.2f} based on relevance, quality, and reusability"
            ))
        
        return scores
    
    def _calculate_relevance_score(self, feature: ExtractedFeature) -> float:
        """Calculate relevance to existing projects"""
        # Check against existing modules and patterns
        relevant_keywords = [
            'analyzer', 'orchestrator', 'integration', 'research',
            'enhancement', 'analytics', 'score', 'task', 'brain'
        ]
        
        name_lower = feature.name.lower()
        desc_lower = feature.description.lower()
        
        matches = sum(1 for keyword in relevant_keywords 
                     if keyword in name_lower or keyword in desc_lower)
        
        return min(matches / len(relevant_keywords), 1.0)
    
    def _calculate_reusability_score(self, feature: ExtractedFeature) -> float:
        """Calculate reusability potential"""
        # Higher score for classes and well-documented functions
        base_score = 0.5
        
        if feature.type == 'class':
            base_score += 0.3
        elif feature.type == 'function':
            base_score += 0.2
        
        if feature.documentation:
            base_score += 0.2
        
        if len(feature.dependencies) < 3:  # Low dependencies
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    async def _generate_integration_recommendations(
        self, features: List[ExtractedFeature], scores: List[CompatibilityScore]
    ) -> Tuple[List[str], Dict[str, str]]:
        """Generate integration recommendations and stubs"""
        recommended = []
        stubs = {}
        
        # Sort features by compatibility score
        feature_score_pairs = list(zip(features, scores))
        feature_score_pairs.sort(key=lambda x: x[1].overall_score, reverse=True)
        
        # Recommend top features
        for feature, score in feature_score_pairs[:5]:  # Top 5
            if score.overall_score >= 0.7:
                recommended.append(feature.name)
                stubs[feature.name] = self._generate_integration_stub(feature)
        
        return recommended, stubs
    
    def _generate_integration_stub(self, feature: ExtractedFeature) -> str:
        """Generate integration stub code"""
        if feature.type == 'function':
            return f"""
# Integration stub for {feature.name}
from external_repo import {feature.name}

def integrated_{feature.name}(*args, **kwargs):
    \"\"\"
    Integrated version of {feature.name}
    {feature.description}
    \"\"\"
    return {feature.name}(*args, **kwargs)
"""
        
        elif feature.type == 'class':
            return f"""
# Integration stub for {feature.name}
from external_repo import {feature.name} as External{feature.name}

class Integrated{feature.name}(External{feature.name}):
    \"\"\"
    Integrated version of {feature.name}
    {feature.description}
    \"\"\"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add AAI-specific initialization
        pass
"""
        
        return f"# TODO: Implement integration for {feature.name}"
    
    async def _store_analysis_results(self, report: AnalysisReport):
        """Store analysis results in database"""
        with sqlite3.connect(self.db_path) as conn:
            # Store main analysis
            conn.execute("""
                INSERT OR REPLACE INTO analyses 
                (id, repo_url, repo_name, timestamp, success, overall_score, report_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                report.analysis_id,
                report.repo_url,
                report.repo_name,
                report.timestamp,
                report.success,
                sum(s.overall_score for s in report.compatibility_scores) / len(report.compatibility_scores) 
                if report.compatibility_scores else 0.0,
                json.dumps(asdict(report))
            ))
            
            # Store features
            for i, feature in enumerate(report.features):
                score = report.compatibility_scores[i] if i < len(report.compatibility_scores) else None
                conn.execute("""
                    INSERT OR REPLACE INTO features
                    (id, analysis_id, name, type, compatibility_score, integrated)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    f"{report.analysis_id}_{i}",
                    report.analysis_id,
                    feature.name,
                    feature.type,
                    score.overall_score if score else 0.0,
                    False
                ))
    
    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Get analysis history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT repo_url, repo_name, timestamp, success, overall_score
                FROM analyses
                ORDER BY timestamp DESC
                LIMIT 20
            """)
            
            return [
                {
                    'repo_url': row[0],
                    'repo_name': row[1],
                    'timestamp': row[2],
                    'success': bool(row[3]),
                    'overall_score': row[4]
                }
                for row in cursor.fetchall()
            ]
    
    def get_recommended_features(self) -> List[Dict[str, Any]]:
        """Get features recommended for integration"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT f.name, f.type, f.compatibility_score, a.repo_name, a.repo_url
                FROM features f
                JOIN analyses a ON f.analysis_id = a.id
                WHERE f.compatibility_score >= 0.7 AND f.integrated = FALSE
                ORDER BY f.compatibility_score DESC
                LIMIT 10
            """)
            
            return [
                {
                    'name': row[0],
                    'type': row[1],
                    'score': row[2],
                    'repo_name': row[3],
                    'repo_url': row[4]
                }
                for row in cursor.fetchall()
            ]

# Example usage and testing
async def main():
    """Example usage of the GitHub Repository Analyzer"""
    analyzer = GitHubRepositoryAnalyzer()
    
    # Test with a small repository
    test_repo = "https://github.com/octocat/Hello-World.git"
    
    try:
        report = await analyzer.analyze_repository(test_repo)
        
        print(f"Analysis Report for {report.repo_name}")
        print(f"Success: {report.success}")
        print(f"Features found: {len(report.features)}")
        print(f"Security score: {report.security_score:.2f}")
        print(f"Recommended features: {report.recommended_features}")
        
        # Print feature details
        for i, feature in enumerate(report.features[:3]):  # First 3 features
            score = report.compatibility_scores[i] if i < len(report.compatibility_scores) else None
            print(f"\nFeature: {feature.name}")
            print(f"Type: {feature.type}")
            print(f"Score: {score.overall_score:.2f}" if score else "No score")
            print(f"Description: {feature.description}")
        
    except Exception as e:
        logging.error(f"Analysis failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())