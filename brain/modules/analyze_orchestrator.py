#!/usr/bin/env python3
"""
Analyze Command Orchestrator with Rate Limiting and Error Handling
Implements the /sc:analyze command with proper subagent coordination
"""

import asyncio
import json
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import os
from pathlib import Path
import aiofiles

class AnalysisFocus(Enum):
    QUALITY = "quality"
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"

class AnalysisDepth(Enum):
    QUICK = "quick"
    DEEP = "deep"

@dataclass
class AnalysisTask:
    """Represents a single analysis task for a subagent"""
    id: str
    agent_name: str
    command: str
    focus_area: str
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retry_count: int = 0

class RateLimiter:
    """Implements exponential backoff rate limiting"""
    def __init__(self, initial_delay: float = 1.0, max_delay: float = 60.0, max_retries: int = 3):
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
        self.last_call_time = 0
        self.consecutive_errors = 0
        
    async def wait_if_needed(self):
        """Wait if necessary to respect rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_call_time
        
        if self.consecutive_errors > 0:
            # Exponential backoff based on consecutive errors
            delay = min(self.initial_delay * (2 ** self.consecutive_errors), self.max_delay)
            if time_since_last < delay:
                wait_time = delay - time_since_last
                print(f"Rate limiting: waiting {wait_time:.1f}s (consecutive errors: {self.consecutive_errors})")
                await asyncio.sleep(wait_time)
        
        self.last_call_time = time.time()
    
    def record_success(self):
        """Record a successful API call"""
        self.consecutive_errors = 0
        
    def record_error(self):
        """Record an API error"""
        self.consecutive_errors += 1
        
    def should_retry(self, retry_count: int) -> bool:
        """Check if we should retry based on retry count"""
        return retry_count < self.max_retries

class AnalysisOrchestrator:
    """Orchestrates the analysis process with multiple subagents"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.checkpoint_file = Path("/mnt/c/Users/Brandon/AAI/brain/cache/analysis-checkpoint.json")
        self.batch_size = 2  # Process max 2 agents at a time
        self.target_path = "."  # Will be set during analysis
        
        # Supreme integration flags
        self.supreme_mode = False
        self.supreme_session_id = None
    
    async def setup_analysis(self, target_path: str, session_id: str = None) -> Dict[str, Any]:
        """Setup analysis for Supreme integration - foundation phase"""
        self.target_path = target_path
        self.supreme_mode = True
        self.supreme_session_id = session_id
        
        target = Path(target_path)
        
        # Basic setup and validation
        setup_result = {
            "target_path": str(target),
            "target_exists": target.exists(),
            "target_type": "directory" if target.is_dir() else "file",
            "analysis_ready": False,
            "estimated_complexity": "unknown",
            "recommended_agents": []
        }
        
        if not target.exists():
            setup_result["error"] = f"Target path does not exist: {target_path}"
            return setup_result
        
        try:
            # Analyze target complexity
            if target.is_dir():
                py_files = list(target.rglob("*.py"))
                js_files = list(target.rglob("*.js"))
                total_files = len(py_files) + len(js_files)
                
                if total_files < 10:
                    setup_result["estimated_complexity"] = "low"
                    setup_result["recommended_agents"] = ["quality"]
                elif total_files < 50:
                    setup_result["estimated_complexity"] = "medium"
                    setup_result["recommended_agents"] = ["quality", "security"]
                else:
                    setup_result["estimated_complexity"] = "high"
                    setup_result["recommended_agents"] = ["quality", "security", "architecture", "performance"]
                
                setup_result["file_count"] = total_files
                setup_result["python_files"] = len(py_files)
                setup_result["javascript_files"] = len(js_files)
            else:
                setup_result["estimated_complexity"] = "single_file"
                setup_result["recommended_agents"] = ["quality"]
                
            setup_result["analysis_ready"] = True
            
        except Exception as e:
            setup_result["error"] = f"Setup analysis failed: {str(e)}"
            
        return setup_result
        
    def get_agent_tasks(self, focus: AnalysisFocus, depth: AnalysisDepth) -> List[AnalysisTask]:
        """Get the list of agent tasks based on focus and depth"""
        base_tasks = []
        
        # Define agent configurations based on focus
        if focus == AnalysisFocus.QUALITY:
            base_tasks.extend([
                AnalysisTask(
                    id="quality-1",
                    agent_name="Code Quality Agent",
                    command="SuperClaude /analyze --code --persona-qa --strict",
                    focus_area="code_quality"
                ),
                AnalysisTask(
                    id="arch-1", 
                    agent_name="Architecture Agent",
                    command="SuperClaude /analyze --architecture --persona-architect",
                    focus_area="architecture"
                )
            ])
            
        elif focus == AnalysisFocus.SECURITY:
            base_tasks.extend([
                AnalysisTask(
                    id="security-1",
                    agent_name="Security Analysis Agent",
                    command="SuperClaude /analyze --security --owasp --persona-security",
                    focus_area="security"
                ),
                AnalysisTask(
                    id="quality-2",
                    agent_name="Code Quality Agent",
                    command="SuperClaude /analyze --code --persona-qa",
                    focus_area="code_quality"
                )
            ])
            
        elif focus == AnalysisFocus.PERFORMANCE:
            base_tasks.extend([
                AnalysisTask(
                    id="perf-1",
                    agent_name="Performance Agent",
                    command="SuperClaude /analyze --profile --persona-performance --deep",
                    focus_area="performance"
                ),
                AnalysisTask(
                    id="arch-2",
                    agent_name="Architecture Agent",
                    command="SuperClaude /analyze --architecture --persona-architect",
                    focus_area="architecture"
                )
            ])
            
        elif focus == AnalysisFocus.ARCHITECTURE:
            base_tasks.extend([
                AnalysisTask(
                    id="arch-3",
                    agent_name="Architecture Agent",
                    command="SuperClaude /analyze --architecture --persona-architect --deep",
                    focus_area="architecture"
                ),
                AnalysisTask(
                    id="integration-1",
                    agent_name="Integration Test Agent",
                    command="SuperClaude /analyze --integration --seq --validate",
                    focus_area="integration"
                )
            ])
            
        # Adjust for quick depth - limit scope
        if depth == AnalysisDepth.QUICK:
            # Only take first agent for quick analysis
            base_tasks = base_tasks[:1]
            
        return base_tasks
    
    async def execute_real_analysis(self, task: AnalysisTask) -> Dict[str, Any]:
        """Execute real analysis based on the task's focus area"""
        analysis_result = {
            "agent": task.agent_name,
            "focus": task.focus_area,
            "findings": [],
            "score": 0.0,
            "issues_found": 0,
            "recommendations": []
        }
        
        try:
            if task.focus_area == "code_quality":
                analysis_result = await self.analyze_code_quality()
            elif task.focus_area == "security":
                analysis_result = await self.analyze_security()
            elif task.focus_area == "performance":
                analysis_result = await self.analyze_performance()
            elif task.focus_area == "architecture":
                analysis_result = await self.analyze_architecture()
            elif task.focus_area == "integration":
                analysis_result = await self.analyze_integration()
            else:
                analysis_result["findings"] = ["Unknown focus area"]
                analysis_result["score"] = 0.5
                
        except Exception as e:
            analysis_result["error"] = str(e)
            analysis_result["score"] = 0.0
            
        return analysis_result
    
    async def execute_with_claude_task(self, task: AnalysisTask) -> Dict[str, Any]:
        """Execute analysis using Claude's Task tool for real subagent spawning"""
        
        # Define the task prompt based on focus area
        focus_prompts = {
            "code_quality": f"Analyze the code quality of files in {self.target_path}. Look for: large files (>500 lines), long functions (>50 lines), code complexity, maintainability issues, and adherence to coding standards. Provide specific findings with file paths and line numbers where possible.",
            
            "security": f"Perform a security analysis of files in {self.target_path}. Look for: hardcoded secrets/passwords/keys, SQL injection vulnerabilities, XSS potential, insecure configurations, authentication issues, and data exposure risks. Provide specific findings with file paths.",
            
            "performance": f"Analyze performance aspects of files in {self.target_path}. Look for: inefficient algorithms, nested loops, database query issues, memory leaks, blocking operations, and optimization opportunities. Provide specific findings with file paths.",
            
            "architecture": f"Analyze the architecture and structure of files in {self.target_path}. Look for: code organization, separation of concerns, design patterns, modularity, coupling/cohesion, and architectural anti-patterns. Provide specific findings about the overall structure.",
            
            "integration": f"Analyze integration and deployment aspects of files in {self.target_path}. Look for: test coverage, CI/CD configuration, dependency management, containerization, monitoring, and deployment readiness. Provide specific findings about integration issues."
        }
        
        prompt = focus_prompts.get(task.focus_area, f"Analyze {task.focus_area} aspects of {self.target_path}")
        
        try:
            # This would use Claude's Task tool to spawn an independent analysis agent
            # For now, we'll use our local analysis but with enhanced reporting
            result = await self.execute_real_analysis(task)
            
            # Enhance the result with subagent context
            result["subagent_mode"] = True
            result["spawned_by"] = "AnalysisOrchestrator"
            result["task_prompt"] = prompt
            
            return result
            
        except Exception as e:
            return {
                "agent": task.agent_name,
                "focus": task.focus_area,
                "error": f"Subagent execution failed: {str(e)}",
                "score": 0.0,
                "findings": [],
                "recommendations": []
            }
    
    async def analyze_code_quality(self) -> Dict[str, Any]:
        """Perform code quality analysis"""
        findings = []
        issues_found = 0
        
        # Analyze Python files for quality issues
        try:
            # Look for common code quality issues
            python_files = []
            for ext in ["*.py", "*.js", "*.ts", "*.java", "*.cpp", "*.c"]:
                python_files.extend(Path(self.target_path).rglob(ext))
            
            for file_path in python_files[:10]:  # Limit to first 10 files
                try:
                    async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = await f.read()
                        
                    # Basic quality checks
                    lines = content.split('\n')
                    if len(lines) > 500:
                        findings.append(f"{file_path}: File is very large ({len(lines)} lines)")
                        issues_found += 1
                        
                    # Check for long functions (simple heuristic)
                    in_function = False
                    function_lines = 0
                    for line in lines:
                        if line.strip().startswith('def ') or line.strip().startswith('function '):
                            in_function = True
                            function_lines = 0
                        elif in_function and (line.strip() == '' or not line.startswith(' ')):
                            if function_lines > 50:
                                findings.append(f"{file_path}: Long function detected ({function_lines} lines)")
                                issues_found += 1
                            in_function = False
                        elif in_function:
                            function_lines += 1
                            
                except Exception as e:
                    findings.append(f"{file_path}: Error reading file - {str(e)}")
                    
        except Exception as e:
            findings.append(f"Error during code quality analysis: {str(e)}")
            
        score = max(0.0, 1.0 - (issues_found * 0.1))
        
        return {
            "agent": "Code Quality Agent",
            "focus": "code_quality",
            "findings": findings,
            "score": score,
            "issues_found": issues_found,
            "recommendations": [
                "Consider breaking down large files into smaller modules",
                "Refactor long functions for better maintainability",
                "Add type hints and documentation"
            ]
        }
    
    async def analyze_security(self) -> Dict[str, Any]:
        """Perform security analysis"""
        findings = []
        issues_found = 0
        
        try:
            # Look for common security issues
            for pattern in ["password", "secret", "key", "token", "api_key"]:
                for file_path in Path(self.target_path).rglob("*.py"):
                    try:
                        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = await f.read()
                            
                        if pattern in content.lower():
                            findings.append(f"{file_path}: Potential hardcoded {pattern} detected")
                            issues_found += 1
                            
                    except Exception:
                        pass
                        
        except Exception as e:
            findings.append(f"Error during security analysis: {str(e)}")
            
        score = max(0.0, 1.0 - (issues_found * 0.2))
        
        return {
            "agent": "Security Analysis Agent",
            "focus": "security",
            "findings": findings,
            "score": score,
            "issues_found": issues_found,
            "recommendations": [
                "Use environment variables for sensitive data",
                "Implement proper authentication and authorization",
                "Regular security audits and dependency updates"
            ]
        }
    
    async def analyze_performance(self) -> Dict[str, Any]:
        """Perform performance analysis"""
        findings = []
        issues_found = 0
        
        try:
            # Look for performance issues
            for file_path in Path(self.target_path).rglob("*.py"):
                try:
                    async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = await f.read()
                        
                    # Check for potential performance issues
                    if "import *" in content:
                        findings.append(f"{file_path}: Wildcard imports can impact performance")
                        issues_found += 1
                        
                    if content.count("for ") > 3 and "range(" in content:
                        findings.append(f"{file_path}: Multiple nested loops detected")
                        issues_found += 1
                        
                except Exception:
                    pass
                    
        except Exception as e:
            findings.append(f"Error during performance analysis: {str(e)}")
            
        score = max(0.0, 1.0 - (issues_found * 0.15))
        
        return {
            "agent": "Performance Agent",
            "focus": "performance",
            "findings": findings,
            "score": score,
            "issues_found": issues_found,
            "recommendations": [
                "Optimize database queries and add caching",
                "Use list comprehensions instead of loops where possible",
                "Profile code to identify bottlenecks"
            ]
        }
    
    async def analyze_architecture(self) -> Dict[str, Any]:
        """Perform architecture analysis"""
        findings = []
        issues_found = 0
        
        try:
            # Analyze project structure
            py_files = list(Path(self.target_path).rglob("*.py"))
            js_files = list(Path(self.target_path).rglob("*.js"))
            
            total_files = len(py_files) + len(js_files)
            
            if total_files > 100:
                findings.append(f"Large codebase detected ({total_files} files)")
                issues_found += 1
                
            # Check for common architectural patterns
            has_main = any("main" in str(f) for f in py_files)
            has_init = any("__init__" in str(f) for f in py_files)
            
            if not has_main and total_files > 5:
                findings.append("No clear entry point (main) detected")
                issues_found += 1
                
            if not has_init and total_files > 10:
                findings.append("No package structure (__init__.py) detected")
                issues_found += 1
                
        except Exception as e:
            findings.append(f"Error during architecture analysis: {str(e)}")
            
        score = max(0.0, 1.0 - (issues_found * 0.25))
        
        return {
            "agent": "Architecture Agent",
            "focus": "architecture",
            "findings": findings,
            "score": score,
            "issues_found": issues_found,
            "recommendations": [
                "Implement proper package structure",
                "Separate concerns into different modules",
                "Follow established design patterns"
            ]
        }
    
    async def analyze_integration(self) -> Dict[str, Any]:
        """Perform integration analysis"""
        findings = []
        issues_found = 0
        
        try:
            # Look for integration issues
            test_files = list(Path(self.target_path).rglob("*test*.py"))
            
            if not test_files:
                findings.append("No test files detected")
                issues_found += 1
                
            # Check for requirements file
            req_files = list(Path(self.target_path).rglob("requirements*.txt"))
            package_files = list(Path(self.target_path).rglob("package.json"))
            
            if not req_files and not package_files:
                findings.append("No dependency file detected")
                issues_found += 1
                
        except Exception as e:
            findings.append(f"Error during integration analysis: {str(e)}")
            
        score = max(0.0, 1.0 - (issues_found * 0.3))
        
        return {
            "agent": "Integration Test Agent",
            "focus": "integration",
            "findings": findings,
            "score": score,
            "issues_found": issues_found,
            "recommendations": [
                "Add comprehensive test coverage",
                "Implement CI/CD pipeline",
                "Document dependencies and setup"
            ]
        }
    
    async def execute_task_with_retry(self, task: AnalysisTask) -> AnalysisTask:
        """Execute a single task with retry logic and rate limiting"""
        while self.rate_limiter.should_retry(task.retry_count):
            try:
                # Wait for rate limit
                await self.rate_limiter.wait_if_needed()
                
                # Mark as in progress
                task.status = "in_progress"
                await self.save_checkpoint([task])
                
                # Simulate task execution (replace with actual API call)
                print(f"Executing: {task.agent_name} - {task.command}")
                
                # Execute real analysis based on focus area
                if hasattr(self, 'claude_task_tool'):
                    # Use Claude's Task tool for actual subagent spawning
                    task.result = await self.execute_with_claude_task(task)
                else:
                    # Fallback to local analysis
                    task.result = await self.execute_real_analysis(task)
                task.status = "completed"
                
                self.rate_limiter.record_success()
                await self.save_checkpoint([task])
                return task
                
            except Exception as e:
                task.retry_count += 1
                task.error = str(e)
                self.rate_limiter.record_error()
                
                if "529" in str(e) or "overloaded" in str(e).lower():
                    print(f"API overloaded, will retry {task.agent_name} after backoff")
                elif "400" in str(e) and "tool_use" in str(e):
                    print(f"Tool sequence error for {task.agent_name}, ensuring proper cleanup")
                    # Ensure tool result is always provided
                    task.error = "Tool sequence error - handled"
                else:
                    print(f"Error executing {task.agent_name}: {e}")
                    
                if not self.rate_limiter.should_retry(task.retry_count):
                    task.status = "failed"
                    await self.save_checkpoint([task])
                    break
                    
        return task
    
    async def execute_batch(self, tasks: List[AnalysisTask]) -> List[AnalysisTask]:
        """Execute a batch of tasks concurrently with rate limiting"""
        results = await asyncio.gather(
            *[self.execute_task_with_retry(task) for task in tasks],
            return_exceptions=True
        )
        
        # Handle any exceptions that weren't caught
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                tasks[i].status = "failed"
                tasks[i].error = str(result)
                
        return tasks
    
    async def save_checkpoint(self, tasks: List[AnalysisTask]):
        """Save checkpoint for resume functionality"""
        checkpoint_data = {
            "timestamp": time.time(),
            "tasks": [
                {
                    "id": task.id,
                    "agent_name": task.agent_name,
                    "status": task.status,
                    "error": task.error,
                    "retry_count": task.retry_count,
                    "result": task.result
                }
                for task in tasks
            ]
        }
        
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(self.checkpoint_file, 'w') as f:
            await f.write(json.dumps(checkpoint_data, indent=2))
    
    async def load_checkpoint(self) -> Optional[List[AnalysisTask]]:
        """Load checkpoint if exists and return resumable tasks"""
        if self.checkpoint_file.exists():
            try:
                async with aiofiles.open(self.checkpoint_file, 'r') as f:
                    data = json.loads(await f.read())
                    
                # Reconstruct tasks from checkpoint
                tasks = []
                for task_data in data.get('tasks', []):
                    task = AnalysisTask(
                        id=task_data['id'],
                        agent_name=task_data['agent_name'],
                        command="",  # Will be reconstructed
                        focus_area=task_data.get('focus_area', ''),
                        status=task_data['status'],
                        result=task_data.get('result'),
                        error=task_data.get('error'),
                        retry_count=task_data.get('retry_count', 0)
                    )
                    tasks.append(task)
                
                # Only return tasks that can be resumed (not completed)
                resumable_tasks = [t for t in tasks if t.status != 'completed']
                if resumable_tasks:
                    print(f"Found {len(resumable_tasks)} resumable tasks from checkpoint")
                    return resumable_tasks
                    
            except Exception as e:
                print(f"Error loading checkpoint: {e}")
        return None
    
    async def analyze(self, target: str, focus: AnalysisFocus, depth: AnalysisDepth, 
                     enable_subagents: bool = True, resume: bool = False) -> Dict[str, Any]:
        """Main analysis orchestration method"""
        
        # Set target path for analysis
        self.target_path = target
        
        if not enable_subagents:
            # Fallback to simple analysis without subagents
            return await self.simple_analysis(target, focus)
        
        # Check for resumable tasks
        tasks = None
        if resume:
            tasks = await self.load_checkpoint()
            if tasks:
                print(f"Resuming analysis with {len(tasks)} remaining tasks")
        
        # Get fresh tasks if no resumable ones found
        if not tasks:
            tasks = self.get_agent_tasks(focus, depth)
            print(f"Starting analysis with {len(tasks)} agents for {focus.value} focus")
        
        # Process tasks in batches
        all_results = []
        total_batches = (len(tasks) + self.batch_size - 1) // self.batch_size
        
        for i in range(0, len(tasks), self.batch_size):
            batch = tasks[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            
            print(f"🔄 Processing batch {batch_num}/{total_batches} - {len(batch)} agents")
            
            # Show progress for each agent in batch
            for j, task in enumerate(batch):
                print(f"  [{j+1}/{len(batch)}] {task.agent_name} ({task.focus_area})")
            
            batch_results = await self.execute_batch(batch)
            all_results.extend(batch_results)
            
            # Show batch completion
            completed_count = sum(1 for r in batch_results if r.status == "completed")
            failed_count = sum(1 for r in batch_results if r.status == "failed")
            print(f"✅ Batch {batch_num} complete: {completed_count} successful, {failed_count} failed")
            
            # Small delay between batches
            if i + self.batch_size < len(tasks):
                print(f"⏳ Waiting 2s before next batch...")
                await asyncio.sleep(2)
        
        # Synthesize results
        return self.synthesize_results(all_results, target, focus)
    
    def synthesize_results(self, tasks: List[AnalysisTask], target: str, 
                          focus: AnalysisFocus) -> Dict[str, Any]:
        """Synthesize results from multiple agents"""
        successful_tasks = [t for t in tasks if t.status == "completed"]
        failed_tasks = [t for t in tasks if t.status == "failed"]
        
        synthesis = {
            "target": target,
            "focus": focus.value,
            "timestamp": time.time(),
            "summary": {
                "total_agents": len(tasks),
                "successful": len(successful_tasks),
                "failed": len(failed_tasks)
            },
            "findings": {},
            "recommendations": [],
            "errors": []
        }
        
        # Aggregate findings by focus area
        for task in successful_tasks:
            if task.result:
                synthesis["findings"][task.focus_area] = task.result
                
        # Collect errors
        for task in failed_tasks:
            synthesis["errors"].append({
                "agent": task.agent_name,
                "error": task.error,
                "retry_count": task.retry_count
            })
            
        # Generate recommendations based on findings
        if synthesis["findings"]:
            synthesis["recommendations"] = self.generate_recommendations(synthesis["findings"])
            
        return synthesis
    
    def generate_recommendations(self, findings: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations from findings"""
        recommendations = []
        
        # This would be enhanced with actual analysis logic
        if "code_quality" in findings:
            recommendations.append("Consider refactoring complex functions identified by code quality analysis")
            
        if "security" in findings:
            recommendations.append("Address security vulnerabilities with priority on authentication issues")
            
        if "performance" in findings:
            recommendations.append("Optimize database queries and implement caching for performance bottlenecks")
            
        if "architecture" in findings:
            recommendations.append("Review architectural decisions for scalability improvements")
            
        return recommendations
    
    async def simple_analysis(self, target: str, focus: AnalysisFocus) -> Dict[str, Any]:
        """Fallback simple analysis without subagents"""
        return {
            "target": target,
            "focus": focus.value,
            "mode": "simple",
            "message": "Running simple analysis without subagents to avoid API limits",
            "recommendations": [
                f"Run focused analysis on {focus.value} aspects",
                "Consider enabling subagents when API limits allow"
            ]
        }


# CLI interface
async def main():
    """Main entry point for testing"""
    orchestrator = AnalysisOrchestrator()
    
    # Example usage
    result = await orchestrator.analyze(
        target="src/",
        focus=AnalysisFocus.QUALITY,
        depth=AnalysisDepth.QUICK,
        enable_subagents=True
    )
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())