#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performance Monitor for Vietnamese Spell Checker
Theo dõi và tối ưu hiệu suất hệ thống
"""

import time
import threading
import logging
from typing import Dict, List, Any
from collections import defaultdict, deque
from datetime import datetime, timedelta

class PerformanceMonitor:
    """Performance monitoring system"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics = defaultdict(lambda: deque(maxlen=max_history))
        self.lock = threading.Lock()
        self.start_time = time.time()
        
        # Performance counters
        self.counters = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'average_response_time': 0.0,
            'peak_response_time': 0.0,
            'min_response_time': float('inf')
        }
    
    def record_request(self, endpoint: str, response_time: float, success: bool = True, cached: bool = False):
        """Record a request metric"""
        with self.lock:
            timestamp = datetime.now()
            
            # Record metrics
            self.metrics['response_times'].append({
                'timestamp': timestamp,
                'endpoint': endpoint,
                'response_time': response_time,
                'success': success,
                'cached': cached
            })
            
            # Update counters
            self.counters['total_requests'] += 1
            if success:
                self.counters['successful_requests'] += 1
            else:
                self.counters['failed_requests'] += 1
            
            if cached:
                self.counters['cache_hits'] += 1
            else:
                self.counters['cache_misses'] += 1
            
            # Update response time statistics
            self.counters['average_response_time'] = (
                (self.counters['average_response_time'] * (self.counters['total_requests'] - 1) + response_time) 
                / self.counters['total_requests']
            )
            
            if response_time > self.counters['peak_response_time']:
                self.counters['peak_response_time'] = response_time
            
            if response_time < self.counters['min_response_time']:
                self.counters['min_response_time'] = response_time
    
    def get_stats(self, time_window: int = 3600) -> Dict[str, Any]:
        """Get performance statistics for the last time window (seconds)"""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(seconds=time_window)
            
            # Filter metrics for time window
            recent_metrics = [
                m for m in self.metrics['response_times']
                if m['timestamp'] >= cutoff_time
            ]
            
            if not recent_metrics:
                return {
                    'time_window': time_window,
                    'total_requests': 0,
                    'average_response_time': 0.0,
                    'peak_response_time': 0.0,
                    'min_response_time': 0.0,
                    'success_rate': 0.0,
                    'cache_hit_rate': 0.0,
                    'endpoint_stats': {}
                }
            
            # Calculate statistics
            response_times = [m['response_time'] for m in recent_metrics]
            successful_requests = sum(1 for m in recent_metrics if m['success'])
            cached_requests = sum(1 for m in recent_metrics if m['cached'])
            
            # Endpoint statistics
            endpoint_stats = defaultdict(lambda: {
                'count': 0,
                'total_time': 0.0,
                'average_time': 0.0,
                'success_count': 0
            })
            
            for metric in recent_metrics:
                endpoint = metric['endpoint']
                endpoint_stats[endpoint]['count'] += 1
                endpoint_stats[endpoint]['total_time'] += metric['response_time']
                if metric['success']:
                    endpoint_stats[endpoint]['success_count'] += 1
            
            # Calculate averages
            for endpoint in endpoint_stats:
                count = endpoint_stats[endpoint]['count']
                if count > 0:
                    endpoint_stats[endpoint]['average_time'] = (
                        endpoint_stats[endpoint]['total_time'] / count
                    )
                    endpoint_stats[endpoint]['success_rate'] = (
                        endpoint_stats[endpoint]['success_count'] / count * 100
                    )
            
            return {
                'time_window': time_window,
                'total_requests': len(recent_metrics),
                'average_response_time': sum(response_times) / len(response_times),
                'peak_response_time': max(response_times),
                'min_response_time': min(response_times),
                'success_rate': (successful_requests / len(recent_metrics)) * 100,
                'cache_hit_rate': (cached_requests / len(recent_metrics)) * 100 if recent_metrics else 0,
                'endpoint_stats': dict(endpoint_stats)
            }
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall performance statistics"""
        with self.lock:
            uptime = time.time() - self.start_time
            
            return {
                'uptime': uptime,
                'uptime_formatted': str(timedelta(seconds=int(uptime))),
                'total_requests': self.counters['total_requests'],
                'successful_requests': self.counters['successful_requests'],
                'failed_requests': self.counters['failed_requests'],
                'success_rate': (
                    (self.counters['successful_requests'] / self.counters['total_requests']) * 100
                    if self.counters['total_requests'] > 0 else 0
                ),
                'cache_hits': self.counters['cache_hits'],
                'cache_misses': self.counters['cache_misses'],
                'cache_hit_rate': (
                    (self.counters['cache_hits'] / (self.counters['cache_hits'] + self.counters['cache_misses'])) * 100
                    if (self.counters['cache_hits'] + self.counters['cache_misses']) > 0 else 0
                ),
                'average_response_time': self.counters['average_response_time'],
                'peak_response_time': self.counters['peak_response_time'],
                'min_response_time': self.counters['min_response_time'] if self.counters['min_response_time'] != float('inf') else 0
            }
    
    def get_endpoint_performance(self, endpoint: str, time_window: int = 3600) -> Dict[str, Any]:
        """Get performance statistics for a specific endpoint"""
        stats = self.get_stats(time_window)
        endpoint_stats = stats['endpoint_stats'].get(endpoint, {})
        
        return {
            'endpoint': endpoint,
            'time_window': time_window,
            'total_requests': endpoint_stats.get('count', 0),
            'average_response_time': endpoint_stats.get('average_time', 0.0),
            'success_rate': endpoint_stats.get('success_rate', 0.0),
            'total_time': endpoint_stats.get('total_time', 0.0)
        }
    
    def clear_history(self):
        """Clear historical metrics"""
        with self.lock:
            self.metrics.clear()
            self.counters = {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'average_response_time': 0.0,
                'peak_response_time': 0.0,
                'min_response_time': float('inf')
            }
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics for analysis"""
        with self.lock:
            return {
                'timestamp': datetime.now().isoformat(),
                'overall_stats': self.get_overall_stats(),
                'recent_stats': self.get_stats(3600),  # Last hour
                'metrics_count': len(self.metrics['response_times'])
            }
