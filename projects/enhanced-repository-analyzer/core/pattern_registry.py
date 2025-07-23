#!/usr/bin/env python3
"""
PatternRegistry - Pre-compiled regex and AST pattern storage
Provides efficient pattern matching with versioning and dynamic loading
"""

import re
import json
import logging
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Pattern, Any, Union
from dataclasses import dataclass, asdict
from collections import defaultdict
import yaml
import tree_sitter_languages as tsl

logger = logging.getLogger(__name__)

@dataclass
class CompiledPattern:
    """Represents a compiled pattern with metadata"""
    name: str
    pattern_type: str  # 'regex', 'ast', 'composite'
    pattern: Union[Pattern, Dict[str, Any], str]
    description: str
    tags: List[str]
    version: str
    created_at: str
    language: Optional[str] = None  # For AST patterns
    confidence: float = 0.9
    examples: List[str] = None

@dataclass
class PatternMatch:
    """Result of a pattern match"""
    pattern_name: str
    match_type: str
    content: str
    location: Optional[Tuple[int, int]] = None  # (start_line, end_line)
    confidence: float = 1.0
    metadata: Dict[str, Any] = None

class PatternRegistry:
    """
    Registry for pre-compiled patterns with efficient matching.
    Supports regex, AST, and composite patterns.
    """
    
    def __init__(self, patterns_dir: Optional[Path] = None):
        """
        Initialize pattern registry.
        
        Args:
            patterns_dir: Directory containing pattern definitions
        """
        self.patterns_dir = patterns_dir or Path('patterns')
        self.regex_patterns: Dict[str, CompiledPattern] = {}
        self.ast_patterns: Dict[str, Dict[str, CompiledPattern]] = defaultdict(dict)  # language -> patterns
        self.composite_patterns: Dict[str, CompiledPattern] = {}
        
        # Pattern categories
        self.categories = {
            'security': ['injection', 'auth', 'crypto', 'validation'],
            'performance': ['n+1', 'memory_leak', 'inefficient_loop', 'blocking_io'],
            'quality': ['duplication', 'complexity', 'naming', 'documentation'],
            'architecture': ['layering', 'coupling', 'pattern_violation', 'anti_pattern'],
            'testing': ['missing_test', 'test_smell', 'assertion', 'coverage']
        }
        
        # Load built-in patterns
        self._load_builtin_patterns()
        
        # Load custom patterns from directory
        if self.patterns_dir.exists():
            self._load_custom_patterns()
    
    def _load_builtin_patterns(self):
        """Load built-in pattern definitions"""
        # Security patterns
        self.register_regex_pattern(
            name='sql_injection_risk',
            pattern=r'(execute|query)\s*\(\s*["\'].*?\+.*?["\']',
            description='Potential SQL injection via string concatenation',
            tags=['security', 'sql', 'injection'],
            confidence=0.8
        )
        
        self.register_regex_pattern(
            name='hardcoded_secret',
            pattern=r'(password|secret|key|token)\s*=\s*["\'][^"\']+["\']',
            description='Hardcoded secret or credential',
            tags=['security', 'secrets'],
            confidence=0.7
        )
        
        # Performance patterns
        self.register_regex_pattern(
            name='synchronous_io_in_async',
            pattern=r'async\s+def.*?\n.*?(open|requests\.|urllib)',
            description='Synchronous I/O operation in async function',
            tags=['performance', 'async', 'blocking'],
            confidence=0.9
        )
        
        # Quality patterns
        self.register_regex_pattern(
            name='todo_fixme',
            pattern=r'#\s*(TODO|FIXME|HACK|XXX|BUG)\b.*',
            description='Code comment indicating technical debt',
            tags=['quality', 'technical_debt'],
            confidence=1.0
        )
        
        self.register_regex_pattern(
            name='long_line',
            pattern=r'^.{121,}$',
            description='Line exceeding 120 characters',
            tags=['quality', 'style'],
            confidence=1.0
        )
        
        # Architecture patterns
        self.register_regex_pattern(
            name='import_violation',
            pattern=r'from\s+\.\.(\.+)\s+import',
            description='Import from parent package (potential layering violation)',
            tags=['architecture', 'imports'],
            confidence=0.6
        )
        
        # Integration patterns (from AAI patterns)
        integration_patterns = {
            "ai_automation": r"ai.{0,20}(assist|help|automat|generat)",
            "llm_integration": r"llm.{0,20}(integration|api|call)",
            "web_scraping": r"web.{0,20}(scrap|crawl|extract)",
            "database_integration": r"database.{0,20}(integration|connection|storage)",
            "multi_agent": r"multi.{0,20}agent",
            "semantic_analysis": r"semantic.{0,20}(analysis|understanding|processing)"
        }
        
        for name, pattern in integration_patterns.items():
            self.register_regex_pattern(
                name=f'integration_{name}',
                pattern=pattern,
                description=f'Pattern indicating {name.replace("_", " ")} integration',
                tags=['integration', 'detection'],
                confidence=0.85
            )
    
    def register_regex_pattern(self, 
                             name: str,
                             pattern: str,
                             description: str,
                             tags: List[str],
                             confidence: float = 0.9,
                             flags: int = re.IGNORECASE | re.MULTILINE) -> bool:
        """
        Register a new regex pattern.
        
        Args:
            name: Unique pattern name
            pattern: Regex pattern string
            description: Pattern description
            tags: Pattern tags for categorization
            confidence: Confidence score for matches
            flags: Regex compilation flags
            
        Returns:
            True if registered successfully
        """
        try:
            compiled_regex = re.compile(pattern, flags)
            
            self.regex_patterns[name] = CompiledPattern(
                name=name,
                pattern_type='regex',
                pattern=compiled_regex,
                description=description,
                tags=tags,
                version='1.0',
                created_at=datetime.now().isoformat(),
                confidence=confidence
            )
            
            logger.debug(f"Registered regex pattern: {name}")
            return True
            
        except re.error as e:
            logger.error(f"Failed to compile regex pattern {name}: {e}")
            return False
    
    def register_ast_pattern(self,
                           name: str,
                           language: str,
                           query: str,
                           description: str,
                           tags: List[str],
                           confidence: float = 0.9) -> bool:
        """
        Register a Tree-sitter AST pattern.
        
        Args:
            name: Unique pattern name
            language: Programming language
            query: Tree-sitter query string
            description: Pattern description
            tags: Pattern tags
            confidence: Confidence score
            
        Returns:
            True if registered successfully
        """
        try:
            # Validate language is supported
            lang = tsl.get_language(language)
            
            # Store query string (will be compiled when needed)
            self.ast_patterns[language][name] = CompiledPattern(
                name=name,
                pattern_type='ast',
                pattern=query,
                description=description,
                tags=tags,
                version='1.0',
                created_at=datetime.now().isoformat(),
                language=language,
                confidence=confidence
            )
            
            logger.debug(f"Registered AST pattern: {name} for {language}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register AST pattern {name}: {e}")
            return False
    
    def match_regex_patterns(self, 
                           content: str,
                           tags: Optional[List[str]] = None,
                           min_confidence: float = 0.0) -> List[PatternMatch]:
        """
        Match content against all regex patterns.
        
        Args:
            content: Text content to match
            tags: Filter patterns by tags
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of pattern matches
        """
        matches = []
        
        for pattern_name, pattern_def in self.regex_patterns.items():
            # Filter by tags if specified
            if tags and not any(tag in pattern_def.tags for tag in tags):
                continue
            
            # Skip if below confidence threshold
            if pattern_def.confidence < min_confidence:
                continue
            
            # Find all matches
            for match in pattern_def.pattern.finditer(content):
                # Calculate line numbers
                start_line = content[:match.start()].count('\n') + 1
                end_line = content[:match.end()].count('\n') + 1
                
                matches.append(PatternMatch(
                    pattern_name=pattern_name,
                    match_type='regex',
                    content=match.group(0),
                    location=(start_line, end_line),
                    confidence=pattern_def.confidence,
                    metadata={
                        'groups': match.groups(),
                        'span': match.span()
                    }
                ))
        
        return matches
    
    def match_ast_patterns(self,
                         tree: Any,
                         language: str,
                         content: str,
                         tags: Optional[List[str]] = None,
                         min_confidence: float = 0.0) -> List[PatternMatch]:
        """
        Match AST patterns against a parsed tree.
        
        Args:
            tree: Tree-sitter parse tree
            language: Programming language
            content: Original source content
            tags: Filter patterns by tags
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of pattern matches
        """
        matches = []
        
        if language not in self.ast_patterns:
            return matches
        
        # Get language object
        try:
            lang = tsl.get_language(language)
        except Exception:
            logger.error(f"Unsupported language for AST matching: {language}")
            return matches
        
        for pattern_name, pattern_def in self.ast_patterns[language].items():
            # Filter by tags if specified
            if tags and not any(tag in pattern_def.tags for tag in tags):
                continue
            
            # Skip if below confidence threshold
            if pattern_def.confidence < min_confidence:
                continue
            
            try:
                # Create query from pattern
                query = lang.query(pattern_def.pattern)
                
                # Execute query
                captures = query.captures(tree.root_node)
                
                for node, capture_name in captures:
                    # Extract matched content
                    matched_content = content[node.start_byte:node.end_byte]
                    
                    matches.append(PatternMatch(
                        pattern_name=pattern_name,
                        match_type='ast',
                        content=matched_content,
                        location=(node.start_point[0] + 1, node.end_point[0] + 1),
                        confidence=pattern_def.confidence,
                        metadata={
                            'node_type': node.type,
                            'capture_name': capture_name
                        }
                    ))
                    
            except Exception as e:
                logger.error(f"Error matching AST pattern {pattern_name}: {e}")
        
        return matches
    
    def _load_custom_patterns(self):
        """Load custom patterns from patterns directory"""
        # Load regex patterns
        regex_file = self.patterns_dir / 'regex_patterns.yaml'
        if regex_file.exists():
            try:
                with open(regex_file, 'r') as f:
                    patterns = yaml.safe_load(f)
                    
                for pattern_data in patterns.get('patterns', []):
                    self.register_regex_pattern(**pattern_data)
                    
            except Exception as e:
                logger.error(f"Error loading regex patterns: {e}")
        
        # Load AST patterns
        ast_file = self.patterns_dir / 'ast_patterns.yaml'
        if ast_file.exists():
            try:
                with open(ast_file, 'r') as f:
                    patterns = yaml.safe_load(f)
                    
                for pattern_data in patterns.get('patterns', []):
                    self.register_ast_pattern(**pattern_data)
                    
            except Exception as e:
                logger.error(f"Error loading AST patterns: {e}")
    
    def export_patterns(self, output_file: Path) -> None:
        """Export all patterns to a file"""
        patterns_data = {
            'regex_patterns': {
                name: asdict(pattern) for name, pattern in self.regex_patterns.items()
            },
            'ast_patterns': {
                lang: {name: asdict(pattern) for name, pattern in lang_patterns.items()}
                for lang, lang_patterns in self.ast_patterns.items()
            },
            'composite_patterns': {
                name: asdict(pattern) for name, pattern in self.composite_patterns.items()
            },
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'total_patterns': len(self.regex_patterns) + sum(len(p) for p in self.ast_patterns.values()),
                'categories': self.categories
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(patterns_data, f, indent=2, default=str)
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get statistics about registered patterns"""
        total_regex = len(self.regex_patterns)
        total_ast = sum(len(patterns) for patterns in self.ast_patterns.values())
        
        tag_counts = defaultdict(int)
        for pattern in self.regex_patterns.values():
            for tag in pattern.tags:
                tag_counts[tag] += 1
        
        for lang_patterns in self.ast_patterns.values():
            for pattern in lang_patterns.values():
                for tag in pattern.tags:
                    tag_counts[tag] += 1
        
        return {
            'total_patterns': total_regex + total_ast,
            'regex_patterns': total_regex,
            'ast_patterns': total_ast,
            'languages': list(self.ast_patterns.keys()),
            'tag_distribution': dict(tag_counts),
            'categories': self.categories
        }