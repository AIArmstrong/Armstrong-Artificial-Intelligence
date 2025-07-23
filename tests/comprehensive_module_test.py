#!/usr/bin/env python3
"""
Comprehensive Testing Framework for all 33 AAI Modules
Tests for efficiency, effectiveness, and identifies ALL issues
"""

import sys
import os
import asyncio
import importlib
import importlib.util
import traceback
import time
import gc
import re
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import inspect
import warnings
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/mnt/c/Users/Brandon/AAI/tests/test_results.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.insert(0, '/mnt/c/Users/Brandon/AAI')

@dataclass
class TestResult:
    module_path: str
    module_name: str
    prp_category: str
    import_success: bool = False
    import_time: float = 0.0
    import_error: Optional[str] = None
    functional_tests: Dict[str, bool] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    memory_usage: Dict[str, float] = field(default_factory=dict)
    issues: List[Dict[str, Any]] = field(default_factory=list)
    fallback_triggers: List[Dict[str, Any]] = field(default_factory=list)
    async_issues: List[str] = field(default_factory=list)
    resource_leaks: List[str] = field(default_factory=list)
    integration_issues: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    missing_dependencies: List[str] = field(default_factory=list)
    circular_imports: List[str] = field(default_factory=list)
    
    @property
    def overall_status(self) -> str:
        if not self.import_success:
            return "FAIL"
        if any(severity == "Critical" for issue in self.issues for severity in [issue.get("severity")]):
            return "FAIL"
        if any(severity == "High" for issue in self.issues for severity in [issue.get("severity")]):
            return "WARN"
        return "PASS"

