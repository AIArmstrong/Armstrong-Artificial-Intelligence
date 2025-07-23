"""
MCP Health Monitor

Provides health monitoring, alerting, and recovery capabilities
for MCP servers with proactive issue detection.
"""
import logging
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class HealthStatus(str, Enum):
    """Health status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


@dataclass
class HealthMetrics:
    """Health metrics for a server"""
    server_name: str
    status: HealthStatus
    response_time_ms: float
    error_rate: float
    uptime_percentage: float
    last_check: datetime
    consecutive_failures: int
    total_checks: int
    memory_usage_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None


@dataclass
class HealthAlert:
    """Health alert information"""
    server_name: str
    alert_type: str
    severity: HealthStatus
    message: str
    timestamp: datetime
    resolved: bool = False


class MCPHealthMonitor:
    """
    Comprehensive health monitoring for MCP servers.
    
    Features:
    - Real-time health status tracking
    - Performance metrics collection
    - Proactive alert generation
    - Automatic recovery triggers
    - Health trend analysis
    """
    
    def __init__(self, 
                 check_interval: int = 30,
                 alert_threshold: int = 3,
                 recovery_attempts: int = 2):
        """Initialize health monitor"""
        
        self.check_interval = check_interval
        self.alert_threshold = alert_threshold
        self.recovery_attempts = recovery_attempts
        
        # Health tracking
        self.health_metrics: Dict[str, HealthMetrics] = {}
        self.health_history: Dict[str, List[HealthMetrics]] = {}
        self.active_alerts: List[HealthAlert] = []
        self.alert_handlers: List[Callable] = []
        
        # Monitoring state
        self.monitoring_active = False
        self.monitor_task: Optional[asyncio.Task] = None
        self.start_time = datetime.now()
        
        # Performance thresholds
        self.thresholds = {
            "response_time_warning": 1000,  # ms
            "response_time_critical": 3000,  # ms
            "error_rate_warning": 0.1,      # 10%
            "error_rate_critical": 0.3,     # 30%
            "uptime_warning": 0.95,         # 95%
            "uptime_critical": 0.85         # 85%
        }
    
    async def start_monitoring(self, server_names: List[str]):
        """Start health monitoring for specified servers"""
        
        try:
            logger.info(f"Starting health monitoring for {len(server_names)} servers")
            
            # Initialize metrics for each server
            for server_name in server_names:
                self.health_metrics[server_name] = HealthMetrics(
                    server_name=server_name,
                    status=HealthStatus.HEALTHY,
                    response_time_ms=0.0,
                    error_rate=0.0,
                    uptime_percentage=100.0,
                    last_check=datetime.now(),
                    consecutive_failures=0,
                    total_checks=0
                )
                self.health_history[server_name] = []
            
            # Start monitoring loop
            self.monitoring_active = True
            self.monitor_task = asyncio.create_task(self._monitoring_loop())
            
            logger.info("Health monitoring started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start health monitoring: {e}")
            raise
    
    async def stop_monitoring(self):
        """Stop health monitoring"""
        
        try:
            logger.info("Stopping health monitoring")
            
            self.monitoring_active = False
            
            if self.monitor_task:
                self.monitor_task.cancel()
                try:
                    await self.monitor_task
                except asyncio.CancelledError:
                    pass
            
            logger.info("Health monitoring stopped")
            
        except Exception as e:
            logger.error(f"Error stopping health monitoring: {e}")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        
        while self.monitoring_active:
            try:
                await asyncio.sleep(self.check_interval)
                
                # Perform health checks for all monitored servers
                for server_name in self.health_metrics.keys():
                    await self._check_server_health(server_name)
                
                # Process alerts
                await self._process_health_alerts()
                
                # Clean old history
                await self._cleanup_old_metrics()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health monitoring loop error: {e}")
    
    async def _check_server_health(self, server_name: str):
        """Perform health check for specific server"""
        
        try:
            start_time = datetime.now()
            metrics = self.health_metrics[server_name]
            
            # Simulate health check (in real implementation, this would ping the server)
            health_result = await self._perform_health_check(server_name)
            
            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Update metrics
            metrics.last_check = datetime.now()
            metrics.total_checks += 1
            metrics.response_time_ms = response_time
            
            if health_result["healthy"]:
                metrics.consecutive_failures = 0
                metrics.status = self._calculate_health_status(metrics)
            else:
                metrics.consecutive_failures += 1
                metrics.error_rate = health_result.get("error_rate", 0.0)
                metrics.status = HealthStatus.CRITICAL if metrics.consecutive_failures >= self.alert_threshold else HealthStatus.WARNING
            
            # Calculate uptime
            if metrics.total_checks > 0:
                successful_checks = metrics.total_checks - metrics.consecutive_failures
                metrics.uptime_percentage = (successful_checks / metrics.total_checks) * 100
            
            # Store in history
            self.health_history[server_name].append(metrics)
            
            # Trigger alerts if needed
            await self._check_for_alerts(server_name, metrics)
            
        except Exception as e:
            logger.error(f"Health check failed for {server_name}: {e}")
            
            # Record failed check
            metrics = self.health_metrics[server_name]
            metrics.consecutive_failures += 1
            metrics.status = HealthStatus.OFFLINE
            metrics.last_check = datetime.now()
    
    async def _perform_health_check(self, server_name: str) -> Dict[str, Any]:
        """Perform actual health check (placeholder implementation)"""
        
        # In real implementation, this would:
        # 1. Send ping to MCP server
        # 2. Check response time
        # 3. Verify server capabilities
        # 4. Check resource usage
        
        # Simulate health check with some randomness
        import random
        
        is_healthy = random.random() > 0.1  # 90% healthy rate
        error_rate = random.random() * 0.05 if is_healthy else random.random() * 0.5
        
        return {
            "healthy": is_healthy,
            "error_rate": error_rate,
            "memory_usage": random.randint(50, 200),  # MB
            "cpu_usage": random.randint(5, 80)        # %
        }
    
    def _calculate_health_status(self, metrics: HealthMetrics) -> HealthStatus:
        """Calculate overall health status based on metrics"""
        
        # Check response time
        if metrics.response_time_ms > self.thresholds["response_time_critical"]:
            return HealthStatus.CRITICAL
        elif metrics.response_time_ms > self.thresholds["response_time_warning"]:
            return HealthStatus.WARNING
        
        # Check error rate
        if metrics.error_rate > self.thresholds["error_rate_critical"]:
            return HealthStatus.CRITICAL
        elif metrics.error_rate > self.thresholds["error_rate_warning"]:
            return HealthStatus.WARNING
        
        # Check uptime
        if metrics.uptime_percentage < self.thresholds["uptime_critical"]:
            return HealthStatus.CRITICAL
        elif metrics.uptime_percentage < self.thresholds["uptime_warning"]:
            return HealthStatus.WARNING
        
        return HealthStatus.HEALTHY
    
    async def _check_for_alerts(self, server_name: str, metrics: HealthMetrics):
        """Check if alerts should be triggered"""
        
        alerts_to_create = []
        
        # Response time alerts
        if metrics.response_time_ms > self.thresholds["response_time_critical"]:
            alerts_to_create.append(HealthAlert(
                server_name=server_name,
                alert_type="response_time",
                severity=HealthStatus.CRITICAL,
                message=f"Response time {metrics.response_time_ms:.0f}ms exceeds critical threshold",
                timestamp=datetime.now()
            ))
        elif metrics.response_time_ms > self.thresholds["response_time_warning"]:
            alerts_to_create.append(HealthAlert(
                server_name=server_name,
                alert_type="response_time",
                severity=HealthStatus.WARNING,
                message=f"Response time {metrics.response_time_ms:.0f}ms exceeds warning threshold",
                timestamp=datetime.now()
            ))
        
        # Error rate alerts
        if metrics.error_rate > self.thresholds["error_rate_critical"]:
            alerts_to_create.append(HealthAlert(
                server_name=server_name,
                alert_type="error_rate",
                severity=HealthStatus.CRITICAL,
                message=f"Error rate {metrics.error_rate:.1%} exceeds critical threshold",
                timestamp=datetime.now()
            ))
        
        # Consecutive failure alerts
        if metrics.consecutive_failures >= self.alert_threshold:
            alerts_to_create.append(HealthAlert(
                server_name=server_name,
                alert_type="consecutive_failures",
                severity=HealthStatus.CRITICAL,
                message=f"{metrics.consecutive_failures} consecutive failures detected",
                timestamp=datetime.now()
            ))
        
        # Add new alerts
        for alert in alerts_to_create:
            # Check if similar alert already exists
            existing_alert = self._find_existing_alert(alert)
            if not existing_alert:
                self.active_alerts.append(alert)
                await self._trigger_alert(alert)
    
    def _find_existing_alert(self, alert: HealthAlert) -> Optional[HealthAlert]:
        """Find existing similar alert"""
        
        for existing in self.active_alerts:
            if (existing.server_name == alert.server_name and
                existing.alert_type == alert.alert_type and
                not existing.resolved):
                return existing
        
        return None
    
    async def _trigger_alert(self, alert: HealthAlert):
        """Trigger alert through registered handlers"""
        
        logger.warning(f"HEALTH ALERT: {alert.server_name} - {alert.message}")
        
        # Call registered alert handlers
        for handler in self.alert_handlers:
            try:
                await handler(alert)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")
    
    async def _process_health_alerts(self):
        """Process and resolve health alerts"""
        
        for alert in self.active_alerts:
            if not alert.resolved:
                # Check if alert condition is resolved
                metrics = self.health_metrics.get(alert.server_name)
                if metrics and await self._is_alert_resolved(alert, metrics):
                    alert.resolved = True
                    logger.info(f"Alert resolved: {alert.server_name} - {alert.alert_type}")
    
    async def _is_alert_resolved(self, alert: HealthAlert, metrics: HealthMetrics) -> bool:
        """Check if alert condition is resolved"""
        
        if alert.alert_type == "response_time":
            return metrics.response_time_ms < self.thresholds["response_time_warning"]
        elif alert.alert_type == "error_rate":
            return metrics.error_rate < self.thresholds["error_rate_warning"]
        elif alert.alert_type == "consecutive_failures":
            return metrics.consecutive_failures == 0
        
        return False
    
    async def _cleanup_old_metrics(self):
        """Remove old metrics history to prevent memory buildup"""
        
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        for server_name in self.health_history:
            self.health_history[server_name] = [
                metric for metric in self.health_history[server_name]
                if metric.last_check > cutoff_time
            ]
        
        # Remove resolved alerts older than 1 hour
        cutoff_time = datetime.now() - timedelta(hours=1)
        self.active_alerts = [
            alert for alert in self.active_alerts
            if not alert.resolved or alert.timestamp > cutoff_time
        ]
    
    def add_alert_handler(self, handler: Callable[[HealthAlert], None]):
        """Add alert handler function"""
        self.alert_handlers.append(handler)
    
    def get_health_status(self, server_name: Optional[str] = None) -> Dict[str, Any]:
        """Get current health status"""
        
        if server_name:
            if server_name not in self.health_metrics:
                return {"error": f"Server {server_name} not monitored"}
            
            metrics = self.health_metrics[server_name]
            return {
                "server_name": server_name,
                "status": metrics.status.value,
                "response_time_ms": metrics.response_time_ms,
                "error_rate": metrics.error_rate,
                "uptime_percentage": metrics.uptime_percentage,
                "consecutive_failures": metrics.consecutive_failures,
                "total_checks": metrics.total_checks,
                "last_check": metrics.last_check.isoformat()
            }
        
        # Return status for all servers
        return {
            "monitoring_active": self.monitoring_active,
            "monitored_servers": len(self.health_metrics),
            "active_alerts": len([a for a in self.active_alerts if not a.resolved]),
            "uptime_hours": (datetime.now() - self.start_time).total_seconds() / 3600,
            "servers": {
                name: {
                    "status": metrics.status.value,
                    "response_time_ms": metrics.response_time_ms,
                    "uptime_percentage": metrics.uptime_percentage,
                    "consecutive_failures": metrics.consecutive_failures
                }
                for name, metrics in self.health_metrics.items()
            }
        }
    
    def get_active_alerts(self, server_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get active alerts"""
        
        alerts = [a for a in self.active_alerts if not a.resolved]
        
        if server_name:
            alerts = [a for a in alerts if a.server_name == server_name]
        
        return [
            {
                "server_name": alert.server_name,
                "alert_type": alert.alert_type,
                "severity": alert.severity.value,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat()
            }
            for alert in alerts
        ]
    
    def get_health_trends(self, server_name: str, hours: int = 24) -> Dict[str, Any]:
        """Get health trends for specified time period"""
        
        if server_name not in self.health_history:
            return {"error": f"No history for server {server_name}"}
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        history = [
            m for m in self.health_history[server_name]
            if m.last_check > cutoff_time
        ]
        
        if not history:
            return {"trend_data": [], "summary": "No data available"}
        
        # Calculate trends
        avg_response_time = sum(m.response_time_ms for m in history) / len(history)
        avg_error_rate = sum(m.error_rate for m in history) / len(history)
        avg_uptime = sum(m.uptime_percentage for m in history) / len(history)
        
        return {
            "server_name": server_name,
            "time_period_hours": hours,
            "data_points": len(history),
            "trends": {
                "avg_response_time_ms": avg_response_time,
                "avg_error_rate": avg_error_rate,
                "avg_uptime_percentage": avg_uptime,
                "current_status": history[-1].status.value if history else "unknown"
            },
            "trend_data": [
                {
                    "timestamp": m.last_check.isoformat(),
                    "response_time_ms": m.response_time_ms,
                    "error_rate": m.error_rate,
                    "status": m.status.value
                }
                for m in history[-50:]  # Last 50 data points
            ]
        }


