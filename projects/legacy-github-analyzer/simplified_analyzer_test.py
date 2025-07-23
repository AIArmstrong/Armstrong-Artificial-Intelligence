#!/usr/bin/env python3
"""
Simplified GitHub Repository Analyzer Test
Tests the analyzer system on a manually cloned repository
"""

import asyncio
import json
import logging
import os
import shutil
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path

from analyzer_agents import MultiAgentOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def clone_repository_simple(repo_url: str, target_dir: Path) -> bool:
    """Simple repository cloning using git command"""
    try:
        # Clean target directory if it exists
        if target_dir.exists():
            shutil.rmtree(target_dir)
        
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Clone using git command
        result = subprocess.run([
            'git', 'clone', '--depth', '1', repo_url, str(target_dir)
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logger.info(f"Successfully cloned {repo_url} to {target_dir}")
            return True
        else:
            logger.error(f"Git clone failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("Git clone timed out")
        return False
    except Exception as e:
        logger.error(f"Clone failed: {e}")
        return False

def analyze_repository_structure(repo_path: Path) -> dict:
    """Simple repository structure analysis"""
    analysis = {
        'total_files': 0,
        'file_types': {},
        'directories': [],
        'size_mb': 0,
        'has_readme': False,
        'has_license': False,
        'has_tests': False
    }
    
    try:
        # Walk through repository
        for item in repo_path.rglob('*'):
            if item.is_file():
                analysis['total_files'] += 1
                
                # Count file types
                suffix = item.suffix.lower()
                if suffix:
                    analysis['file_types'][suffix] = analysis['file_types'].get(suffix, 0) + 1
                
                # Check file size
                try:
                    analysis['size_mb'] += item.stat().st_size / (1024 * 1024)
                except:
                    pass
                
                # Check for important files
                name_lower = item.name.lower()
                if 'readme' in name_lower:
                    analysis['has_readme'] = True
                elif 'license' in name_lower:
                    analysis['has_license'] = True
                elif 'test' in name_lower:
                    analysis['has_tests'] = True
            
            elif item.is_dir() and not item.name.startswith('.'):
                analysis['directories'].append(item.name)
        
        # Sort file types by count
        analysis['file_types'] = dict(sorted(
            analysis['file_types'].items(), 
            key=lambda x: x[1], 
            reverse=True
        ))
        
        logger.info(f"Repository analysis: {analysis['total_files']} files, {analysis['size_mb']:.1f}MB")
        
    except Exception as e:
        logger.error(f"Structure analysis failed: {e}")
    
    return analysis

def identify_technologies(repo_path: Path) -> dict:
    """Identify technologies and frameworks used"""
    technologies = {
        'languages': [],
        'frameworks': [],
        'tools': [],
        'confidence': 'medium'
    }
    
    # Check for language indicators
    indicator_files = {
        'python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
        'javascript': ['package.json', 'npm-shrinkwrap.json', 'yarn.lock'],
        'typescript': ['tsconfig.json', 'tslint.json'],
        'java': ['pom.xml', 'build.gradle', 'gradle.properties'],
        'go': ['go.mod', 'go.sum'],
        'rust': ['Cargo.toml', 'Cargo.lock'],
        'ruby': ['Gemfile', 'Gemfile.lock'],
        'php': ['composer.json', 'composer.lock'],
        'csharp': ['*.csproj', '*.sln'],
        'docker': ['Dockerfile', 'docker-compose.yml']
    }
    
    for tech, files in indicator_files.items():
        for file_pattern in files:
            matches = list(repo_path.rglob(file_pattern))
            if matches:
                technologies['languages'].append(tech)
                break
    
    # Check for specific framework indicators
    framework_indicators = {
        'react': ['package.json'],
        'vue': ['package.json'],
        'angular': ['package.json', 'angular.json'],
        'django': ['manage.py', 'settings.py'],
        'flask': ['app.py', 'requirements.txt'],
        'express': ['package.json'],
        'spring': ['pom.xml']
    }
    
    # Read package.json for JavaScript frameworks
    package_json = repo_path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json, 'r') as f:
                package_data = json.load(f)
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                if 'react' in deps:
                    technologies['frameworks'].append('React')
                if 'vue' in deps:
                    technologies['frameworks'].append('Vue.js')
                if '@angular/core' in deps:
                    technologies['frameworks'].append('Angular')
                if 'express' in deps:
                    technologies['frameworks'].append('Express.js')
                    
        except Exception as e:
            logger.warning(f"Failed to parse package.json: {e}")
    
    # Check requirements.txt for Python frameworks
    requirements_txt = repo_path / 'requirements.txt'
    if requirements_txt.exists():
        try:
            with open(requirements_txt, 'r') as f:
                content = f.read().lower()
                if 'django' in content:
                    technologies['frameworks'].append('Django')
                if 'flask' in content:
                    technologies['frameworks'].append('Flask')
                if 'fastapi' in content:
                    technologies['frameworks'].append('FastAPI')
                if 'streamlit' in content:
                    technologies['frameworks'].append('Streamlit')
                    
        except Exception as e:
            logger.warning(f"Failed to parse requirements.txt: {e}")
    
    return technologies

async def run_comprehensive_analysis(repo_url: str):
    """Run comprehensive analysis on the repository"""
    logger.info(f"Starting comprehensive analysis of {repo_url}")
    start_time = time.time()
    
    # Create temporary directory for cloning
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir) / "repo"
        
        # Clone repository
        logger.info("Cloning repository...")
        if not clone_repository_simple(repo_url, repo_path):
            logger.error("Failed to clone repository")
            return None
        
        # Basic structure analysis
        logger.info("Analyzing repository structure...")
        structure_analysis = analyze_repository_structure(repo_path)
        
        # Technology identification
        logger.info("Identifying technologies...")
        tech_analysis = identify_technologies(repo_path)
        
        # Multi-agent analysis
        logger.info("Running multi-agent analysis...")
        orchestrator = MultiAgentOrchestrator()
        agent_results = await orchestrator.run_analysis(repo_path)
        
        # Compile comprehensive report
        report = {
            'metadata': {
                'repo_url': repo_url,
                'repo_name': repo_url.split('/')[-1].replace('.git', ''),
                'analysis_timestamp': datetime.now().isoformat(),
                'analysis_duration': time.time() - start_time
            },
            'structure_analysis': structure_analysis,
            'technology_analysis': tech_analysis,
            'agent_analysis': {},
            'integration_assessment': {},
            'recommendations': [],
            'issues_found': []
        }
        
        # Process agent results
        for agent_name, result in agent_results.items():
            report['agent_analysis'][agent_name] = {
                'success': result.success,
                'execution_time': result.execution_time,
                'errors': result.errors,
                'warnings': result.warnings,
                'summary': {}
            }
            
            if result.success and result.data:
                # Extract key metrics from each agent
                if agent_name == 'structure':
                    data = result.data
                    summary = {
                        'languages_detected': list(data.get('languages', {}).keys()),
                        'total_functions': sum(lang.get('functions', 0) for lang in data.get('languages', {}).values() if isinstance(lang, dict)),
                        'total_classes': sum(lang.get('classes', 0) for lang in data.get('languages', {}).values() if isinstance(lang, dict)),
                        'architecture_patterns': data.get('architecture_patterns', []),
                        'file_structure_score': data.get('file_structure', {}).get('structure_score', 0)
                    }
                    report['agent_analysis'][agent_name]['summary'] = summary
                
                elif agent_name == 'security':
                    data = result.data
                    summary = {
                        'security_score': data.get('security_score', 0),
                        'vulnerabilities_count': len(data.get('vulnerabilities', [])),
                        'secret_leaks_count': len(data.get('secret_leaks', [])),
                        'dependency_issues_count': len(data.get('dependency_issues', [])),
                        'license_compatible': data.get('license_compliance', {}).get('compatible', None)
                    }
                    report['agent_analysis'][agent_name]['summary'] = summary
                
                elif agent_name == 'quality':
                    data = result.data
                    summary = {
                        'overall_score': data.get('overall_score', 0),
                        'test_coverage': data.get('test_coverage', 0),
                        'documentation_score': data.get('documentation_score', 0),
                        'technical_debt_items': len(data.get('technical_debt', [])),
                        'average_complexity': data.get('code_complexity', {}).get('average_complexity', 0)
                    }
                    report['agent_analysis'][agent_name]['summary'] = summary
                
                elif agent_name == 'performance':
                    data = result.data
                    summary = {
                        'performance_score': data.get('performance_score', 0),
                        'bottlenecks_count': len(data.get('bottlenecks', [])),
                        'optimization_opportunities': len(data.get('optimization_opportunities', [])),
                        'resource_intensive_files': len(data.get('resource_usage', {}).get('memory_intensive', []))
                    }
                    report['agent_analysis'][agent_name]['summary'] = summary
        
        # Generate integration assessment
        report['integration_assessment'] = generate_integration_assessment(report)
        
        # Generate recommendations
        report['recommendations'] = generate_recommendations(report)
        
        return report

def generate_integration_assessment(report: dict) -> dict:
    """Generate integration assessment for AAI ecosystem"""
    assessment = {
        'overall_suitability': 'unknown',
        'integration_complexity': 'medium',
        'value_score': 0.0,
        'risk_factors': [],
        'opportunities': []
    }
    
    # Calculate value score based on various factors
    value_factors = []
    
    # Technology alignment
    tech_langs = report['technology_analysis']['languages']
    if 'python' in tech_langs:
        value_factors.append(0.3)  # High value for Python
        assessment['opportunities'].append("Python codebase aligns with AAI technology stack")
    
    if 'javascript' in tech_langs or 'typescript' in tech_langs:
        value_factors.append(0.2)  # Medium value for JS/TS
        assessment['opportunities'].append("JavaScript/TypeScript components could enhance web interfaces")
    
    # Quality indicators
    quality_data = report['agent_analysis'].get('quality', {}).get('summary', {})
    if quality_data.get('overall_score', 0) > 0.7:
        value_factors.append(0.2)
        assessment['opportunities'].append("High code quality indicates reliable integration potential")
    elif quality_data.get('overall_score', 0) < 0.4:
        assessment['risk_factors'].append("Low code quality may require significant refactoring")
    
    # Security assessment
    security_data = report['agent_analysis'].get('security', {}).get('summary', {})
    security_score = security_data.get('security_score', 0)
    if security_score > 0.8:
        value_factors.append(0.15)
        assessment['opportunities'].append("High security score reduces integration risks")
    elif security_score < 0.6:
        assessment['risk_factors'].append("Security vulnerabilities need addressing before integration")
    
    # Documentation and testing
    if quality_data.get('documentation_score', 0) > 0.6:
        value_factors.append(0.1)
        assessment['opportunities'].append("Good documentation will ease integration process")
    
    if quality_data.get('test_coverage', 0) > 0.5:
        value_factors.append(0.1)
        assessment['opportunities'].append("Good test coverage indicates code reliability")
    
    # Structure and patterns
    structure_data = report['agent_analysis'].get('structure', {}).get('summary', {})
    if structure_data.get('file_structure_score', 0) > 0.7:
        value_factors.append(0.1)
        assessment['opportunities'].append("Well-organized code structure facilitates integration")
    
    # Calculate overall value score
    assessment['value_score'] = sum(value_factors)
    
    # Determine overall suitability
    if assessment['value_score'] > 0.8:
        assessment['overall_suitability'] = 'excellent'
        assessment['integration_complexity'] = 'low'
    elif assessment['value_score'] > 0.6:
        assessment['overall_suitability'] = 'good'
        assessment['integration_complexity'] = 'medium'
    elif assessment['value_score'] > 0.4:
        assessment['overall_suitability'] = 'moderate'
        assessment['integration_complexity'] = 'medium'
    else:
        assessment['overall_suitability'] = 'low'
        assessment['integration_complexity'] = 'high'
    
    return assessment

def generate_recommendations(report: dict) -> list:
    """Generate actionable recommendations"""
    recommendations = []
    
    assessment = report['integration_assessment']
    
    if assessment['overall_suitability'] in ['excellent', 'good']:
        recommendations.append({
            'priority': 'high',
            'category': 'integration',
            'action': 'Proceed with feature extraction and integration planning',
            'rationale': f"High value score ({assessment['value_score']:.2f}) indicates strong integration potential"
        })
    
    # Security recommendations
    security_data = report['agent_analysis'].get('security', {}).get('summary', {})
    if security_data.get('vulnerabilities_count', 0) > 0:
        recommendations.append({
            'priority': 'high',
            'category': 'security',
            'action': 'Address security vulnerabilities before integration',
            'rationale': f"Found {security_data['vulnerabilities_count']} security issues"
        })
    
    if security_data.get('secret_leaks_count', 0) > 0:
        recommendations.append({
            'priority': 'critical',
            'category': 'security',
            'action': 'Remove hardcoded secrets and credentials',
            'rationale': f"Found {security_data['secret_leaks_count']} potential secret leaks"
        })
    
    # Quality recommendations
    quality_data = report['agent_analysis'].get('quality', {}).get('summary', {})
    if quality_data.get('technical_debt_items', 0) > 10:
        recommendations.append({
            'priority': 'medium',
            'category': 'quality',
            'action': 'Address technical debt before integration',
            'rationale': f"High technical debt ({quality_data['technical_debt_items']} items) may complicate integration"
        })
    
    # Performance recommendations
    performance_data = report['agent_analysis'].get('performance', {}).get('summary', {})
    if performance_data.get('bottlenecks_count', 0) > 5:
        recommendations.append({
            'priority': 'medium',
            'category': 'performance',
            'action': 'Optimize performance bottlenecks before integration',
            'rationale': f"Found {performance_data['bottlenecks_count']} potential bottlenecks"
        })
    
    # Technology-specific recommendations
    tech_langs = report['technology_analysis']['languages']
    if 'python' in tech_langs:
        recommendations.append({
            'priority': 'medium',
            'category': 'integration',
            'action': 'Extract Python modules for AAI brain system integration',
            'rationale': 'Python components can be directly integrated into AAI architecture'
        })
    
    if 'javascript' in tech_langs or 'typescript' in tech_langs:
        recommendations.append({
            'priority': 'low',
            'category': 'integration',
            'action': 'Consider extracting JavaScript components for web interface enhancements',
            'rationale': 'JavaScript/TypeScript components could enhance AAI web interfaces'
        })
    
    return recommendations

async def main():
    """Main execution function"""
    repo_url = "https://github.com/penwyp/ClaudePreference.git"
    
    logger.info("Starting GitHub Repository Analysis Test")
    logger.info("=" * 60)
    
    try:
        # Run comprehensive analysis
        report = await run_comprehensive_analysis(repo_url)
        
        if report is None:
            logger.error("Analysis failed")
            return
        
        # Save report
        output_file = Path(__file__).parent / "analysis_report.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Print summary
        logger.info("\nANALYSIS COMPLETE")
        logger.info("=" * 60)
        
        metadata = report['metadata']
        logger.info(f"Repository: {metadata['repo_name']}")
        logger.info(f"Analysis duration: {metadata['analysis_duration']:.2f} seconds")
        
        structure = report['structure_analysis']
        logger.info(f"Files analyzed: {structure['total_files']}")
        logger.info(f"Repository size: {structure['size_mb']:.1f} MB")
        logger.info(f"Primary file types: {list(structure['file_types'].keys())[:5]}")
        
        tech = report['technology_analysis']
        logger.info(f"Languages detected: {tech['languages']}")
        logger.info(f"Frameworks detected: {tech['frameworks']}")
        
        # Agent results summary
        logger.info("\nAgent Analysis Results:")
        for agent_name, result in report['agent_analysis'].items():
            status = "SUCCESS" if result['success'] else "FAILED"
            logger.info(f"  {agent_name.upper()}: {status} ({result['execution_time']:.2f}s)")
            if result['errors']:
                logger.info(f"    Errors: {result['errors']}")
        
        # Integration assessment
        assessment = report['integration_assessment']
        logger.info(f"\nIntegration Assessment:")
        logger.info(f"  Overall suitability: {assessment['overall_suitability'].upper()}")
        logger.info(f"  Value score: {assessment['value_score']:.2f}")
        logger.info(f"  Integration complexity: {assessment['integration_complexity']}")
        
        # Top recommendations
        recommendations = report['recommendations']
        high_priority = [r for r in recommendations if r['priority'] == 'high']
        if high_priority:
            logger.info(f"\nHigh Priority Recommendations:")
            for rec in high_priority:
                logger.info(f"  - {rec['action']}")
        
        logger.info(f"\nFull report saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Analysis failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())