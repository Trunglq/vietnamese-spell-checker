#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file for Vietnamese Spell Checker
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class"""
    
    # Server Configuration
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 3000))
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Model Configuration
    MODEL_PATH = os.getenv('MODEL_PATH', '')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'spell_checker.log')
    
    # Performance Configuration
    MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', 10000))
    PROCESSING_TIMEOUT = int(os.getenv('PROCESSING_TIMEOUT', 30))
    
    # API Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', 100))
    
    # Spell Checker Configuration
    CONFIDENCE_THRESHOLD = 0.7
    MAX_SUGGESTIONS = 5
    
    # Cache Configuration
    ENABLE_CACHE = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hour
    CACHE_MAX_SIZE = int(os.getenv('CACHE_MAX_SIZE', 1000))
    
    # Performance Optimization
    ENABLE_COMPRESSION = os.getenv('ENABLE_COMPRESSION', 'true').lower() == 'true'
    ENABLE_ASYNC = os.getenv('ENABLE_ASYNC', 'true').lower() == 'true'
    WORKER_THREADS = int(os.getenv('WORKER_THREADS', 4))
    
    # Monitoring Configuration
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    METRICS_INTERVAL = int(os.getenv('METRICS_INTERVAL', 60))  # 1 minute
    
    @classmethod
    def get_config(cls):
        """Get configuration as dictionary"""
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': cls.DEBUG,
            'model_path': cls.MODEL_PATH,
            'log_level': cls.LOG_LEVEL,
            'log_file': cls.LOG_FILE,
            'max_text_length': cls.MAX_TEXT_LENGTH,
            'processing_timeout': cls.PROCESSING_TIMEOUT,
            'cors_origins': cls.CORS_ORIGINS,
            'rate_limit': cls.RATE_LIMIT,
            'confidence_threshold': cls.CONFIDENCE_THRESHOLD,
            'max_suggestions': cls.MAX_SUGGESTIONS,
            'enable_cache': cls.ENABLE_CACHE,
            'cache_ttl': cls.CACHE_TTL,
            'cache_max_size': cls.CACHE_MAX_SIZE,
            'enable_compression': cls.ENABLE_COMPRESSION,
            'enable_async': cls.ENABLE_ASYNC,
            'worker_threads': cls.WORKER_THREADS,
            'enable_metrics': cls.ENABLE_METRICS,
            'metrics_interval': cls.METRICS_INTERVAL
        } 