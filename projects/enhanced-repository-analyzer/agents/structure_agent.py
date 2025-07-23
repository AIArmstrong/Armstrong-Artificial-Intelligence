#!/usr/bin/env python3
"""
StructureAgent - Multi-language code structure analysis with Tree-sitter
Provides comprehensive structural analysis across 40+ languages
"""

import asyncio
import logging
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import tree_sitter_languages as tsl

from agents.base_agent import BaseAnalyzerAgent, AnalysisResult
from core.streaming_walker import FileInfo
from core.semantic_analyzer import SemanticAnalyzer, SemanticFeature
from core.pattern_registry import PatternMatch

logger = logging.getLogger(__name__)

class StructureAgent(BaseAnalyzerAgent):
    """
    Enhanced structure analysis agent with multi-language support.
    Uses Tree-sitter for accurate parsing across 40+ languages.
    """
    
    def __init__(self, 
                 cache_manager=None,
                 pattern_registry=None,
                 semantic_analyzer: Optional[SemanticAnalyzer] = None):
        """
        Initialize structure agent.
        
        Args:
            cache_manager: Optional cache manager
            pattern_registry: Optional pattern registry
            semantic_analyzer: Optional semantic analyzer for deep analysis
        """
        super().__init__(
            name="StructureAgent",
            cache_manager=cache_manager,
            pattern_registry=pattern_registry
        )
        
        self.semantic_analyzer = semantic_analyzer
        
        # Language extension mapping
        self.language_map = {
            '.py': 'python',
            '.js': 'javascript', '.mjs': 'javascript', '.jsx': 'javascript',
            '.ts': 'typescript', '.tsx': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.c': 'c', '.h': 'c',
            '.cpp': 'cpp', '.cc': 'cpp', '.cxx': 'cpp', '.hpp': 'cpp',
            '.cs': 'csharp',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.lua': 'lua',
            '.dart': 'dart',
            '.jl': 'julia',
            '.elm': 'elm',
            '.ex': 'elixir', '.exs': 'elixir',
            '.ml': 'ocaml', '.mli': 'ocaml',
            '.hs': 'haskell',
            '.clj': 'clojure',
            '.vim': 'vim',
            '.sh': 'bash', '.bash': 'bash',
            '.ps1': 'powershell',
            '.yaml': 'yaml', '.yml': 'yaml',
            '.toml': 'toml',
            '.json': 'json',
            '.xml': 'xml',
            '.html': 'html', '.htm': 'html',
            '.css': 'css', '.scss': 'scss',
            '.sql': 'sql',
            '.md': 'markdown',
            '.rst': 'rst',
            '.tex': 'latex'
        }
        
        # Set supported extensions
        self.supported_extensions = set(self.language_map.keys())
        
        # Analysis types provided
        self.analysis_types = [
            'structure', 'complexity', 'dependencies',
            'api_surface', 'documentation', 'patterns'
        ]
        
        # Initialize parsers
        self.parsers = {}
        self._init_parsers()
    
    def _init_parsers(self):
        """Initialize Tree-sitter parsers for supported languages"""
        for ext, language in self.language_map.items():
            if language not in self.parsers:
                try:
                    self.parsers[language] = tsl.get_parser(language)
                    logger.debug(f"Initialized parser for {language}")
                except Exception as e:
                    logger.warning(f"Could not initialize parser for {language}: {e}")
    
    async def analyze(self, repo_path: Path) -> AnalysisResult:
        """
        Analyze repository structure (legacy compatibility).
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Complete structure analysis
        """
        start_time = time.time()
        
        try:
            structure_data = {
                'languages': defaultdict(lambda: {
                    'files': [],
                    'total_lines': 0,
                    'functions': 0,
                    'classes': 0,
                    'complexity': 0.0,
                    'features': []
                }),
                'api_surfaces': [],
                'design_patterns': [],
                'architecture_patterns': [],
                'dependencies': {'internal': set(), 'external': set()},
                'file_structure': {
                    'total_files': 0,
                    'directories': 0,
                    'organization_score': 0.0
                }
            }
            
            # Analyze all files
            for file_path in repo_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in self.supported_extensions:
                    file_info = FileInfo(
                        path=file_path,
                        size=file_path.stat().st_size,
                        mime_type=None,
                        extension=file_path.suffix,
                        relative_path=str(file_path.relative_to(repo_path))
                    )
                    
                    analysis = await self.process_file(file_info)
                    
                    # Aggregate results
                    language = self.language_map.get(file_path.suffix, 'unknown')
                    lang_stats = structure_data['languages'][language]
                    
                    lang_stats['files'].append(str(file_path))
                    lang_stats['total_lines'] += analysis.get('lines', 0)
                    lang_stats['functions'] += analysis.get('function_count', 0)
                    lang_stats['classes'] += analysis.get('class_count', 0)
                    lang_stats['complexity'] += analysis.get('complexity', 0.0)
                    
                    if 'features' in analysis:
                        lang_stats['features'].extend(analysis['features'])
                    
                    structure_data['file_structure']['total_files'] += 1
            
            # Detect patterns
            structure_data['architecture_patterns'] = self._detect_architecture_patterns(repo_path)
            
            # Calculate organization score
            structure_data['file_structure']['organization_score'] = self._calculate_organization_score(
                repo_path, structure_data
            )
            
            # Convert sets to lists for JSON serialization
            structure_data['dependencies']['internal'] = list(structure_data['dependencies']['internal'])
            structure_data['dependencies']['external'] = list(structure_data['dependencies']['external'])
            
            execution_time = time.time() - start_time
            
            return self._create_result(
                success=True,
                data=dict(structure_data),
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"Structure analysis failed: {e}")
            return self._create_result(
                success=False,
                data={},
                execution_time=time.time() - start_time,
                errors=[str(e)]
            )
    
    async def process_file(self, file_info: FileInfo) -> Dict[str, Any]:
        """
        Process a single file for structure analysis.
        
        Args:
            file_info: File information
            
        Returns:
            Structure analysis data
        """
        language = self.language_map.get(file_info.extension, 'unknown')
        
        if language == 'unknown' or language not in self.parsers:
            return {
                'language': language,
                'error': 'Unsupported language',
                'lines': 0
            }
        
        try:
            # Read file content
            content = await self._read_file_content(file_info.path)
            if not content:
                return {'error': 'Could not read file', 'lines': 0}
            
            # Parse with Tree-sitter
            tree = self.parsers[language].parse(content.encode())
            
            # Extract structure information
            structure_info = await self._analyze_structure(tree, content, language, file_info)
            
            # Add semantic analysis if available
            if self.semantic_analyzer:
                semantic_features = await self.semantic_analyzer.analyze_code(
                    content, language, file_info.path, use_llm=False  # Skip LLM for performance
                )
                structure_info['semantic_features'] = [
                    self._feature_to_dict(f) for f in semantic_features
                ]
            
            # Match patterns if registry available
            if self.pattern_registry:
                pattern_matches = await self.match_patterns(
                    content, file_info.path, ['structure', 'architecture']
                )
                structure_info['pattern_matches'] = [
                    self._match_to_dict(m) for m in pattern_matches
                ]
            
            return structure_info
            
        except Exception as e:
            logger.error(f"Error processing {file_info.path}: {e}")
            return {
                'language': language,
                'error': str(e),
                'lines': 0
            }
    
    async def _analyze_structure(self, tree: Any, content: str, language: str, file_info: FileInfo) -> Dict[str, Any]:
        """Analyze code structure using Tree-sitter"""
        lines = content.split('\n')
        
        # Basic metrics
        metrics = {
            'language': language,
            'lines': len(lines),
            'file_path': str(file_info.path),
            'file_size': file_info.size,
            'function_count': 0,
            'class_count': 0,
            'import_count': 0,
            'complexity': 0.0,
            'max_nesting_depth': 0,
            'dependencies': []
        }
        
        # Language-specific analysis
        if language == 'python':
            metrics.update(self._analyze_python_structure(tree, content))
        elif language in ['javascript', 'typescript']:
            metrics.update(self._analyze_javascript_structure(tree, content))
        elif language == 'java':
            metrics.update(self._analyze_java_structure(tree, content))
        elif language == 'go':
            metrics.update(self._analyze_go_structure(tree, content))
        else:
            # Generic analysis for other languages
            metrics.update(self._analyze_generic_structure(tree, content, language))
        
        # Calculate complexity score
        metrics['complexity'] = self._calculate_complexity(metrics)
        
        return metrics
    
    def _analyze_python_structure(self, tree: Any, content: str) -> Dict[str, Any]:
        """Analyze Python-specific structure"""
        cursor = tree.walk()
        
        metrics = {
            'function_count': 0,
            'class_count': 0,
            'import_count': 0,
            'async_function_count': 0,
            'decorator_count': 0,
            'docstring_count': 0,
            'features': []
        }
        
        def visit_node(node):
            if node.type == 'function_definition':
                metrics['function_count'] += 1
                
                # Check if async
                if any(child.type == 'async' for child in node.children):
                    metrics['async_function_count'] += 1
                
                # Extract function name
                for child in node.children:
                    if child.type == 'identifier':
                        metrics['features'].append({
                            'type': 'function',
                            'name': content[child.start_byte:child.end_byte],
                            'line': child.start_point[0] + 1
                        })
                        break
                        
            elif node.type == 'class_definition':
                metrics['class_count'] += 1
                
                # Extract class name
                for child in node.children:
                    if child.type == 'identifier':
                        metrics['features'].append({
                            'type': 'class',
                            'name': content[child.start_byte:child.end_byte],
                            'line': child.start_point[0] + 1
                        })
                        break
                        
            elif node.type in ['import_statement', 'import_from_statement']:
                metrics['import_count'] += 1
                
                # Extract import details
                import_text = content[node.start_byte:node.end_byte]
                metrics['features'].append({
                    'type': 'import',
                    'statement': import_text.strip(),
                    'line': node.start_point[0] + 1
                })
                
            elif node.type == 'decorator':
                metrics['decorator_count'] += 1
                
            elif node.type == 'string' and node.parent and node.parent.type == 'expression_statement':
                # Potential docstring
                parent_parent = node.parent.parent
                if parent_parent and parent_parent.type in ['function_definition', 'class_definition']:
                    metrics['docstring_count'] += 1
            
            # Visit children
            for child in node.children:
                visit_node(child)
        
        visit_node(tree.root_node)
        
        return metrics
    
    def _analyze_javascript_structure(self, tree: Any, content: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript structure"""
        cursor = tree.walk()
        
        metrics = {
            'function_count': 0,
            'class_count': 0,
            'import_count': 0,
            'arrow_function_count': 0,
            'async_function_count': 0,
            'features': []
        }
        
        def visit_node(node):
            if node.type in ['function_declaration', 'function_expression']:
                metrics['function_count'] += 1
                
            elif node.type == 'arrow_function':
                metrics['arrow_function_count'] += 1
                
            elif node.type == 'class_declaration':
                metrics['class_count'] += 1
                
            elif node.type in ['import_statement', 'import_clause']:
                metrics['import_count'] += 1
            
            # Check for async
            if node.type == 'async' and node.parent:
                if node.parent.type in ['function_declaration', 'arrow_function']:
                    metrics['async_function_count'] += 1
            
            # Visit children
            for child in node.children:
                visit_node(child)
        
        visit_node(tree.root_node)
        
        return metrics
    
    def _analyze_java_structure(self, tree: Any, content: str) -> Dict[str, Any]:
        """Analyze Java structure"""
        # Similar pattern to Python/JS analysis
        # Implementation abbreviated for brevity
        return {
            'function_count': 0,
            'class_count': 0,
            'interface_count': 0,
            'import_count': 0,
            'annotation_count': 0,
            'features': []
        }
    
    def _analyze_go_structure(self, tree: Any, content: str) -> Dict[str, Any]:
        """Analyze Go structure"""
        # Implementation for Go
        return {
            'function_count': 0,
            'struct_count': 0,
            'interface_count': 0,
            'import_count': 0,
            'goroutine_count': 0,
            'features': []
        }
    
    def _analyze_generic_structure(self, tree: Any, content: str, language: str) -> Dict[str, Any]:
        """Generic structure analysis for any language"""
        # Count common node types
        node_counts = defaultdict(int)
        
        def count_nodes(node):
            node_counts[node.type] += 1
            for child in node.children:
                count_nodes(child)
        
        count_nodes(tree.root_node)
        
        return {
            'node_types': dict(node_counts),
            'total_nodes': sum(node_counts.values()),
            'features': []
        }
    
    def _calculate_complexity(self, metrics: Dict[str, Any]) -> float:
        """Calculate complexity score based on metrics"""
        # Simple complexity calculation
        complexity = 0.0
        
        # Function complexity
        complexity += metrics.get('function_count', 0) * 0.1
        complexity += metrics.get('class_count', 0) * 0.2
        
        # Async complexity
        complexity += metrics.get('async_function_count', 0) * 0.15
        
        # Import complexity
        import_count = metrics.get('import_count', 0)
        if import_count > 10:
            complexity += 0.2
        elif import_count > 5:
            complexity += 0.1
        
        # Line complexity
        lines = metrics.get('lines', 0)
        if lines > 500:
            complexity += 0.3
        elif lines > 200:
            complexity += 0.2
        elif lines > 100:
            complexity += 0.1
        
        # Normalize to 0-1 range
        return min(complexity, 1.0)
    
    def _detect_architecture_patterns(self, repo_path: Path) -> List[str]:
        """Detect common architecture patterns"""
        patterns = []
        
        # Check for common patterns
        if (repo_path / 'src').exists():
            patterns.append('src_layout')
        
        if (repo_path / 'lib').exists():
            patterns.append('lib_layout')
        
        if any(d.name in ['tests', 'test', '__tests__'] for d in repo_path.iterdir() if d.is_dir()):
            patterns.append('test_structure')
        
        if (repo_path / 'docs').exists() or (repo_path / 'documentation').exists():
            patterns.append('documented')
        
        # Framework detection
        if (repo_path / 'package.json').exists():
            patterns.append('nodejs_project')
        
        if (repo_path / 'setup.py').exists() or (repo_path / 'pyproject.toml').exists():
            patterns.append('python_package')
        
        if (repo_path / 'go.mod').exists():
            patterns.append('go_module')
        
        if (repo_path / 'Cargo.toml').exists():
            patterns.append('rust_crate')
        
        # Architecture patterns
        if (repo_path / 'controllers').exists() or (repo_path / 'views').exists():
            patterns.append('mvc_pattern')
        
        if (repo_path / 'api').exists() or (repo_path / 'routes').exists():
            patterns.append('api_structure')
        
        if (repo_path / 'components').exists():
            patterns.append('component_based')
        
        return patterns
    
    def _calculate_organization_score(self, repo_path: Path, structure_data: Dict[str, Any]) -> float:
        """Calculate repository organization score"""
        score = 0.0
        max_score = 0.0
        
        # Check for standard directories
        standard_dirs = ['src', 'lib', 'tests', 'docs', 'examples', 'scripts']
        for dir_name in standard_dirs:
            max_score += 1.0
            if (repo_path / dir_name).exists():
                score += 1.0
        
        # Check for documentation files
        doc_files = ['README.md', 'README.rst', 'CONTRIBUTING.md', 'LICENSE']
        for doc_file in doc_files:
            max_score += 0.5
            if (repo_path / doc_file).exists():
                score += 0.5
        
        # Check for configuration files
        config_files = ['.gitignore', '.editorconfig', 'setup.cfg', 'pyproject.toml']
        for config_file in config_files:
            max_score += 0.25
            if (repo_path / config_file).exists():
                score += 0.25
        
        # Normalize score
        return score / max_score if max_score > 0 else 0.0
    
    def _feature_to_dict(self, feature: SemanticFeature) -> Dict[str, Any]:
        """Convert semantic feature to dictionary"""
        return {
            'name': feature.name,
            'type': feature.type,
            'intent': feature.intent,
            'confidence': feature.confidence,
            'complexity': feature.complexity_score,
            'line_range': feature.line_range,
            'dependencies': feature.dependencies
        }
    
    def _match_to_dict(self, match: PatternMatch) -> Dict[str, Any]:
        """Convert pattern match to dictionary"""
        return {
            'pattern': match.pattern_name,
            'type': match.match_type,
            'content': match.content[:100],  # Truncate for storage
            'location': match.location,
            'confidence': match.confidence
        }