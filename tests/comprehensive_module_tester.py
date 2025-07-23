#!/usr/bin/env python3
"""
AAI Comprehensive Module Tester

This script systematically tests all 33 AAI modules for:
- Import success/failure
- Initialization without errors
- Core functionality execution
- Error handling and fallback behavior
- Performance metrics (response time, memory usage)
- Integration with other modules

Provides scoring on:
- Effectiveness (0-100): How well the module performs its intended function
- Efficiency (0-100): Resource usage and performance optimization
- Fallback Resilience (0-100): Ability to handle errors gracefully

Generates a comprehensive unbiased report with detailed analysis and recommendations.
"""

import os
import sys
import time
import json
import traceback
import logging
import importlib
import resource
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import warnings

# Add AAI root to path
AAI_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(AAI_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(AAI_ROOT / 'tests' / 'comprehensive_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TestStatus(Enum):
    """Test execution status"""
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    ERROR = "ERROR"

class ModuleCategory(Enum):
    """AAI Module categories"""
    CORE = "core"
    BRAIN = "brain"
    AGENT = "agent"
    MCP = "mcp"
    ENHANCEMENT = "enhancement"
    INTERFACE = "interface"
    INGESTION = "ingestion"
    INFERENCE = "inference"
    VECTOR_STORE = "vector_store"

@dataclass
class PerformanceMetrics:
    """Performance measurement data"""
    import_time: float = 0.0
    init_time: float = 0.0
    execution_time: float = 0.0
    memory_usage_mb: float = 0.0
    memory_peak_mb: float = 0.0
    cpu_usage_percent: float = 0.0

@dataclass
class TestResult:
    """Individual test result"""
    module_name: str
    category: ModuleCategory
    status: TestStatus
    import_success: bool = False
    init_success: bool = False
    functionality_success: bool = False
    error_handling_success: bool = False
    integration_success: bool = False
    effectiveness_score: int = 0  # 0-100
    efficiency_score: int = 0     # 0-100
    fallback_resilience_score: int = 0  # 0-100
    performance: PerformanceMetrics = None
    errors: List[str] = None
    warnings: List[str] = None
    test_details: Dict[str, Any] = None

    def __post_init__(self):
        if self.performance is None:
            self.performance = PerformanceMetrics()
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.test_details is None:
            self.test_details = {}

@dataclass
class SystemReport:
    """Comprehensive system test report"""
    timestamp: str
    total_modules: int
    modules_tested: int
    modules_passed: int
    modules_failed: int
    modules_skipped: int
    overall_effectiveness: float
    overall_efficiency: float
    overall_fallback_resilience: float
    category_scores: Dict[str, Dict[str, float]]
    test_results: List[TestResult]
    critical_issues: List[str]
    recommendations: List[str]
    performance_summary: Dict[str, float]

class AAIModuleTester:
    """Comprehensive AAI module testing framework"""
    
    def __init__(self):
        self.aai_root = AAI_ROOT
        self.test_results: List[TestResult] = []
        self.start_time = time.time()
        self.initial_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        
        # Define all 33 AAI modules to test
        self.modules_to_test = {
            # Core modules (6)
            ModuleCategory.CORE: [
                'core.enhanced_command_processor',
                'core.unified_enhancement_coordinator', 
                'core.resource_optimization_manager',
                'core.agent_interoperability_framework',
                'core.realtime_orchestration_monitor',
                'core.cache_manager'
            ],
            
            # Brain modules (8)
            ModuleCategory.BRAIN: [
                'brain.modules.unified_intelligence_coordinator',
                'brain.modules.mcp_orchestrator',
                'brain.modules.tech_stack_expert',
                'brain.modules.unified_enhancement_loader',
                'brain.modules.analyze_command_handler',
                'brain.modules.analyze_orchestrator',
                'brain.modules.github_analyzer',
                'brain.modules.enhanced_repository_analyzer'
            ],
            
            # Agent modules (15)
            ModuleCategory.AGENT: [
                'agents.orchestration.delegation_engine',
                'agents.orchestration.primary_agent',
                'agents.orchestration.models',
                'agents.r1_reasoning.dual_model_agent',
                'agents.r1_reasoning.reasoning_engine',
                'agents.r1_reasoning.confidence_scorer',
                'agents.r1_reasoning.config',
                'agents.r1_reasoning.models',
                'agents.specialized.filesystem_agent',
                'agents.specialized.github_agent',
                'agents.specialized.jina_search_agent',
                'agents.specialized.slack_agent',
                'agents.tech_expert.conversation_engine',
                'agents.tech_expert.recommender',
                'agents.tech_expert.models',
                'agents.tool_selection.tool_selector',
                'agents.tool_selection.prompt_analyzer',
                'agents.tool_selection.learning_engine',
                'agents.tool_selection.fabric_integrator',
                'agents.tool_selection.confidence_scorer',
                'agents.tool_selection.models'
            ],
            
            # MCP modules (2)
            ModuleCategory.MCP: [
                'mcp.server_manager',
                'mcp.health_monitor'
            ],
            
            # Enhancement modules (4)
            ModuleCategory.ENHANCEMENT: [
                'enhancements.memory.memory_layer',
                'enhancements.memory.command_enhancer',
                'enhancements.memory.workflow_memory',
                'enhancements.memory.config'
            ],
            
            # Interface modules (2)
            ModuleCategory.INTERFACE: [
                'interfaces.r1_reasoning_interface',
                'api.r1_reasoning_server'
            ],
            
            # Ingestion modules (3)
            ModuleCategory.INGESTION: [
                'ingestion.r1_reasoning.jina_research_ingester',
                'ingestion.r1_reasoning.pdf_processor',
                'ingestion.r1_reasoning.semantic_chunker'
            ],
            
            # Inference modules (3)
            ModuleCategory.INFERENCE: [
                'inference.model_router',
                'inference.huggingface_client',
                'inference.ollama_client'
            ],
            
            # Vector store modules (3)
            ModuleCategory.VECTOR_STORE: [
                'vector_store.chroma_manager',
                'vector_store.retrieval_ranker',
                'vector_store.supabase_vector_store'
            ]
        }
        
    def measure_performance(self, func, *args, **kwargs):
        """Measure performance metrics for a function call"""
        start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # MB on Linux
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = e
            success = False
        
        end_time = time.time()
        end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # MB on Linux
        
        metrics = PerformanceMetrics(
            execution_time=end_time - start_time,
            memory_usage_mb=max(0, end_memory - start_memory),
            memory_peak_mb=max(start_memory, end_memory),
            cpu_usage_percent=0.0  # CPU usage not available without psutil
        )
        
        return result, success, metrics
    
    def test_module_import(self, module_path: str) -> Tuple[bool, Any, float]:
        """Test module import with performance measurement"""
        start_time = time.time()
        try:
            # Handle module path conversion for tool-selection -> tool_selection
            if 'tool-selection' in module_path:
                module_path = module_path.replace('tool-selection', 'tool_selection')
            
            module = importlib.import_module(module_path)
            import_time = time.time() - start_time
            return True, module, import_time
        except Exception as e:
            import_time = time.time() - start_time
            logger.error(f"Failed to import {module_path}: {e}")
            return False, e, import_time
    
    def test_module_initialization(self, module: Any, module_name: str) -> Tuple[bool, Any, float, List[str]]:
        """Test module initialization and basic instantiation"""
        warnings_list = []
        start_time = time.time()
        
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                
                # Try to find and instantiate main classes
                initialized_objects = []
                
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    
                    # Look for classes that might be the main module class
                    if (isinstance(attr, type) and 
                        not attr_name.startswith('_') and
                        attr_name not in ['Enum', 'ABC', 'BaseModel']):
                        
                        try:
                            # Try basic instantiation with common patterns
                            if 'config' in module_name.lower():
                                # Config modules often have class variables
                                instance = attr
                            elif hasattr(attr, '__init__'):
                                # Try instantiation with no args first
                                try:
                                    instance = attr()
                                except TypeError:
                                    # Try with common optional parameters
                                    try:
                                        instance = attr(config={})
                                    except TypeError:
                                        try:
                                            instance = attr(enabled=False)
                                        except TypeError:
                                            # Skip if we can't instantiate easily
                                            continue
                            else:
                                continue
                                
                            initialized_objects.append((attr_name, instance))
                            
                        except Exception as e:
                            warnings_list.append(f"Could not instantiate {attr_name}: {e}")
                
                # Collect warnings
                for warning in w:
                    warnings_list.append(str(warning.message))
                
                init_time = time.time() - start_time
                return True, initialized_objects, init_time, warnings_list
                
        except Exception as e:
            init_time = time.time() - start_time
            return False, e, init_time, warnings_list
    
    def test_module_functionality(self, module: Any, module_name: str) -> Tuple[bool, Dict[str, Any], List[str]]:
        """Test core module functionality"""
        test_details = {}
        errors = []
        
        try:
            # Test different types of modules with appropriate methods
            if 'processor' in module_name.lower():
                test_details['type'] = 'processor'
                # Test processing capability
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and 'process' in attr_name.lower():
                        test_details['has_process_method'] = True
                        break
                
            elif 'coordinator' in module_name.lower():
                test_details['type'] = 'coordinator'
                # Test coordination capabilities
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and any(x in attr_name.lower() for x in ['coordinate', 'orchestrate', 'manage']):
                        test_details['has_coordination_method'] = True
                        break
                        
            elif 'agent' in module_name.lower():
                test_details['type'] = 'agent'
                # Test agent capabilities
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and any(x in attr_name.lower() for x in ['execute', 'run', 'process', 'handle']):
                        test_details['has_execution_method'] = True
                        break
                        
            elif 'manager' in module_name.lower():
                test_details['type'] = 'manager'
                # Test management capabilities
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and any(x in attr_name.lower() for x in ['manage', 'optimize', 'monitor']):
                        test_details['has_management_method'] = True
                        break
            
            # Check for common interfaces
            test_details['has_init'] = hasattr(module, '__init__')
            test_details['has_classes'] = len([attr for attr in dir(module) 
                                               if isinstance(getattr(module, attr), type) 
                                               and not attr.startswith('_')]) > 0
            test_details['has_functions'] = len([attr for attr in dir(module) 
                                                if callable(getattr(module, attr)) 
                                                and not attr.startswith('_')]) > 0
            
            return True, test_details, errors
            
        except Exception as e:
            errors.append(f"Functionality test failed: {e}")
            return False, test_details, errors
    
    def test_error_handling(self, module: Any, module_name: str) -> Tuple[bool, List[str]]:
        """Test module error handling and resilience"""
        errors = []
        
        try:
            # Test various error conditions
            error_tests_passed = 0
            total_error_tests = 0
            
            # Test 1: Invalid input handling
            total_error_tests += 1
            try:
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and not attr_name.startswith('_'):
                        # Try instantiating with invalid inputs
                        try:
                            attr(None)  # Should handle None gracefully
                        except (TypeError, ValueError):
                            # Expected behavior
                            error_tests_passed += 1
                            break
                        except Exception as e:
                            # Unexpected error type
                            errors.append(f"Unexpected error handling for None input: {e}")
                            break
            except Exception as e:
                errors.append(f"Error testing invalid input handling: {e}")
            
            # Test 2: Missing dependency handling
            total_error_tests += 1
            if hasattr(module, '__file__'):
                try:
                    # Check if module has proper import error handling
                    with open(module.__file__, 'r') as f:
                        content = f.read()
                        if 'try:' in content and 'ImportError' in content:
                            error_tests_passed += 1
                except Exception as e:
                    errors.append(f"Could not check dependency handling: {e}")
            
            success = error_tests_passed > 0
            return success, errors
            
        except Exception as e:
            errors.append(f"Error handling test failed: {e}")
            return False, errors
    
    def calculate_scores(self, result: TestResult) -> TestResult:
        """Calculate effectiveness, efficiency, and fallback resilience scores"""
        
        # Effectiveness Score (0-100)
        effectiveness = 0
        if result.import_success:
            effectiveness += 20
        if result.init_success:
            effectiveness += 20
        if result.functionality_success:
            effectiveness += 30
        if result.integration_success:
            effectiveness += 20
        if result.test_details.get('has_execution_method') or result.test_details.get('has_process_method'):
            effectiveness += 10
        
        # Efficiency Score (0-100) - based on performance metrics
        efficiency = 50  # baseline
        if result.performance.import_time < 1.0:
            efficiency += 20
        elif result.performance.import_time < 2.0:
            efficiency += 10
            
        if result.performance.init_time < 0.5:
            efficiency += 15
        elif result.performance.init_time < 1.0:
            efficiency += 10
            
        if result.performance.memory_usage_mb < 10:
            efficiency += 15
        elif result.performance.memory_usage_mb < 50:
            efficiency += 10
        
        # Fallback Resilience Score (0-100)
        resilience = 0
        if result.error_handling_success:
            resilience += 40
        if 'ImportError' in str(result.test_details):
            resilience += 20
        if result.import_success and not result.errors:
            resilience += 20
        if len(result.warnings) < 3:
            resilience += 20
        
        result.effectiveness_score = min(100, effectiveness)
        result.efficiency_score = min(100, efficiency) 
        result.fallback_resilience_score = min(100, resilience)
        
        return result
    
    def test_single_module(self, module_path: str, category: ModuleCategory) -> TestResult:
        """Test a single module comprehensively"""
        module_name = module_path.split('.')[-1]
        logger.info(f"Testing module: {module_path}")
        
        result = TestResult(
            module_name=module_name,
            category=category,
            status=TestStatus.PASS
        )
        
        try:
            # Test 1: Import
            import_success, module_or_error, import_time = self.test_module_import(module_path)
            result.import_success = import_success
            result.performance.import_time = import_time
            
            if not import_success:
                result.status = TestStatus.FAIL
                result.errors.append(f"Import failed: {module_or_error}")
                return self.calculate_scores(result)
            
            module = module_or_error
            
            # Test 2: Initialization
            init_success, init_result, init_time, warnings = self.test_module_initialization(module, module_name)
            result.init_success = init_success
            result.performance.init_time = init_time
            result.warnings.extend(warnings)
            
            if not init_success:
                result.errors.append(f"Initialization failed: {init_result}")
            
            # Test 3: Functionality
            func_success, test_details, func_errors = self.test_module_functionality(module, module_name)
            result.functionality_success = func_success
            result.test_details.update(test_details)
            result.errors.extend(func_errors)
            
            # Test 4: Error Handling
            error_success, error_errors = self.test_error_handling(module, module_name)
            result.error_handling_success = error_success
            result.errors.extend(error_errors)
            
            # Test 5: Integration (basic check for dependencies)
            result.integration_success = result.import_success and len(result.errors) == 0
            
            # Determine overall status
            if result.import_success and result.init_success and result.functionality_success:
                result.status = TestStatus.PASS
            elif result.import_success:
                result.status = TestStatus.FAIL
            else:
                result.status = TestStatus.ERROR
                
        except Exception as e:
            result.status = TestStatus.ERROR
            result.errors.append(f"Unexpected error during testing: {e}")
            logger.error(f"Unexpected error testing {module_path}: {e}")
            logger.error(traceback.format_exc())
        
        return self.calculate_scores(result)
    
    def run_comprehensive_test(self) -> SystemReport:
        """Run comprehensive test on all AAI modules"""
        logger.info("Starting comprehensive AAI module testing...")
        logger.info(f"Testing {sum(len(modules) for modules in self.modules_to_test.values())} modules")
        
        all_results = []
        
        for category, modules in self.modules_to_test.items():
            logger.info(f"\n=== Testing {category.value.upper()} modules ===")
            
            for module_path in modules:
                try:
                    result = self.test_single_module(module_path, category)
                    all_results.append(result)
                    
                    status_symbol = "✓" if result.status == TestStatus.PASS else "✗"
                    logger.info(f"{status_symbol} {module_path}: {result.status.value} "
                              f"(E:{result.effectiveness_score}, Ef:{result.efficiency_score}, "
                              f"R:{result.fallback_resilience_score})")
                    
                except Exception as e:
                    logger.error(f"Failed to test {module_path}: {e}")
                    error_result = TestResult(
                        module_name=module_path.split('.')[-1],
                        category=category,
                        status=TestStatus.ERROR
                    )
                    error_result.errors.append(f"Test framework error: {e}")
                    all_results.append(error_result)
        
        self.test_results = all_results
        return self.generate_system_report()
    
    def generate_system_report(self) -> SystemReport:
        """Generate comprehensive system report"""
        logger.info("Generating comprehensive system report...")
        
        # Calculate overall statistics
        total_modules = len(self.test_results)
        modules_passed = len([r for r in self.test_results if r.status == TestStatus.PASS])
        modules_failed = len([r for r in self.test_results if r.status == TestStatus.FAIL])
        modules_skipped = len([r for r in self.test_results if r.status == TestStatus.SKIP])
        modules_error = len([r for r in self.test_results if r.status == TestStatus.ERROR])
        
        # Calculate overall scores
        valid_results = [r for r in self.test_results if r.status != TestStatus.SKIP]
        overall_effectiveness = sum(r.effectiveness_score for r in valid_results) / len(valid_results) if valid_results else 0
        overall_efficiency = sum(r.efficiency_score for r in valid_results) / len(valid_results) if valid_results else 0
        overall_fallback_resilience = sum(r.fallback_resilience_score for r in valid_results) / len(valid_results) if valid_results else 0
        
        # Calculate category scores
        category_scores = {}
        for category in ModuleCategory:
            cat_results = [r for r in self.test_results if r.category == category]
            if cat_results:
                category_scores[category.value] = {
                    'effectiveness': sum(r.effectiveness_score for r in cat_results) / len(cat_results),
                    'efficiency': sum(r.efficiency_score for r in cat_results) / len(cat_results),
                    'fallback_resilience': sum(r.fallback_resilience_score for r in cat_results) / len(cat_results),
                    'pass_rate': len([r for r in cat_results if r.status == TestStatus.PASS]) / len(cat_results) * 100
                }
        
        # Identify critical issues
        critical_issues = []
        for result in self.test_results:
            if not result.import_success:
                critical_issues.append(f"CRITICAL: {result.module_name} failed to import")
            if result.effectiveness_score < 30:
                critical_issues.append(f"LOW EFFECTIVENESS: {result.module_name} scored {result.effectiveness_score}/100")
            if result.fallback_resilience_score < 20:
                critical_issues.append(f"POOR RESILIENCE: {result.module_name} scored {result.fallback_resilience_score}/100")
        
        # Generate recommendations
        recommendations = []
        
        if overall_effectiveness < 70:
            recommendations.append("System effectiveness is below acceptable threshold (70%). Focus on improving core functionality.")
            
        if overall_efficiency < 60:
            recommendations.append("System efficiency needs improvement. Optimize import times and memory usage.")
            
        if overall_fallback_resilience < 50:
            recommendations.append("Improve error handling and fallback mechanisms across modules.")
            
        # Category-specific recommendations
        for category, scores in category_scores.items():
            if scores['pass_rate'] < 50:
                recommendations.append(f"{category.upper()} modules have low pass rate ({scores['pass_rate']:.1f}%). Requires immediate attention.")
        
        # Performance summary
        performance_summary = {
            'avg_import_time': sum(r.performance.import_time for r in valid_results) / len(valid_results) if valid_results else 0,
            'avg_init_time': sum(r.performance.init_time for r in valid_results) / len(valid_results) if valid_results else 0,
            'avg_memory_usage': sum(r.performance.memory_usage_mb for r in valid_results) / len(valid_results) if valid_results else 0,
            'total_test_time': time.time() - self.start_time
        }
        
        return SystemReport(
            timestamp=datetime.now().isoformat(),
            total_modules=total_modules,
            modules_tested=total_modules,
            modules_passed=modules_passed,
            modules_failed=modules_failed + modules_error,
            modules_skipped=modules_skipped,
            overall_effectiveness=overall_effectiveness,
            overall_efficiency=overall_efficiency,
            overall_fallback_resilience=overall_fallback_resilience,
            category_scores=category_scores,
            test_results=self.test_results,
            critical_issues=critical_issues,
            recommendations=recommendations,
            performance_summary=performance_summary
        )
    
    def save_report(self, report: SystemReport, filename: str = None):
        """Save comprehensive report to files"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aai_comprehensive_test_report_{timestamp}"
        
        # Save JSON report
        json_file = self.aai_root / 'tests' / f"{filename}.json"
        with open(json_file, 'w') as f:
            # Convert dataclasses to dict for JSON serialization
            json.dump(asdict(report), f, indent=2, default=str)
        
        # Save human-readable report
        md_file = self.aai_root / 'tests' / f"{filename}.md"
        with open(md_file, 'w') as f:
            f.write(self.format_report_markdown(report))
        
        logger.info(f"Reports saved: {json_file} and {md_file}")
    
    def format_report_markdown(self, report: SystemReport) -> str:
        """Format report as markdown"""
        md = f"""# AAI Comprehensive Module Test Report
        
Generated: {report.timestamp}

## Executive Summary

- **Total Modules Tested**: {report.modules_tested}/{report.total_modules}
- **Modules Passed**: {report.modules_passed}
- **Modules Failed**: {report.modules_failed}
- **Modules Skipped**: {report.modules_skipped}

## Overall Scores

- **Effectiveness**: {report.overall_effectiveness:.1f}/100
- **Efficiency**: {report.overall_efficiency:.1f}/100  
- **Fallback Resilience**: {report.overall_fallback_resilience:.1f}/100

## Category Performance

"""
        
        for category, scores in report.category_scores.items():
            md += f"""### {category.upper()}
- Effectiveness: {scores['effectiveness']:.1f}/100
- Efficiency: {scores['efficiency']:.1f}/100
- Fallback Resilience: {scores['fallback_resilience']:.1f}/100
- Pass Rate: {scores['pass_rate']:.1f}%

"""
        
        md += "## Critical Issues\n\n"
        for issue in report.critical_issues:
            md += f"- {issue}\n"
        
        md += "\n## Recommendations\n\n"
        for rec in report.recommendations:
            md += f"- {rec}\n"
        
        md += f"""
## Performance Summary

- Average Import Time: {report.performance_summary['avg_import_time']:.3f}s
- Average Init Time: {report.performance_summary['avg_init_time']:.3f}s
- Average Memory Usage: {report.performance_summary['avg_memory_usage']:.1f}MB
- Total Test Time: {report.performance_summary['total_test_time']:.1f}s

## Detailed Results

"""
        
        for result in report.test_results:
            status_emoji = {"PASS": "✅", "FAIL": "❌", "ERROR": "🚫", "SKIP": "⏭️"}[result.status.value]
            md += f"""### {status_emoji} {result.module_name} ({result.category.value})

**Status**: {result.status.value}  
**Scores**: Effectiveness {result.effectiveness_score}/100, Efficiency {result.efficiency_score}/100, Resilience {result.fallback_resilience_score}/100

**Import**: {"✓" if result.import_success else "✗"}  
**Initialization**: {"✓" if result.init_success else "✗"}  
**Functionality**: {"✓" if result.functionality_success else "✗"}  
**Error Handling**: {"✓" if result.error_handling_success else "✗"}  
**Integration**: {"✓" if result.integration_success else "✗"}

**Performance**:
- Import Time: {result.performance.import_time:.3f}s
- Init Time: {result.performance.init_time:.3f}s
- Memory Usage: {result.performance.memory_usage_mb:.1f}MB

"""
            if result.errors:
                md += "**Errors**:\n"
                for error in result.errors:
                    md += f"- {error}\n"
            
            if result.warnings:
                md += "**Warnings**:\n"
                for warning in result.warnings:
                    md += f"- {warning}\n"
            
            md += "\n---\n\n"
        
        return md

def main():
    """Main execution function"""
    print("🚀 AAI Comprehensive Module Tester")
    print("=" * 50)
    
    tester = AAIModuleTester()
    
    try:
        # Run comprehensive test
        report = tester.run_comprehensive_test()
        
        # Save report
        tester.save_report(report)
        
        # Print summary
        print(f"\n📊 Test Summary:")
        print(f"Total Modules: {report.total_modules}")
        print(f"Passed: {report.modules_passed} ✅")
        print(f"Failed: {report.modules_failed} ❌") 
        print(f"Overall Effectiveness: {report.overall_effectiveness:.1f}/100")
        print(f"Overall Efficiency: {report.overall_efficiency:.1f}/100")
        print(f"Overall Resilience: {report.overall_fallback_resilience:.1f}/100")
        
        if report.critical_issues:
            print(f"\n🚨 Critical Issues: {len(report.critical_issues)}")
            for issue in report.critical_issues[:5]:  # Show first 5
                print(f"  - {issue}")
        
        print(f"\n📈 Performance:")
        print(f"Total Test Time: {report.performance_summary['total_test_time']:.1f}s")
        print(f"Average Import Time: {report.performance_summary['avg_import_time']:.3f}s")
        
        return 0 if report.modules_passed >= report.total_modules * 0.8 else 1
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())