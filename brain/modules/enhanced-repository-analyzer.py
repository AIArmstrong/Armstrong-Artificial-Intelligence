#!/usr/bin/env python3
"""
Enhanced Repository Analyzer - AAI Brain Integration Module
Provides intelligent repository analysis with semantic understanding and learning capabilities
"""

import asyncio
import json
import logging
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import sys

# Add the enhanced analyzer to path for imports
enhanced_analyzer_path = Path(__file__).parent.parent.parent / "projects" / "enhanced-repository-analyzer"
sys.path.insert(0, str(enhanced_analyzer_path))

from core.cache_manager import CacheManager
from core.pattern_registry import PatternRegistry
from core.semantic_analyzer import SemanticAnalyzer
from core.streaming_walker import StreamingFileWalker
from agents.structure_agent import StructureAgent
from integrations.openrouter_integration import OpenRouterIntegration

# Import AAI brain modules for integration
from brain.modules.unified_analytics import UnifiedAnalytics
from brain.modules.integration_aware_prp_enhancer import IntegrationAwarePRPEnhancer

# Import Supreme Improve modules for multi-dimensional quality scoring
try:
    from brain.modules.supreme_improve import (
        MultiDimensionalScorer,
        QualityMetrics,
        ImprovementRecommendation
    )
    SUPREME_IMPROVE_AVAILABLE = True
except ImportError:
    logger.warning("Supreme Improve modules not available - quality scoring disabled")
    SUPREME_IMPROVE_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class AnalysisSession:
    """Represents an analysis session with metrics"""
    session_id: str
    repository_path: str
    start_time: str
    end_time: Optional[str] = None
    analysis_types: List[str] = None
    performance_metrics: Dict[str, float] = None
    success: bool = True
    errors: List[str] = None
    insights_generated: int = 0
    patterns_detected: int = 0