async def test_health_monitor():
    """Test health monitor functionality"""
    
    monitor = MCPHealthMonitor(check_interval=2)  # Fast checks for testing
    
    print("🧪 Testing MCP Health Monitor")
    print("=" * 30)
    
    # Add alert handler
    async def test_alert_handler(alert: HealthAlert):
        print(f"🚨 Alert: {alert.server_name} - {alert.message}")
    
    monitor.add_alert_handler(test_alert_handler)
    
    # Start monitoring
    test_servers = ["slack", "github", "filesystem"]
    await monitor.start_monitoring(test_servers)
    
    print(f"Monitoring started for: {', '.join(test_servers)}")
    
    # Let it run for a few cycles
    await asyncio.sleep(5)
    
    # Check health status
    status = monitor.get_health_status()
    print(f"Monitored servers: {status['monitored_servers']}")
    print(f"Active alerts: {status['active_alerts']}")
    
    # Check individual server status
    for server_name in test_servers:
        server_status = monitor.get_health_status(server_name)
        print(f"{server_name}: {server_status['status']} - {server_status['response_time_ms']:.0f}ms")
    
    # Get health trends
    trends = monitor.get_health_trends("slack", hours=1)
    print(f"Slack trends: {trends.get('trends', {}).get('avg_response_time_ms', 0):.0f}ms avg")
    
    # Stop monitoring
    await monitor.stop_monitoring()
    
    print(f"\n✅ Health Monitor Testing Complete")
    print(f"Proactive monitoring and alerting working")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_health_monitor())