class ComprehensiveModuleTester:
    def __init__(self):
        self.results: Dict[str, TestResult] = {}
        self.modules = self._get_all_modules()
        
    def _get_all_modules(self) -> List[Tuple[str, str, str]]:
        """Get all modules organized by PRP category - ACTUAL EXISTING MODULES"""
        return [
            # Existing brain modules
            ("BRAIN", "mcp-orchestrator", "/mnt/c/Users/Brandon/AAI/brain/modules/mcp-orchestrator.py"),
            ("BRAIN", "tech-stack-expert", "/mnt/c/Users/Brandon/AAI/brain/modules/tech-stack-expert.py"),
            ("BRAIN", "unified_enhancement_loader", "/mnt/c/Users/Brandon/AAI/brain/modules/unified_enhancement_loader.py"),
            ("BRAIN", "unified_intelligence_coordinator", "/mnt/c/Users/Brandon/AAI/brain/modules/unified_intelligence_coordinator.py"),
            ("BRAIN", "analyze_command_handler", "/mnt/c/Users/Brandon/AAI/brain/modules/analyze_command_handler.py"),
            ("BRAIN", "analyze_orchestrator", "/mnt/c/Users/Brandon/AAI/brain/modules/analyze_orchestrator.py"),
            ("BRAIN", "anthropic-docs-integration", "/mnt/c/Users/Brandon/AAI/brain/modules/anthropic-docs-integration.py"),
            ("BRAIN", "dashboard-visualizer", "/mnt/c/Users/Brandon/AAI/brain/modules/dashboard-visualizer.py"),
            ("BRAIN", "enhanced-repository-analyzer", "/mnt/c/Users/Brandon/AAI/brain/modules/enhanced-repository-analyzer.py"),
            ("BRAIN", "github-analyzer", "/mnt/c/Users/Brandon/AAI/brain/modules/github-analyzer.py"),
            ("BRAIN", "smart-tool-selector", "/mnt/c/Users/Brandon/AAI/brain/modules/smart-tool-selector.py"),
            
            # Core modules
            ("CORE", "enhanced_command_processor", "/mnt/c/Users/Brandon/AAI/core/enhanced_command_processor.py"),
            ("CORE", "unified_enhancement_coordinator", "/mnt/c/Users/Brandon/AAI/core/unified_enhancement_coordinator.py"),
            ("CORE", "resource_optimization_manager", "/mnt/c/Users/Brandon/AAI/core/resource_optimization_manager.py"),
            ("CORE", "agent_interoperability_framework", "/mnt/c/Users/Brandon/AAI/core/agent_interoperability_framework.py"),
            ("CORE", "realtime_orchestration_monitor", "/mnt/c/Users/Brandon/AAI/core/realtime_orchestration_monitor.py"),
            
            # MCP modules
            ("MCP", "server_manager", "/mnt/c/Users/Brandon/AAI/mcp/server_manager.py"),
            ("MCP", "health_monitor", "/mnt/c/Users/Brandon/AAI/mcp/health_monitor.py"),
            
            # Agent modules - Orchestration
            ("AGENTS_ORCH", "delegation_engine", "/mnt/c/Users/Brandon/AAI/agents/orchestration/delegation_engine.py"),
            ("AGENTS_ORCH", "primary_agent", "/mnt/c/Users/Brandon/AAI/agents/orchestration/primary_agent.py"),
            
            # Agent modules - Specialized
            ("AGENTS_SPEC", "slack_agent", "/mnt/c/Users/Brandon/AAI/agents/specialized/slack_agent.py"),
            ("AGENTS_SPEC", "github_agent", "/mnt/c/Users/Brandon/AAI/agents/specialized/github_agent.py"),
            ("AGENTS_SPEC", "filesystem_agent", "/mnt/c/Users/Brandon/AAI/agents/specialized/filesystem_agent.py"),
            ("AGENTS_SPEC", "jina_search_agent", "/mnt/c/Users/Brandon/AAI/agents/specialized/jina_search_agent.py"),
            
            # Agent modules - Tech Expert
            ("AGENTS_TECH", "conversation_engine", "/mnt/c/Users/Brandon/AAI/agents/tech_expert/conversation_engine.py"),
            ("AGENTS_TECH", "recommender", "/mnt/c/Users/Brandon/AAI/agents/tech_expert/recommender.py"),
            
            # Agent modules - R1 Reasoning
            ("AGENTS_R1", "dual_model_agent", "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/dual_model_agent.py"),
            ("AGENTS_R1", "reasoning_engine", "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/reasoning_engine.py"),
            ("AGENTS_R1", "confidence_scorer", "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/confidence_scorer.py"),
            
            # Agent modules - Tool Selection
            ("AGENTS_TOOL", "tool_selector", "/mnt/c/Users/Brandon/AAI/agents/tool-selection/tool_selector.py"),
            ("AGENTS_TOOL", "learning_engine", "/mnt/c/Users/Brandon/AAI/agents/tool-selection/learning_engine.py"),
            ("AGENTS_TOOL", "fabric_integrator", "/mnt/c/Users/Brandon/AAI/agents/tool-selection/fabric_integrator.py"),
            ("AGENTS_TOOL", "prompt_analyzer", "/mnt/c/Users/Brandon/AAI/agents/tool-selection/prompt_analyzer.py"),
            ("AGENTS_TOOL", "confidence_scorer", "/mnt/c/Users/Brandon/AAI/agents/tool-selection/confidence_scorer.py"),
        ]
    
    @contextmanager
    def memory_monitor(self):
        """Monitor memory usage during operation"""
        gc.collect()
        initial_objects = len(gc.get_objects())
        yield
        gc.collect()
        final_objects = len(gc.get_objects())
        object_delta = final_objects - initial_objects
        if object_delta > 1000:  # More than 1000 new objects
            logger.warning(f"Significant object increase: {object_delta} objects")
    
    def analyze_module_code(self, module_path: str) -> Dict[str, Any]:
        """Analyze module code for issues"""
        issues = {
            "hardcoded_values": [],
            "missing_error_handling": [],
            "blocking_operations": [],
            "resource_management": [],
            "async_issues": [],
            "fallback_patterns": []
        }
        
        try:
            with open(module_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for hardcoded values
            hardcoded_patterns = [
                (r'["\']http[s]?://[^"\']+["\']', "Hardcoded URL"),
                (r'["\'][0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}["\']', "Hardcoded IP"),
                (r'(api_key|password|token)\s*=\s*["\'][^"\']+["\']', "Hardcoded credentials"),
                (r'port\s*=\s*[0-9]+', "Hardcoded port"),
            ]
            
            import re
            for pattern, issue_type in hardcoded_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    issues["hardcoded_values"].append({
                        "line": line_num,
                        "type": issue_type,
                        "content": match.group()
                    })
            
            # Check for missing error handling
            try_blocks = re.finditer(r'try:', content)
            for try_block in try_blocks:
                line_num = content[:try_block.start()].count('\n') + 1
                # Check if there's a corresponding except
                try_line_indent = len(lines[line_num - 1]) - len(lines[line_num - 1].lstrip())
                found_except = False
                for i in range(line_num, min(line_num + 20, len(lines))):
                    if re.match(r'\s*except\s*:', lines[i]):
                        found_except = True
                        # Check for bare except
                        if re.match(r'\s*except\s*:\s*$', lines[i]):
                            issues["missing_error_handling"].append({
                                "line": i + 1,
                                "type": "Bare except clause",
                                "content": lines[i].strip()
                            })
                        break
                
                if not found_except:
                    issues["missing_error_handling"].append({
                        "line": line_num,
                        "type": "Try without except",
                        "content": lines[line_num - 1].strip()
                    })
            
            # Check for blocking operations in async functions
            async_funcs = re.finditer(r'async\s+def\s+\w+', content)
            for async_func in async_funcs:
                func_start = content[:async_func.start()].count('\n') + 1
                # Find function end
                func_indent = len(lines[func_start - 1]) - len(lines[func_start - 1].lstrip())
                func_end = func_start
                for i in range(func_start, len(lines)):
                    line = lines[i]
                    if line.strip() and not line.startswith(' ' * (func_indent + 1)):
                        func_end = i
                        break
                
                # Check for blocking operations
                func_content = '\n'.join(lines[func_start:func_end])
                blocking_patterns = [
                    (r'time\.sleep', "time.sleep in async function"),
                    (r'requests\.|urllib\.', "Synchronous HTTP in async function"),
                    (r'open\s*\(', "Synchronous file I/O in async function"),
                    (r'\.read\(\)|\.write\(', "Synchronous I/O operations"),
                ]
                
                for pattern, issue_type in blocking_patterns:
                    if re.search(pattern, func_content):
                        issues["blocking_operations"].append({
                            "function": async_func.group(),
                            "line": func_start,
                            "type": issue_type
                        })
            
            # Check for resource management issues
            resource_patterns = [
                (r'open\s*\([^)]+\)', "File opened without context manager"),
                (r'connect\s*\([^)]+\)', "Connection without context manager"),
                (r'Session\s*\(\)', "Session without context manager"),
            ]
            
            for pattern, issue_type in resource_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    # Check if it's in a with statement
                    line = lines[line_num - 1]
                    if not re.search(r'with\s+', line):
                        issues["resource_management"].append({
                            "line": line_num,
                            "type": issue_type,
                            "content": match.group()
                        })
            
            # Check for fallback patterns
            fallback_patterns = [
                (r'except.*:.*\n.*fallback', "Exception triggering fallback"),
                (r'if.*error.*:.*\n.*fallback', "Error condition triggering fallback"),
                (r'fallback.*=.*True', "Fallback flag set"),
                (r'use_fallback', "Fallback usage"),
            ]
            
            for pattern, issue_type in fallback_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    issues["fallback_patterns"].append({
                        "line": line_num,
                        "type": issue_type,
                        "content": match.group().replace('\n', ' ')
                    })
            
        except Exception as e:
            logger.error(f"Error analyzing {module_path}: {e}")
        
        return issues
    
    def test_module_import(self, module_path: str, module_name: str) -> Tuple[bool, float, Optional[str], List[str]]:
        """Test module import and measure time"""
        start_time = time.time()
        dependencies = []
        
        try:
            # Extract module dependencies before import
            with open(module_path, 'r') as f:
                content = f.read()
                import_lines = re.findall(r'^(?:from|import)\s+([^\s]+)', content, re.MULTILINE)
                dependencies = list(set(import_lines))
            
            # Try to import the module
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                import_time = time.time() - start_time
                return True, import_time, None, dependencies
            else:
                return False, 0, "Failed to create module spec", dependencies
                
        except Exception as e:
            import_time = time.time() - start_time
            error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            return False, import_time, error_msg, dependencies
    
    def check_circular_imports(self, module_path: str, dependencies: List[str]) -> List[str]:
        """Check for circular import patterns"""
        circular_imports = []
        module_dir = os.path.dirname(module_path)
        module_name = os.path.basename(module_path).replace('.py', '')
        
        for dep in dependencies:
            if dep.startswith('.'):
                # Relative import
                continue
            
            # Check if dependency might import this module back
            dep_parts = dep.split('.')
            if any(part in module_name for part in dep_parts):
                circular_imports.append(f"Potential circular import with {dep}")
        
        return circular_imports
    
    def test_async_patterns(self, module_path: str) -> List[str]:
        """Test for async/await pattern issues"""
        issues = []
        
        try:
            with open(module_path, 'r') as f:
                content = f.read()
            
            # Check for common async issues
            patterns = [
                (r'async\s+def.*\n(?:(?!await).)*(return|$)', "Async function without await"),
                (r'await\s+(?!.*async)', "Await outside async function"),
                (r'asyncio\.run.*async\s+def', "Nested asyncio.run calls"),
                (r'def\s+\w+.*await\s+', "Await in non-async function"),
            ]
            
            for pattern, issue in patterns:
                if re.search(pattern, content, re.MULTILINE | re.DOTALL):
                    issues.append(issue)
            
        except Exception as e:
            issues.append(f"Error checking async patterns: {e}")
        
        return issues
    
    def test_module_functionality(self, module_path: str, module_name: str) -> Dict[str, bool]:
        """Test core functionality of the module"""
        tests = {}
        
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check for required classes/functions
                if 'Enhancement' in module_name:
                    tests['has_enhancement_class'] = any(
                        name.endswith('Enhancement') 
                        for name in dir(module)
                        if inspect.isclass(getattr(module, name))
                    )
                
                if 'Agent' in module_name or 'agent' in module_name:
                    tests['has_agent_class'] = any(
                        'Agent' in name or 'agent' in name.lower()
                        for name in dir(module)
                        if inspect.isclass(getattr(module, name))
                    )
                
                if 'Coordinator' in module_name:
                    tests['has_coordinator_class'] = any(
                        'Coordinator' in name
                        for name in dir(module)
                        if inspect.isclass(getattr(module, name))
                    )
                
                # Check for async methods
                tests['has_async_methods'] = any(
                    inspect.iscoroutinefunction(getattr(module, name))
                    for name in dir(module)
                    if not name.startswith('_')
                )
                
                # Check for proper initialization
                tests['has_init_method'] = any(
                    hasattr(getattr(module, name), '__init__')
                    for name in dir(module)
                    if inspect.isclass(getattr(module, name))
                )
                
        except Exception as e:
            tests['import_error'] = False
            logger.error(f"Functionality test error for {module_name}: {e}")
        
        return tests
    
    def measure_performance(self, module_path: str, module_name: str) -> Dict[str, float]:
        """Measure performance metrics"""
        metrics = {}
        
        try:
            # Measure import time
            import_times = []
            for _ in range(3):
                start = time.time()
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                import_times.append(time.time() - start)
            
            metrics['avg_import_time'] = sum(import_times) / len(import_times)
            metrics['max_import_time'] = max(import_times)
            
            # Check module size
            metrics['file_size_kb'] = os.path.getsize(module_path) / 1024
            
            # Count lines of code
            with open(module_path, 'r') as f:
                lines = f.readlines()
                metrics['total_lines'] = len(lines)
                metrics['code_lines'] = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
            
        except Exception as e:
            logger.error(f"Performance measurement error for {module_name}: {e}")
        
        return metrics
    
    def check_resource_leaks(self, module_path: str) -> List[str]:
        """Check for potential resource leaks"""
        leaks = []
        
        try:
            with open(module_path, 'r') as f:
                content = f.read()
            
            # Check for unclosed resources
            patterns = [
                (r'open\s*\([^)]+\)(?!.*\.close\(\))', "Unclosed file handle"),
                (r'Session\s*\(\)(?!.*\.close\(\))', "Unclosed session"),
                (r'connect\s*\([^)]+\)(?!.*\.close\(\))', "Unclosed connection"),
                (r'Thread\s*\([^)]+\)(?!.*\.join\(\))', "Unjoined thread"),
                (r'Process\s*\([^)]+\)(?!.*\.join\(\))', "Unjoined process"),
            ]
            
            for pattern, leak_type in patterns:
                if re.search(pattern, content, re.MULTILINE | re.DOTALL):
                    leaks.append(leak_type)
            
        except Exception as e:
            leaks.append(f"Error checking resource leaks: {e}")
        
        return leaks
    
    def check_integration_compatibility(self, module_path: str, module_name: str) -> List[str]:
        """Check AAI Brain integration compatibility"""
        issues = []
        
        try:
            with open(module_path, 'r') as f:
                content = f.read()
            
            # Check for required AAI integration patterns
            if 'Enhancement' in module_name:
                if 'async def enhance' not in content:
                    issues.append("Missing async enhance method for AAI integration")
                if 'confidence' not in content.lower():
                    issues.append("Missing confidence scoring for Smart Module Loading")
            
            if 'Agent' in module_name:
                if 'async def process' not in content and 'async def execute' not in content:
                    issues.append("Missing async process/execute method for agent")
            
            # Check for proper error handling for AAI
            if 'try:' in content and 'except Exception' not in content:
                issues.append("Missing comprehensive error handling for AAI integration")
            
        except Exception as e:
            issues.append(f"Error checking integration: {e}")
        
        return issues
    
    def analyze_fallback_triggers(self, module_path: str) -> List[Dict[str, Any]]:
        """Analyze why fallbacks are triggered"""
        triggers = []
        
        try:
            with open(module_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Find fallback occurrences
            for i, line in enumerate(lines):
                if 'fallback' in line.lower():
                    # Look for context around fallback
                    context_start = max(0, i - 5)
                    context_end = min(len(lines), i + 5)
                    context = lines[context_start:context_end]
                    
                    # Identify trigger condition
                    trigger_reason = "Unknown"
                    for j in range(context_start, i):
                        context_line = lines[j]
                        if 'except' in context_line:
                            trigger_reason = f"Exception handling: {context_line.strip()}"
                        elif 'if' in context_line and ('error' in context_line or 'fail' in context_line):
                            trigger_reason = f"Error condition: {context_line.strip()}"
                        elif 'timeout' in context_line:
                            trigger_reason = f"Timeout condition: {context_line.strip()}"
                    
                    triggers.append({
                        "line": i + 1,
                        "code": line.strip(),
                        "reason": trigger_reason,
                        "context": '\n'.join(context)
                    })
        
        except Exception as e:
            logger.error(f"Error analyzing fallback triggers: {e}")
        
        return triggers
    
    async def run_comprehensive_tests(self):
        """Run all tests on all modules"""
        logger.info("Starting comprehensive testing of all 33 AAI modules...")
        
        for prp, module_name, module_path in self.modules:
            logger.info(f"\nTesting {prp} - {module_name}")
            result = TestResult(
                module_path=module_path,
                module_name=module_name,
                prp_category=prp
            )
            
            # Check if file exists
            if not os.path.exists(module_path):
                result.issues.append({
                    "severity": "Critical",
                    "type": "Missing Module",
                    "details": f"Module file not found: {module_path}"
                })
                self.results[module_name] = result
                continue
            
            # Test 1: Module Import
            logger.info(f"  Testing import...")
            import_success, import_time, import_error, dependencies = self.test_module_import(module_path, module_name)
            result.import_success = import_success
            result.import_time = import_time
            result.import_error = import_error
            result.dependencies = dependencies
            
            if not import_success:
                result.issues.append({
                    "severity": "Critical",
                    "type": "Import Failure",
                    "details": import_error
                })
            
            # Test 2: Analyze Code Issues
            logger.info(f"  Analyzing code...")
            code_issues = self.analyze_module_code(module_path)
            
            # Convert code issues to result issues
            for issue_type, issues in code_issues.items():
                for issue in issues:
                    severity = "High" if issue_type in ["hardcoded_values", "missing_error_handling", "blocking_operations"] else "Medium"
                    result.issues.append({
                        "severity": severity,
                        "type": issue_type,
                        "details": issue
                    })
            
            # Test 3: Check Circular Imports
            circular_imports = self.check_circular_imports(module_path, dependencies)
            result.circular_imports = circular_imports
            if circular_imports:
                for ci in circular_imports:
                    result.issues.append({
                        "severity": "High",
                        "type": "Circular Import Risk",
                        "details": ci
                    })
            
            # Test 4: Async Pattern Analysis
            logger.info(f"  Checking async patterns...")
            async_issues = self.test_async_patterns(module_path)
            result.async_issues = async_issues
            for issue in async_issues:
                result.issues.append({
                    "severity": "High",
                    "type": "Async Pattern Issue",
                    "details": issue
                })
            
            # Test 5: Functionality Tests
            if import_success:
                logger.info(f"  Testing functionality...")
                result.functional_tests = self.test_module_functionality(module_path, module_name)
            
            # Test 6: Performance Metrics
            logger.info(f"  Measuring performance...")
            result.performance_metrics = self.measure_performance(module_path, module_name)
            
            # Check for performance issues
            if result.performance_metrics.get('avg_import_time', 0) > 1.0:
                result.issues.append({
                    "severity": "Medium",
                    "type": "Slow Import",
                    "details": f"Average import time: {result.performance_metrics['avg_import_time']:.2f}s"
                })
            
            # Test 7: Resource Leak Detection
            logger.info(f"  Checking for resource leaks...")
            result.resource_leaks = self.check_resource_leaks(module_path)
            for leak in result.resource_leaks:
                result.issues.append({
                    "severity": "High",
                    "type": "Resource Leak",
                    "details": leak
                })
            
            # Test 8: Integration Compatibility
            logger.info(f"  Checking AAI integration...")
            result.integration_issues = self.check_integration_compatibility(module_path, module_name)
            for issue in result.integration_issues:
                result.issues.append({
                    "severity": "Medium",
                    "type": "Integration Issue",
                    "details": issue
                })
            
            # Test 9: Fallback Analysis
            logger.info(f"  Analyzing fallback triggers...")
            result.fallback_triggers = self.analyze_fallback_triggers(module_path)
            
            # Store result
            self.results[module_name] = result
            
            # Log summary
            logger.info(f"  Status: {result.overall_status}")
            logger.info(f"  Issues found: {len(result.issues)}")
            
        logger.info("\nTesting complete!")
    
    def generate_comprehensive_report(self) -> str:
        """Generate detailed test report"""
        report = []
        report.append("# AAI Comprehensive Module Test Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("\n## Executive Summary")
        
        # Count statuses
        total_modules = len(self.results)
        passed = sum(1 for r in self.results.values() if r.overall_status == "PASS")
        warned = sum(1 for r in self.results.values() if r.overall_status == "WARN")
        failed = sum(1 for r in self.results.values() if r.overall_status == "FAIL")
        
        report.append(f"- Total Modules Tested: {total_modules}")
        report.append(f"- Passed: {passed} ({passed/total_modules*100:.1f}%)")
        report.append(f"- Warnings: {warned} ({warned/total_modules*100:.1f}%)")
        report.append(f"- Failed: {failed} ({failed/total_modules*100:.1f}%)")
        
        # Critical issues
        critical_issues = []
        for module_name, result in self.results.items():
            for issue in result.issues:
                if issue.get("severity") == "Critical":
                    critical_issues.append((module_name, issue))
        
        report.append(f"\n### Critical Issues Found: {len(critical_issues)}")
        for module, issue in critical_issues[:5]:  # Show top 5
            report.append(f"- **{module}**: {issue['type']} - {issue['details'][:100]}...")
        
        # Module naming issues
        report.append("\n### Module Naming Verification")
        naming_issues = []
        if "mcp-orchestrator" in self.results:
            report.append("- ✓ mcp-orchestrator.py found (PRP7)")
        else:
            naming_issues.append("mcp-orchestrator.py")
            report.append("- ✗ mcp-orchestrator.py NOT FOUND - needs renaming")
        
        if "tech-stack-expert" in self.results:
            report.append("- ✓ tech-stack-expert.py found (PRP8)")
        else:
            naming_issues.append("tech-stack-expert.py")
            report.append("- ✗ tech-stack-expert.py NOT FOUND - needs renaming")
        
        # Detailed results by Module Category
        report.append("\n## Detailed Results by Module Category")
        
        for prp in ["BRAIN", "CORE", "MCP", "AGENTS_ORCH", "AGENTS_SPEC", "AGENTS_TECH", "AGENTS_R1", "AGENTS_TOOL"]:
            prp_modules = [(name, result) for name, result in self.results.items() if result.prp_category == prp]
            
            report.append(f"\n### {prp} ({len(prp_modules)} modules)")
            
            for module_name, result in prp_modules:
                report.append(f"\n#### {module_name}")
                report.append(f"- **Status**: {result.overall_status}")
                report.append(f"- **Path**: {result.module_path}")
                
                if not result.import_success:
                    report.append(f"- **Import Error**: {result.import_error}")
                else:
                    report.append(f"- **Import Time**: {result.import_time:.3f}s")
                
                if result.issues:
                    report.append(f"- **Issues** ({len(result.issues)}):")
                    # Group by severity
                    by_severity = {}
                    for issue in result.issues:
                        sev = issue.get("severity", "Unknown")
                        if sev not in by_severity:
                            by_severity[sev] = []
                        by_severity[sev].append(issue)
                    
                    for severity in ["Critical", "High", "Medium", "Low"]:
                        if severity in by_severity:
                            report.append(f"  - {severity}: {len(by_severity[severity])}")
                            for issue in by_severity[severity][:3]:  # Show first 3
                                report.append(f"    - {issue['type']}: {str(issue['details'])[:80]}...")
                
                if result.fallback_triggers:
                    report.append(f"- **Fallback Triggers** ({len(result.fallback_triggers)}):")
                    for trigger in result.fallback_triggers[:2]:  # Show first 2
                        report.append(f"  - Line {trigger['line']}: {trigger['reason']}")
                
                if result.resource_leaks:
                    report.append(f"- **Resource Leaks**: {', '.join(result.resource_leaks)}")
                
                if result.async_issues:
                    report.append(f"- **Async Issues**: {', '.join(result.async_issues)}")
                
                if result.performance_metrics:
                    if result.performance_metrics.get('avg_import_time', 0) > 0.5:
                        report.append(f"- **Performance Warning**: Slow import ({result.performance_metrics['avg_import_time']:.2f}s)")
        
        # Fallback Analysis Summary
        report.append("\n## Fallback Analysis")
        all_fallbacks = []
        for module_name, result in self.results.items():
            for trigger in result.fallback_triggers:
                all_fallbacks.append((module_name, trigger))
        
        report.append(f"Total fallback occurrences: {len(all_fallbacks)}")
        
        # Group fallbacks by reason
        fallback_reasons = {}
        for module, trigger in all_fallbacks:
            reason = trigger['reason'].split(':')[0]
            if reason not in fallback_reasons:
                fallback_reasons[reason] = []
            fallback_reasons[reason].append(module)
        
        report.append("\nFallback triggers by type:")
        for reason, modules in sorted(fallback_reasons.items(), key=lambda x: len(x[1]), reverse=True):
            report.append(f"- {reason}: {len(modules)} occurrences")
            report.append(f"  Modules: {', '.join(set(modules[:5]))}...")
        
        # Performance Bottlenecks
        report.append("\n## Performance Bottlenecks")
        slow_imports = []
        large_files = []
        
        for module_name, result in self.results.items():
            if result.performance_metrics:
                if result.performance_metrics.get('avg_import_time', 0) > 0.5:
                    slow_imports.append((module_name, result.performance_metrics['avg_import_time']))
                if result.performance_metrics.get('file_size_kb', 0) > 100:
                    large_files.append((module_name, result.performance_metrics['file_size_kb']))
        
        report.append(f"\n### Slow Imports (>0.5s): {len(slow_imports)}")
        for module, time in sorted(slow_imports, key=lambda x: x[1], reverse=True)[:5]:
            report.append(f"- {module}: {time:.2f}s")
        
        report.append(f"\n### Large Files (>100KB): {len(large_files)}")
        for module, size in sorted(large_files, key=lambda x: x[1], reverse=True)[:5]:
            report.append(f"- {module}: {size:.1f}KB")
        
        # Resource Management Issues
        report.append("\n## Resource Management Issues")
        modules_with_leaks = [(name, result) for name, result in self.results.items() if result.resource_leaks]
        report.append(f"Modules with potential resource leaks: {len(modules_with_leaks)}")
        
        for module_name, result in modules_with_leaks[:10]:
            report.append(f"- {module_name}: {', '.join(result.resource_leaks)}")
        
        # Integration Issues
        report.append("\n## AAI Integration Issues")
        integration_problems = [(name, result) for name, result in self.results.items() if result.integration_issues]
        report.append(f"Modules with integration issues: {len(integration_problems)}")
        
        for module_name, result in integration_problems[:10]:
            report.append(f"- {module_name}:")
            for issue in result.integration_issues:
                report.append(f"  - {issue}")
        
        # Recommendations
        report.append("\n## Critical Recommendations")
        
        report.append("\n### Immediate Actions Required:")
        report.append("1. **Fix Module Naming**:")
        if naming_issues:
            for module in naming_issues:
                report.append(f"   - Rename/create {module}")
        else:
            report.append("   - All modules properly named")
        
        report.append("\n2. **Fix Critical Import Failures**:")
        import_failures = [(name, result) for name, result in self.results.items() if not result.import_success]
        for module_name, result in import_failures[:5]:
            report.append(f"   - {module_name}: {result.import_error.split(':')[0] if result.import_error else 'Unknown error'}")
        
        report.append("\n3. **Address Resource Leaks**:")
        report.append(f"   - {len(modules_with_leaks)} modules need resource management fixes")
        
        report.append("\n4. **Optimize Slow Imports**:")
        report.append(f"   - {len(slow_imports)} modules have slow import times")
        
        report.append("\n5. **Fix Async Pattern Issues**:")
        async_problem_modules = [(name, result) for name, result in self.results.items() if result.async_issues]
        report.append(f"   - {len(async_problem_modules)} modules have async implementation issues")
        
        return '\n'.join(report)
    
    def save_results(self):
        """Save test results to files"""
        # Save detailed JSON results
        json_results = {}
        for module_name, result in self.results.items():
            json_results[module_name] = {
                "module_path": result.module_path,
                "prp_category": result.prp_category,
                "overall_status": result.overall_status,
                "import_success": result.import_success,
                "import_time": result.import_time,
                "import_error": result.import_error,
                "functional_tests": result.functional_tests,
                "performance_metrics": result.performance_metrics,
                "issues": result.issues,
                "fallback_triggers": result.fallback_triggers,
                "async_issues": result.async_issues,
                "resource_leaks": result.resource_leaks,
                "integration_issues": result.integration_issues,
                "dependencies": result.dependencies,
                "circular_imports": result.circular_imports
            }
        
        with open('/mnt/c/Users/Brandon/AAI/tests/comprehensive_test_results.json', 'w') as f:
            json.dump(json_results, f, indent=2)
        
        # Save markdown report
        report = self.generate_comprehensive_report()
        with open('/mnt/c/Users/Brandon/AAI/tests/comprehensive_test_report.md', 'w') as f:
            f.write(report)
        
        # Save critical issues CSV for quick reference
        import csv
        with open('/mnt/c/Users/Brandon/AAI/tests/critical_issues.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Module', 'PRP', 'Status', 'Severity', 'Issue Type', 'Details'])
            
            for module_name, result in self.results.items():
                for issue in result.issues:
                    writer.writerow([
                        module_name,
                        result.prp_category,
                        result.overall_status,
                        issue.get('severity', 'Unknown'),
                        issue.get('type', 'Unknown'),
                        str(issue.get('details', ''))[:200]
                    ])

async def main():
    """Main test execution"""
    tester = ComprehensiveModuleTester()
    
    try:
        await tester.run_comprehensive_tests()
        tester.save_results()
        
        # Print summary
        print("\n" + "="*80)
        print("COMPREHENSIVE TEST COMPLETE")
        print("="*80)
        
        # Quick summary
        total = len(tester.results)
        passed = sum(1 for r in tester.results.values() if r.overall_status == "PASS")
        failed = sum(1 for r in tester.results.values() if r.overall_status == "FAIL")
        
        print(f"\nTotal Modules: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"\nDetailed reports saved to:")
        print("- /mnt/c/Users/Brandon/AAI/tests/comprehensive_test_report.md")
        print("- /mnt/c/Users/Brandon/AAI/tests/comprehensive_test_results.json")
        print("- /mnt/c/Users/Brandon/AAI/tests/critical_issues.csv")
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    # Run tests
    asyncio.run(main())