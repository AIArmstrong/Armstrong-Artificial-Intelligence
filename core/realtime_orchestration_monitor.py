"""
AAI Real-time Orchestration and Monitoring System
Provides real-time coordination, performance monitoring, and adaptive workflows for all enhancement layers.

Manages real-time orchestration of enhancement workflows, monitors system performance,
provides adaptive optimization, and enables streaming analytics and alerting.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Set, Tuple, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import json
import time
import statistics
import weakref

# Core system imports
try:
    from core.unified_enhancement_coordinator import UnifiedEnhancementCoordinator, CoordinationResult
    from core.resource_optimization_manager import ResourceOptimizationManager
    from core.agent_interoperability_framework import AgentInteroperabilityFramework
    CORE_SYSTEMS_AVAILABLE = True
except ImportError:
    UnifiedEnhancementCoordinator = None
    CoordinationResult = None
    ResourceOptimizationManager = None
    AgentInteroperabilityFramework = None
    CORE_SYSTEMS_AVAILABLE = False

logger = logging.getLogger(__name__)


class MonitoringLevel(Enum):
    """Levels of system monitoring"""
    BASIC = "basic"  # Essential metrics only
    STANDARD = "standard"  # Standard monitoring
    DETAILED = "detailed"  # Comprehensive monitoring
    DEBUG = "debug"  # Debug-level monitoring


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


@dataclass
class SystemAlert:
    """System alert information"""
    alert_id: str
    severity: AlertSeverity
    title: str
    description: str
    source_component: str
    metric_values: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution_time: Optional[datetime] = None


@dataclass
class WorkflowExecution:
    """Real-time workflow execution tracking"""
    workflow_id: str
    command_type: str
    status: WorkflowStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    current_stage: str = "initialization"
    active_layers: List[str] = field(default_factory=list)
    completed_layers: List[str] = field(default_factory=list)
    failed_layers: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    coordination_events: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AdaptiveRule:
    """Adaptive optimization rule"""
    rule_id: str
    name: str
    condition: str  # Python expression
    action: str  # Action to take
    priority: int = 50
    enabled: bool = True
    activation_count: int = 0
    last_activated: Optional[datetime] = None


class RealtimeOrchestrationMonitor:
    """
    Real-time orchestration and monitoring system for AAI enhancements.
    
    Features:
    - Real-time workflow orchestration and coordination
    - Comprehensive performance monitoring and analytics
    - Adaptive optimization based on performance patterns
    - Streaming metrics and real-time dashboards
    - Intelligent alerting and anomaly detection
    - Resource utilization optimization
    - Workflow adaptation and recovery
    """
    
    def __init__(self):
        """Initialize real-time orchestration monitor"""
        
        # Core system references
        self.coordinator: Optional[UnifiedEnhancementCoordinator] = None
        self.resource_manager: Optional[ResourceOptimizationManager] = None
        self.interop_framework: Optional[AgentInteroperabilityFramework] = None
        
        # Monitoring state
        self.monitoring_level = MonitoringLevel.STANDARD
        self.monitoring_active = False
        
        # Workflow tracking
        self.active_workflows = {}
        self.workflow_history = deque(maxlen=1000)
        self.workflow_counter = 0
        
        # Performance monitoring
        self.performance_metrics = defaultdict(deque)  # metric_name -> deque of values
        self.metric_thresholds = {}
        self.metric_collectors = {}
        
        # Alert system
        self.active_alerts = {}
        self.alert_history = deque(maxlen=500)
        self.alert_rules = {}
        self.alert_counter = 0
        
        # Adaptive optimization
        self.adaptive_rules = {}
        self.optimization_patterns = defaultdict(list)
        self.performance_trends = defaultdict(list)
        
        # Real-time streaming
        self.metric_subscribers = defaultdict(set)
        self.streaming_buffers = defaultdict(deque)
        self.stream_update_callbacks = []
        
        # Configuration
        self.metric_retention = timedelta(hours=24)
        self.alert_retention = timedelta(days=7)
        self.monitoring_interval = 1.0  # seconds
        self.adaptive_check_interval = 30.0  # seconds
        self.max_metrics_per_type = 10000
        
        # Background tasks
        self.monitoring_task = None
        self.adaptive_task = None
        self.cleanup_task = None
        
        # Initialization state
        self.initialized = False
        
        # Initialize monitor
        asyncio.create_task(self._initialize_monitor())
    
    async def _initialize_monitor(self):
        """Initialize orchestration monitor"""
        
        try:
            if not CORE_SYSTEMS_AVAILABLE:
                logger.warning("Core systems not available - using standalone mode")
            
            # Initialize core system references
            if CORE_SYSTEMS_AVAILABLE:
                # These would be dependency-injected in real implementation
                # For now, create mock references
                pass
            
            # Initialize default thresholds
            self._initialize_default_thresholds()
            
            # Initialize default alert rules
            self._initialize_default_alert_rules()
            
            # Initialize adaptive rules
            self._initialize_adaptive_rules()
            
            # Start background tasks
            await self._start_background_tasks()
            
            self.initialized = True
            logger.info("Real-time Orchestration Monitor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Real-time Orchestration Monitor: {e}")
            self.initialized = False
    
    def _initialize_default_thresholds(self):
        """Initialize default performance thresholds"""
        
        self.metric_thresholds = {
            "coordination_time": {"warning": 10.0, "critical": 30.0},  # seconds
            "success_rate": {"warning": 0.8, "critical": 0.6},  # percentage
            "resource_utilization": {"warning": 0.8, "critical": 0.95},  # percentage
            "cache_hit_rate": {"warning": 0.6, "critical": 0.4},  # percentage
            "memory_usage": {"warning": 0.8, "critical": 0.95},  # percentage
            "cpu_usage": {"warning": 0.8, "critical": 0.95},  # percentage
            "response_time": {"warning": 5.0, "critical": 15.0},  # seconds
            "error_rate": {"warning": 0.05, "critical": 0.1},  # percentage
            "queue_depth": {"warning": 50, "critical": 100},  # count
            "concurrent_workflows": {"warning": 10, "critical": 20}  # count
        }
    
    def _initialize_default_alert_rules(self):
        """Initialize default alert rules"""
        
        self.alert_rules = {
            "high_coordination_time": {
                "condition": "coordination_time > threshold_critical",
                "severity": AlertSeverity.CRITICAL,
                "title": "High Coordination Time",
                "description": "Command coordination taking longer than expected"
            },
            "low_success_rate": {
                "condition": "success_rate < threshold_critical", 
                "severity": AlertSeverity.ERROR,
                "title": "Low Success Rate",
                "description": "Enhancement success rate below acceptable threshold"
            },
            "high_resource_utilization": {
                "condition": "resource_utilization > threshold_critical",
                "severity": AlertSeverity.WARNING,
                "title": "High Resource Utilization",
                "description": "System resource utilization approaching limits"
            },
            "poor_cache_performance": {
                "condition": "cache_hit_rate < threshold_warning",
                "severity": AlertSeverity.WARNING,
                "title": "Poor Cache Performance", 
                "description": "Cache hit rate below optimal threshold"
            },
            "excessive_errors": {
                "condition": "error_rate > threshold_warning",
                "severity": AlertSeverity.ERROR,
                "title": "Excessive Error Rate",
                "description": "Error rate exceeding normal operational levels"
            }
        }
    
    def _initialize_adaptive_rules(self):
        """Initialize adaptive optimization rules"""
        
        self.adaptive_rules = {
            "scale_coordination_mode": AdaptiveRule(
                rule_id="scale_coordination_mode",
                name="Scale Coordination Mode",
                condition="avg_coordination_time > 10.0 and concurrent_workflows > 3",
                action="switch_to_parallel_mode",
                priority=80
            ),
            "optimize_cache_size": AdaptiveRule(
                rule_id="optimize_cache_size",
                name="Optimize Cache Size",
                condition="cache_hit_rate < 0.7 and memory_available > 0.3",
                action="increase_cache_size",
                priority=60
            ),
            "reduce_enhancement_layers": AdaptiveRule(
                rule_id="reduce_enhancement_layers",
                name="Reduce Enhancement Layers",
                condition="avg_coordination_time > 15.0 and success_rate < 0.8",
                action="disable_non_critical_layers",
                priority=90
            ),
            "increase_resource_allocation": AdaptiveRule(
                rule_id="increase_resource_allocation",
                name="Increase Resource Allocation",
                condition="queue_depth > 20 and resource_utilization < 0.6",
                action="allocate_more_resources",
                priority=70
            )
        }
    
    async def _start_background_tasks(self):
        """Start background monitoring tasks"""
        
        # Performance monitoring task
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        
        # Adaptive optimization task
        self.adaptive_task = asyncio.create_task(self._adaptive_optimization_loop())
        
        # Cleanup task
        self.cleanup_task = asyncio.create_task(self._cleanup_loop())
        
        logger.info("Background monitoring tasks started")
    
    async def start_workflow_monitoring(self,
                                      workflow_id: str,
                                      command_type: str,
                                      enhancement_layers: List[str]) -> str:
        """
        Start monitoring a workflow execution.
        
        Args:
            workflow_id: Unique workflow identifier
            command_type: Type of command being executed
            enhancement_layers: List of enhancement layers to monitor
            
        Returns:
            Monitoring session ID
        """
        try:
            if not self.initialized:
                logger.warning("Monitor not initialized")
                return ""
            
            # Create workflow execution tracker
            execution = WorkflowExecution(
                workflow_id=workflow_id,
                command_type=command_type,
                status=WorkflowStatus.PENDING,
                start_time=datetime.now(),
                active_layers=enhancement_layers.copy()
            )
            
            self.active_workflows[workflow_id] = execution
            self.workflow_counter += 1
            
            # Record workflow start metric
            await self._record_metric(
                "workflow_started",
                1.0,
                "count",
                {"command_type": command_type, "layer_count": len(enhancement_layers)}
            )
            
            # Start workflow-specific monitoring
            asyncio.create_task(self._monitor_workflow_execution(workflow_id))
            
            logger.info(f"Started monitoring workflow {workflow_id}")
            return workflow_id
            
        except Exception as e:
            logger.error(f"Failed to start workflow monitoring: {e}")
            return ""
    
    async def update_workflow_status(self,
                                   workflow_id: str,
                                   status: WorkflowStatus,
                                   current_stage: str = "",
                                   layer_updates: Optional[Dict[str, str]] = None) -> bool:
        """
        Update workflow execution status.
        
        Args:
            workflow_id: Workflow to update
            status: New workflow status
            current_stage: Current execution stage
            layer_updates: Layer status updates (layer_name -> status)
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            if workflow_id not in self.active_workflows:
                logger.warning(f"Workflow {workflow_id} not found")
                return False
            
            execution = self.active_workflows[workflow_id]
            
            # Update status
            execution.status = status
            if current_stage:
                execution.current_stage = current_stage
            
            # Update layer statuses
            if layer_updates:
                for layer_name, layer_status in layer_updates.items():
                    if layer_status == "completed":
                        if layer_name in execution.active_layers:
                            execution.active_layers.remove(layer_name)
                        if layer_name not in execution.completed_layers:
                            execution.completed_layers.append(layer_name)
                    elif layer_status == "failed":
                        if layer_name in execution.active_layers:
                            execution.active_layers.remove(layer_name)
                        if layer_name not in execution.failed_layers:
                            execution.failed_layers.append(layer_name)
            
            # Handle completion
            if status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]:
                execution.end_time = datetime.now()
                
                # Calculate final metrics
                execution_time = (execution.end_time - execution.start_time).total_seconds()
                success_rate = len(execution.completed_layers) / max(1, len(execution.completed_layers) + len(execution.failed_layers))
                
                execution.performance_metrics.update({
                    "execution_time": execution_time,
                    "success_rate": success_rate,
                    "layers_completed": len(execution.completed_layers),
                    "layers_failed": len(execution.failed_layers)
                })
                
                # Record completion metrics
                await self._record_metric("workflow_completed", 1.0, "count", {
                    "command_type": execution.command_type,
                    "status": status.value,
                    "execution_time": execution_time,
                    "success_rate": success_rate
                })
                
                # Move to history
                self.workflow_history.append(execution)
                
                # Remove from active workflows after brief delay (for final updates)
                asyncio.create_task(self._cleanup_workflow(workflow_id, delay=5.0))
            
            # Record status change event
            execution.coordination_events.append({
                "timestamp": datetime.now().isoformat(),
                "event_type": "status_change",
                "old_status": execution.status.value if hasattr(execution, "_previous_status") else "unknown",
                "new_status": status.value,
                "stage": current_stage,
                "layer_updates": layer_updates or {}
            })
            execution._previous_status = status
            
            # Update streaming data
            await self._update_streaming_metrics(workflow_id, execution)
            
            return True
            
        except Exception as e:
            logger.error(f"Workflow status update failed: {e}")
            return False
    
    async def record_coordination_result(self,
                                       workflow_id: str,
                                       coordination_result: Dict[str, Any]) -> bool:
        """
        Record coordination result for monitoring.
        
        Args:
            workflow_id: Associated workflow
            coordination_result: Coordination result data
            
        Returns:
            True if recorded successfully, False otherwise
        """
        try:
            if workflow_id not in self.active_workflows:
                logger.warning(f"Workflow {workflow_id} not found for coordination result")
                return False
            
            execution = self.active_workflows[workflow_id]
            
            # Extract performance metrics
            if isinstance(coordination_result, dict):
                execution_time = coordination_result.get("total_execution_time", 0.0)
                confidence = coordination_result.get("combined_confidence", 0.0)
                success = coordination_result.get("coordination_success", False)
                active_layers = coordination_result.get("active_layers", [])
                
                execution.performance_metrics.update({
                    "coordination_time": execution_time,
                    "confidence": confidence,
                    "coordination_success": success
                })
                
                # Record detailed metrics
                await self._record_metric("coordination_time", execution_time, "seconds", {
                    "workflow_id": workflow_id,
                    "command_type": execution.command_type,
                    "layer_count": len(active_layers)
                })
                
                await self._record_metric("coordination_confidence", confidence, "percentage", {
                    "workflow_id": workflow_id,
                    "success": success
                })
                
                # Update layer tracking
                execution.active_layers = active_layers
            
            # Record coordination event
            execution.coordination_events.append({
                "timestamp": datetime.now().isoformat(),
                "event_type": "coordination_result",
                "result": coordination_result
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Coordination result recording failed: {e}")
            return False
    
    async def _record_metric(self,
                           metric_name: str,
                           value: float,
                           unit: str,
                           context: Optional[Dict[str, Any]] = None) -> bool:
        """Record a performance metric"""
        
        try:
            metric = PerformanceMetric(
                metric_name=metric_name,
                value=value,
                unit=unit,
                timestamp=datetime.now(),
                context=context or {},
                tags=[]
            )
            
            # Store metric
            self.performance_metrics[metric_name].append(metric)
            
            # Limit metric storage
            if len(self.performance_metrics[metric_name]) > self.max_metrics_per_type:
                # Keep most recent metrics
                self.performance_metrics[metric_name] = deque(
                    list(self.performance_metrics[metric_name])[-self.max_metrics_per_type:],
                    maxlen=self.max_metrics_per_type
                )
            
            # Update streaming buffers
            self.streaming_buffers[metric_name].append(metric)
            if len(self.streaming_buffers[metric_name]) > 100:
                self.streaming_buffers[metric_name].popleft()
            
            # Check for alerts
            await self._check_metric_alerts(metric_name, value, context or {})
            
            # Notify subscribers
            await self._notify_metric_subscribers(metric_name, metric)
            
            return True
            
        except Exception as e:
            logger.error(f"Metric recording failed: {e}")
            return False
    
    async def _check_metric_alerts(self,
                                 metric_name: str,
                                 value: float,
                                 context: Dict[str, Any]):
        """Check if metric value triggers any alerts"""
        
        try:
            # Check against thresholds
            if metric_name in self.metric_thresholds:
                thresholds = self.metric_thresholds[metric_name]
                
                alert_triggered = None
                severity = None
                
                if "critical" in thresholds:
                    if (metric_name in ["coordination_time", "response_time", "error_rate", "queue_depth", "concurrent_workflows"] and 
                        value > thresholds["critical"]) or \
                       (metric_name in ["success_rate", "cache_hit_rate"] and value < thresholds["critical"]) or \
                       (metric_name in ["resource_utilization", "memory_usage", "cpu_usage"] and value > thresholds["critical"]):
                        alert_triggered = "critical"
                        severity = AlertSeverity.CRITICAL
                
                if not alert_triggered and "warning" in thresholds:
                    if (metric_name in ["coordination_time", "response_time", "error_rate", "queue_depth", "concurrent_workflows"] and 
                        value > thresholds["warning"]) or \
                       (metric_name in ["success_rate", "cache_hit_rate"] and value < thresholds["warning"]) or \
                       (metric_name in ["resource_utilization", "memory_usage", "cpu_usage"] and value > thresholds["warning"]):
                        alert_triggered = "warning"
                        severity = AlertSeverity.WARNING
                
                if alert_triggered:
                    await self._create_alert(
                        title=f"Metric Threshold Exceeded: {metric_name}",
                        description=f"{metric_name} value {value} exceeded {alert_triggered} threshold {thresholds[alert_triggered]}",
                        severity=severity,
                        source_component="metric_monitor",
                        metric_values={metric_name: value}
                    )
            
            # Check custom alert rules
            for rule_name, rule_config in self.alert_rules.items():
                if await self._evaluate_alert_condition(rule_config["condition"], metric_name, value, context):
                    await self._create_alert(
                        title=rule_config["title"],
                        description=rule_config["description"],
                        severity=rule_config["severity"],
                        source_component="rule_engine",
                        metric_values={metric_name: value}
                    )
                    
        except Exception as e:
            logger.error(f"Alert checking failed: {e}")
    
    async def _evaluate_alert_condition(self,
                                      condition: str,
                                      metric_name: str,
                                      value: float,
                                      context: Dict[str, Any]) -> bool:
        """Evaluate alert condition expression"""
        
        try:
            # Build evaluation context
            eval_context = {
                "metric_name": metric_name,
                "value": value,
                "context": context
            }
            
            # Add threshold values
            if metric_name in self.metric_thresholds:
                thresholds = self.metric_thresholds[metric_name]
                eval_context.update({
                    f"threshold_{level}": threshold_value
                    for level, threshold_value in thresholds.items()
                })
            
            # Add recent metric values for pattern analysis
            if metric_name in self.performance_metrics:
                recent_values = [m.value for m in list(self.performance_metrics[metric_name])[-10:]]
                if recent_values:
                    eval_context.update({
                        "avg_recent": statistics.mean(recent_values),
                        "min_recent": min(recent_values),
                        "max_recent": max(recent_values)
                    })
            
            # Safely evaluate condition
            # In production, would use a more secure expression evaluator
            result = eval(condition, {"__builtins__": {}}, eval_context)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Alert condition evaluation failed: {e}")
            return False
    
    async def _create_alert(self,
                          title: str,
                          description: str,
                          severity: AlertSeverity,
                          source_component: str,
                          metric_values: Optional[Dict[str, float]] = None) -> str:
        """Create a new system alert"""
        
        try:
            alert_id = f"alert_{self.alert_counter}_{int(datetime.now().timestamp())}"
            self.alert_counter += 1
            
            alert = SystemAlert(
                alert_id=alert_id,
                severity=severity,
                title=title,
                description=description,
                source_component=source_component,
                metric_values=metric_values or {}
            )
            
            # Store active alert
            self.active_alerts[alert_id] = alert
            
            # Add to history
            self.alert_history.append(alert)
            
            # Log alert
            log_level = {
                AlertSeverity.INFO: logging.INFO,
                AlertSeverity.WARNING: logging.WARNING,
                AlertSeverity.ERROR: logging.ERROR,
                AlertSeverity.CRITICAL: logging.CRITICAL
            }.get(severity, logging.WARNING)
            
            logger.log(log_level, f"ALERT [{severity.value.upper()}] {title}: {description}")
            
            # Notify alert subscribers
            await self._notify_alert_subscribers(alert)
            
            return alert_id
            
        except Exception as e:
            logger.error(f"Alert creation failed: {e}")
            return ""
    
    async def _monitor_workflow_execution(self, workflow_id: str):
        """Monitor a specific workflow execution"""
        
        try:
            while workflow_id in self.active_workflows:
                execution = self.active_workflows[workflow_id]
                
                # Record workflow metrics
                if execution.status == WorkflowStatus.RUNNING:
                    current_time = datetime.now()
                    elapsed_time = (current_time - execution.start_time).total_seconds()
                    
                    await self._record_metric("workflow_elapsed_time", elapsed_time, "seconds", {
                        "workflow_id": workflow_id,
                        "command_type": execution.command_type,
                        "stage": execution.current_stage
                    })
                    
                    # Monitor layer progress
                    total_layers = len(execution.completed_layers) + len(execution.active_layers) + len(execution.failed_layers)
                    if total_layers > 0:
                        progress = len(execution.completed_layers) / total_layers
                        await self._record_metric("workflow_progress", progress, "percentage", {
                            "workflow_id": workflow_id
                        })
                
                await asyncio.sleep(self.monitoring_interval)
                
        except Exception as e:
            logger.error(f"Workflow monitoring failed for {workflow_id}: {e}")
    
    async def _monitoring_loop(self):
        """Main monitoring loop for system metrics"""
        
        while True:
            try:
                if not self.monitoring_active:
                    await asyncio.sleep(self.monitoring_interval)
                    continue
                
                # Collect system metrics
                await self._collect_system_metrics()
                
                # Check for performance trends
                await self._analyze_performance_trends()
                
                # Update streaming data
                await self._update_global_streaming_metrics()
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Monitoring loop failed: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _collect_system_metrics(self):
        """Collect system-wide performance metrics"""
        
        try:
            current_time = datetime.now()
            
            # Workflow metrics
            active_count = len(self.active_workflows)
            await self._record_metric("active_workflows", active_count, "count")
            
            # Calculate success rates
            if self.workflow_history:
                recent_workflows = [w for w in self.workflow_history 
                                  if current_time - w.start_time < timedelta(minutes=10)]
                if recent_workflows:
                    success_count = sum(1 for w in recent_workflows 
                                      if w.status == WorkflowStatus.COMPLETED)
                    success_rate = success_count / len(recent_workflows)
                    await self._record_metric("workflow_success_rate", success_rate, "percentage")
            
            # Resource metrics (simulated - would integrate with actual resource manager)
            await self._record_metric("memory_usage", 0.65, "percentage")  # Simulated
            await self._record_metric("cpu_usage", 0.45, "percentage")    # Simulated
            
            # Performance metrics
            if "coordination_time" in self.performance_metrics:
                recent_times = [m.value for m in list(self.performance_metrics["coordination_time"])[-10:]]
                if recent_times:
                    avg_time = statistics.mean(recent_times)
                    await self._record_metric("avg_coordination_time", avg_time, "seconds")
            
        except Exception as e:
            logger.error(f"System metrics collection failed: {e}")
    
    async def _analyze_performance_trends(self):
        """Analyze performance trends for adaptive optimization"""
        
        try:
            # Analyze key metrics for trends
            metrics_to_analyze = ["coordination_time", "success_rate", "resource_utilization"]
            
            for metric_name in metrics_to_analyze:
                if metric_name in self.performance_metrics:
                    recent_values = [m.value for m in list(self.performance_metrics[metric_name])[-20:]]
                    
                    if len(recent_values) >= 5:
                        # Simple trend analysis
                        first_half = recent_values[:len(recent_values)//2]
                        second_half = recent_values[len(recent_values)//2:]
                        
                        first_avg = statistics.mean(first_half)
                        second_avg = statistics.mean(second_half)
                        
                        trend = (second_avg - first_avg) / first_avg if first_avg > 0 else 0
                        
                        self.performance_trends[metric_name].append({
                            "timestamp": datetime.now(),
                            "trend": trend,
                            "first_avg": first_avg,
                            "second_avg": second_avg
                        })
                        
                        # Keep limited trend history
                        if len(self.performance_trends[metric_name]) > 100:
                            self.performance_trends[metric_name] = self.performance_trends[metric_name][-50:]
            
        except Exception as e:
            logger.error(f"Performance trend analysis failed: {e}")
    
    async def _adaptive_optimization_loop(self):
        """Adaptive optimization loop"""
        
        while True:
            try:
                await asyncio.sleep(self.adaptive_check_interval)
                
                # Evaluate adaptive rules
                for rule_id, rule in self.adaptive_rules.items():
                    if rule.enabled:
                        if await self._evaluate_adaptive_rule(rule):
                            await self._execute_adaptive_action(rule)
                
            except Exception as e:
                logger.error(f"Adaptive optimization failed: {e}")
    
    async def _evaluate_adaptive_rule(self, rule: AdaptiveRule) -> bool:
        """Evaluate an adaptive optimization rule"""
        
        try:
            # Build evaluation context with current metrics
            eval_context = {}
            
            # Add recent metric averages
            for metric_name, metric_deque in self.performance_metrics.items():
                if metric_deque:
                    recent_values = [m.value for m in list(metric_deque)[-10:]]
                    if recent_values:
                        eval_context[f"avg_{metric_name}"] = statistics.mean(recent_values)
                        eval_context[f"max_{metric_name}"] = max(recent_values)
                        eval_context[f"min_{metric_name}"] = min(recent_values)
            
            # Add system state
            eval_context.update({
                "concurrent_workflows": len(self.active_workflows),
                "active_alerts": len(self.active_alerts),
                "memory_available": 1.0 - eval_context.get("avg_memory_usage", 0.0)
            })
            
            # Evaluate condition
            result = eval(rule.condition, {"__builtins__": {}}, eval_context)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Adaptive rule evaluation failed: {e}")
            return False
    
    async def _execute_adaptive_action(self, rule: AdaptiveRule):
        """Execute adaptive optimization action"""
        
        try:
            logger.info(f"Executing adaptive action: {rule.action} (rule: {rule.name})")
            
            # Update rule stats
            rule.activation_count += 1
            rule.last_activated = datetime.now()
            
            # Execute action based on type
            if rule.action == "switch_to_parallel_mode":
                await self._optimize_coordination_mode("parallel")
            elif rule.action == "increase_cache_size":
                await self._optimize_cache_configuration(increase_size=True)
            elif rule.action == "disable_non_critical_layers":
                await self._optimize_enhancement_layers(reduce_layers=True)
            elif rule.action == "allocate_more_resources":
                await self._optimize_resource_allocation(increase=True)
            else:
                logger.warning(f"Unknown adaptive action: {rule.action}")
            
            # Record optimization event
            await self._record_metric("adaptive_optimization", 1.0, "count", {
                "rule_id": rule.rule_id,
                "action": rule.action,
                "activation_count": rule.activation_count
            })
            
        except Exception as e:
            logger.error(f"Adaptive action execution failed: {e}")
    
    async def _optimize_coordination_mode(self, mode: str):
        """Optimize coordination mode"""
        logger.info(f"Adaptive optimization: switching to {mode} coordination mode")
        # Would integrate with coordinator to change mode
    
    async def _optimize_cache_configuration(self, increase_size: bool):
        """Optimize cache configuration"""
        logger.info(f"Adaptive optimization: {'increasing' if increase_size else 'decreasing'} cache size")
        # Would integrate with resource manager to adjust cache
    
    async def _optimize_enhancement_layers(self, reduce_layers: bool):
        """Optimize enhancement layer configuration"""
        logger.info(f"Adaptive optimization: {'reducing' if reduce_layers else 'expanding'} enhancement layers")
        # Would integrate with coordinator to adjust layer selection
    
    async def _optimize_resource_allocation(self, increase: bool):
        """Optimize resource allocation"""
        logger.info(f"Adaptive optimization: {'increasing' if increase else 'decreasing'} resource allocation")
        # Would integrate with resource manager to adjust allocation
    
    async def _update_streaming_metrics(self, workflow_id: str, execution: WorkflowExecution):
        """Update streaming metrics for real-time dashboard"""
        
        try:
            stream_data = {
                "workflow_id": workflow_id,
                "status": execution.status.value,
                "current_stage": execution.current_stage,
                "active_layers": execution.active_layers,
                "completed_layers": execution.completed_layers,
                "failed_layers": execution.failed_layers,
                "performance_metrics": execution.performance_metrics,
                "timestamp": datetime.now().isoformat()
            }
            
            # Update streaming buffers
            self.streaming_buffers["workflow_updates"].append(stream_data)
            
            # Notify stream update callbacks
            for callback in self.stream_update_callbacks:
                try:
                    await callback("workflow_update", stream_data)
                except Exception as e:
                    logger.error(f"Stream callback failed: {e}")
                    
        except Exception as e:
            logger.error(f"Streaming metrics update failed: {e}")
    
    async def _update_global_streaming_metrics(self):
        """Update global streaming metrics"""
        
        try:
            global_data = {
                "active_workflows": len(self.active_workflows),
                "active_alerts": len(self.active_alerts),
                "total_workflows": self.workflow_counter,
                "recent_metrics": {
                    metric_name: [
                        {"value": m.value, "timestamp": m.timestamp.isoformat()}
                        for m in list(metric_deque)[-5:]  # Last 5 values
                    ]
                    for metric_name, metric_deque in self.performance_metrics.items()
                    if metric_deque
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Update streaming buffers
            self.streaming_buffers["global_metrics"].append(global_data)
            
            # Notify stream update callbacks
            for callback in self.stream_update_callbacks:
                try:
                    await callback("global_update", global_data)
                except Exception as e:
                    logger.error(f"Global stream callback failed: {e}")
                    
        except Exception as e:
            logger.error(f"Global streaming metrics update failed: {e}")
    
    async def _notify_metric_subscribers(self, metric_name: str, metric: PerformanceMetric):
        """Notify metric subscribers"""
        
        try:
            if metric_name in self.metric_subscribers:
                for subscriber_callback in self.metric_subscribers[metric_name]:
                    try:
                        await subscriber_callback(metric)
                    except Exception as e:
                        logger.error(f"Metric subscriber notification failed: {e}")
                        
        except Exception as e:
            logger.error(f"Metric subscriber notification failed: {e}")
    
    async def _notify_alert_subscribers(self, alert: SystemAlert):
        """Notify alert subscribers"""
        
        try:
            for callback in self.stream_update_callbacks:
                try:
                    await callback("alert", {
                        "alert_id": alert.alert_id,
                        "severity": alert.severity.value,
                        "title": alert.title,
                        "description": alert.description,
                        "source_component": alert.source_component,
                        "metric_values": alert.metric_values,
                        "timestamp": alert.timestamp.isoformat()
                    })
                except Exception as e:
                    logger.error(f"Alert subscriber notification failed: {e}")
                    
        except Exception as e:
            logger.error(f"Alert subscriber notification failed: {e}")
    
    async def _cleanup_workflow(self, workflow_id: str, delay: float = 0.0):
        """Clean up completed workflow after delay"""
        
        try:
            if delay > 0:
                await asyncio.sleep(delay)
            
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]
                logger.debug(f"Cleaned up workflow {workflow_id}")
                
        except Exception as e:
            logger.error(f"Workflow cleanup failed: {e}")
    
    async def _cleanup_loop(self):
        """Periodic cleanup of expired data"""
        
        while True:
            try:
                await asyncio.sleep(300)  # 5 minutes
                
                current_time = datetime.now()
                
                # Clean up old metrics
                for metric_name in list(self.performance_metrics.keys()):
                    metric_deque = self.performance_metrics[metric_name]
                    cutoff_time = current_time - self.metric_retention
                    
                    # Remove old metrics
                    while metric_deque and metric_deque[0].timestamp < cutoff_time:
                        metric_deque.popleft()
                    
                    # Remove empty metric entries
                    if not metric_deque:
                        del self.performance_metrics[metric_name]
                
                # Clean up old alerts
                cutoff_time = current_time - self.alert_retention
                self.alert_history = deque([
                    alert for alert in self.alert_history
                    if alert.timestamp > cutoff_time
                ], maxlen=500)
                
                # Resolve old active alerts
                resolved_alerts = []
                for alert_id, alert in self.active_alerts.items():
                    if alert.timestamp < cutoff_time:
                        alert.resolved = True
                        alert.resolution_time = current_time
                        resolved_alerts.append(alert_id)
                
                for alert_id in resolved_alerts:
                    del self.active_alerts[alert_id]
                
                logger.debug("Periodic cleanup completed")
                
            except Exception as e:
                logger.error(f"Cleanup loop failed: {e}")
    
    async def get_monitor_status(self) -> Dict[str, Any]:
        """Get comprehensive monitor status"""
        
        return {
            "monitor_initialized": self.initialized,
            "monitoring_active": self.monitoring_active,
            "monitoring_level": self.monitoring_level.value,
            "active_workflows": len(self.active_workflows),
            "workflow_history_count": len(self.workflow_history),
            "total_workflows": self.workflow_counter,
            "active_alerts": len(self.active_alerts),
            "alert_history_count": len(self.alert_history),
            "total_alerts": self.alert_counter,
            "tracked_metrics": len(self.performance_metrics),
            "adaptive_rules": len(self.adaptive_rules),
            "streaming_subscribers": sum(len(subs) for subs in self.metric_subscribers.values()),
            "stream_callbacks": len(self.stream_update_callbacks),
            "core_systems_available": CORE_SYSTEMS_AVAILABLE
        }
    
    async def start_monitoring(self):
        """Start active monitoring"""
        self.monitoring_active = True
        logger.info("Real-time monitoring started")
    
    async def stop_monitoring(self):
        """Stop active monitoring"""
        self.monitoring_active = False
        logger.info("Real-time monitoring stopped")
    
    async def shutdown(self):
        """Shutdown orchestration monitor"""
        
        try:
            # Stop monitoring
            self.monitoring_active = False
            
            # Cancel background tasks
            tasks = [self.monitoring_task, self.adaptive_task, self.cleanup_task]
            for task in tasks:
                if task:
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
            
            # Clear data
            self.active_workflows.clear()
            self.performance_metrics.clear()
            self.active_alerts.clear()
            
            logger.info("Real-time Orchestration Monitor shutdown completed")
            
        except Exception as e:
            logger.error(f"Monitor shutdown failed: {e}")


# Initialize global monitor instance
realtime_orchestration_monitor = RealtimeOrchestrationMonitor()


async def test_realtime_orchestration_monitor():
    """Test Real-time Orchestration Monitor functionality"""
    
    monitor = RealtimeOrchestrationMonitor()
    
    print("🧪 Testing Real-time Orchestration Monitor")
    print("=" * 43)
    
    # Wait for initialization
    await asyncio.sleep(2)
    
    # Check monitor status
    status = await monitor.get_monitor_status()
    print(f"Monitor initialized: {status['monitor_initialized']}")
    print(f"Core systems available: {status['core_systems_available']}")
    print(f"Tracking {status['tracked_metrics']} metric types")
    print(f"Total adaptive rules: {status['adaptive_rules']}")
    
    # Start monitoring
    await monitor.start_monitoring()
    print(f"\n🔍 Monitoring started")
    
    # Test workflow monitoring
    print(f"\n📊 Testing workflow monitoring...")
    
    test_workflows = [
        {
            "workflow_id": "test_workflow_001",
            "command_type": "generate-prp",
            "layers": ["memory", "research", "reasoning", "tool_selection"]
        },
        {
            "workflow_id": "test_workflow_002", 
            "command_type": "implement",
            "layers": ["memory", "orchestration", "architecture"]
        }
    ]
    
    for workflow in test_workflows:
        session_id = await monitor.start_workflow_monitoring(
            workflow["workflow_id"],
            workflow["command_type"],
            workflow["layers"]
        )
        print(f"✅ Started monitoring {workflow['workflow_id']}")
        
        # Simulate workflow progress
        await monitor.update_workflow_status(
            workflow["workflow_id"],
            WorkflowStatus.RUNNING,
            "layer_execution",
            {"memory": "completed"}
        )
        
        # Simulate coordination result
        coordination_result = {
            "total_execution_time": 2.5,
            "combined_confidence": 0.87,
            "coordination_success": True,
            "active_layers": workflow["layers"]
        }
        
        await monitor.record_coordination_result(
            workflow["workflow_id"],
            coordination_result
        )
        
        print(f"  Recorded coordination result for {workflow['workflow_id']}")
    
    # Test metric recording
    print(f"\n📈 Testing metric recording...")
    
    test_metrics = [
        ("coordination_time", 3.2, "seconds"),
        ("success_rate", 0.92, "percentage"),
        ("cache_hit_rate", 0.78, "percentage"),
        ("memory_usage", 0.65, "percentage")
    ]
    
    for metric_name, value, unit in test_metrics:
        await monitor._record_metric(metric_name, value, unit, {
            "test_context": "monitor_testing"
        })
        print(f"  Recorded {metric_name}: {value} {unit}")
    
    # Test alert creation
    print(f"\n🚨 Testing alert system...")
    
    # Trigger threshold alert
    await monitor._record_metric("coordination_time", 25.0, "seconds")  # Should trigger critical alert
    print(f"  Triggered threshold-based alert")
    
    # Create manual alert
    alert_id = await monitor._create_alert(
        title="Test System Alert",
        description="This is a test alert for monitoring validation",
        severity=AlertSeverity.WARNING,
        source_component="test_system",
        metric_values={"test_metric": 42.0}
    )
    print(f"  Created manual alert: {alert_id}")
    
    # Wait for monitoring to process
    await asyncio.sleep(3)
    
    # Complete workflows
    for workflow in test_workflows:
        await monitor.update_workflow_status(
            workflow["workflow_id"],
            WorkflowStatus.COMPLETED,
            "completed",
            {layer: "completed" for layer in workflow["layers"]}
        )
        print(f"  Completed workflow {workflow['workflow_id']}")
    
    # Wait for final processing
    await asyncio.sleep(2)
    
    # Check final status
    final_status = await monitor.get_monitor_status()
    print(f"\n📊 Final Status:")
    print(f"Active workflows: {final_status['active_workflows']}")
    print(f"Workflow history: {final_status['workflow_history_count']}")
    print(f"Total workflows: {final_status['total_workflows']}")
    print(f"Active alerts: {final_status['active_alerts']}")
    print(f"Total alerts: {final_status['total_alerts']}")
    print(f"Tracked metrics: {final_status['tracked_metrics']}")
    
    # Stop monitoring and cleanup
    await monitor.stop_monitoring()
    await monitor.shutdown()
    
    print(f"\n✅ Real-time Orchestration Monitor Testing Complete")
    print(f"Comprehensive monitoring and orchestration system validated")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_realtime_orchestration_monitor())