class EnhancedRepositoryAnalyzer:
    """
    Enhanced Repository Analyzer with AAI brain integration.
    Provides intelligent analysis, learning, and integration recommendations.
    """
    
    def __init__(self, base_path: str = "/mnt/c/Users/Brandon/AAI"):
        """
        Initialize enhanced repository analyzer.
        
        Args:
            base_path: Base path to AAI installation
        """
        self.base_path = Path(base_path)
        self.projects_path = self.base_path / "projects" / "enhanced-repository-analyzer"
        self.db_path = self.base_path / "brain" / "enhanced_analyzer.db"
        
        # Core components
        self.cache_manager = None
        self.pattern_registry = None
        self.semantic_analyzer = None
        self.streaming_walker = None
        self.structure_agent = None
        self.openrouter_client = None
        
        # AAI brain integration
        self.unified_analytics = UnifiedAnalytics(str(self.base_path))
        self.integration_enhancer = IntegrationAwarePRPEnhancer(str(self.base_path))
        
        # Supreme Improve integration - Multi-dimensional quality scoring
        if SUPREME_IMPROVE_AVAILABLE:
            self.quality_scorer = MultiDimensionalScorer()
            logger.info("Multi-dimensional quality scoring enabled")
        else:
            self.quality_scorer = None
        
        # Session tracking
        self.current_session: Optional[AnalysisSession] = None
        
        # Initialize database
        self._init_database()
        
        # Initialize components
        asyncio.create_task(self._init_components())
    
    def _init_database(self):
        """Initialize enhanced analyzer database"""
        self.db_path.parent.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analysis sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                repository_path TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                analysis_types TEXT,  -- JSON array
                performance_metrics TEXT,  -- JSON object
                success BOOLEAN NOT NULL,
                errors TEXT,  -- JSON array
                insights_generated INTEGER DEFAULT 0,
                patterns_detected INTEGER DEFAULT 0,
                created_date TEXT NOT NULL
            )
        ''')
        
        # Performance benchmarks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_benchmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                benchmark_type TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                target_value REAL,
                threshold_met BOOLEAN,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id)
            )
        ''')
        
        # Learning events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                pattern_name TEXT,
                confidence_score REAL,
                event_data TEXT,  -- JSON object
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id)
            )
        ''')
        
        # Integration recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integration_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                repository_path TEXT NOT NULL,
                integration_type TEXT NOT NULL,
                confidence_score REAL NOT NULL,
                recommendation_data TEXT,  -- JSON object
                implemented BOOLEAN DEFAULT FALSE,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id)
            )
        ''')
        
        # Quality metrics table for multi-dimensional scoring
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quality_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                file_path TEXT,
                maintainability_score REAL,
                complexity_score REAL,
                readability_score REAL,
                test_coverage REAL,
                documentation_score REAL,
                security_score REAL,
                performance_score REAL,
                overall_score REAL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def _init_components(self):
        """Initialize enhanced analyzer components"""
        try:
            # Initialize cache
            cache_dir = self.base_path / "brain" / "cache" / "enhanced-analyzer"
            self.cache_manager = CacheManager(disk_cache_dir=cache_dir)
            
            # Initialize pattern registry
            self.pattern_registry = PatternRegistry()
            
            # Initialize OpenRouter if available
            try:
                self.openrouter_client = OpenRouterIntegration()
                self.semantic_analyzer = SemanticAnalyzer(self.openrouter_client)
                logger.info("OpenRouter integration initialized")
            except Exception as e:
                logger.warning(f"OpenRouter not available: {e}")
                self.semantic_analyzer = SemanticAnalyzer()
            
            # Initialize streaming walker
            self.streaming_walker = StreamingFileWalker()
            
            # Initialize structure agent
            self.structure_agent = StructureAgent(
                cache_manager=self.cache_manager,
                pattern_registry=self.pattern_registry,
                semantic_analyzer=self.semantic_analyzer
            )
            
            # Register agents
            self.streaming_walker.register_agent('structure', self.structure_agent)
            
            logger.info("Enhanced Repository Analyzer components initialized")
            
        except Exception as e:
            logger.error(f"Component initialization failed: {e}")
            raise
    
    async def analyze_repository(self,
                               repository_path: str,
                               analysis_types: List[str] = None,
                               use_semantic: bool = True,
                               performance_targets: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Perform comprehensive repository analysis.
        
        Args:
            repository_path: Path to repository
            analysis_types: Types of analysis to perform
            use_semantic: Enable semantic analysis
            performance_targets: Performance targets to validate
            
        Returns:
            Complete analysis results with brain integration
        """
        session_id = f"session_{int(time.time())}"
        repo_path = Path(repository_path)
        
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repository_path}")
        
        # Start session
        session = AnalysisSession(
            session_id=session_id,
            repository_path=str(repo_path),
            start_time=datetime.now().isoformat(),
            analysis_types=analysis_types or ['structure', 'semantic', 'patterns']
        )
        self.current_session = session
        
        start_time = time.time()
        
        try:
            # Track session in database
            await self._track_session_start(session)
            
            results = {
                'session_id': session_id,
                'repository_path': str(repo_path),
                'analysis_types': session.analysis_types,
                'performance_metrics': {},
                'insights': [],
                'recommendations': [],
                'success': True,
                'errors': []
            }
            
            # Perform structure analysis
            if 'structure' in session.analysis_types:
                structure_result = await self.structure_agent.analyze(repo_path)
                results['structure_analysis'] = {
                    'success': structure_result.success,
                    'data': structure_result.data,
                    'execution_time': structure_result.execution_time,
                    'patterns_matched': len(structure_result.patterns_matched),
                    'cache_hit': structure_result.cache_hit
                }
                
                # Track patterns detected
                session.patterns_detected += len(structure_result.patterns_matched)
            
            # Perform semantic analysis if enabled
            if 'semantic' in session.analysis_types and use_semantic:
                semantic_results = []
                
                # Analyze key files for semantic insights
                key_files = self._identify_key_files(repo_path)
                for file_path in key_files:
                    try:
                        features = await self.semantic_analyzer.analyze_file(
                            file_path, use_llm=bool(self.openrouter_client)
                        )
                        if features:
                            semantic_results.extend(features)
                    except Exception as e:
                        logger.warning(f"Semantic analysis failed for {file_path}: {e}")
                
                results['semantic_analysis'] = {
                    'features_count': len(semantic_results),
                    'features': [self._feature_to_dict(f) for f in semantic_results[:20]],  # Limit for response size
                    'high_confidence_features': len([f for f in semantic_results if f.confidence > 0.8])
                }
                
                session.insights_generated += len(semantic_results)
            
            # Perform multi-dimensional quality scoring
            if 'quality' in session.analysis_types or 'quality' not in session.analysis_types:  # Default to always include quality
                quality_results = await self._perform_quality_analysis(repo_path, session_id)
                results['quality_analysis'] = quality_results
                
                # Generate improvement recommendations based on quality analysis
                if quality_results.get('project_metrics') and self.quality_scorer:
                    improvement_recommendations = await self._generate_improvement_recommendations(
                        repo_path, quality_results
                    )
                    results['improvement_recommendations'] = improvement_recommendations
            
            # Generate integration recommendations
            if 'integration' in session.analysis_types:
                recommendations = await self._generate_integration_recommendations(repo_path, results)
                results['integration_recommendations'] = recommendations
            
            # Calculate performance metrics
            execution_time = time.time() - start_time
            performance_metrics = await self._calculate_performance_metrics(execution_time, results)
            results['performance_metrics'] = performance_metrics
            session.performance_metrics = performance_metrics
            
            # Validate against targets
            if performance_targets:
                validation_results = self._validate_performance_targets(performance_metrics, performance_targets)
                results['performance_validation'] = validation_results
            
            # Update session
            session.end_time = datetime.now().isoformat()
            session.success = True
            
            # Track session completion
            await self._track_session_complete(session)
            
            # Log learning events
            await self._log_learning_events(session, results)
            
            # Update unified analytics
            await self._update_unified_analytics(session, results)
            
            return results
            
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")
            
            session.end_time = datetime.now().isoformat()
            session.success = False
            session.errors = [str(e)]
            
            await self._track_session_complete(session)
            
            return {
                'session_id': session_id,
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def _identify_key_files(self, repo_path: Path) -> List[Path]:
        """Identify key files for semantic analysis"""
        key_files = []
        
        # Look for main entry points
        entry_points = ['main.py', 'app.py', 'index.js', 'main.go', 'main.rs']
        for entry in entry_points:
            file_path = repo_path / entry
            if file_path.exists():
                key_files.append(file_path)
        
        # Look for configuration files
        config_files = ['setup.py', 'package.json', 'Cargo.toml', 'go.mod']
        for config in config_files:
            file_path = repo_path / config
            if file_path.exists():
                key_files.append(file_path)
        
        # Sample other files (limit to avoid overwhelming analysis)
        for ext in ['.py', '.js', '.go', '.rs', '.java']:
            files = list(repo_path.rglob(f"*{ext}"))[:5]  # Limit to 5 files per type
            key_files.extend(files)
        
        return key_files[:20]  # Maximum 20 files for semantic analysis
    
    async def _generate_integration_recommendations(self, repo_path: Path, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate integration recommendations using AAI brain"""
        recommendations = []
        
        try:
            # Read some repository content for analysis
            readme_path = repo_path / "README.md"
            content = ""
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # Use integration enhancer to detect potential integrations
            # This would normally analyze the content, but for now we'll use basic detection
            
            # Check for common patterns
            if 'web.{0,20}(scrap|crawl|extract)' in content.lower():
                recommendations.append({
                    'type': 'jina',
                    'confidence': 0.8,
                    'reason': 'Web scraping patterns detected',
                    'benefits': ['Content extraction', 'Data harvesting', 'Document processing']
                })
            
            if 'llm.{0,20}(integration|api|call)' in content.lower() or 'ai' in content.lower():
                recommendations.append({
                    'type': 'openrouter',
                    'confidence': 0.9,
                    'reason': 'AI/LLM integration patterns detected',
                    'benefits': ['Semantic analysis', 'Content generation', 'Intelligent processing']
                })
            
            if 'database.{0,20}(integration|connection|storage)' in content.lower():
                recommendations.append({
                    'type': 'supabase',
                    'confidence': 0.7,
                    'reason': 'Database integration patterns detected',
                    'benefits': ['Real-time data', 'Authentication', 'Storage solution']
                })
            
        except Exception as e:
            logger.error(f"Integration recommendation failed: {e}")
        
        return recommendations
    
    async def _calculate_performance_metrics(self, execution_time: float, results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate performance metrics for the analysis"""
        metrics = {
            'total_execution_time': execution_time,
            'cache_hit_rate': 0.0,
            'files_per_second': 0.0,
            'memory_efficiency': 0.0,
            'semantic_accuracy': 0.0
        }
        
        # Cache hit rate
        if self.cache_manager:
            cache_stats = await self.cache_manager.get_statistics()
            metrics['cache_hit_rate'] = cache_stats['performance']['overall_hit_rate']
        
        # Files per second (from structure analysis)
        if 'structure_analysis' in results:
            structure_data = results['structure_analysis']['data']
            total_files = structure_data.get('file_structure', {}).get('total_files', 0)
            if total_files > 0 and execution_time > 0:
                metrics['files_per_second'] = total_files / execution_time
        
        # Semantic accuracy (based on high confidence features)
        if 'semantic_analysis' in results:
            semantic_data = results['semantic_analysis']
            total_features = semantic_data.get('features_count', 0)
            high_conf_features = semantic_data.get('high_confidence_features', 0)
            if total_features > 0:
                metrics['semantic_accuracy'] = high_conf_features / total_features
        
        return metrics
    
    def _validate_performance_targets(self, metrics: Dict[str, float], targets: Dict[str, float]) -> Dict[str, bool]:
        """Validate performance metrics against targets"""
        validation = {}
        
        for target_name, target_value in targets.items():
            if target_name in metrics:
                validation[target_name] = metrics[target_name] >= target_value
            else:
                validation[target_name] = False
        
        return validation
    
    def _feature_to_dict(self, feature) -> Dict[str, Any]:
        """Convert semantic feature to dictionary"""
        return {
            'name': feature.name,
            'type': feature.type,
            'intent': feature.intent,
            'confidence': feature.confidence,
            'complexity': feature.complexity_score,
            'line_range': feature.line_range,
            'dependencies': feature.dependencies[:5]  # Limit for response size
        }
    
    async def _track_session_start(self, session: AnalysisSession):
        """Track session start in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO analysis_sessions 
                (session_id, repository_path, start_time, analysis_types, success, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session.session_id,
                session.repository_path,
                session.start_time,
                json.dumps(session.analysis_types),
                session.success,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to track session start: {e}")
    
    async def _track_session_complete(self, session: AnalysisSession):
        """Track session completion in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE analysis_sessions 
                SET end_time = ?, performance_metrics = ?, success = ?, errors = ?,
                    insights_generated = ?, patterns_detected = ?
                WHERE session_id = ?
            ''', (
                session.end_time,
                json.dumps(session.performance_metrics) if session.performance_metrics else None,
                session.success,
                json.dumps(session.errors) if session.errors else None,
                session.insights_generated,
                session.patterns_detected,
                session.session_id
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to track session completion: {e}")
    
    async def _log_learning_events(self, session: AnalysisSession, results: Dict[str, Any]):
        """Log learning events for AAI brain system"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Log performance learning event
            if session.performance_metrics:
                cursor.execute('''
                    INSERT INTO learning_events 
                    (session_id, event_type, confidence_score, event_data, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    session.session_id,
                    'performance_metrics',
                    1.0,
                    json.dumps(session.performance_metrics),
                    datetime.now().isoformat()
                ))
            
            # Log pattern detection events
            if session.patterns_detected > 0:
                cursor.execute('''
                    INSERT INTO learning_events 
                    (session_id, event_type, pattern_name, confidence_score, event_data, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    session.session_id,
                    'pattern_detection',
                    'multiple_patterns',
                    0.9,
                    json.dumps({'patterns_count': session.patterns_detected}),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to log learning events: {e}")
    
    async def _update_unified_analytics(self, session: AnalysisSession, results: Dict[str, Any]):
        """Update unified analytics for cross-system learning"""
        try:
            # Track this as a successful enhanced analyzer usage
            self.unified_analytics.track_prp_to_project(
                prp_id="enhanced-repository-analyzer",
                project_id=f"analysis-{session.session_id}",
                template_ids=["repository_analysis"],
                integration_ids=["tree-sitter", "openrouter"] if self.openrouter_client else ["tree-sitter"],
                status="completed" if session.success else "failed"
            )
            
            # Update success metrics if analysis was successful
            if session.success and session.performance_metrics:
                execution_time = session.performance_metrics.get('total_execution_time', 0)
                cache_hit_rate = session.performance_metrics.get('cache_hit_rate', 0)
                
                # This would update template metrics in the unified analytics
                # For now, log the success
                logger.info(f"Enhanced analyzer success: {execution_time:.2f}s, cache hit rate: {cache_hit_rate:.2%}")
            
        except Exception as e:
            logger.error(f"Failed to update unified analytics: {e}")
    
    async def _perform_quality_analysis(self, repo_path: Path, session_id: str) -> Dict[str, Any]:
        """Perform multi-dimensional quality analysis for Supreme integration"""
        quality_results = {
            "file_metrics": {},
            "project_metrics": {},
            "score_distribution": {},
            "quality_trends": []
        }
        
        try:
            # Analyze Python files for quality metrics
            python_files = list(repo_path.rglob("*.py"))
            total_score = 0
            file_count = 0
            
            # Track scores for distribution
            maintainability_scores = []
            complexity_scores = []
            readability_scores = []
            
            for py_file in python_files[:20]:  # Limit to 20 files for performance
                try:
                    # Read file content
                    with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    lines = content.split('\n')
                    line_count = len(lines)
                    
                    # Calculate basic quality metrics
                    maintainability = self._calculate_maintainability_score(content, line_count)
                    complexity = self._calculate_complexity_score(content, lines)
                    readability = self._calculate_readability_score(content, lines)
                    test_coverage = self._estimate_test_coverage(py_file, repo_path)
                    documentation = self._calculate_documentation_score(content, lines)
                    security = self._calculate_security_score(content)
                    performance = self._calculate_performance_score(content)
                    
                    # Calculate overall score
                    overall = (maintainability + complexity + readability + test_coverage + 
                              documentation + security + performance) / 7.0
                    
                    file_metrics = {
                        "maintainability_score": maintainability,
                        "complexity_score": complexity,
                        "readability_score": readability,
                        "test_coverage": test_coverage,
                        "documentation_score": documentation,
                        "security_score": security,
                        "performance_score": performance,
                        "overall_score": overall,
                        "line_count": line_count
                    }
                    
                    quality_results["file_metrics"][str(py_file.relative_to(repo_path))] = file_metrics
                    
                    # Track for aggregation
                    maintainability_scores.append(maintainability)
                    complexity_scores.append(complexity)
                    readability_scores.append(readability)
                    total_score += overall
                    file_count += 1
                    
                    # Store in database
                    await self._store_quality_metrics(session_id, str(py_file), file_metrics)
                    
                except Exception as e:
                    logger.warning(f"Quality analysis failed for {py_file}: {e}")
            
            # Calculate project-level metrics
            if file_count > 0:
                quality_results["project_metrics"] = {
                    "average_maintainability": sum(maintainability_scores) / len(maintainability_scores),
                    "average_complexity": sum(complexity_scores) / len(complexity_scores),
                    "average_readability": sum(readability_scores) / len(readability_scores),
                    "overall_project_score": total_score / file_count,
                    "files_analyzed": file_count,
                    "total_python_files": len(python_files)
                }
                
                # Score distribution analysis
                quality_results["score_distribution"] = {
                    "excellent_files": len([s for s in [overall] if s >= 0.8]),
                    "good_files": len([s for s in [overall] if 0.6 <= s < 0.8]),
                    "needs_improvement": len([s for s in [overall] if s < 0.6])
                }
            
        except Exception as e:
            logger.error(f"Quality analysis failed: {e}")
            quality_results["error"] = str(e)
        
        return quality_results
    
    async def _generate_improvement_recommendations(self, repo_path: Path, quality_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate improvement recommendations based on quality analysis"""
        recommendations = []
        
        try:
            project_metrics = quality_results.get("project_metrics", {})
            file_metrics = quality_results.get("file_metrics", {})
            
            # Overall project recommendations
            overall_score = project_metrics.get("overall_project_score", 0)
            if overall_score < 0.6:
                recommendations.append({
                    "type": "critical",
                    "category": "project_health",
                    "title": "Critical: Overall code quality below 60%",
                    "description": "Project requires significant refactoring and quality improvements",
                    "priority": "high",
                    "estimated_effort": "3-5 days",
                    "impact": "high",
                    "specific_actions": [
                        "Focus on files with lowest quality scores first",
                        "Implement comprehensive code review process",
                        "Add automated quality gates to CI/CD"
                    ]
                })
            
            # Maintainability recommendations
            avg_maintainability = project_metrics.get("average_maintainability", 0)
            if avg_maintainability < 0.7:
                recommendations.append({
                    "type": "improvement",
                    "category": "maintainability",
                    "title": "Improve code maintainability",
                    "description": "Code complexity and structure need attention",
                    "priority": "medium",
                    "estimated_effort": "2-3 days",
                    "impact": "medium",
                    "specific_actions": [
                        "Break down large functions into smaller ones",
                        "Extract reusable components",
                        "Improve variable and function naming"
                    ]
                })
            
            # File-specific recommendations
            low_quality_files = []
            for file_path, metrics in file_metrics.items():
                if metrics.get("overall_score", 0) < 0.5:
                    low_quality_files.append({
                        "file": file_path,
                        "score": metrics.get("overall_score", 0),
                        "main_issues": self._identify_main_issues(metrics)
                    })
            
            if low_quality_files:
                recommendations.append({
                    "type": "targeted",
                    "category": "file_quality",
                    "title": f"Address {len(low_quality_files)} low-quality files",
                    "description": "Specific files require immediate attention",
                    "priority": "high" if len(low_quality_files) > 5 else "medium",
                    "estimated_effort": f"{len(low_quality_files) * 0.5:.1f} hours",
                    "impact": "high",
                    "files": low_quality_files[:10],  # Limit to top 10
                    "specific_actions": [
                        "Refactor files with lowest scores first",
                        "Add unit tests for untested files",
                        "Improve documentation and comments"
                    ]
                })
            
            # Test coverage recommendations
            if any(metrics.get("test_coverage", 0) < 0.5 for metrics in file_metrics.values()):
                recommendations.append({
                    "type": "improvement",
                    "category": "testing",
                    "title": "Increase test coverage",
                    "description": "Many files lack adequate test coverage",
                    "priority": "medium",
                    "estimated_effort": "1-2 days",
                    "impact": "medium",
                    "specific_actions": [
                        "Create unit tests for core functionality",
                        "Add integration tests for key workflows",
                        "Set up code coverage reporting"
                    ]
                })
            
            # Security recommendations
            security_issues = []
            for file_path, metrics in file_metrics.items():
                if metrics.get("security_score", 1.0) < 0.8:
                    security_issues.append(file_path)
            
            if security_issues:
                recommendations.append({
                    "type": "security",
                    "category": "security",
                    "title": "Address security concerns",
                    "description": f"Security issues found in {len(security_issues)} files",
                    "priority": "high",
                    "estimated_effort": "1-2 days",
                    "impact": "critical",
                    "affected_files": security_issues[:10],
                    "specific_actions": [
                        "Review and remove hardcoded secrets",
                        "Implement proper input validation",
                        "Update dependencies with security vulnerabilities"
                    ]
                })
                
        except Exception as e:
            logger.error(f"Failed to generate improvement recommendations: {e}")
            recommendations.append({
                "type": "error",
                "category": "system",
                "title": "Recommendation generation failed",
                "description": f"Error occurred: {str(e)}",
                "priority": "low",
                "estimated_effort": "N/A",
                "impact": "none"
            })
        
        return recommendations
    
    def _calculate_maintainability_score(self, content: str, line_count: int) -> float:
        """Calculate maintainability score (0.0-1.0)"""
        score = 1.0
        
        # Penalize very large files
        if line_count > 500:
            score -= 0.3
        elif line_count > 300:
            score -= 0.1
            
        # Check for long functions
        long_functions = content.count('def ') + content.count('function ')
        if long_functions > 10:
            score -= 0.2
            
        # Check for complex nesting (simple heuristic)
        nesting_level = max(len(line) - len(line.lstrip()) for line in content.split('\n'))
        if nesting_level > 32:  # More than 8 levels of 4-space indentation
            score -= 0.2
            
        return max(0.0, score)
    
    def _calculate_complexity_score(self, content: str, lines: List[str]) -> float:
        """Calculate complexity score (0.0-1.0)"""
        score = 1.0
        
        # Count cyclomatic complexity indicators
        complexity_keywords = ['if ', 'elif ', 'for ', 'while ', 'try:', 'except', 'and ', 'or ']
        complexity_count = sum(content.count(keyword) for keyword in complexity_keywords)
        
        if complexity_count > 50:
            score -= 0.4
        elif complexity_count > 20:
            score -= 0.2
        
        return max(0.0, score)
    
    def _calculate_readability_score(self, content: str, lines: List[str]) -> float:
        """Calculate readability score (0.0-1.0)"""
        score = 1.0
        
        # Check comment ratio
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        total_code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        
        if total_code_lines > 0:
            comment_ratio = comment_lines / total_code_lines
            if comment_ratio < 0.1:  # Less than 10% comments
                score -= 0.3
            elif comment_ratio < 0.05:  # Less than 5% comments
                score -= 0.5
        
        # Check for descriptive variable names (simple heuristic)
        short_vars = len([word for word in content.split() if len(word) == 1 and word.isalpha()])
        if short_vars > 10:
            score -= 0.2
        
        return max(0.0, score)
    
    def _estimate_test_coverage(self, file_path: Path, repo_path: Path) -> float:
        """Estimate test coverage for a file (0.0-1.0)"""
        # Look for corresponding test file
        relative_path = file_path.relative_to(repo_path)
        test_patterns = [
            repo_path / "tests" / f"test_{file_path.name}",
            repo_path / "test" / f"test_{file_path.name}",
            file_path.parent / f"test_{file_path.name}",
            repo_path / f"test_{relative_path}",
        ]
        
        for test_path in test_patterns:
            if test_path.exists():
                return 0.8  # Assume good coverage if test file exists
        
        # Check if it's already a test file
        if "test" in file_path.name.lower():
            return 1.0
            
        return 0.2  # Low coverage assumption if no test file found
    
    def _calculate_documentation_score(self, content: str, lines: List[str]) -> float:
        """Calculate documentation score (0.0-1.0)"""
        score = 0.5  # Base score
        
        # Check for docstrings
        if '"""' in content or "'''" in content:
            score += 0.3
        
        # Check for type hints
        if ': ' in content and '->' in content:
            score += 0.2
            
        return min(1.0, score)
    
    def _calculate_security_score(self, content: str) -> float:
        """Calculate security score (0.0-1.0)"""
        score = 1.0
        
        # Check for security red flags
        security_issues = ['password', 'secret', 'key', 'token', 'api_key', 'private_key']
        for issue in security_issues:
            if issue in content.lower():
                score -= 0.2
        
        # Check for SQL injection patterns
        if 'execute(' in content and '%' in content:
            score -= 0.3
            
        return max(0.0, score)
    
    def _calculate_performance_score(self, content: str) -> float:
        """Calculate performance score (0.0-1.0)"""
        score = 1.0
        
        # Check for performance red flags
        if 'import *' in content:
            score -= 0.1
            
        # Count nested loops (simple heuristic)
        nested_loops = content.count('for ') + content.count('while ')
        if nested_loops > 5:
            score -= 0.2
            
        return max(0.0, score)
    
    def _identify_main_issues(self, metrics: Dict[str, Any]) -> List[str]:
        """Identify main quality issues for a file"""
        issues = []
        
        if metrics.get("maintainability_score", 1.0) < 0.6:
            issues.append("low maintainability")
        if metrics.get("complexity_score", 1.0) < 0.6:
            issues.append("high complexity")
        if metrics.get("test_coverage", 1.0) < 0.5:
            issues.append("poor test coverage")
        if metrics.get("security_score", 1.0) < 0.8:
            issues.append("security concerns")
        if metrics.get("documentation_score", 1.0) < 0.5:
            issues.append("lacks documentation")
            
        return issues
    
    async def _store_quality_metrics(self, session_id: str, file_path: str, metrics: Dict[str, Any]):
        """Store quality metrics in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO quality_metrics 
                (session_id, file_path, maintainability_score, complexity_score, readability_score,
                 test_coverage, documentation_score, security_score, performance_score, overall_score, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                file_path,
                metrics.get("maintainability_score", 0),
                metrics.get("complexity_score", 0),
                metrics.get("readability_score", 0),
                metrics.get("test_coverage", 0),
                metrics.get("documentation_score", 0),
                metrics.get("security_score", 0),
                metrics.get("performance_score", 0),
                metrics.get("overall_score", 0),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store quality metrics: {e}")
    
    def get_session_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get session statistics for the last N days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate cutoff date
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            # Get session statistics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_sessions,
                    SUM(success) as successful_sessions,
                    AVG(insights_generated) as avg_insights,
                    AVG(patterns_detected) as avg_patterns,
                    AVG(json_extract(performance_metrics, '$.total_execution_time')) as avg_execution_time
                FROM analysis_sessions 
                WHERE created_date > ?
            ''', (cutoff_date,))
            
            stats = cursor.fetchone()
            
            conn.close()
            
            return {
                'total_sessions': stats[0] or 0,
                'successful_sessions': stats[1] or 0,
                'success_rate': (stats[1] / stats[0]) if stats[0] > 0 else 0,
                'avg_insights_per_session': stats[2] or 0,
                'avg_patterns_per_session': stats[3] or 0,
                'avg_execution_time': stats[4] or 0,
                'days_analyzed': days
            }
            
        except Exception as e:
            logger.error(f"Failed to get session statistics: {e}")
            return {}

# Global instance for module usage
enhanced_analyzer = EnhancedRepositoryAnalyzer()

# Async initialization
async def initialize_enhanced_analyzer():
    """Initialize the enhanced analyzer"""
    await enhanced_analyzer._init_components()

# Export main functions
async def analyze_repository(repository_path: str, **kwargs) -> Dict[str, Any]:
    """Main analysis function for external use"""
    return await enhanced_analyzer.analyze_repository(repository_path, **kwargs)

def get_analyzer_statistics(days: int = 30) -> Dict[str, Any]:
    """Get analyzer statistics for external use"""
    return enhanced_analyzer.get_session_statistics(days)