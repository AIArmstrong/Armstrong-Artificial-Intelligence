#!/usr/bin/env python3
"""
Quick GitHub Repository Analyzer
Analyzes ClaudePreference repository without Docker dependencies
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import subprocess
import asyncio
import time

try:
    import git
    from git import Repo
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    print("GitPython not available - using git command directly")

class QuickAnalyzer:
    def __init__(self):
        self.repo_url = None
        self.repo_path = None
        self.analysis_results = {}

    async def analyze_repository(self, repo_url: str):
        """Analyze GitHub repository"""
        self.repo_url = repo_url
        print(f"Starting analysis of: {repo_url}")
        
        try:
            # Step 1: Clone repository
            print("Step 1: Cloning repository...")
            await self._clone_repository()
            
            # Step 2: Run analysis agents
            print("Step 2: Running analysis agents...")
            await self._run_analysis_agents()
            
            # Step 3: Generate results
            print("Step 3: Generating analysis report...")
            return await self._generate_analysis_report()
            
        except Exception as e:
            print(f"Analysis failed: {e}")
            return {"error": str(e), "success": False}
        finally:
            # Cleanup
            if self.repo_path and os.path.exists(self.repo_path):
                try:
                    shutil.rmtree(self.repo_path)
                    print(f"Cleaned up temporary directory: {self.repo_path}")
                except Exception as e:
                    print(f"Warning: Could not clean up {self.repo_path}: {e}")

    async def _clone_repository(self):
        """Clone the repository to temporary directory"""
        temp_dir = tempfile.mkdtemp(prefix="github_analyzer_")
        self.repo_path = temp_dir
        
        try:
            if GIT_AVAILABLE:
                repo = Repo.clone_from(self.repo_url, temp_dir)
                print(f"Successfully cloned repository to: {temp_dir}")
            else:
                # Fallback to git command
                result = subprocess.run([
                    'git', 'clone', self.repo_url, temp_dir
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode != 0:
                    raise Exception(f"Git clone failed: {result.stderr}")
                print(f"Successfully cloned repository to: {temp_dir}")
                
        except Exception as e:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise Exception(f"Failed to clone repository: {e}")

    async def _run_analysis_agents(self):
        """Run analysis agents on cloned repository"""
        repo_path = Path(self.repo_path)
        
        # Code Structure Analysis
        print("  - Running code structure analysis...")
        structure_result = await self._analyze_code_structure(repo_path)
        self.analysis_results['structure'] = structure_result
        
        # Security Analysis
        print("  - Running security analysis...")
        security_result = await self._analyze_security(repo_path)
        self.analysis_results['security'] = security_result
        
        # Quality Analysis
        print("  - Running quality analysis...")
        quality_result = await self._analyze_quality(repo_path)
        self.analysis_results['quality'] = quality_result
        
        # Integration Analysis
        print("  - Running integration analysis...")
        integration_result = await self._analyze_integration_potential(repo_path)
        self.analysis_results['integration'] = integration_result

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

    async def _analyze_integration_potential(self, repo_path: Path):
        """Analyze integration potential with AAI system"""
        integration_data = {
            'compatibility_score': 0.0,
            'integration_opportunities': [],
            'required_adaptations': [],
            'feature_extraction': {}
        }
        
        try:
            # Analyze repository type and features
            features = []
            
            # Check for common patterns
            if list(repo_path.rglob('*.py')):
                features.append('Python codebase')
            if list(repo_path.rglob('*.md')):
                features.append('Documentation-rich')
            if list(repo_path.rglob('*template*')):
                features.append('Template-based')
            if list(repo_path.rglob('*workflow*')):
                features.append('Workflow-oriented')
            if list(repo_path.rglob('*agent*')) or list(repo_path.rglob('*multi*')):
                features.append('Multi-agent architecture')
            
            integration_data['feature_extraction'] = {
                'detected_features': features,
                'repository_type': 'documentation' if len(list(repo_path.rglob('*.md'))) > len(list(repo_path.rglob('*.py'))) else 'code',
                'complexity_level': 'medium'
            }
            
            # Calculate compatibility score
            compatibility_factors = []
            if 'Python codebase' in features:
                compatibility_factors.append(0.3)
            if 'Documentation-rich' in features:
                compatibility_factors.append(0.2)
            if 'Template-based' in features:
                compatibility_factors.append(0.3)
            if 'Workflow-oriented' in features:
                compatibility_factors.append(0.4)
            if 'Multi-agent architecture' in features:
                compatibility_factors.append(0.5)
            
            integration_data['compatibility_score'] = min(1.0, sum(compatibility_factors))
            
            # Generate integration opportunities
            if 'Template-based' in features:
                integration_data['integration_opportunities'].append('Template system integration')
            if 'Workflow-oriented' in features:
                integration_data['integration_opportunities'].append('Workflow automation integration')
            if 'Multi-agent architecture' in features:
                integration_data['integration_opportunities'].append('Multi-agent orchestration patterns')
            
            return {
                'success': True,
                'execution_time': 0.02,
                'data': integration_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'execution_time': 0.0,
                'error': str(e)
            }

    async def _generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        report = {
            'repository_url': self.repo_url,
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_results': self.analysis_results,
            'summary': {},
            'recommendations': []
        }
        
        # Generate summary
        if 'structure' in self.analysis_results and self.analysis_results['structure']['success']:
            struct_data = self.analysis_results['structure']['data']
            report['summary']['total_files'] = struct_data['total_files']
            report['summary']['main_languages'] = dict(struct_data['main_languages'])
            
        if 'quality' in self.analysis_results and self.analysis_results['quality']['success']:
            qual_data = self.analysis_results['quality']['data']
            report['summary']['documentation_score'] = qual_data['documentation_score']
            report['summary']['has_license'] = qual_data['license_present']
            
        if 'integration' in self.analysis_results and self.analysis_results['integration']['success']:
            integ_data = self.analysis_results['integration']['data']
            report['summary']['compatibility_score'] = integ_data['compatibility_score']
            report['summary']['integration_opportunities'] = integ_data['integration_opportunities']
        
        # Generate recommendations
        if report['summary'].get('compatibility_score', 0) > 0.7:
            report['recommendations'].append("High integration potential - recommend detailed integration planning")
        if report['summary'].get('documentation_score', 0) > 0.5:
            report['recommendations'].append("Well-documented - good candidate for workflow template extraction")
        
        report['success'] = True
        return report

async def main():
    if len(sys.argv) != 2:
        print("Usage: python quick_analyzer.py <github_repo_url>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    analyzer = QuickAnalyzer()
    
    start_time = time.time()
    result = await analyzer.analyze_repository(repo_url)
    end_time = time.time()
    
    print(f"\n=== ANALYSIS COMPLETE ===")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    print(f"Success: {result.get('success', False)}")
    
    if result.get('success'):
        print(f"\n=== ANALYSIS SUMMARY ===")
        summary = result.get('summary', {})
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        print(f"\n=== RECOMMENDATIONS ===")
        for rec in result.get('recommendations', []):
            print(f"- {rec}")
        
        # Save detailed results
        output_file = f"claude_preference_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nDetailed analysis saved to: {output_file}")
    else:
        print(f"Analysis failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())