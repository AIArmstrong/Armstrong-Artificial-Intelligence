#!/usr/bin/env python3
"""
Specialized Analyzer Agents for GitHub Repository Analysis
Each agent focuses on specific aspects of repository analysis
"""

import asyncio
import ast
import json
import logging
import os
import re
import shlex
import subprocess
import tempfile
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

@dataclass
class AnalysisResult:
    """Base class for analysis results"""
    agent_name: str
    success: bool
    execution_time: float
    data: Dict[str, Any]
    errors: List[str]
    warnings: List[str]

class BaseAnalyzerAgent(ABC):
    """Base class for all analyzer agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.timeout = 300  # 5 minutes default
    
    @abstractmethod
    async def analyze(self, repo_path: Path) -> AnalysisResult:
        """Perform analysis on the repository"""
        pass
    
    def _create_result(self, success: bool, data: Dict[str, Any], 
                      execution_time: float, errors: List[str] = None, 
                      warnings: List[str] = None) -> AnalysisResult:
        """Helper to create standardized results"""
        return AnalysisResult(
            agent_name=self.name,
            success=success,
            execution_time=execution_time,
            data=data or {},
            errors=errors or [],
            warnings=warnings or []
        )

class CodeStructureAgent(BaseAnalyzerAgent):
    """Analyzes code structure, APIs, and architectural patterns"""
    
    def __init__(self):
        super().__init__("CodeStructureAgent")
        self.supported_extensions = {
            '.py': self._analyze_python,
            '.js': self._analyze_javascript,
            '.ts': self._analyze_typescript,
            '.go': self._analyze_go,
            '.rs': self._analyze_rust,
            '.java': self._analyze_java
        }
    
    async def analyze(self, repo_path: Path) -> AnalysisResult:
        """Analyze code structure across multiple languages"""
        start_time = time.time()
        
        try:
            structure_data = {
                'languages': {},
                'api_surfaces': [],
                'design_patterns': [],
                'complexity_metrics': {},
                'dependencies': {'internal': [], 'external': []},
                'file_structure': self._analyze_file_structure(repo_path)
            }
            
            # Analyze files by language
            for file_path in repo_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in self.supported_extensions:
                    lang_analyzer = self.supported_extensions[file_path.suffix]
                    file_analysis = await lang_analyzer(file_path)
                    
                    lang = file_path.suffix[1:]  # Remove dot
                    if lang not in structure_data['languages']:
                        structure_data['languages'][lang] = {
                            'files': [],
                            'total_lines': 0,
                            'functions': 0,
                            'classes': 0,
                            'complexity': 0
                        }
                    
                    structure_data['languages'][lang]['files'].append(str(file_path))
                    structure_data['languages'][lang].update(file_analysis)
            
            # Detect architectural patterns
            structure_data['architecture_patterns'] = self._detect_architecture_patterns(repo_path)
            
            execution_time = time.time() - start_time
            return self._create_result(True, structure_data, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_result(False, {}, execution_time, [str(e)])
    
    def _analyze_file_structure(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze overall file structure and organization"""
        structure = {
            'total_files': 0,
            'directories': 0,
            'structure_score': 0.0,
            'organization_patterns': []
        }
        
        # Common patterns
        patterns = {
            'src_pattern': bool((repo_path / 'src').exists()),
            'lib_pattern': bool((repo_path / 'lib').exists()),
            'tests_pattern': any(d.name in ['tests', 'test', '__tests__'] 
                                for d in repo_path.iterdir() if d.is_dir()),
            'docs_pattern': bool((repo_path / 'docs').exists()),
            'config_pattern': any(f.name in ['config', 'configs', '.config'] 
                                 for f in repo_path.iterdir())
        }
        
        structure['organization_patterns'] = [k for k, v in patterns.items() if v]
        structure['structure_score'] = sum(patterns.values()) / len(patterns)
        
        # Count files and directories
        for item in repo_path.rglob("*"):
            if item.is_file():
                structure['total_files'] += 1
            elif item.is_dir():
                structure['directories'] += 1
        
        return structure
    
    async def _analyze_python(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Python file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            analysis = {
                'functions': [],
                'classes': [],
                'imports': [],
                'complexity': 0,
                'lines': len(content.splitlines()),
                'docstring_coverage': 0.0
            }
            
            documented_items = 0
            total_items = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'line_start': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'is_async': isinstance(node, ast.AsyncFunctionDef),
                        'has_docstring': bool(ast.get_docstring(node)),
                        'complexity': self._calculate_complexity(node)
                    }
                    analysis['functions'].append(func_info)
                    total_items += 1
                    if func_info['has_docstring']:
                        documented_items += 1
                
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'line_start': node.lineno,
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                        'has_docstring': bool(ast.get_docstring(node)),
                        'inheritance': [base.id for base in node.bases if hasattr(base, 'id')]
                    }
                    analysis['classes'].append(class_info)
                    total_items += 1
                    if class_info['has_docstring']:
                        documented_items += 1
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis['imports'].append(alias.name)
                    else:
                        analysis['imports'].append(node.module or '')
            
            analysis['complexity'] = sum(f['complexity'] for f in analysis['functions'])
            analysis['docstring_coverage'] = documented_items / max(total_items, 1)
            
            return analysis
            
        except Exception as e:
            return {'error': str(e), 'lines': 0, 'functions': [], 'classes': []}
    
    async def _analyze_javascript(self, file_path: Path) -> Dict[str, Any]:
        """Analyze JavaScript file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple regex-based analysis for JavaScript
            analysis = {
                'functions': [],
                'classes': [],
                'exports': [],
                'imports': [],
                'lines': len(content.splitlines())
            }
            
            # Find function declarations
            func_pattern = r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))'
            for match in re.finditer(func_pattern, content):
                func_name = match.group(1) or match.group(2)
                if func_name:
                    analysis['functions'].append({
                        'name': func_name,
                        'line': content[:match.start()].count('\n') + 1
                    })
            
            # Find class declarations
            class_pattern = r'class\s+(\w+)'
            for match in re.finditer(class_pattern, content):
                analysis['classes'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            # Find imports/exports
            import_pattern = r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]'
            for match in re.finditer(import_pattern, content):
                analysis['imports'].append(match.group(1))
            
            export_pattern = r'export\s+(?:default\s+)?(?:function\s+(\w+)|class\s+(\w+)|(?:const|let|var)\s+(\w+))'
            for match in re.finditer(export_pattern, content):
                export_name = match.group(1) or match.group(2) or match.group(3)
                if export_name:
                    analysis['exports'].append(export_name)
            
            return analysis
            
        except Exception as e:
            return {'error': str(e), 'lines': 0, 'functions': [], 'classes': []}
    
    async def _analyze_typescript(self, file_path: Path) -> Dict[str, Any]:
        """Analyze TypeScript file structure"""
        # For now, use JavaScript analyzer as base
        analysis = await self._analyze_javascript(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add TypeScript-specific analysis
            analysis['interfaces'] = []
            analysis['types'] = []
            
            # Find interface declarations
            interface_pattern = r'interface\s+(\w+)'
            for match in re.finditer(interface_pattern, content):
                analysis['interfaces'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            # Find type declarations
            type_pattern = r'type\s+(\w+)\s*='
            for match in re.finditer(type_pattern, content):
                analysis['types'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            return analysis
            
        except Exception as e:
            analysis['error'] = str(e)
            return analysis
    
    async def _analyze_go(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Go file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                'functions': [],
                'structs': [],
                'interfaces': [],
                'imports': [],
                'lines': len(content.splitlines())
            }
            
            # Find function declarations
            func_pattern = r'func\s+(?:\([^)]*\)\s+)?(\w+)\s*\('
            for match in re.finditer(func_pattern, content):
                analysis['functions'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            # Find struct declarations
            struct_pattern = r'type\s+(\w+)\s+struct'
            for match in re.finditer(struct_pattern, content):
                analysis['structs'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            # Find interface declarations
            interface_pattern = r'type\s+(\w+)\s+interface'
            for match in re.finditer(interface_pattern, content):
                analysis['interfaces'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            return analysis
            
        except Exception as e:
            return {'error': str(e), 'lines': 0, 'functions': [], 'structs': []}
    
    async def _analyze_rust(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Rust file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                'functions': [],
                'structs': [],
                'enums': [],
                'traits': [],
                'lines': len(content.splitlines())
            }
            
            # Find function declarations
            func_pattern = r'fn\s+(\w+)\s*\('
            for match in re.finditer(func_pattern, content):
                analysis['functions'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            # Find struct declarations
            struct_pattern = r'struct\s+(\w+)'
            for match in re.finditer(struct_pattern, content):
                analysis['structs'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            return analysis
            
        except Exception as e:
            return {'error': str(e), 'lines': 0, 'functions': [], 'structs': []}
    
    async def _analyze_java(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Java file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                'classes': [],
                'methods': [],
                'interfaces': [],
                'imports': [],
                'lines': len(content.splitlines())
            }
            
            # Find class declarations
            class_pattern = r'(?:public\s+)?class\s+(\w+)'
            for match in re.finditer(class_pattern, content):
                analysis['classes'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            # Find method declarations
            method_pattern = r'(?:public|private|protected)\s+(?:static\s+)?(?:\w+\s+)+(\w+)\s*\('
            for match in re.finditer(method_pattern, content):
                analysis['methods'].append({
                    'name': match.group(1),
                    'line': content[:match.start()].count('\n') + 1
                })
            
            return analysis
            
        except Exception as e:
            return {'error': str(e), 'lines': 0, 'classes': [], 'methods': []}
    
    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity for AST node"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def _detect_architecture_patterns(self, repo_path: Path) -> List[str]:
        """Detect common architectural patterns"""
        patterns = []
        
        # Check for common patterns
        if (repo_path / 'src' / 'controllers').exists():
            patterns.append('MVC')
        
        if (repo_path / 'models').exists() and (repo_path / 'views').exists():
            patterns.append('MVC')
        
        if any(f.name.endswith('Service.py') for f in repo_path.rglob("*.py")):
            patterns.append('Service Layer')
        
        if (repo_path / 'tests').exists():
            patterns.append('Test-Driven Development')
        
        if (repo_path / 'Dockerfile').exists():
            patterns.append('Containerization')
        
        if (repo_path / 'docker-compose.yml').exists():
            patterns.append('Multi-Container')
        
        return patterns

class SecurityAuditAgent(BaseAnalyzerAgent):
    """Performs comprehensive security analysis"""
    
    def __init__(self):
        super().__init__("SecurityAuditAgent")
        self.security_tools = {
            'python': ['bandit', 'safety'],
            'javascript': ['npm audit', 'semgrep'],
            'go': ['gosec'],
            'rust': ['cargo-audit']
        }
    
    async def analyze(self, repo_path: Path) -> AnalysisResult:
        """Perform security analysis"""
        start_time = time.time()
        
        try:
            security_data = {
                'vulnerabilities': [],
                'secret_leaks': [],
                'dependency_issues': [],
                'security_score': 1.0,
                'license_compliance': {},
                'sensitive_files': []
            }
            
            # Run language-specific security tools
            await self._run_bandit_scan(repo_path, security_data)
            await self._scan_for_secrets(repo_path, security_data)
            await self._check_dependencies(repo_path, security_data)
            await self._analyze_license_compliance(repo_path, security_data)
            
            # Calculate overall security score
            security_data['security_score'] = self._calculate_security_score(security_data)
            
            execution_time = time.time() - start_time
            return self._create_result(True, security_data, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_result(False, {}, execution_time, [str(e)])
    
    async def _run_bandit_scan(self, repo_path: Path, security_data: Dict):
        """Run Bandit security scanner for Python files"""
        try:
            # Check if there are Python files
            python_files = list(repo_path.rglob("*.py"))
            if not python_files:
                return
            
            # Run bandit with safe path handling
            safe_path = shlex.quote(str(repo_path))
            result = subprocess.run([
                'bandit', '-r', safe_path, '-f', 'json'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and result.stdout:
                bandit_results = json.loads(result.stdout)
                
                for issue in bandit_results.get('results', []):
                    security_data['vulnerabilities'].append({
                        'tool': 'bandit',
                        'severity': issue['issue_severity'],
                        'confidence': issue['issue_confidence'],
                        'description': issue['issue_text'],
                        'file': issue['filename'],
                        'line': issue['line_number'],
                        'code': issue.get('code', ''),
                        'test_id': issue['test_id']
                    })
        
        except Exception as e:
            logging.error(f"Bandit scan failed: {e}")
    
    async def _scan_for_secrets(self, repo_path: Path, security_data: Dict):
        """Scan for potential secret leaks"""
        secret_patterns = [
            (r'(?i)api[_-]?key["\s]*[:=]["\s]*([a-zA-Z0-9-_]{20,})', 'API Key'),
            (r'(?i)secret[_-]?key["\s]*[:=]["\s]*([a-zA-Z0-9-_]{20,})', 'Secret Key'),
            (r'(?i)password["\s]*[:=]["\s]*([a-zA-Z0-9-_]{8,})', 'Password'),
            (r'(?i)token["\s]*[:=]["\s]*([a-zA-Z0-9-_]{20,})', 'Token'),
            (r'(?i)(aws_access_key_id|aws_secret_access_key)', 'AWS Credentials'),
            (r'(?i)(github_token|gh_token)', 'GitHub Token')
        ]
        
        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.ts', '.env', '.config']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern, secret_type in secret_patterns:
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            security_data['secret_leaks'].append({
                                'type': secret_type,
                                'file': str(file_path),
                                'line': content[:match.start()].count('\n') + 1,
                                'pattern': pattern
                            })
                
                except Exception:
                    continue
    
    async def _check_dependencies(self, repo_path: Path, security_data: Dict):
        """Check for vulnerable dependencies"""
        # Check Python requirements
        requirements_files = ['requirements.txt', 'Pipfile', 'pyproject.toml']
        for req_file in requirements_files:
            req_path = repo_path / req_file
            if req_path.exists():
                try:
                    safe_path = shlex.quote(str(req_path))
                    result = subprocess.run([
                        'safety', 'check', '--file', safe_path, '--json'
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.stdout:
                        safety_results = json.loads(result.stdout)
                        for vuln in safety_results:
                            security_data['dependency_issues'].append({
                                'package': vuln['package'],
                                'version': vuln['installed_version'],
                                'vulnerability': vuln['vulnerability'],
                                'severity': 'high'  # Safety reports high-severity issues
                            })
                
                except Exception as e:
                    logging.error(f"Safety check failed: {e}")
        
        # Check JavaScript/Node.js dependencies
        package_json = repo_path / 'package.json'
        if package_json.exists():
            try:
                safe_cwd = shlex.quote(str(repo_path))
                result = subprocess.run([
                    'npm', 'audit', '--json'
                ], cwd=repo_path, capture_output=True, text=True, timeout=30)
                
                if result.stdout:
                    audit_results = json.loads(result.stdout)
                    for vuln_id, vuln_data in audit_results.get('vulnerabilities', {}).items():
                        security_data['dependency_issues'].append({
                            'package': vuln_data.get('name', vuln_id),
                            'severity': vuln_data.get('severity', 'unknown'),
                            'vulnerability': vuln_data.get('title', 'Unknown vulnerability')
                        })
            
            except Exception as e:
                logging.error(f"npm audit failed: {e}")
    
    async def _analyze_license_compliance(self, repo_path: Path, security_data: Dict):
        """Analyze license compliance"""
        license_files = ['LICENSE', 'LICENSE.txt', 'LICENSE.md', 'COPYING']
        
        for license_file in license_files:
            license_path = repo_path / license_file
            if license_path.exists():
                try:
                    with open(license_path, 'r', encoding='utf-8') as f:
                        content = f.read().upper()
                    
                    if 'MIT' in content:
                        security_data['license_compliance']['license'] = 'MIT'
                        security_data['license_compliance']['compatible'] = True
                    elif 'APACHE' in content:
                        security_data['license_compliance']['license'] = 'Apache-2.0'
                        security_data['license_compliance']['compatible'] = True
                    elif 'GPL' in content:
                        security_data['license_compliance']['license'] = 'GPL'
                        security_data['license_compliance']['compatible'] = False
                        security_data['license_compliance']['warning'] = 'GPL license may have compatibility issues'
                    else:
                        security_data['license_compliance']['license'] = 'Custom'
                        security_data['license_compliance']['compatible'] = None
                    
                    break
                
                except Exception:
                    continue
        
        if 'license' not in security_data['license_compliance']:
            security_data['license_compliance']['license'] = 'None'
            security_data['license_compliance']['compatible'] = None
            security_data['license_compliance']['warning'] = 'No license file found'
    
    def _calculate_security_score(self, security_data: Dict) -> float:
        """Calculate overall security score"""
        score = 1.0
        
        # Deduct for vulnerabilities
        for vuln in security_data['vulnerabilities']:
            if vuln['severity'].lower() == 'high':
                score -= 0.3
            elif vuln['severity'].lower() == 'medium':
                score -= 0.1
            else:
                score -= 0.05
        
        # Deduct for secret leaks
        score -= len(security_data['secret_leaks']) * 0.2
        
        # Deduct for dependency issues
        for dep_issue in security_data['dependency_issues']:
            if dep_issue['severity'] == 'high':
                score -= 0.2
            elif dep_issue['severity'] == 'medium':
                score -= 0.1
            else:
                score -= 0.05
        
        # License compliance impact
        if not security_data['license_compliance'].get('compatible', True):
            score -= 0.3
        
        return max(0.0, score)

class QualityAssessmentAgent(BaseAnalyzerAgent):
    """Assesses code quality metrics"""
    
    def __init__(self):
        super().__init__("QualityAssessmentAgent")
    
    async def analyze(self, repo_path: Path) -> AnalysisResult:
        """Perform quality assessment"""
        start_time = time.time()
        
        try:
            quality_data = {
                'overall_score': 0.0,
                'test_coverage': 0.0,
                'documentation_score': 0.0,
                'code_complexity': {},
                'maintainability_index': 0.0,
                'technical_debt': [],
                'quality_metrics': {}
            }
            
            # Analyze different quality aspects
            quality_data['test_coverage'] = await self._analyze_test_coverage(repo_path)
            quality_data['documentation_score'] = await self._analyze_documentation(repo_path)
            quality_data['code_complexity'] = await self._analyze_complexity(repo_path)
            quality_data['technical_debt'] = await self._analyze_technical_debt(repo_path)
            
            # Calculate overall quality score
            quality_data['overall_score'] = self._calculate_overall_score(quality_data)
            
            execution_time = time.time() - start_time
            return self._create_result(True, quality_data, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_result(False, {}, execution_time, [str(e)])
    
    async def _analyze_test_coverage(self, repo_path: Path) -> float:
        """Estimate test coverage"""
        test_files = []
        source_files = []
        
        # Find test files
        test_patterns = ['*test*.py', 'test_*.py', '*.test.js', '*.spec.js', '*_test.go']
        for pattern in test_patterns:
            test_files.extend(repo_path.rglob(pattern))
        
        # Find source files
        source_patterns = ['*.py', '*.js', '*.ts', '*.go', '*.java']
        for pattern in source_patterns:
            files = list(repo_path.rglob(pattern))
            # Filter out test files
            source_files.extend([f for f in files if not any(test_pattern in f.name.lower() 
                                                           for test_pattern in ['test', 'spec'])])
        
        if not source_files:
            return 0.0
        
        # Simple ratio-based estimation
        coverage_ratio = len(test_files) / len(source_files)
        return min(coverage_ratio, 1.0)
    
    async def _analyze_documentation(self, repo_path: Path) -> float:
        """Analyze documentation quality"""
        score = 0.0
        
        # Check for README
        readme_files = ['README.md', 'README.txt', 'README.rst', 'README']
        for readme in readme_files:
            if (repo_path / readme).exists():
                score += 0.3
                break
        
        # Check for docs directory
        if (repo_path / 'docs').exists():
            score += 0.2
        
        # Check for API documentation
        api_docs = ['API.md', 'api.md', 'docs/api.md']
        for api_doc in api_docs:
            if (repo_path / api_doc).exists():
                score += 0.1
                break
        
        # Check for inline documentation in code
        documented_files = 0
        total_files = 0
        
        for py_file in repo_path.rglob("*.py"):
            total_files += 1
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '"""' in content or "'''" in content:
                        documented_files += 1
            except:
                continue
        
        if total_files > 0:
            score += 0.4 * (documented_files / total_files)
        
        return min(score, 1.0)
    
    async def _analyze_complexity(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze code complexity"""
        complexity_data = {
            'average_complexity': 0.0,
            'max_complexity': 0,
            'complex_functions': [],
            'total_functions': 0
        }
        
        total_complexity = 0
        function_count = 0
        
        for py_file in repo_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        complexity = self._calculate_function_complexity(node)
                        total_complexity += complexity
                        function_count += 1
                        
                        if complexity > 10:  # High complexity threshold
                            complexity_data['complex_functions'].append({
                                'name': node.name,
                                'file': str(py_file),
                                'line': node.lineno,
                                'complexity': complexity
                            })
                        
                        complexity_data['max_complexity'] = max(
                            complexity_data['max_complexity'], complexity
                        )
            
            except Exception:
                continue
        
        if function_count > 0:
            complexity_data['average_complexity'] = total_complexity / function_count
        
        complexity_data['total_functions'] = function_count
        return complexity_data
    
    def _calculate_function_complexity(self, node) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    async def _analyze_technical_debt(self, repo_path: Path) -> List[Dict[str, Any]]:
        """Identify technical debt indicators"""
        debt_indicators = []
        
        # Common debt patterns
        debt_patterns = [
            (r'# TODO', 'TODO comment'),
            (r'# FIXME', 'FIXME comment'),
            (r'# HACK', 'HACK comment'),
            (r'# XXX', 'XXX comment'),
            (r'\.catch\(\s*\)\s*;', 'Empty catch block'),
            (r'console\.log\(', 'Debug statement'),
            (r'print\(', 'Debug print statement')
        ]
        
        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.ts']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern, description in debt_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            debt_indicators.append({
                                'type': description,
                                'file': str(file_path),
                                'line': content[:match.start()].count('\n') + 1,
                                'context': content[match.start():match.end()]
                            })
                
                except Exception:
                    continue
        
        return debt_indicators
    
    def _calculate_overall_score(self, quality_data: Dict) -> float:
        """Calculate overall quality score"""
        weights = {
            'test_coverage': 0.3,
            'documentation': 0.25,
            'complexity': 0.25,
            'technical_debt': 0.2
        }
        
        score = 0.0
        
        # Test coverage contribution
        score += weights['test_coverage'] * quality_data['test_coverage']
        
        # Documentation contribution
        score += weights['documentation'] * quality_data['documentation_score']
        
        # Complexity contribution (inverse - lower complexity is better)
        avg_complexity = quality_data['code_complexity'].get('average_complexity', 0)
        complexity_score = max(0, 1.0 - (avg_complexity / 20))  # Normalize to 0-1
        score += weights['complexity'] * complexity_score
        
        # Technical debt contribution (inverse - less debt is better)
        debt_count = len(quality_data['technical_debt'])
        debt_score = max(0, 1.0 - (debt_count / 50))  # Normalize to 0-1
        score += weights['technical_debt'] * debt_score
        
        return min(score, 1.0)

class PerformanceProfilerAgent(BaseAnalyzerAgent):
    """Analyzes performance characteristics"""
    
    def __init__(self):
        super().__init__("PerformanceProfilerAgent")
    
    async def analyze(self, repo_path: Path) -> AnalysisResult:
        """Perform performance analysis"""
        start_time = time.time()
        
        try:
            performance_data = {
                'bottlenecks': [],
                'optimization_opportunities': [],
                'resource_usage': {},
                'scalability_concerns': [],
                'performance_score': 0.0
            }
            
            # Analyze for common performance issues
            await self._detect_bottlenecks(repo_path, performance_data)
            await self._identify_optimization_opportunities(repo_path, performance_data)
            await self._analyze_resource_usage(repo_path, performance_data)
            
            # Calculate performance score
            performance_data['performance_score'] = self._calculate_performance_score(performance_data)
            
            execution_time = time.time() - start_time
            return self._create_result(True, performance_data, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            return self._create_result(False, {}, execution_time, [str(e)])
    
    async def _detect_bottlenecks(self, repo_path: Path, performance_data: Dict):
        """Detect potential performance bottlenecks"""
        bottleneck_patterns = [
            (r'for\s+\w+\s+in\s+.*:\s*\n\s*for\s+\w+\s+in', 'Nested loops'),
            (r'while\s+True:', 'Infinite loop'),
            (r'\.sort\(\)', 'Sorting operation'),
            (r'\.join\(.*\)', 'String concatenation in loop'),
            (r'open\(.*\)\.read\(\)', 'File reading without context manager')
        ]
        
        for file_path in repo_path.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, description in bottleneck_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        performance_data['bottlenecks'].append({
                            'type': description,
                            'file': str(file_path),
                            'line': content[:match.start()].count('\n') + 1,
                            'severity': 'medium'
                        })
            
            except Exception:
                continue
    
    async def _identify_optimization_opportunities(self, repo_path: Path, performance_data: Dict):
        """Identify optimization opportunities"""
        optimization_patterns = [
            (r'import\s+\*', 'Wildcard import (consider specific imports)'),
            (r'\.append\(.*\)\s*\n.*\.append\(', 'Multiple appends (consider extend)'),
            (r'len\(.*\)\s*==\s*0', 'Length check (consider "not" operator)'),
            (r'range\(len\(', 'Range with len (consider enumerate)')
        ]
        
        for file_path in repo_path.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, suggestion in optimization_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        performance_data['optimization_opportunities'].append({
                            'suggestion': suggestion,
                            'file': str(file_path),
                            'line': content[:match.start()].count('\n') + 1,
                            'impact': 'low'
                        })
            
            except Exception:
                continue
    
    async def _analyze_resource_usage(self, repo_path: Path, performance_data: Dict):
        """Analyze resource usage patterns"""
        resource_data = {
            'memory_intensive': [],
            'io_operations': [],
            'cpu_intensive': []
        }
        
        memory_patterns = [
            r'\.load\(\)',
            r'\.read\(\)',
            r'pandas\.read_.*\(',
            r'numpy\.array\('
        ]
        
        for file_path in repo_path.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern in memory_patterns:
                    if re.search(pattern, content):
                        resource_data['memory_intensive'].append(str(file_path))
                        break
            
            except Exception:
                continue
        
        performance_data['resource_usage'] = resource_data
    
    def _calculate_performance_score(self, performance_data: Dict) -> float:
        """Calculate overall performance score"""
        score = 1.0
        
        # Deduct for bottlenecks
        score -= len(performance_data['bottlenecks']) * 0.1
        
        # Deduct for missed optimization opportunities
        score -= len(performance_data['optimization_opportunities']) * 0.05
        
        return max(0.0, score)

# Multi-agent orchestrator
class MultiAgentOrchestrator:
    """Orchestrates multiple analyzer agents"""
    
    def __init__(self):
        self.agents = {
            'structure': CodeStructureAgent(),
            'security': SecurityAuditAgent(),
            'quality': QualityAssessmentAgent(),
            'performance': PerformanceProfilerAgent()
        }
    
    async def run_analysis(self, repo_path: Path, agent_names: List[str] = None) -> Dict[str, AnalysisResult]:
        """Run analysis with specified agents"""
        if agent_names is None:
            agent_names = list(self.agents.keys())
        
        # Run agents in parallel
        tasks = []
        for agent_name in agent_names:
            if agent_name in self.agents:
                task = self.agents[agent_name].analyze(repo_path)
                tasks.append((agent_name, task))
        
        results = {}
        completed_tasks = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        for (agent_name, _), result in zip(tasks, completed_tasks):
            if isinstance(result, Exception):
                results[agent_name] = AnalysisResult(
                    agent_name=agent_name,
                    success=False,
                    execution_time=0.0,
                    data={},
                    errors=[str(result)],
                    warnings=[]
                )
            else:
                results[agent_name] = result
        
        return results

# Example usage
async def test_agents():
    """Test the analyzer agents"""
    # This would be used with a real repository path
    test_repo_path = Path("/tmp/test_repo")
    
    orchestrator = MultiAgentOrchestrator()
    results = await orchestrator.run_analysis(test_repo_path)
    
    for agent_name, result in results.items():
        print(f"\n{agent_name.upper()} ANALYSIS:")
        print(f"Success: {result.success}")
        print(f"Execution time: {result.execution_time:.2f}s")
        if result.errors:
            print(f"Errors: {result.errors}")
        print(f"Data keys: {list(result.data.keys())}")

if __name__ == "__main__":
    asyncio.run(test_agents())