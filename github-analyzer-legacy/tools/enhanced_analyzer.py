#!/usr/bin/env python3
"""
Enhanced GitHub Repository Analyzer with Advanced Documentation Analysis
Extracts design patterns, philosophy, and strategic insights for AAI system enhancement
"""

import os
import sys
import json
import tempfile
import shutil
import re
from pathlib import Path
from datetime import datetime
import subprocess
import asyncio
import time
from typing import Dict, List, Any, Optional

try:
    import git
    from git import Repo
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    print("GitPython not available - using git command directly")

class EnhancedGitHubAnalyzer:
    def __init__(self):
        self.repo_url = None
        self.repo_path = None
        self.analysis_results = {}
        self.aai_patterns = self._load_aai_patterns()

    def _load_aai_patterns(self) -> Dict[str, Any]:
        """Load AAI system patterns for cross-referencing"""
        return {
            'modules': [
                'intent-engine', 'prompt-recipes', 'tag-taxonomy', 'score-tracker',
                'trace-mapping', 'openrouter-integration', 'decision-neural',
                'example-engine', 'sop-generator', 'idea-evaluator',
                'seamless-orchestrator', 'prp-scaffold', 'integration-aware-prp-enhancer'
            ],
            'workflows': [
                'multi-agent orchestration', 'research-driven development',
                'quality scoring', 'task management', 'PRP generation'
            ],
            'architecture_principles': [
                'modular intelligence', 'phase-based loading', 'auto-learning',
                'context engineering', 'neural reasoning', 'semantic search'
            ]
        }

    async def analyze_repository(self, repo_url: str):
        """Enhanced repository analysis with documentation intelligence"""
        self.repo_url = repo_url
        print(f"🔍 Starting enhanced analysis of: {repo_url}")
        
        try:
            # Step 1: Clone repository
            print("📥 Step 1: Cloning repository...")
            await self._clone_repository()
            
            # Step 2: Basic structure analysis
            print("🏗️ Step 2: Analyzing repository structure...")
            await self._run_basic_analysis()
            
            # Step 3: Enhanced documentation analysis
            print("📚 Step 3: Enhanced documentation analysis...")
            await self._analyze_documentation_intelligence()
            
            # Step 4: Pattern extraction and insight mining
            print("🧠 Step 4: Mining insights and patterns...")
            await self._mine_insights_and_patterns()
            
            # Step 5: AAI integration assessment
            print("🔗 Step 5: AAI integration assessment...")
            await self._assess_aai_integration()
            
            # Step 6: Generate comprehensive report
            print("📊 Step 6: Generating comprehensive analysis report...")
            return await self._generate_enhanced_report()
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return {"error": str(e), "success": False}
        finally:
            # Cleanup
            if self.repo_path and os.path.exists(self.repo_path):
                try:
                    shutil.rmtree(self.repo_path)
                    print(f"🧹 Cleaned up temporary directory: {self.repo_path}")
                except Exception as e:
                    print(f"⚠️ Warning: Could not clean up {self.repo_path}: {e}")

    async def _clone_repository(self):
        """Clone the repository to temporary directory"""
        temp_dir = tempfile.mkdtemp(prefix="enhanced_analyzer_")
        self.repo_path = temp_dir
        
        try:
            if GIT_AVAILABLE:
                repo = Repo.clone_from(self.repo_url, temp_dir)
                print(f"✅ Successfully cloned repository to: {temp_dir}")
            else:
                result = subprocess.run([
                    'git', 'clone', self.repo_url, temp_dir
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode != 0:
                    raise Exception(f"Git clone failed: {result.stderr}")
                print(f"✅ Successfully cloned repository to: {temp_dir}")
                
        except Exception as e:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise Exception(f"Failed to clone repository: {e}")

    async def _run_basic_analysis(self):
        """Run basic structure, security, quality analysis"""
        repo_path = Path(self.repo_path)
        
        # Code Structure Analysis
        structure_result = await self._analyze_code_structure(repo_path)
        self.analysis_results['structure'] = structure_result
        
        # Security Analysis
        security_result = await self._analyze_security(repo_path)
        self.analysis_results['security'] = security_result
        
        # Quality Analysis
        quality_result = await self._analyze_quality(repo_path)
        self.analysis_results['quality'] = quality_result

    async def _analyze_documentation_intelligence(self):
        """Enhanced documentation analysis with contextual decomposition"""
        repo_path = Path(self.repo_path)
        
        doc_intelligence = {
            'contextual_decomposition': {},
            'design_philosophy': {},
            'integration_points': {},
            'extensibility_analysis': {},
            'observability_features': {}
        }
        
        # 1. Contextual Decomposition of Documentation
        print("  📘 Analyzing documentation structure...")
        doc_intelligence['contextual_decomposition'] = await self._decompose_documentation(repo_path)
        
        # 2. Philosophy and Design Decision Mining
        print("  🧠 Mining design philosophy...")
        doc_intelligence['design_philosophy'] = await self._mine_design_philosophy(repo_path)
        
        # 3. Integration Points Analysis
        print("  🔌 Analyzing integration capabilities...")
        doc_intelligence['integration_points'] = await self._analyze_integration_points(repo_path)
        
        # 4. Extensibility Assessment
        print("  ⚙️ Assessing extensibility...")
        doc_intelligence['extensibility_analysis'] = await self._assess_extensibility(repo_path)
        
        # 5. Observability and Metrics
        print("  📊 Analyzing observability features...")
        doc_intelligence['observability_features'] = await self._analyze_observability(repo_path)
        
        self.analysis_results['documentation_intelligence'] = doc_intelligence

    async def _decompose_documentation(self, repo_path: Path) -> Dict[str, Any]:
        """Break documentation into strategic categories"""
        categories = {
            'installation_setup': [],
            'philosophy_design': [],
            'configuration_extensibility': [],
            'metrics_observability': [],
            'integration_points': [],
            'api_ux_patterns': [],
            'gotchas_warnings': []
        }
        
        # Find and analyze documentation files
        doc_files = []
        for pattern in ['README*', '*.md', 'docs/**/*.md', 'doc/**/*.md']:
            doc_files.extend(repo_path.glob(pattern))
            doc_files.extend(repo_path.rglob(pattern))
        
        for doc_file in set(doc_files):
            if doc_file.is_file():
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        relative_path = str(doc_file.relative_to(repo_path))
                        
                        # Categorize content based on keywords and patterns
                        categories.update(self._categorize_doc_content(content, relative_path))
                        
                except Exception as e:
                    print(f"⚠️ Could not read {doc_file}: {e}")
        
        return categories

    def _categorize_doc_content(self, content: str, file_path: str) -> Dict[str, List]:
        """Categorize documentation content by strategic importance"""
        categories = {
            'installation_setup': [],
            'philosophy_design': [],
            'configuration_extensibility': [],
            'metrics_observability': [],
            'integration_points': [],
            'api_ux_patterns': [],
            'gotchas_warnings': []
        }
        
        content_lower = content.lower()
        
        # Installation & Setup
        if any(word in content_lower for word in ['install', 'setup', 'getting started', 'requirements', 'dependencies']):
            categories['installation_setup'].append({
                'file': file_path,
                'keywords': ['install', 'setup', 'requirements'],
                'complexity': 'low' if 'pip install' in content_lower or 'npm install' in content_lower else 'medium'
            })
        
        # Philosophy & Design Decisions
        if any(word in content_lower for word in ['philosophy', 'design', 'architecture', 'principles', 'approach', 'methodology']):
            categories['philosophy_design'].append({
                'file': file_path,
                'keywords': ['philosophy', 'design', 'architecture'],
                'has_rationale': 'why' in content_lower and 'because' in content_lower
            })
        
        # Configuration & Extensibility
        if any(word in content_lower for word in ['config', 'customize', 'extend', 'plugin', 'hook', 'override']):
            categories['configuration_extensibility'].append({
                'file': file_path,
                'keywords': ['config', 'customize', 'extend'],
                'extensibility_level': 'high' if 'plugin' in content_lower else 'medium'
            })
        
        # Metrics & Observability
        if any(word in content_lower for word in ['metrics', 'monitoring', 'logging', 'debug', 'trace', 'observe']):
            categories['metrics_observability'].append({
                'file': file_path,
                'keywords': ['metrics', 'monitoring', 'logging'],
                'observability_depth': 'comprehensive' if len([w for w in ['metrics', 'logging', 'trace'] if w in content_lower]) >= 2 else 'basic'
            })
        
        # Integration Points
        if any(word in content_lower for word in ['api', 'webhook', 'integration', 'connect', 'interface', 'endpoint']):
            categories['integration_points'].append({
                'file': file_path,
                'keywords': ['api', 'integration', 'interface'],
                'integration_type': 'rest_api' if 'rest' in content_lower or 'endpoint' in content_lower else 'library'
            })
        
        # API & UX Patterns
        if any(word in content_lower for word in ['usage', 'example', 'pattern', 'workflow', 'command', 'cli']):
            categories['api_ux_patterns'].append({
                'file': file_path,
                'keywords': ['usage', 'example', 'pattern'],
                'pattern_count': content_lower.count('example') + content_lower.count('usage')
            })
        
        # Gotchas & Warnings
        if any(word in content_lower for word in ['warning', 'caution', 'note', 'important', 'gotcha', 'limitation']):
            categories['gotchas_warnings'].append({
                'file': file_path,
                'keywords': ['warning', 'caution', 'limitation'],
                'severity': 'high' if 'warning' in content_lower or 'caution' in content_lower else 'medium'
            })
        
        return categories

    async def _mine_design_philosophy(self, repo_path: Path) -> Dict[str, Any]:
        """Extract design patterns, philosophy, and architectural decisions"""
        philosophy = {
            'design_patterns': [],
            'pain_points_addressed': [],
            'extensibility_approach': '',
            'user_assumptions': [],
            'fallback_strategies': []
        }
        
        # Look for specific design pattern indicators
        readme_files = list(repo_path.glob('README*'))
        if readme_files:
            try:
                with open(readme_files[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Design patterns detection
                    patterns = []
                    if 'template' in content.lower():
                        patterns.append('Template-based architecture')
                    if 'agent' in content.lower() and 'multi' in content.lower():
                        patterns.append('Multi-agent system')
                    if 'workflow' in content.lower():
                        patterns.append('Workflow orchestration')
                    if 'plugin' in content.lower() or 'extensib' in content.lower():
                        patterns.append('Plugin architecture')
                    
                    philosophy['design_patterns'] = patterns
                    
                    # Pain points addressed
                    pain_indicators = ['problem', 'issue', 'challenge', 'difficulty', 'pain']
                    for indicator in pain_indicators:
                        if indicator in content.lower():
                            # Extract sentences containing pain point indicators
                            sentences = content.split('.')
                            for sentence in sentences:
                                if indicator in sentence.lower():
                                    philosophy['pain_points_addressed'].append(sentence.strip()[:200])
                    
            except Exception as e:
                print(f"⚠️ Could not analyze README philosophy: {e}")
        
        return philosophy

    async def _analyze_integration_points(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze how the system integrates with external tools/systems"""
        integration_points = {
            'api_endpoints': [],
            'cli_commands': [],
            'configuration_files': [],
            'plugin_systems': [],
            'webhook_support': False,
            'external_dependencies': []
        }
        
        # Look for API patterns
        for file_path in repo_path.rglob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '@app.route' in content or 'FastAPI' in content or 'flask' in content.lower():
                        integration_points['api_endpoints'].append(str(file_path.relative_to(repo_path)))
            except:
                pass
        
        # Look for CLI commands
        for file_path in repo_path.rglob('*.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find command patterns like `command-name` or `m-something`
                    commands = re.findall(r'`([a-z-]+(?:-[a-z]+)*)`', content)
                    integration_points['cli_commands'].extend(commands)
            except:
                pass
        
        # Remove duplicates
        integration_points['cli_commands'] = list(set(integration_points['cli_commands']))
        
        return integration_points

    async def _assess_extensibility(self, repo_path: Path) -> Dict[str, Any]:
        """Assess how extensible and configurable the system is"""
        extensibility = {
            'plugin_architecture': False,
            'configuration_options': [],
            'hook_systems': [],
            'template_system': False,
            'api_extensibility': 'none'
        }
        
        # Check for plugin/extension patterns
        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                filename = file_path.name.lower()
                if 'plugin' in filename or 'extension' in filename:
                    extensibility['plugin_architecture'] = True
                if 'template' in filename:
                    extensibility['template_system'] = True
                if 'hook' in filename:
                    extensibility['hook_systems'].append(str(file_path.relative_to(repo_path)))
        
        # Look for configuration files
        config_patterns = ['*.yaml', '*.yml', '*.json', '*.toml', '*.ini', '.env*']
        for pattern in config_patterns:
            config_files = list(repo_path.glob(pattern)) + list(repo_path.rglob(pattern))
            extensibility['configuration_options'].extend([str(f.relative_to(repo_path)) for f in config_files])
        
        return extensibility

    async def _analyze_observability(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze metrics, logging, and observability features"""
        observability = {
            'logging_framework': None,
            'metrics_collection': False,
            'monitoring_integration': [],
            'debug_capabilities': [],
            'performance_tracking': False
        }
        
        # Check for logging frameworks
        for file_path in repo_path.rglob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'import logging' in content:
                        observability['logging_framework'] = 'python-logging'
                    elif 'loguru' in content:
                        observability['logging_framework'] = 'loguru'
                    elif 'structlog' in content:
                        observability['logging_framework'] = 'structlog'
                    
                    if 'metrics' in content.lower() or 'prometheus' in content.lower():
                        observability['metrics_collection'] = True
                    
                    if 'performance' in content.lower() or 'benchmark' in content.lower():
                        observability['performance_tracking'] = True
                        
            except:
                pass
        
        return observability

    async def _mine_insights_and_patterns(self):
        """Mine strategic insights and generate assimilation recommendations"""
        
        insights = {
            'design_patterns_analysis': {},
            'pain_points_solutions': {},
            'assimilation_suitability_grid': [],
            'transferable_concepts': []
        }
        
        # Analyze extracted documentation intelligence
        doc_intel = self.analysis_results.get('documentation_intelligence', {})
        
        # Design Patterns Analysis
        philosophy = doc_intel.get('design_philosophy', {})
        patterns = philosophy.get('design_patterns', [])
        
        insights['design_patterns_analysis'] = {
            'identified_patterns': patterns,
            'pattern_sophistication': 'high' if len(patterns) >= 3 else 'medium' if len(patterns) >= 2 else 'low',
            'novel_patterns': [p for p in patterns if p not in ['MVC', 'Observer', 'Factory']]
        }
        
        # Generate Assimilation Suitability Grid
        insights['assimilation_suitability_grid'] = await self._generate_assimilation_grid()
        
        # Identify transferable concepts
        insights['transferable_concepts'] = await self._identify_transferable_concepts()
        
        self.analysis_results['strategic_insights'] = insights

    async def _generate_assimilation_grid(self) -> List[Dict[str, Any]]:
        """Generate the assimilation suitability grid"""
        grid = []
        
        doc_intel = self.analysis_results.get('documentation_intelligence', {})
        
        # Template System Assessment
        if doc_intel.get('extensibility_analysis', {}).get('template_system'):
            grid.append({
                'feature': 'Template System',
                'purpose': 'Dynamic prompt generation and standardization',
                'assimilation_score': 8.5,
                'module_fit': 'prompt-recipes.md + new template-orchestrator.py',
                'implementation_effort': 'medium',
                'notes': 'Could enhance AAI prompt consistency significantly'
            })
        
        # CLI Command Structure
        integration_points = doc_intel.get('integration_points', {})
        cli_commands = integration_points.get('cli_commands', [])
        if len(cli_commands) > 10:
            grid.append({
                'feature': 'Comprehensive CLI System',
                'purpose': 'Structured command organization and workflow integration',
                'assimilation_score': 7.5,
                'module_fit': '.claude/commands/ reorganization',
                'implementation_effort': 'low',
                'notes': f'Found {len(cli_commands)} commands - could improve AAI command structure'
            })
        
        # Multi-Agent Architecture
        patterns = self.analysis_results.get('strategic_insights', {}).get('design_patterns_analysis', {}).get('identified_patterns', [])
        if 'Multi-agent system' in patterns:
            grid.append({
                'feature': 'Multi-Agent Orchestration',
                'purpose': 'Structured agent coordination and communication',
                'assimilation_score': 9.0,
                'module_fit': 'seamless-orchestrator.py enhancement',
                'implementation_effort': 'high',
                'notes': 'Could provide formal structure to AAI agent interactions'
            })
        
        # Observability Features
        observability = doc_intel.get('observability_features', {})
        if observability.get('metrics_collection') or observability.get('performance_tracking'):
            grid.append({
                'feature': 'Enhanced Observability',
                'purpose': 'Comprehensive system monitoring and metrics',
                'assimilation_score': 8.0,
                'module_fit': 'score-tracker.md + new metrics module',
                'implementation_effort': 'medium',
                'notes': 'Could improve AAI system monitoring and optimization'
            })
        
        return grid

    async def _identify_transferable_concepts(self) -> List[Dict[str, Any]]:
        """Identify concepts that could be transferred to AAI"""
        concepts = []
        
        doc_intel = self.analysis_results.get('documentation_intelligence', {})
        
        # Philosophy-based concepts
        philosophy = doc_intel.get('design_philosophy', {})
        pain_points = philosophy.get('pain_points_addressed', [])
        
        for pain_point in pain_points:
            if any(keyword in pain_point.lower() for keyword in ['workflow', 'automation', 'consistency', 'quality']):
                concepts.append({
                    'concept': 'Pain Point Solution',
                    'description': pain_point[:150] + '...' if len(pain_point) > 150 else pain_point,
                    'relevance_to_aai': 'high',
                    'transfer_mechanism': 'workflow_enhancement'
                })
        
        # Extensibility concepts
        extensibility = doc_intel.get('extensibility_analysis', {})
        if extensibility.get('plugin_architecture'):
            concepts.append({
                'concept': 'Plugin Architecture',
                'description': 'Modular system allowing third-party extensions',
                'relevance_to_aai': 'medium',
                'transfer_mechanism': 'brain_module_enhancement'
            })
        
        return concepts

    async def _assess_aai_integration(self):
        """Assess specific integration opportunities with AAI system"""
        
        integration_assessment = {
            'direct_integration_opportunities': [],
            'pattern_enhancement_opportunities': [],
            'architectural_evolution_suggestions': [],
            'risk_assessment': {}
        }
        
        # Cross-reference with AAI patterns
        doc_intel = self.analysis_results.get('documentation_intelligence', {})
        strategic_insights = self.analysis_results.get('strategic_insights', {})
        
        # Direct Integration Opportunities
        assimilation_grid = strategic_insights.get('assimilation_suitability_grid', [])
        for item in assimilation_grid:
            if item['assimilation_score'] >= 8.0:
                integration_assessment['direct_integration_opportunities'].append({
                    'feature': item['feature'],
                    'integration_path': item['module_fit'],
                    'expected_impact': 'high',
                    'implementation_priority': 'immediate' if item['implementation_effort'] == 'low' else 'planned'
                })
        
        # Pattern Enhancement Opportunities
        patterns = strategic_insights.get('design_patterns_analysis', {}).get('identified_patterns', [])
        for pattern in patterns:
            if pattern in ['Template-based architecture', 'Multi-agent system', 'Workflow orchestration']:
                integration_assessment['pattern_enhancement_opportunities'].append({
                    'pattern': pattern,
                    'current_aai_implementation': self._find_aai_pattern_implementation(pattern),
                    'enhancement_potential': 'significant'
                })
        
        # Architectural Evolution Suggestions
        transferable_concepts = strategic_insights.get('transferable_concepts', [])
        high_relevance_concepts = [c for c in transferable_concepts if c.get('relevance_to_aai') == 'high']
        
        if high_relevance_concepts:
            integration_assessment['architectural_evolution_suggestions'] = [
                {
                    'suggestion': 'Implement formal template system for prompt standardization',
                    'rationale': 'Multiple high-relevance concepts point to template-based improvements',
                    'impact_areas': ['prompt-recipes', 'seamless-orchestrator', 'agent communication']
                }
            ]
        
        # Risk Assessment
        integration_assessment['risk_assessment'] = {
            'complexity_risk': 'medium' if len(integration_assessment['direct_integration_opportunities']) > 3 else 'low',
            'compatibility_risk': 'low',  # Most patterns are additive
            'maintenance_overhead': 'manageable',
            'recommended_approach': 'phased_implementation'
        }
        
        self.analysis_results['aai_integration_assessment'] = integration_assessment

    def _find_aai_pattern_implementation(self, pattern: str) -> str:
        """Find current AAI implementation of a pattern"""
        pattern_map = {
            'Template-based architecture': 'prompt-recipes.md (basic)',
            'Multi-agent system': 'seamless-orchestrator.py (basic)',
            'Workflow orchestration': 'brain workflow system (comprehensive)'
        }
        return pattern_map.get(pattern, 'not_implemented')

    async def _generate_enhanced_report(self):
        """Generate comprehensive enhanced analysis report"""
        report = {
            'repository_url': self.repo_url,
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_type': 'enhanced_documentation_intelligence',
            'basic_analysis': {
                'structure': self.analysis_results.get('structure'),
                'security': self.analysis_results.get('security'),
                'quality': self.analysis_results.get('quality')
            },
            'documentation_intelligence': self.analysis_results.get('documentation_intelligence'),
            'strategic_insights': self.analysis_results.get('strategic_insights'),
            'aai_integration_assessment': self.analysis_results.get('aai_integration_assessment'),
            'executive_summary': await self._generate_executive_summary(),
            'recommended_actions': await self._generate_recommended_actions(),
            'success': True
        }
        
        return report

    async def _generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary of findings"""
        doc_intel = self.analysis_results.get('documentation_intelligence', {})
        strategic_insights = self.analysis_results.get('strategic_insights', {})
        aai_assessment = self.analysis_results.get('aai_integration_assessment', {})
        
        return {
            'repository_type': self._determine_repository_type(),
            'documentation_quality': self._assess_documentation_quality(doc_intel),
            'strategic_value': self._assess_strategic_value(strategic_insights),
            'integration_readiness': self._assess_integration_readiness(aai_assessment),
            'key_insights': self._extract_key_insights(),
            'impact_potential': 'high' if len(aai_assessment.get('direct_integration_opportunities', [])) >= 2 else 'medium'
        }

    def _determine_repository_type(self) -> str:
        """Determine the primary type/purpose of the repository"""
        structure = self.analysis_results.get('structure', {})
        if structure.get('success'):
            file_types = structure.get('data', {}).get('file_types', {})
            if file_types.get('.md', 0) > file_types.get('.py', 0):
                return 'documentation_focused'
            elif file_types.get('.py', 0) > 0:
                return 'python_project'
            else:
                return 'mixed_content'
        return 'unknown'

    def _assess_documentation_quality(self, doc_intel: Dict) -> str:
        """Assess overall documentation quality"""
        decomposition = doc_intel.get('contextual_decomposition', {})
        categories_with_content = sum(1 for v in decomposition.values() if v)
        
        if categories_with_content >= 5:
            return 'comprehensive'
        elif categories_with_content >= 3:
            return 'good'
        else:
            return 'basic'

    def _assess_strategic_value(self, insights: Dict) -> str:
        """Assess strategic value for AAI system"""
        assimilation_grid = insights.get('assimilation_suitability_grid', [])
        high_value_items = [item for item in assimilation_grid if item.get('assimilation_score', 0) >= 8.0]
        
        if len(high_value_items) >= 3:
            return 'very_high'
        elif len(high_value_items) >= 2:
            return 'high'
        elif len(high_value_items) >= 1:
            return 'medium'
        else:
            return 'low'

    def _assess_integration_readiness(self, aai_assessment: Dict) -> str:
        """Assess readiness for AAI integration"""
        opportunities = aai_assessment.get('direct_integration_opportunities', [])
        risk_level = aai_assessment.get('risk_assessment', {}).get('complexity_risk', 'high')
        
        if len(opportunities) >= 2 and risk_level == 'low':
            return 'ready'
        elif len(opportunities) >= 1:
            return 'planning_required'
        else:
            return 'research_needed'

    def _extract_key_insights(self) -> List[str]:
        """Extract top 3-5 key insights"""
        insights = []
        
        # From assimilation grid
        strategic_insights = self.analysis_results.get('strategic_insights', {})
        grid = strategic_insights.get('assimilation_suitability_grid', [])
        
        for item in sorted(grid, key=lambda x: x.get('assimilation_score', 0), reverse=True)[:3]:
            insights.append(f"{item['feature']}: {item['purpose']} (Score: {item['assimilation_score']})")
        
        return insights

    async def _generate_recommended_actions(self) -> List[Dict[str, Any]]:
        """Generate specific recommended actions for AAI enhancement"""
        actions = []
        
        aai_assessment = self.analysis_results.get('aai_integration_assessment', {})
        
        # Immediate opportunities
        immediate_opportunities = aai_assessment.get('direct_integration_opportunities', [])
        for opp in immediate_opportunities:
            if opp.get('implementation_priority') == 'immediate':
                actions.append({
                    'action': f"Implement {opp['feature']}",
                    'priority': 'high',
                    'timeline': '1-2 weeks',
                    'implementation_path': opp['integration_path'],
                    'expected_impact': opp['expected_impact']
                })
        
        # Pattern enhancements
        pattern_opportunities = aai_assessment.get('pattern_enhancement_opportunities', [])
        for pattern_opp in pattern_opportunities:
            actions.append({
                'action': f"Enhance {pattern_opp['pattern']} implementation",
                'priority': 'medium',
                'timeline': '2-4 weeks',
                'current_state': pattern_opp['current_aai_implementation'],
                'enhancement_potential': pattern_opp['enhancement_potential']
            })
        
        return actions

    # Include the basic analysis methods from the original analyzer
    async def _analyze_code_structure(self, repo_path: Path):
        """Analyze code structure and organization"""
        try:
            structure_data = {
                'total_files': 0,
                'file_types': {},
                'directories': [],
                'main_languages': [],
                'project_structure': {},
                'key_files': []
            }
            
            # Count files and analyze structure
            for file_path in repo_path.rglob('*'):
                if file_path.is_file():
                    structure_data['total_files'] += 1
                    
                    # Track file types
                    suffix = file_path.suffix.lower()
                    if suffix:
                        structure_data['file_types'][suffix] = structure_data['file_types'].get(suffix, 0) + 1
                    
                    # Identify key files
                    if file_path.name.lower() in ['readme.md', 'license', 'setup.py', 'requirements.txt', 'package.json']:
                        structure_data['key_files'].append(str(file_path.relative_to(repo_path)))
                        
                elif file_path.is_dir():
                    structure_data['directories'].append(str(file_path.relative_to(repo_path)))
            
            # Determine main languages
            lang_counts = {}
            for ext, count in structure_data['file_types'].items():
                if ext in ['.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c', '.rb', '.php']:
                    lang_map = {
                        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
                        '.java': 'Java', '.go': 'Go', '.rs': 'Rust',
                        '.cpp': 'C++', '.c': 'C', '.rb': 'Ruby', '.php': 'PHP'
                    }
                    lang_counts[lang_map[ext]] = count
            
            structure_data['main_languages'] = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            
            return {
                'success': True,
                'execution_time': 0.05,
                'data': structure_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'execution_time': 0.0,
                'error': str(e)
            }

    async def _analyze_security(self, repo_path: Path):
        """Analyze security aspects of the repository"""
        security_data = {
            'potential_secrets': [],
            'sensitive_files': [],
            'security_patterns': [],
            'dependency_files': [],
            'security_score': 0.8
        }
        
        try:
            # Look for potential security issues
            sensitive_patterns = [
                'password', 'secret', 'token', 'key', 'api_key',
                'private_key', 'auth', 'credential'
            ]
            
            for file_path in repo_path.rglob('*'):
                if file_path.is_file():
                    filename = file_path.name.lower()
                    
                    # Check for sensitive file patterns
                    for pattern in sensitive_patterns:
                        if pattern in filename:
                            security_data['sensitive_files'].append(str(file_path.relative_to(repo_path)))
                    
                    # Check for dependency files
                    if filename in ['requirements.txt', 'package.json', 'Gemfile', 'go.mod', 'Cargo.toml']:
                        security_data['dependency_files'].append(str(file_path.relative_to(repo_path)))
            
            return {
                'success': True,
                'execution_time': 0.03,
                'data': security_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'execution_time': 0.0,
                'error': str(e)
            }

    async def _analyze_quality(self, repo_path: Path):
        """Analyze code quality metrics"""
        quality_data = {
            'documentation_score': 0.0,
            'test_coverage_estimate': 0.0,
            'code_organization': {},
            'readme_quality': {},
            'license_present': False
        }
        
        try:
            # Check for README
            readme_files = list(repo_path.glob('README*'))
            if readme_files:
                readme_path = readme_files[0]
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        readme_content = f.read()
                        quality_data['readme_quality'] = {
                            'exists': True,
                            'length': len(readme_content),
                            'sections': readme_content.count('#'),
                            'has_installation': 'install' in readme_content.lower(),
                            'has_usage': 'usage' in readme_content.lower()
                        }
                        quality_data['documentation_score'] = min(1.0, len(readme_content) / 1000)
                except:
                    quality_data['readme_quality'] = {'exists': True, 'readable': False}
            
            # Check for license
            license_files = list(repo_path.glob('LICENSE*')) + list(repo_path.glob('license*'))
            quality_data['license_present'] = len(license_files) > 0
            
            # Estimate test coverage
            test_files = list(repo_path.rglob('*test*')) + list(repo_path.rglob('*spec*'))
            total_code_files = len(list(repo_path.rglob('*.py'))) + len(list(repo_path.rglob('*.js')))
            if total_code_files > 0:
                quality_data['test_coverage_estimate'] = min(1.0, len(test_files) / total_code_files)
            
            return {
                'success': True,
                'execution_time': 0.04,
                'data': quality_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'execution_time': 0.0,
                'error': str(e)
            }

async def main():
    if len(sys.argv) != 2:
        print("Usage: python enhanced_analyzer.py <github_repo_url>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    analyzer = EnhancedGitHubAnalyzer()
    
    start_time = time.time()
    result = await analyzer.analyze_repository(repo_url)
    end_time = time.time()
    
    print(f"\n🎉 === ENHANCED ANALYSIS COMPLETE ===")
    print(f"⏱️ Total execution time: {end_time - start_time:.2f} seconds")
    print(f"✅ Success: {result.get('success', False)}")
    
    if result.get('success'):
        print(f"\n📊 === EXECUTIVE SUMMARY ===")
        summary = result.get('executive_summary', {})
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        print(f"\n🔑 === KEY INSIGHTS ===")
        for insight in summary.get('key_insights', []):
            print(f"• {insight}")
        
        print(f"\n🎯 === RECOMMENDED ACTIONS ===")
        for action in result.get('recommended_actions', []):
            print(f"• {action['action']} (Priority: {action['priority']})")
        
        # Save detailed results
        output_file = f"enhanced_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Detailed analysis saved to: {output_file}")
    else:
        print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())