#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cache Manager for Vietnamese Spell Checker
Tối ưu performance với caching
"""

import time
import hashlib
import json
from typing import Any, Dict, Optional
from collections import OrderedDict
from threading import Lock
import logging

class LRUCache:
    """LRU Cache implementation"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self.cache = OrderedDict()
        self.timestamps = {}
        self.lock = Lock()
    
    def _hash_key(self, key: str) -> str:
        """Hash key for consistent storage"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _is_expired(self, key: str) -> bool:
        """Check if key is expired"""
        if key not in self.timestamps:
            return True
        return time.time() - self.timestamps[key] > self.ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            hashed_key = self._hash_key(key)
            
            if hashed_key not in self.cache:
                return None
            
            if self._is_expired(hashed_key):
                self._remove(hashed_key)
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(hashed_key)
            return self.cache[hashed_key]
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        with self.lock:
            hashed_key = self._hash_key(key)
            
            # Remove if exists
            if hashed_key in self.cache:
                self._remove(hashed_key)
            
            # Remove oldest if cache is full
            if len(self.cache) >= self.max_size:
                oldest_key = next(iter(self.cache))
                self._remove(oldest_key)
            
            # Add new item
            self.cache[hashed_key] = value
            self.timestamps[hashed_key] = time.time()
    
    def _remove(self, key: str) -> None:
        """Remove key from cache"""
        if key in self.cache:
            del self.cache[key]
        if key in self.timestamps:
            del self.timestamps[key]
    
    def clear(self) -> None:
        """Clear all cache"""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
    
    def size(self) -> int:
        """Get cache size"""
        return len(self.cache)
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'ttl': self.ttl,
                'hit_rate': 0  # TODO: Implement hit rate tracking
            }

class CacheManager:
    """Main cache manager for spell checker"""
    
    def __init__(self, enable_cache: bool = True, max_size: int = 1000, ttl: int = 3600):
        self.enable_cache = enable_cache
        self.cache = LRUCache(max_size, ttl) if enable_cache else None
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0
        }
        self.lock = Lock()
    
    def _generate_key(self, text: str, method: str = 'check_spelling') -> str:
        """Generate cache key"""
        content = f"{method}:{text}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, text: str, method: str = 'check_spelling') -> Optional[Dict]:
        """Get cached result"""
        if not self.enable_cache or not self.cache:
            return None
        
        key = self._generate_key(text, method)
        result = self.cache.get(key)
        
        with self.lock:
            if result is not None:
                self.stats['hits'] += 1
                logging.debug(f"Cache HIT for key: {key[:8]}...")
            else:
                self.stats['misses'] += 1
                logging.debug(f"Cache MISS for key: {key[:8]}...")
        
        return result
    
    def set(self, text: str, result: Dict, method: str = 'check_spelling') -> None:
        """Set cached result"""
        if not self.enable_cache or not self.cache:
            return
        
        key = self._generate_key(text, method)
        self.cache.set(key, result)
        
        with self.lock:
            self.stats['sets'] += 1
        
        logging.debug(f"Cache SET for key: {key[:8]}...")
    
    def clear(self) -> None:
        """Clear all cache"""
        if self.cache:
            self.cache.clear()
        with self.lock:
            self.stats = {'hits': 0, 'misses': 0, 'sets': 0}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'enabled': self.enable_cache,
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'sets': self.stats['sets'],
                'hit_rate': round(hit_rate, 2),
                'cache_size': self.cache.size() if self.cache else 0,
                'cache_stats': self.cache.stats() if self.cache else {}
            }
