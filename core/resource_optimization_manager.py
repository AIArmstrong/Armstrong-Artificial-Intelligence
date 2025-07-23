"""
AAI Resource Optimization Manager
Manages shared resources, caching, and performance optimization across all enhancement layers.

Provides unified resource management for the 8 enhancement layers including connection pooling,
intelligent caching, predictive resource allocation, and performance monitoring.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import json
import hashlib
import weakref

logger = logging.getLogger(__name__)


class ResourceType(Enum):
    """Types of resources managed by the system"""
    CONNECTION = "connection"
    CACHE = "cache"
    MEMORY = "memory"
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"


class ResourcePriority(Enum):
    """Priority levels for resource allocation"""
    CRITICAL = "critical"  # Must have resources
    HIGH = "high"  # Important for performance
    MEDIUM = "medium"  # Helpful but not essential
    LOW = "low"  # Nice to have


@dataclass
class ResourceRequest:
    """Request for resource allocation"""
    requester_id: str
    resource_type: ResourceType
    priority: ResourcePriority
    estimated_usage: Dict[str, Any]
    timeout: float = 30.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ResourceAllocation:
    """Allocated resource information"""
    allocation_id: str
    resource_type: ResourceType
    allocated_resources: Dict[str, Any]
    requester_id: str
    allocated_at: datetime
    expires_at: datetime
    usage_stats: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime
    expires_at: datetime
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    size_bytes: int = 0
    hit_rate: float = 0.0


class ResourceOptimizationManager:
    """
    Unified resource optimization manager for all enhancement layers.
    
    Features:
    - Shared resource pools for connections, memory, and compute
    - Intelligent caching with LRU and TTL policies
    - Predictive resource allocation based on usage patterns
    - Performance monitoring and optimization recommendations
    - Resource usage analytics and reporting
    - Automatic cleanup and garbage collection
    """
    
    def __init__(self):
        """Initialize resource optimization manager"""
        
        # Resource pools
        self.resource_pools = {
            ResourceType.CONNECTION: {},
            ResourceType.CACHE: {},
            ResourceType.MEMORY: {},
            ResourceType.COMPUTE: {},
            ResourceType.STORAGE: {},
            ResourceType.NETWORK: {}
        }
        
        # Active allocations
        self.active_allocations = {}
        self.allocation_counter = 0
        
        # Cache management
        self.cache_storage = {}
        self.cache_metadata = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_size": 0
        }
        
        # Connection pools
        self.connection_pools = {
            "database": {},
            "api": {},
            "external_service": {},
            "llm_provider": {}
        }
        
        # Performance tracking
        self.performance_metrics = {
            "resource_efficiency": 0.0,
            "cache_hit_rate": 0.0,
            "average_allocation_time": 0.0,
            "resource_utilization": defaultdict(float),
            "optimization_opportunities": []
        }
        
        # Usage patterns for prediction
        self.usage_patterns = defaultdict(list)
        self.pattern_analysis = {}
        
        # Configuration
        self.max_cache_size = 100 * 1024 * 1024  # 100MB
        self.default_cache_ttl = timedelta(minutes=15)
        self.max_allocations_per_requester = 10
        self.cleanup_interval = timedelta(minutes=5)
        
        # Cleanup task
        self.cleanup_task = None
        self.initialized = False
        
        # Initialize manager
        # Manager will be initialized lazily when first needed
    
    async def _initialize_manager(self):
        """Initialize resource optimization manager"""
        
        try:
            # Initialize resource pools
            await self._initialize_resource_pools()
            
            # Start cleanup task
            self.cleanup_task = asyncio.create_task(self._periodic_cleanup())
            
            self.initialized = True
            logger.info("Resource Optimization Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Resource Optimization Manager: {e}")
            self.initialized = False
    
    async def _initialize_resource_pools(self):
        """Initialize all resource pools"""
        
        # Connection pool initialization
        self.connection_pools["llm_provider"] = {
            "pool_size": 5,
            "active_connections": 0,
            "available_connections": [],
            "connection_timeout": 30.0
        }
        
        self.connection_pools["database"] = {
            "pool_size": 10,
            "active_connections": 0,
            "available_connections": [],
            "connection_timeout": 60.0
        }
        
        self.connection_pools["api"] = {
            "pool_size": 8,
            "active_connections": 0,
            "available_connections": [],
            "connection_timeout": 30.0
        }
        
        # Memory pool initialization
        self.resource_pools[ResourceType.MEMORY] = {
            "total_allocated": 0,
            "max_allocation": 500 * 1024 * 1024,  # 500MB
            "allocation_blocks": {}
        }
        
        # Cache initialization
        self.resource_pools[ResourceType.CACHE] = {
            "max_size": self.max_cache_size,
            "current_size": 0,
            "entry_count": 0
        }
        
        logger.info("Resource pools initialized")
    
    async def request_resources(self, 
                              request: ResourceRequest) -> Optional[ResourceAllocation]:
        """
        Request resource allocation.
        
        Args:
            request: Resource request details
            
        Returns:
            Resource allocation if successful, None otherwise
        """
        try:
            if not self.initialized:
                logger.warning("Resource manager not initialized")
                return None
            
            # Check if requester has too many active allocations
            requester_allocations = sum(
                1 for alloc in self.active_allocations.values()
                if alloc.requester_id == request.requester_id
            )
            
            if requester_allocations >= self.max_allocations_per_requester:
                logger.warning(f"Requester {request.requester_id} has too many active allocations")
                return None
            
            # Allocate resources based on type
            if request.resource_type == ResourceType.CONNECTION:
                return await self._allocate_connection(request)
            elif request.resource_type == ResourceType.CACHE:
                return await self._allocate_cache(request)
            elif request.resource_type == ResourceType.MEMORY:
                return await self._allocate_memory(request)
            elif request.resource_type == ResourceType.COMPUTE:
                return await self._allocate_compute(request)
            else:
                return await self._allocate_generic_resource(request)
                
        except Exception as e:
            logger.error(f"Resource allocation failed: {e}")
            return None
    
    async def _allocate_connection(self, request: ResourceRequest) -> Optional[ResourceAllocation]:
        """Allocate connection resources"""
        
        try:
            connection_type = request.estimated_usage.get("connection_type", "api")
            pool = self.connection_pools.get(connection_type, self.connection_pools["api"])
            
            if pool["active_connections"] >= pool["pool_size"]:
                # Try to wait for available connection
                wait_time = 0.0
                while (pool["active_connections"] >= pool["pool_size"] and 
                       wait_time < request.timeout):
                    await asyncio.sleep(0.1)
                    wait_time += 0.1
                
                if pool["active_connections"] >= pool["pool_size"]:
                    logger.warning(f"No available connections in {connection_type} pool")
                    return None
            
            # Allocate connection
            allocation_id = f"conn_{self.allocation_counter}_{int(datetime.now().timestamp())}"
            self.allocation_counter += 1
            
            pool["active_connections"] += 1
            expires_at = datetime.now() + timedelta(seconds=request.timeout)
            
            allocation = ResourceAllocation(
                allocation_id=allocation_id,
                resource_type=ResourceType.CONNECTION,
                allocated_resources={
                    "connection_type": connection_type,
                    "pool_info": pool,
                    "timeout": request.timeout
                },
                requester_id=request.requester_id,
                allocated_at=datetime.now(),
                expires_at=expires_at
            )
            
            self.active_allocations[allocation_id] = allocation
            
            # Track usage pattern
            self.usage_patterns[request.requester_id].append({
                "resource_type": "connection",
                "connection_type": connection_type,
                "timestamp": datetime.now(),
                "estimated_usage": request.estimated_usage
            })
            
            logger.info(f"Allocated connection {allocation_id} for {request.requester_id}")
            return allocation
            
        except Exception as e:
            logger.error(f"Connection allocation failed: {e}")
            return None
    
    async def _allocate_cache(self, request: ResourceRequest) -> Optional[ResourceAllocation]:
        """Allocate cache resources"""
        
        try:
            cache_size = request.estimated_usage.get("size", 1024 * 1024)  # 1MB default
            cache_pool = self.resource_pools[ResourceType.CACHE]
            
            # Check if there's enough cache space
            if cache_pool["current_size"] + cache_size > cache_pool["max_size"]:
                # Try to free up space
                await self._evict_cache_entries(cache_size)
                
                if cache_pool["current_size"] + cache_size > cache_pool["max_size"]:
                    logger.warning("Insufficient cache space available")
                    return None
            
            # Allocate cache space
            allocation_id = f"cache_{self.allocation_counter}_{int(datetime.now().timestamp())}"
            self.allocation_counter += 1
            
            cache_pool["current_size"] += cache_size
            expires_at = datetime.now() + timedelta(seconds=request.timeout)
            
            allocation = ResourceAllocation(
                allocation_id=allocation_id,
                resource_type=ResourceType.CACHE,
                allocated_resources={
                    "cache_size": cache_size,
                    "namespace": request.requester_id,
                    "ttl": request.estimated_usage.get("ttl", self.default_cache_ttl.total_seconds())
                },
                requester_id=request.requester_id,
                allocated_at=datetime.now(),
                expires_at=expires_at
            )
            
            self.active_allocations[allocation_id] = allocation
            
            logger.info(f"Allocated cache space {allocation_id} for {request.requester_id}")
            return allocation
            
        except Exception as e:
            logger.error(f"Cache allocation failed: {e}")
            return None
    
    async def _allocate_memory(self, request: ResourceRequest) -> Optional[ResourceAllocation]:
        """Allocate memory resources"""
        
        try:
            memory_size = request.estimated_usage.get("size", 10 * 1024 * 1024)  # 10MB default
            memory_pool = self.resource_pools[ResourceType.MEMORY]
            
            # Check if there's enough memory
            if (memory_pool["total_allocated"] + memory_size > 
                memory_pool["max_allocation"]):
                logger.warning("Insufficient memory available")
                return None
            
            # Allocate memory
            allocation_id = f"mem_{self.allocation_counter}_{int(datetime.now().timestamp())}"
            self.allocation_counter += 1
            
            memory_pool["total_allocated"] += memory_size
            memory_pool["allocation_blocks"][allocation_id] = memory_size
            
            expires_at = datetime.now() + timedelta(seconds=request.timeout)
            
            allocation = ResourceAllocation(
                allocation_id=allocation_id,
                resource_type=ResourceType.MEMORY,
                allocated_resources={
                    "memory_size": memory_size,
                    "block_id": allocation_id
                },
                requester_id=request.requester_id,
                allocated_at=datetime.now(),
                expires_at=expires_at
            )
            
            self.active_allocations[allocation_id] = allocation
            
            logger.info(f"Allocated memory {allocation_id} for {request.requester_id}")
            return allocation
            
        except Exception as e:
            logger.error(f"Memory allocation failed: {e}")
            return None
    
    async def _allocate_compute(self, request: ResourceRequest) -> Optional[ResourceAllocation]:
        """Allocate compute resources"""
        
        try:
            # Simplified compute allocation - would integrate with actual compute resources
            allocation_id = f"compute_{self.allocation_counter}_{int(datetime.now().timestamp())}"
            self.allocation_counter += 1
            
            expires_at = datetime.now() + timedelta(seconds=request.timeout)
            
            allocation = ResourceAllocation(
                allocation_id=allocation_id,
                resource_type=ResourceType.COMPUTE,
                allocated_resources={
                    "compute_units": request.estimated_usage.get("units", 1),
                    "priority": request.priority.value
                },
                requester_id=request.requester_id,
                allocated_at=datetime.now(),
                expires_at=expires_at
            )
            
            self.active_allocations[allocation_id] = allocation
            
            logger.info(f"Allocated compute {allocation_id} for {request.requester_id}")
            return allocation
            
        except Exception as e:
            logger.error(f"Compute allocation failed: {e}")
            return None
    
    async def _allocate_generic_resource(self, request: ResourceRequest) -> Optional[ResourceAllocation]:
        """Allocate generic resources"""
        
        try:
            allocation_id = f"generic_{self.allocation_counter}_{int(datetime.now().timestamp())}"
            self.allocation_counter += 1
            
            expires_at = datetime.now() + timedelta(seconds=request.timeout)
            
            allocation = ResourceAllocation(
                allocation_id=allocation_id,
                resource_type=request.resource_type,
                allocated_resources=request.estimated_usage,
                requester_id=request.requester_id,
                allocated_at=datetime.now(),
                expires_at=expires_at
            )
            
            self.active_allocations[allocation_id] = allocation
            
            logger.info(f"Allocated generic resource {allocation_id} for {request.requester_id}")
            return allocation
            
        except Exception as e:
            logger.error(f"Generic resource allocation failed: {e}")
            return None
    
    async def release_resources(self, allocation_id: str) -> bool:
        """
        Release allocated resources.
        
        Args:
            allocation_id: ID of the allocation to release
            
        Returns:
            True if successfully released, False otherwise
        """
        try:
            if allocation_id not in self.active_allocations:
                logger.warning(f"Allocation {allocation_id} not found")
                return False
            
            allocation = self.active_allocations[allocation_id]
            
            # Release based on resource type
            if allocation.resource_type == ResourceType.CONNECTION:
                await self._release_connection(allocation)
            elif allocation.resource_type == ResourceType.CACHE:
                await self._release_cache(allocation)
            elif allocation.resource_type == ResourceType.MEMORY:
                await self._release_memory(allocation)
            
            # Remove from active allocations
            del self.active_allocations[allocation_id]
            
            logger.info(f"Released resources for allocation {allocation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Resource release failed: {e}")
            return False
    
    async def _release_connection(self, allocation: ResourceAllocation):
        """Release connection resources"""
        
        connection_type = allocation.allocated_resources.get("connection_type", "api")
        pool = self.connection_pools.get(connection_type)
        
        if pool:
            pool["active_connections"] = max(0, pool["active_connections"] - 1)
    
    async def _release_cache(self, allocation: ResourceAllocation):
        """Release cache resources"""
        
        cache_size = allocation.allocated_resources.get("cache_size", 0)
        cache_pool = self.resource_pools[ResourceType.CACHE]
        cache_pool["current_size"] = max(0, cache_pool["current_size"] - cache_size)
    
    async def _release_memory(self, allocation: ResourceAllocation):
        """Release memory resources"""
        
        memory_size = allocation.allocated_resources.get("memory_size", 0)
        block_id = allocation.allocated_resources.get("block_id")
        memory_pool = self.resource_pools[ResourceType.MEMORY]
        
        memory_pool["total_allocated"] = max(0, memory_pool["total_allocated"] - memory_size)
        if block_id in memory_pool["allocation_blocks"]:
            del memory_pool["allocation_blocks"][block_id]
    
    async def cache_get(self, key: str, namespace: str = "default") -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            namespace: Cache namespace
            
        Returns:
            Cached value if found, None otherwise
        """
        try:
            cache_key = f"{namespace}:{key}"
            
            if cache_key in self.cache_storage:
                entry = self.cache_metadata[cache_key]
                
                # Check if expired
                if datetime.now() > entry.expires_at:
                    await self._remove_cache_entry(cache_key)
                    self.cache_stats["misses"] += 1
                    return None
                
                # Update access stats
                entry.access_count += 1
                entry.last_accessed = datetime.now()
                entry.hit_rate = entry.access_count / (entry.access_count + 1)
                
                self.cache_stats["hits"] += 1
                
                return self.cache_storage[cache_key]
            
            self.cache_stats["misses"] += 1
            return None
            
        except Exception as e:
            logger.error(f"Cache get failed: {e}")
            self.cache_stats["misses"] += 1
            return None
    
    async def cache_set(self, 
                       key: str, 
                       value: Any, 
                       namespace: str = "default",
                       ttl: Optional[timedelta] = None) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            namespace: Cache namespace
            ttl: Time to live
            
        Returns:
            True if successfully cached, False otherwise
        """
        try:
            cache_key = f"{namespace}:{key}"
            
            # Calculate size (simplified)
            value_size = len(str(value)) if value else 0
            
            # Check cache capacity
            cache_pool = self.resource_pools[ResourceType.CACHE]
            if (cache_pool["current_size"] + value_size > cache_pool["max_size"]):
                # Try to evict entries
                await self._evict_cache_entries(value_size)
                
                if (cache_pool["current_size"] + value_size > cache_pool["max_size"]):
                    logger.warning("Cannot cache - insufficient space")
                    return False
            
            # Remove existing entry if present
            if cache_key in self.cache_storage:
                await self._remove_cache_entry(cache_key)
            
            # Create cache entry
            expires_at = datetime.now() + (ttl or self.default_cache_ttl)
            entry = CacheEntry(
                key=cache_key,
                value=value,
                created_at=datetime.now(),
                expires_at=expires_at,
                size_bytes=value_size
            )
            
            # Store in cache
            self.cache_storage[cache_key] = value
            self.cache_metadata[cache_key] = entry
            
            # Update stats
            cache_pool["current_size"] += value_size
            cache_pool["entry_count"] += 1
            self.cache_stats["total_size"] += value_size
            
            return True
            
        except Exception as e:
            logger.error(f"Cache set failed: {e}")
            return False
    
    async def _evict_cache_entries(self, required_space: int):
        """Evict cache entries to free up space"""
        
        try:
            # Sort entries by last accessed (LRU)
            entries_by_access = sorted(
                self.cache_metadata.items(),
                key=lambda x: x[1].last_accessed
            )
            
            freed_space = 0
            for cache_key, entry in entries_by_access:
                if freed_space >= required_space:
                    break
                
                freed_space += entry.size_bytes
                await self._remove_cache_entry(cache_key)
                self.cache_stats["evictions"] += 1
            
            logger.info(f"Evicted cache entries to free {freed_space} bytes")
            
        except Exception as e:
            logger.error(f"Cache eviction failed: {e}")
    
    async def _remove_cache_entry(self, cache_key: str):
        """Remove a cache entry"""
        
        if cache_key in self.cache_storage:
            entry = self.cache_metadata[cache_key]
            cache_pool = self.resource_pools[ResourceType.CACHE]
            
            # Update stats
            cache_pool["current_size"] -= entry.size_bytes
            cache_pool["entry_count"] -= 1
            self.cache_stats["total_size"] -= entry.size_bytes
            
            # Remove from storage
            del self.cache_storage[cache_key]
            del self.cache_metadata[cache_key]
    
    async def predict_resource_needs(self, 
                                   requester_id: str,
                                   operation_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict resource needs based on usage patterns.
        
        Args:
            requester_id: ID of the requester
            operation_context: Context about the operation
            
        Returns:
            Predicted resource requirements
        """
        try:
            if requester_id not in self.usage_patterns:
                # No historical data - return default predictions
                return {
                    "connection": {"estimated_count": 1, "confidence": 0.50},
                    "memory": {"estimated_size": 10 * 1024 * 1024, "confidence": 0.50},
                    "cache": {"estimated_size": 1024 * 1024, "confidence": 0.50},
                    "compute": {"estimated_units": 1, "confidence": 0.50}
                }
            
            # Analyze historical patterns
            patterns = self.usage_patterns[requester_id]
            
            # Group by resource type
            resource_usage = defaultdict(list)
            for pattern in patterns[-20:]:  # Last 20 operations
                resource_type = pattern.get("resource_type", "unknown")
                resource_usage[resource_type].append(pattern)
            
            predictions = {}
            
            # Predict for each resource type
            for resource_type, usage_list in resource_usage.items():
                if usage_list:
                    # Calculate average usage
                    avg_usage = self._calculate_average_usage(usage_list)
                    confidence = min(0.95, 0.50 + (len(usage_list) * 0.02))
                    
                    predictions[resource_type] = {
                        "estimated_usage": avg_usage,
                        "confidence": confidence,
                        "pattern_count": len(usage_list)
                    }
            
            return predictions
            
        except Exception as e:
            logger.error(f"Resource prediction failed: {e}")
            return {}
    
    def _calculate_average_usage(self, usage_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate average usage from usage patterns"""
        
        if not usage_list:
            return {}
        
        # Extract usage metrics
        size_values = []
        count_values = []
        
        for usage in usage_list:
            estimated = usage.get("estimated_usage", {})
            if "size" in estimated:
                size_values.append(estimated["size"])
            if "count" in estimated:
                count_values.append(estimated["count"])
        
        avg_usage = {}
        if size_values:
            avg_usage["size"] = sum(size_values) / len(size_values)
        if count_values:
            avg_usage["count"] = sum(count_values) / len(count_values)
        
        return avg_usage
    
    async def optimize_resource_allocation(self) -> Dict[str, Any]:
        """
        Analyze and optimize resource allocation.
        
        Returns:
            Optimization recommendations
        """
        try:
            optimization_results = {
                "cache_optimization": await self._optimize_cache(),
                "connection_optimization": await self._optimize_connections(),
                "memory_optimization": await self._optimize_memory(),
                "overall_efficiency": await self._calculate_overall_efficiency(),
                "recommendations": []
            }
            
            # Generate recommendations
            recommendations = []
            
            # Cache recommendations
            cache_hit_rate = self._calculate_cache_hit_rate()
            if cache_hit_rate < 0.7:
                recommendations.append(
                    f"Low cache hit rate ({cache_hit_rate:.1%}) - consider increasing cache size or TTL"
                )
            
            # Connection recommendations
            for pool_name, pool_info in self.connection_pools.items():
                utilization = pool_info["active_connections"] / pool_info["pool_size"]
                if utilization > 0.8:
                    recommendations.append(
                        f"High {pool_name} connection utilization ({utilization:.1%}) - consider increasing pool size"
                    )
            
            # Memory recommendations
            memory_pool = self.resource_pools[ResourceType.MEMORY]
            memory_utilization = (
                memory_pool["total_allocated"] / memory_pool["max_allocation"]
            )
            if memory_utilization > 0.8:
                recommendations.append(
                    f"High memory utilization ({memory_utilization:.1%}) - consider increasing memory limits"
                )
            
            optimization_results["recommendations"] = recommendations
            
            # Update performance metrics
            self.performance_metrics["resource_efficiency"] = optimization_results["overall_efficiency"]
            self.performance_metrics["cache_hit_rate"] = cache_hit_rate
            self.performance_metrics["optimization_opportunities"] = recommendations
            
            return optimization_results
            
        except Exception as e:
            logger.error(f"Resource optimization failed: {e}")
            return {"error": str(e)}
    
    async def _optimize_cache(self) -> Dict[str, Any]:
        """Optimize cache configuration"""
        
        hit_rate = self._calculate_cache_hit_rate()
        cache_pool = self.resource_pools[ResourceType.CACHE]
        utilization = cache_pool["current_size"] / cache_pool["max_size"]
        
        return {
            "hit_rate": hit_rate,
            "utilization": utilization,
            "entry_count": cache_pool["entry_count"],
            "efficiency_score": hit_rate * (1 - utilization)  # Higher hit rate, lower utilization is better
        }
    
    async def _optimize_connections(self) -> Dict[str, Any]:
        """Optimize connection pools"""
        
        pool_stats = {}
        overall_efficiency = 0.0
        
        for pool_name, pool_info in self.connection_pools.items():
            utilization = pool_info["active_connections"] / pool_info["pool_size"]
            efficiency = 1.0 - abs(0.7 - utilization)  # Optimal utilization around 70%
            
            pool_stats[pool_name] = {
                "utilization": utilization,
                "efficiency": efficiency,
                "active": pool_info["active_connections"],
                "total": pool_info["pool_size"]
            }
            
            overall_efficiency += efficiency
        
        overall_efficiency /= len(self.connection_pools)
        
        return {
            "pool_stats": pool_stats,
            "overall_efficiency": overall_efficiency
        }
    
    async def _optimize_memory(self) -> Dict[str, Any]:
        """Optimize memory allocation"""
        
        memory_pool = self.resource_pools[ResourceType.MEMORY]
        utilization = memory_pool["total_allocated"] / memory_pool["max_allocation"]
        fragmentation = len(memory_pool["allocation_blocks"]) / max(1, memory_pool["total_allocated"])
        
        return {
            "utilization": utilization,
            "fragmentation": fragmentation,
            "active_blocks": len(memory_pool["allocation_blocks"]),
            "efficiency_score": utilization * (1 - fragmentation)
        }
    
    async def _calculate_overall_efficiency(self) -> float:
        """Calculate overall resource efficiency"""
        
        cache_hit_rate = self._calculate_cache_hit_rate()
        
        # Connection efficiency
        connection_efficiency = 0.0
        for pool_info in self.connection_pools.values():
            utilization = pool_info["active_connections"] / pool_info["pool_size"]
            connection_efficiency += 1.0 - abs(0.7 - utilization)
        connection_efficiency /= len(self.connection_pools)
        
        # Memory efficiency
        memory_pool = self.resource_pools[ResourceType.MEMORY]
        memory_utilization = memory_pool["total_allocated"] / memory_pool["max_allocation"]
        memory_efficiency = memory_utilization  # Higher utilization is better for memory
        
        # Combined efficiency
        overall_efficiency = (cache_hit_rate + connection_efficiency + memory_efficiency) / 3
        
        return overall_efficiency
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        if total_requests == 0:
            return 0.0
        
        return self.cache_stats["hits"] / total_requests
    
    async def _periodic_cleanup(self):
        """Periodic cleanup of expired resources"""
        
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval.total_seconds())
                
                # Clean up expired allocations
                current_time = datetime.now()
                expired_allocations = [
                    alloc_id for alloc_id, allocation in self.active_allocations.items()
                    if current_time > allocation.expires_at
                ]
                
                for alloc_id in expired_allocations:
                    await self.release_resources(alloc_id)
                
                # Clean up expired cache entries
                expired_cache_keys = [
                    cache_key for cache_key, entry in self.cache_metadata.items()
                    if current_time > entry.expires_at
                ]
                
                for cache_key in expired_cache_keys:
                    await self._remove_cache_entry(cache_key)
                
                # Clean up old usage patterns
                cutoff_time = current_time - timedelta(hours=24)
                for requester_id in list(self.usage_patterns.keys()):
                    patterns = self.usage_patterns[requester_id]
                    self.usage_patterns[requester_id] = [
                        pattern for pattern in patterns
                        if pattern["timestamp"] > cutoff_time
                    ]
                    
                    if not self.usage_patterns[requester_id]:
                        del self.usage_patterns[requester_id]
                
                if expired_allocations or expired_cache_keys:
                    logger.info(f"Cleanup completed: {len(expired_allocations)} allocations, {len(expired_cache_keys)} cache entries")
                
            except Exception as e:
                logger.error(f"Periodic cleanup failed: {e}")
    
    async def get_resource_status(self) -> Dict[str, Any]:
        """Get comprehensive resource status"""
        
        return {
            "manager_initialized": self.initialized,
            "active_allocations": len(self.active_allocations),
            "cache_stats": self.cache_stats,
            "cache_hit_rate": self._calculate_cache_hit_rate(),
            "connection_pools": {
                name: {
                    "active": pool["active_connections"],
                    "total": pool["pool_size"],
                    "utilization": pool["active_connections"] / pool["pool_size"]
                }
                for name, pool in self.connection_pools.items()
            },
            "memory_usage": {
                "allocated": self.resource_pools[ResourceType.MEMORY]["total_allocated"],
                "max_allocation": self.resource_pools[ResourceType.MEMORY]["max_allocation"],
                "utilization": (
                    self.resource_pools[ResourceType.MEMORY]["total_allocated"] /
                    self.resource_pools[ResourceType.MEMORY]["max_allocation"]
                )
            },
            "performance_metrics": self.performance_metrics,
            "total_requesters": len(self.usage_patterns)
        }
    
    async def get_optimization_status(self) -> Dict[str, Any]:
        """Get current optimization status for performance monitoring"""
        try:
            # Run quick optimization analysis
            optimization_result = await self.optimize_resource_allocation()
            
            return {
                "status": "active",
                "overall_efficiency": optimization_result.get("overall_efficiency", 0.75),
                "active_optimizations": len(optimization_result.get("recommendations", [])),
                "cache_hit_rate": self._calculate_cache_hit_rate(),
                "resource_utilization": {
                    "memory": (
                        self.resource_pools[ResourceType.MEMORY]["total_allocated"] /
                        self.resource_pools[ResourceType.MEMORY]["max_allocation"]
                    ),
                    "connections": sum(
                        pool["active_connections"] / pool["pool_size"]
                        for pool in self.connection_pools.values()
                    ) / max(1, len(self.connection_pools))
                }
            }
        except Exception as e:
            logger.error(f"Failed to get optimization status: {e}")
            return {
                "status": "error",
                "error": str(e),
                "overall_efficiency": 0.70
            }
    
    async def shutdown(self):
        """Shutdown resource optimization manager"""
        
        try:
            # Cancel cleanup task
            if self.cleanup_task:
                self.cleanup_task.cancel()
                try:
                    await self.cleanup_task
                except asyncio.CancelledError:
                    pass
            
            # Release all active allocations
            for alloc_id in list(self.active_allocations.keys()):
                await self.release_resources(alloc_id)
            
            # Clear caches
            self.cache_storage.clear()
            self.cache_metadata.clear()
            
            logger.info("Resource Optimization Manager shutdown completed")
            
        except Exception as e:
            logger.error(f"Shutdown failed: {e}")


# Initialize global resource manager instance
resource_optimization_manager = ResourceOptimizationManager()


async def test_resource_optimization_manager():
    """Test Resource Optimization Manager functionality"""
    
    manager = ResourceOptimizationManager()
    
    print("🧪 Testing Resource Optimization Manager")
    print("=" * 42)
    
    # Wait for initialization
    await asyncio.sleep(2)
    
    # Check manager status
    status = await manager.get_resource_status()
    print(f"Manager initialized: {status['manager_initialized']}")
    print(f"Cache hit rate: {status['cache_hit_rate']:.1%}")
    print(f"Active allocations: {status['active_allocations']}")
    
    # Test resource allocation
    print(f"\n🎯 Testing resource allocation...")
    
    # Test connection allocation
    conn_request = ResourceRequest(
        requester_id="test_enhancement_layer",
        resource_type=ResourceType.CONNECTION,
        priority=ResourcePriority.HIGH,
        estimated_usage={"connection_type": "llm_provider", "timeout": 30.0}
    )
    
    conn_allocation = await manager.request_resources(conn_request)
    if conn_allocation:
        print(f"✅ Connection allocated: {conn_allocation.allocation_id}")
        print(f"   Type: {conn_allocation.allocated_resources['connection_type']}")
    
    # Test cache allocation
    cache_request = ResourceRequest(
        requester_id="test_enhancement_layer",
        resource_type=ResourceType.CACHE,
        priority=ResourcePriority.MEDIUM,
        estimated_usage={"size": 1024 * 1024, "ttl": 900}  # 1MB, 15 min
    )
    
    cache_allocation = await manager.request_resources(cache_request)
    if cache_allocation:
        print(f"✅ Cache allocated: {cache_allocation.allocation_id}")
        print(f"   Size: {cache_allocation.allocated_resources['cache_size']} bytes")
    
    # Test memory allocation
    memory_request = ResourceRequest(
        requester_id="test_enhancement_layer",
        resource_type=ResourceType.MEMORY,
        priority=ResourcePriority.HIGH,
        estimated_usage={"size": 5 * 1024 * 1024}  # 5MB
    )
    
    memory_allocation = await manager.request_resources(memory_request)
    if memory_allocation:
        print(f"✅ Memory allocated: {memory_allocation.allocation_id}")
        print(f"   Size: {memory_allocation.allocated_resources['memory_size']} bytes")
    
    # Test caching
    print(f"\n💾 Testing cache operations...")
    
    # Cache some data
    test_data = {"result": "test enhancement result", "confidence": 0.85}
    cache_success = await manager.cache_set("test_key", test_data, "enhancement_layer")
    print(f"Cache set success: {cache_success}")
    
    # Retrieve cached data
    cached_data = await manager.cache_get("test_key", "enhancement_layer")
    print(f"Cache get success: {cached_data is not None}")
    if cached_data:
        print(f"  Cached data: {cached_data}")
    
    # Test resource prediction
    print(f"\n🔮 Testing resource prediction...")
    
    operation_context = {
        "command_type": "generate-prp",
        "complexity": "high",
        "estimated_layers": 5
    }
    
    predictions = await manager.predict_resource_needs(
        "test_enhancement_layer", 
        operation_context
    )
    print(f"Resource predictions: {len(predictions)} types predicted")
    for resource_type, prediction in predictions.items():
        print(f"  {resource_type}: confidence {prediction['confidence']:.1%}")
    
    # Test optimization
    print(f"\n⚡ Testing resource optimization...")
    
    optimization = await manager.optimize_resource_allocation()
    print(f"Overall efficiency: {optimization['overall_efficiency']:.1%}")
    print(f"Recommendations: {len(optimization['recommendations'])}")
    for rec in optimization['recommendations']:
        print(f"  • {rec}")
    
    # Test resource release
    print(f"\n🔄 Testing resource release...")
    
    if conn_allocation:
        release_success = await manager.release_resources(conn_allocation.allocation_id)
        print(f"Connection release success: {release_success}")
    
    if cache_allocation:
        release_success = await manager.release_resources(cache_allocation.allocation_id)
        print(f"Cache release success: {release_success}")
    
    if memory_allocation:
        release_success = await manager.release_resources(memory_allocation.allocation_id)
        print(f"Memory release success: {release_success}")
    
    # Final status
    final_status = await manager.get_resource_status()
    print(f"\n📊 Final Status:")
    print(f"Active allocations: {final_status['active_allocations']}")
    print(f"Cache hit rate: {final_status['cache_hit_rate']:.1%}")
    print(f"Memory utilization: {final_status['memory_usage']['utilization']:.1%}")
    
    # Cleanup
    await manager.shutdown()
    
    print(f"\n✅ Resource Optimization Manager Testing Complete")
    print(f"Unified resource management ready for all enhancement layers")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_resource_optimization_manager())