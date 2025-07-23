"""
Delegation Engine for Intelligent Task Analysis and Agent Selection

Implements sophisticated task decomposition, agent selection, and confidence
scoring for optimal task delegation across specialized agents.
"""
import logging
import asyncio
import re
from typing import List, Dict, Any, Optional, Tuple, Set
from datetime import datetime
import uuid

try:
    from .models import (
        TaskDelegation, AgentSpecialization, TaskComplexity, DelegationStatus,
        AgentProfile, AgentCapability, DelegationRequest, OrchestrationResult
    )
except ImportError:
    from agents.orchestration.models import (
        TaskDelegation, AgentSpecialization, TaskComplexity, DelegationStatus,
        AgentProfile, AgentCapability, DelegationRequest, OrchestrationResult
    )

logger = logging.getLogger(__name__)


class TaskAnalyzer:
    """Analyzes tasks for complexity, requirements, and optimal delegation"""
    
    def __init__(self):
        """Initialize task analyzer with pattern recognition"""
        
        # Task type patterns for agent mapping
        self.agent_patterns = {
            AgentSpecialization.SLACK: [
                "send message", "slack", "notify", "communicate", "alert", "channel",
                "team", "post", "dm", "direct message", "status update"
            ],
            AgentSpecialization.GITHUB: [
                "github", "repository", "repo", "issue", "pull request", "pr", "commit",
                "branch", "code", "merge", "release", "version control", "git"
            ],
            AgentSpecialization.AIRTABLE: [
                "airtable", "database", "record", "table", "spreadsheet", "data entry",
                "update record", "create record", "query", "filter", "sort"
            ],
            AgentSpecialization.FIRECRAWL: [
                "scrape", "crawl", "website", "web page", "extract", "parse", "html",
                "content", "firecrawl", "web data", "site content"
            ],
            AgentSpecialization.FILESYSTEM: [
                "file", "directory", "folder", "read", "write", "create", "delete",
                "copy", "move", "path", "filesystem", "save", "load", "download"
            ],
            AgentSpecialization.JINA_SEARCH: [
                "search", "find", "look up", "query", "research", "information",
                "web search", "internet", "google", "results", "discover"
            ],
            AgentSpecialization.MEMORY: [
                "remember", "recall", "store", "memory", "save information", "note",
                "knowledge", "learn", "memorize", "retrieve", "history"
            ],
            AgentSpecialization.TIME: [
                "time", "date", "schedule", "calendar", "reminder", "appointment",
                "meeting", "deadline", "timer", "clock", "when", "duration"
            ]
        }
        
        # Complexity indicators
        self.complexity_indicators = {
            "simple": ["quick", "simple", "just", "only", "basic", "easy"],
            "moderate": ["analyze", "process", "create", "update", "moderate", "standard"],
            "complex": ["comprehensive", "detailed", "complex", "advanced", "multiple", "all"],
            "expert": ["optimize", "enterprise", "production", "critical", "expert", "advanced"]
        }
        
        # Dependency detection patterns
        self.dependency_patterns = {
            "sequential": ["then", "after", "next", "following", "once"],
            "conditional": ["if", "when", "unless", "provided", "assuming"],
            "parallel": ["and", "also", "simultaneously", "at the same time", "together"]
        }
    
    async def analyze_task_requirements(self, query: str) -> Dict[str, Any]:
        """
        Analyze task requirements from user query.
        
        Args:
            query: User query to analyze
            
        Returns:
            Task analysis with decomposition and requirements
        """
        try:
            logger.debug(f"Analyzing task requirements for: {query[:100]}...")
            
            # Decompose query into subtasks
            subtasks = await self._decompose_query(query)
            
            # Analyze complexity
            complexity_analysis = await self._analyze_complexity(query)
            
            # Detect dependencies
            dependencies = await self._detect_dependencies(subtasks)
            
            # Estimate execution metrics
            execution_metrics = await self._estimate_execution_metrics(subtasks, complexity_analysis)
            
            return {
                "original_query": query,
                "subtasks": subtasks,
                "complexity_analysis": complexity_analysis,
                "dependencies": dependencies,
                "execution_metrics": execution_metrics,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Task analysis failed: {e}")
            return {
                "original_query": query,
                "subtasks": [{"description": query, "agent_candidates": [AgentSpecialization.GENERAL]}],
                "complexity_analysis": {"overall_complexity": TaskComplexity.MODERATE},
                "dependencies": [],
                "execution_metrics": {"estimated_duration": 30},
                "error": str(e)
            }
    
    async def _decompose_query(self, query: str) -> List[Dict[str, Any]]:
        """Decompose complex query into individual subtasks"""
        
        subtasks = []
        
        # Split query by common separators
        separators = [" and then ", " then ", " and ", " also ", " plus ", " followed by "]
        
        parts = [query]
        for separator in separators:
            new_parts = []
            for part in parts:
                new_parts.extend(part.split(separator))
            parts = new_parts
        
        # Clean and analyze each part
        for i, part in enumerate(parts):
            part = part.strip()
            if len(part) < 5:  # Skip very short parts
                continue
            
            # Determine candidate agents for this subtask
            agent_candidates = await self._identify_agent_candidates(part)
            
            # Analyze subtask complexity
            subtask_complexity = await self._analyze_subtask_complexity(part)
            
            subtask = {
                "id": f"subtask_{i+1}",
                "description": part,
                "agent_candidates": agent_candidates,
                "complexity": subtask_complexity,
                "order": i + 1,
                "estimated_duration": await self._estimate_subtask_duration(part, subtask_complexity)
            }
            
            subtasks.append(subtask)
        
        # If no decomposition occurred, treat as single task
        if len(subtasks) == 0:
            agent_candidates = await self._identify_agent_candidates(query)
            complexity = await self._analyze_subtask_complexity(query)
            
            subtasks.append({
                "id": "subtask_1", 
                "description": query,
                "agent_candidates": agent_candidates,
                "complexity": complexity,
                "order": 1,
                "estimated_duration": await self._estimate_subtask_duration(query, complexity)
            })
        
        return subtasks
    
    async def _identify_agent_candidates(self, task_description: str) -> List[AgentSpecialization]:
        """Identify candidate agents for a task based on pattern matching"""
        
        task_lower = task_description.lower()
        candidates = []
        scores = {}
        
        # Score each agent based on pattern matches
        for agent, patterns in self.agent_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in task_lower:
                    score += 1
            
            if score > 0:
                scores[agent] = score
        
        # Sort by score and return top candidates
        if scores:
            sorted_agents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            candidates = [agent for agent, score in sorted_agents[:3]]  # Top 3
        
        # Default to general agent if no specific matches
        if not candidates:
            candidates = [AgentSpecialization.GENERAL]
        
        return candidates
    
    async def _analyze_complexity(self, query: str) -> Dict[str, Any]:
        """Analyze overall query complexity"""
        
        query_lower = query.lower()
        complexity_scores = {}
        
        # Score complexity levels
        for level, indicators in self.complexity_indicators.items():
            score = sum(1 for indicator in indicators if indicator in query_lower)
            complexity_scores[level] = score
        
        # Determine overall complexity
        if complexity_scores["expert"] > 0:
            overall_complexity = TaskComplexity.EXPERT
        elif complexity_scores["complex"] > 1:
            overall_complexity = TaskComplexity.COMPLEX
        elif complexity_scores["moderate"] > 0 or len(query.split()) > 20:
            overall_complexity = TaskComplexity.MODERATE
        else:
            overall_complexity = TaskComplexity.SIMPLE
        
        # Additional complexity factors
        factors = []
        if len(query.split()) > 30:
            factors.append("long_query")
        if "multiple" in query_lower or "several" in query_lower:
            factors.append("multiple_operations")
        if any(word in query_lower for word in ["analyze", "optimize", "comprehensive"]):
            factors.append("analytical_task")
        
        return {
            "overall_complexity": overall_complexity,
            "complexity_scores": complexity_scores,
            "complexity_factors": factors,
            "estimated_effort": self._complexity_to_effort(overall_complexity)
        }
    
    async def _analyze_subtask_complexity(self, task_description: str) -> TaskComplexity:
        """Analyze complexity of individual subtask"""
        
        task_lower = task_description.lower()
        
        # Simple heuristics for subtask complexity
        if any(word in task_lower for word in ["advanced", "complex", "optimize", "comprehensive"]):
            return TaskComplexity.EXPERT
        elif any(word in task_lower for word in ["analyze", "create", "process", "multiple"]):
            return TaskComplexity.COMPLEX
        elif any(word in task_lower for word in ["update", "modify", "check", "review"]):
            return TaskComplexity.MODERATE
        else:
            return TaskComplexity.SIMPLE
    
    async def _detect_dependencies(self, subtasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect dependencies between subtasks"""
        
        dependencies = []
        
        for i, subtask in enumerate(subtasks):
            # Check for sequential dependencies
            if i > 0:  # Not the first task
                description = subtask["description"].lower()
                prev_description = subtasks[i-1]["description"].lower()
                
                # Look for dependency keywords
                for pattern in self.dependency_patterns["sequential"]:
                    if pattern in description:
                        dependencies.append({
                            "dependent_task": subtask["id"],
                            "dependency_task": subtasks[i-1]["id"],
                            "type": "sequential",
                            "confidence": 0.8
                        })
                        break
        
        return dependencies
    
    async def _estimate_execution_metrics(self, 
                                        subtasks: List[Dict[str, Any]], 
                                        complexity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate execution metrics for the overall task"""
        
        total_duration = sum(subtask["estimated_duration"] for subtask in subtasks)
        
        # Adjust for complexity
        complexity_multiplier = {
            TaskComplexity.SIMPLE: 1.0,
            TaskComplexity.MODERATE: 1.3,
            TaskComplexity.COMPLEX: 1.8,
            TaskComplexity.EXPERT: 2.5
        }
        
        overall_complexity = complexity_analysis["overall_complexity"]
        adjusted_duration = total_duration * complexity_multiplier[overall_complexity]
        
        return {
            "estimated_duration_seconds": int(adjusted_duration),
            "estimated_subtasks": len(subtasks),
            "complexity_factor": complexity_multiplier[overall_complexity],
            "parallelizable_tasks": len([t for t in subtasks if len(t["agent_candidates"]) > 1]),
            "resource_requirements": self._estimate_resource_requirements(subtasks)
        }
    
    async def _estimate_subtask_duration(self, task_description: str, complexity: TaskComplexity) -> int:
        """Estimate duration for individual subtask"""
        
        base_durations = {
            TaskComplexity.SIMPLE: 15,
            TaskComplexity.MODERATE: 30,
            TaskComplexity.COMPLEX: 60,
            TaskComplexity.EXPERT: 120
        }
        
        base_duration = base_durations[complexity]
        
        # Adjust based on task type
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ["search", "find", "look"]):
            base_duration *= 0.8  # Search tasks are typically faster
        elif any(word in task_lower for word in ["create", "generate", "write"]):
            base_duration *= 1.2  # Creation tasks take longer
        elif any(word in task_lower for word in ["analyze", "process", "examine"]):
            base_duration *= 1.5  # Analysis tasks take longer
        
        return int(base_duration)
    
    def _complexity_to_effort(self, complexity: TaskComplexity) -> int:
        """Convert complexity to effort score (1-10)"""
        
        mapping = {
            TaskComplexity.SIMPLE: 2,
            TaskComplexity.MODERATE: 5,
            TaskComplexity.COMPLEX: 7,
            TaskComplexity.EXPERT: 9
        }
        
        return mapping[complexity]
    
    def _estimate_resource_requirements(self, subtasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate resource requirements for subtasks"""
        
        agent_usage = {}
        for subtask in subtasks:
            for candidate in subtask["agent_candidates"]:
                agent_usage[candidate.value] = agent_usage.get(candidate.value, 0) + 1
        
        return {
            "required_agents": list(agent_usage.keys()),
            "agent_usage": agent_usage,
            "max_parallel": min(len(subtasks), 3),  # Limit parallelism
            "estimated_memory_mb": len(subtasks) * 50,  # Rough estimate
            "network_intensive": any(
                agent in agent_usage for agent in ["jina_search", "firecrawl", "github", "slack"]
            )
        }


class DelegationEngine:
    """
    Intelligent delegation engine for task assignment and orchestration.
    
    Features:
    - Task decomposition and analysis
    - Agent selection with confidence scoring
    - Dependency management
    - Performance tracking and learning
    - AAI-compliant confidence scoring (70-95%)
    """
    
    def __init__(self):
        """Initialize delegation engine"""
        
        self.task_analyzer = TaskAnalyzer()
        
        # Agent profiles and capabilities
        self.agent_profiles: Dict[AgentSpecialization, AgentProfile] = {}
        
        # Performance tracking
        self.delegation_history = []
        self.agent_performance = {}
        
        # Configuration
        self.aai_min_confidence = 0.70
        self.aai_max_confidence = 0.95
        
        # Initialize agent profiles
        self._initialize_agent_profiles()
    
    def _initialize_agent_profiles(self):
        """Initialize profiles for specialized agents"""
        
        # Slack Agent Profile
        self.agent_profiles[AgentSpecialization.SLACK] = AgentProfile(
            agent_type=AgentSpecialization.SLACK,
            name="Slack Communication Agent",
            description="Handles Slack messaging, notifications, and team communication",
            capabilities=[
                AgentCapability(
                    name="send_message",
                    description="Send messages to Slack channels or users",
                    complexity_support=[TaskComplexity.SIMPLE, TaskComplexity.MODERATE],
                    confidence_baseline=0.88,
                    typical_duration_seconds=10
                ),
                AgentCapability(
                    name="manage_channels",
                    description="Create and manage Slack channels",
                    complexity_support=[TaskComplexity.MODERATE, TaskComplexity.COMPLEX],
                    confidence_baseline=0.82,
                    typical_duration_seconds=20
                )
            ],
            success_rate=0.92,
            average_response_time=1.2
        )
        
        # GitHub Agent Profile
        self.agent_profiles[AgentSpecialization.GITHUB] = AgentProfile(
            agent_type=AgentSpecialization.GITHUB,
            name="GitHub Repository Agent",
            description="Manages GitHub repositories, issues, and pull requests",
            capabilities=[
                AgentCapability(
                    name="manage_issues",
                    description="Create, update, and manage GitHub issues",
                    complexity_support=[TaskComplexity.SIMPLE, TaskComplexity.MODERATE, TaskComplexity.COMPLEX],
                    confidence_baseline=0.85,
                    typical_duration_seconds=25
                ),
                AgentCapability(
                    name="repository_operations",
                    description="Repository management operations",
                    complexity_support=[TaskComplexity.MODERATE, TaskComplexity.COMPLEX, TaskComplexity.EXPERT],
                    confidence_baseline=0.78,
                    typical_duration_seconds=45
                )
            ],
            success_rate=0.87,
            average_response_time=2.1
        )
        
        # Add profiles for other agents...
        self._add_remaining_agent_profiles()
    
    def _add_remaining_agent_profiles(self):
        """Add profiles for remaining specialized agents"""
        
        # Filesystem Agent
        self.agent_profiles[AgentSpecialization.FILESYSTEM] = AgentProfile(
            agent_type=AgentSpecialization.FILESYSTEM,
            name="Filesystem Operations Agent",
            description="Handles file and directory operations",
            capabilities=[
                AgentCapability(
                    name="file_operations",
                    description="Read, write, create, delete files",
                    complexity_support=[TaskComplexity.SIMPLE, TaskComplexity.MODERATE],
                    confidence_baseline=0.90,
                    typical_duration_seconds=15
                )
            ],
            success_rate=0.94,
            average_response_time=0.8
        )
        
        # Search Agent
        self.agent_profiles[AgentSpecialization.JINA_SEARCH] = AgentProfile(
            agent_type=AgentSpecialization.JINA_SEARCH,
            name="Web Search Agent",
            description="Performs web searches and information retrieval",
            capabilities=[
                AgentCapability(
                    name="web_search",
                    description="Search the web for information",
                    complexity_support=[TaskComplexity.SIMPLE, TaskComplexity.MODERATE, TaskComplexity.COMPLEX],
                    confidence_baseline=0.83,
                    typical_duration_seconds=20
                )
            ],
            success_rate=0.89,
            average_response_time=2.5
        )
        
        # Add other agents (Airtable, Firecrawl, Memory, Time) with similar patterns
        for agent_type in [AgentSpecialization.AIRTABLE, AgentSpecialization.FIRECRAWL, 
                          AgentSpecialization.MEMORY, AgentSpecialization.TIME]:
            self.agent_profiles[agent_type] = AgentProfile(
                agent_type=agent_type,
                name=f"{agent_type.value.title()} Agent",
                description=f"Specialized agent for {agent_type.value} operations",
                capabilities=[
                    AgentCapability(
                        name=f"{agent_type.value}_operations",
                        description=f"Core {agent_type.value} operations",
                        complexity_support=[TaskComplexity.SIMPLE, TaskComplexity.MODERATE],
                        confidence_baseline=0.80,
                        typical_duration_seconds=30
                    )
                ],
                success_rate=0.85,
                average_response_time=1.8
            )
    
    async def analyze_and_delegate(self, request: DelegationRequest) -> List[TaskDelegation]:
        """
        Analyze request and create task delegations.
        
        Args:
            request: Delegation request to process
            
        Returns:
            List of task delegations with confidence scoring
        """
        try:
            logger.info(f"Analyzing delegation request: {request.query[:100]}...")
            
            # Analyze task requirements
            task_analysis = await self.task_analyzer.analyze_task_requirements(request.query)
            
            # Create delegations for each subtask
            delegations = []
            
            for subtask in task_analysis["subtasks"]:
                # Select best agent for subtask
                selected_agent = await self._select_best_agent(
                    subtask, 
                    request.preferred_agents,
                    request.excluded_agents
                )
                
                # Calculate delegation confidence
                confidence = await self._calculate_delegation_confidence(
                    subtask, 
                    selected_agent,
                    task_analysis["complexity_analysis"]
                )
                
                # Generate reasoning
                reasoning = await self._generate_delegation_reasoning(
                    subtask, 
                    selected_agent,
                    confidence
                )
                
                # Create delegation
                delegation = TaskDelegation(
                    task_id=f"{request.session_id or 'req'}_{subtask['id']}",
                    task_description=subtask["description"],
                    assigned_agent=selected_agent,
                    confidence=confidence,
                    reasoning=reasoning,
                    estimated_complexity=self._complexity_to_int(subtask["complexity"]),
                    complexity_category=subtask["complexity"],
                    priority=request.priority,
                    estimated_duration_seconds=subtask["estimated_duration"]
                )
                
                delegations.append(delegation)
            
            # Handle dependencies
            await self._apply_dependencies(delegations, task_analysis["dependencies"])
            
            logger.info(f"Created {len(delegations)} task delegations")
            
            return delegations
            
        except Exception as e:
            logger.error(f"Delegation analysis failed: {e}")
            
            # Fallback delegation
            fallback_delegation = TaskDelegation(
                task_id=f"{request.session_id or 'req'}_fallback",
                task_description=request.query,
                assigned_agent=AgentSpecialization.GENERAL,
                confidence=self.aai_min_confidence,
                reasoning=f"Fallback delegation due to analysis error: {str(e)}",
                estimated_complexity=5
            )
            
            return [fallback_delegation]
    
    async def _select_best_agent(self, 
                               subtask: Dict[str, Any],
                               preferred_agents: List[AgentSpecialization],
                               excluded_agents: List[AgentSpecialization]) -> AgentSpecialization:
        """Select the best agent for a subtask"""
        
        candidates = subtask["agent_candidates"]
        
        # Apply preferences and exclusions
        if preferred_agents:
            preferred_candidates = [a for a in candidates if a in preferred_agents]
            if preferred_candidates:
                candidates = preferred_candidates
        
        if excluded_agents:
            candidates = [a for a in candidates if a not in excluded_agents]
        
        if not candidates:
            candidates = [AgentSpecialization.GENERAL]
        
        # Score candidates based on multiple factors
        scores = {}
        for candidate in candidates:
            score = await self._score_agent_for_task(candidate, subtask)
            scores[candidate] = score
        
        # Return highest scoring agent
        best_agent = max(scores.items(), key=lambda x: x[1])[0]
        
        return best_agent
    
    async def _score_agent_for_task(self, agent: AgentSpecialization, subtask: Dict[str, Any]) -> float:
        """Score an agent's suitability for a specific task"""
        
        score = 0.0
        
        # Base score from agent profile
        if agent in self.agent_profiles:
            profile = self.agent_profiles[agent]
            score += profile.success_rate * 0.4
            
            # Response time factor (faster is better)
            time_score = max(0, (5.0 - profile.average_response_time) / 5.0)
            score += time_score * 0.2
            
            # Capability match
            task_complexity = subtask["complexity"]
            for capability in profile.capabilities:
                if task_complexity in capability.complexity_support:
                    score += capability.confidence_baseline * 0.3
                    break
        else:
            score = 0.5  # Default score for unknown agents
        
        # Historical performance
        if agent in self.agent_performance:
            historical_score = self.agent_performance[agent].get("success_rate", 0.8)
            score += historical_score * 0.1
        
        return min(1.0, score)
    
    async def _calculate_delegation_confidence(self, 
                                             subtask: Dict[str, Any],
                                             selected_agent: AgentSpecialization,
                                             complexity_analysis: Dict[str, Any]) -> float:
        """Calculate AAI-compliant confidence for delegation"""
        
        # Base confidence from agent capability
        base_confidence = 0.75
        
        if selected_agent in self.agent_profiles:
            profile = self.agent_profiles[selected_agent]
            
            # Find matching capability
            task_complexity = subtask["complexity"]
            for capability in profile.capabilities:
                if task_complexity in capability.complexity_support:
                    base_confidence = capability.confidence_baseline
                    break
        
        # Adjust for task complexity
        complexity_adjustments = {
            TaskComplexity.SIMPLE: 0.05,
            TaskComplexity.MODERATE: 0.0,
            TaskComplexity.COMPLEX: -0.03,
            TaskComplexity.EXPERT: -0.07
        }
        
        task_complexity = subtask["complexity"]
        base_confidence += complexity_adjustments.get(task_complexity, 0.0)
        
        # Adjust for agent performance history
        if selected_agent in self.agent_performance:
            historical_performance = self.agent_performance[selected_agent].get("success_rate", 0.8)
            performance_adjustment = (historical_performance - 0.8) * 0.1
            base_confidence += performance_adjustment
        
        # Adjust for overall task complexity
        overall_complexity = complexity_analysis["overall_complexity"]
        if overall_complexity == TaskComplexity.EXPERT:
            base_confidence -= 0.05
        elif overall_complexity == TaskComplexity.SIMPLE:
            base_confidence += 0.03
        
        # Ensure AAI compliance
        final_confidence = max(self.aai_min_confidence, min(self.aai_max_confidence, base_confidence))
        
        return final_confidence
    
    async def _generate_delegation_reasoning(self, 
                                           subtask: Dict[str, Any],
                                           selected_agent: AgentSpecialization,
                                           confidence: float) -> str:
        """Generate human-readable reasoning for delegation decision"""
        
        reasoning_parts = []
        
        # Agent selection reasoning
        reasoning_parts.append(f"Selected {selected_agent.value} agent")
        
        # Capability match reasoning
        if selected_agent in self.agent_profiles:
            profile = self.agent_profiles[selected_agent]
            reasoning_parts.append(f"based on specialized capabilities for {profile.description.lower()}")
        
        # Complexity reasoning
        task_complexity = subtask["complexity"]
        reasoning_parts.append(f"with {task_complexity.value} complexity support")
        
        # Confidence reasoning
        if confidence >= 0.85:
            reasoning_parts.append("with high confidence")
        elif confidence >= 0.75:
            reasoning_parts.append("with moderate confidence")
        else:
            reasoning_parts.append("with basic confidence")
        
        # Performance reasoning
        if selected_agent in self.agent_performance:
            historical_rate = self.agent_performance[selected_agent].get("success_rate", 0.8)
            if historical_rate >= 0.9:
                reasoning_parts.append("and excellent historical performance")
            elif historical_rate >= 0.8:
                reasoning_parts.append("and good historical performance")
        
        return " ".join(reasoning_parts) + "."
    
    async def _apply_dependencies(self, 
                                delegations: List[TaskDelegation],
                                dependencies: List[Dict[str, Any]]):
        """Apply dependency relationships to delegations"""
        
        # Create dependency mapping
        delegation_map = {d.task_id: d for d in delegations}
        
        for dependency in dependencies:
            dependent_id = dependency["dependent_task"]
            dependency_id = dependency["dependency_task"]
            
            # Find corresponding delegations and update
            for delegation in delegations:
                if delegation.task_id.endswith(dependent_id):
                    if dependency_id not in delegation.dependencies:
                        delegation.dependencies.append(dependency_id)
    
    def _complexity_to_int(self, complexity: TaskComplexity) -> int:
        """Convert complexity enum to integer scale"""
        
        mapping = {
            TaskComplexity.SIMPLE: 2,
            TaskComplexity.MODERATE: 5,
            TaskComplexity.COMPLEX: 7,
            TaskComplexity.EXPERT: 9
        }
        
        return mapping[complexity]
    
    async def update_agent_performance(self, 
                                     agent: AgentSpecialization,
                                     success: bool,
                                     execution_time: float,
                                     user_satisfaction: float):
        """Update agent performance metrics based on execution results"""
        
        if agent not in self.agent_performance:
            self.agent_performance[agent] = {
                "total_tasks": 0,
                "successful_tasks": 0,
                "total_time": 0.0,
                "satisfaction_scores": []
            }
        
        metrics = self.agent_performance[agent]
        metrics["total_tasks"] += 1
        
        if success:
            metrics["successful_tasks"] += 1
        
        metrics["total_time"] += execution_time
        metrics["satisfaction_scores"].append(user_satisfaction)
        
        # Keep only recent satisfaction scores
        if len(metrics["satisfaction_scores"]) > 20:
            metrics["satisfaction_scores"] = metrics["satisfaction_scores"][-20:]
        
        # Update derived metrics
        metrics["success_rate"] = metrics["successful_tasks"] / metrics["total_tasks"]
        metrics["average_time"] = metrics["total_time"] / metrics["total_tasks"]
        metrics["average_satisfaction"] = sum(metrics["satisfaction_scores"]) / len(metrics["satisfaction_scores"])
    
    def get_delegation_statistics(self) -> Dict[str, Any]:
        """Get delegation engine statistics"""
        
        return {
            "total_delegations": len(self.delegation_history),
            "agent_profiles": len(self.agent_profiles),
            "tracked_agents": len(self.agent_performance),
            "agent_performance": {
                agent.value: {
                    "success_rate": metrics.get("success_rate", 0.0),
                    "average_time": metrics.get("average_time", 0.0),
                    "total_tasks": metrics.get("total_tasks", 0)
                }
                for agent, metrics in self.agent_performance.items()
            },
            "confidence_range": f"{self.aai_min_confidence:.0%}-{self.aai_max_confidence:.0%}",
            "ready": True
        }


async def test_delegation_engine():
    """Test delegation engine functionality"""
    
    engine = DelegationEngine()
    
    print("🧪 Testing Delegation Engine")
    print("=" * 28)
    
    # Check engine statistics
    stats = engine.get_delegation_statistics()
    print(f"Agent profiles: {stats['agent_profiles']}")
    print(f"Confidence range: {stats['confidence_range']}")
    print(f"Ready: {stats['ready']}")
    
    # Test delegation analysis
    print(f"\n🎯 Testing delegation analysis...")
    
    request = DelegationRequest(
        query="Send a Slack message to the team about the new release and then create a GitHub issue to track feedback",
        user_id="test_user",
        session_id="test_session",
        max_parallel_tasks=2
    )
    
    delegations = await engine.analyze_and_delegate(request)
    
    print(f"Created delegations: {len(delegations)}")
    
    for i, delegation in enumerate(delegations, 1):
        print(f"\nDelegation {i}:")
        print(f"  Agent: {delegation.assigned_agent.value}")
        print(f"  Task: {delegation.task_description[:50]}...")
        print(f"  Confidence: {delegation.confidence:.1%}")
        print(f"  Complexity: {delegation.complexity_category.value}")
        print(f"  Reasoning: {delegation.reasoning}")
    
    # Test agent performance update
    print(f"\n📊 Testing performance tracking...")
    
    await engine.update_agent_performance(
        AgentSpecialization.SLACK, 
        success=True, 
        execution_time=15.0, 
        user_satisfaction=0.9
    )
    
    updated_stats = engine.get_delegation_statistics()
    slack_performance = updated_stats["agent_performance"].get("slack", {})
    print(f"Slack agent performance: {slack_performance.get('success_rate', 0):.1%} success rate")
    
    print(f"\n✅ Delegation Engine Testing Complete")
    print(f"Intelligent task delegation with AAI compliance working")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_delegation_engine())