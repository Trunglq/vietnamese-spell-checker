#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
import subprocess
import threading
import time
import argparse
import importlib
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from flask_compress import Compress

# Import configuration
from config import Config
from cache_manager import CacheManager
from performance_monitor import PerformanceMonitor

# Import và reload module để đảm bảo phiên bản mới nhất
import categorized_spell_checker
importlib.reload(categorized_spell_checker)
from categorized_spell_checker import categorized_spell_checker

# Cấu hình logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app, origins=Config.CORS_ORIGINS.split(','))

# Enable compression if configured
if Config.ENABLE_COMPRESSION:
    Compress(app)

# Initialize cache manager
cache_manager = CacheManager(
    enable_cache=Config.ENABLE_CACHE,
    max_size=Config.CACHE_MAX_SIZE,
    ttl=Config.CACHE_TTL
)

# Initialize performance monitor
performance_monitor = PerformanceMonitor(max_history=1000)

# Sử dụng categorized spell checker
spell_checker = categorized_spell_checker

# Performance monitoring
performance_stats = {
    'total_requests': 0,
    'total_processing_time': 0,
    'average_processing_time': 0,
    'start_time': time.time()
}

def initialize_spell_checker():
    """Khởi tạo spell checker với GPT-OSS"""
    global spell_checker
    try:
        logging.info("🔄 Đang khởi tạo Categorized Vietnamese Spell Checker...")
        # Spell checker đã được khởi tạo sẵn
        logging.info("✅ Categorized spell checker đã sẵn sàng!")
    except Exception as e:
        logging.error(f"❌ Lỗi khởi tạo spell checker: {e}")

def update_performance_stats(processing_time: float):
    """Update performance statistics"""
    performance_stats['total_requests'] += 1
    performance_stats['total_processing_time'] += processing_time
    performance_stats['average_processing_time'] = (
        performance_stats['total_processing_time'] / performance_stats['total_requests']
    )

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/api/check_spelling', methods=['POST'])
def check_spelling():
    """API kiểm tra chính tả với caching và performance monitoring"""
    start_time = time.time()
    success = False
    cached = False
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dữ liệu JSON không hợp lệ'}), 400
        
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Vui lòng nhập văn bản'}), 400
        
        # Kiểm tra độ dài văn bản
        if len(text) > Config.MAX_TEXT_LENGTH:
            return jsonify({'error': f'Văn bản quá dài. Tối đa {Config.MAX_TEXT_LENGTH} ký tự'}), 400
        
        if not spell_checker:
            return jsonify({'error': 'Spell checker chưa sẵn sàng'}), 500
        
        # Check cache first
        cached_result = cache_manager.get(text, 'check_spelling')
        if cached_result:
            logging.info(f"📝 Cache HIT for text: {text[:50]}...")
            cached = True
            success = True
            performance_monitor.record_request('/api/check_spelling', time.time() - start_time, success, cached)
            return jsonify(cached_result)
        
        # Log request
        logging.info(f"📝 Kiểm tra chính tả: {text[:50]}...")
        
        # Kiểm tra chính tả với timeout
        result = spell_checker.check_text(text)
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Update performance stats
        update_performance_stats(processing_time)
        
        # Thêm thông tin processing time
        result['processing_time_ms'] = round(processing_time, 2)
        result['timestamp'] = datetime.now().isoformat()
        result['text_length'] = len(text)
        result['cached'] = False
        
        # Cache the result
        cache_manager.set(text, result, 'check_spelling')
        
        success = True
        logging.info(f"✅ Hoàn thành kiểm tra: {result.get('error_count', 0)} lỗi, {processing_time:.2f}ms")
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"❌ Lỗi kiểm tra chính tả: {str(e)}")
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500
    finally:
        # Record performance metrics
        performance_monitor.record_request('/api/check_spelling', time.time() - start_time, success, cached)

@app.route('/api/health')
def health_check():
    """Kiểm tra trạng thái hệ thống"""
    try:
        uptime = time.time() - performance_stats['start_time']
        overall_stats = performance_monitor.get_overall_stats()
        
        return jsonify({
            'status': 'healthy',
            'spell_checker_ready': spell_checker is not None,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'uptime': round(uptime, 2),
            'config': Config.get_config(),
            'cache_stats': cache_manager.get_stats(),
            'performance_stats': overall_stats
        })
    except Exception as e:
        logging.error(f"❌ Lỗi health check: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """API lấy gợi ý sửa lỗi với caching và performance monitoring"""
    start_time = time.time()
    success = False
    cached = False
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dữ liệu JSON không hợp lệ'}), 400
        
        word = data.get('word', '')
        
        if not word:
            return jsonify({'error': 'Vui lòng nhập từ cần gợi ý'}), 400
        
        if not spell_checker:
            return jsonify({'error': 'Spell checker chưa sẵn sàng'}), 500
        
        # Check cache first
        cached_result = cache_manager.get(word, 'suggestions')
        if cached_result:
            cached = True
            success = True
            performance_monitor.record_request('/api/suggestions', time.time() - start_time, success, cached)
            return jsonify(cached_result)
        
        # Lấy gợi ý
        suggestions = spell_checker.get_suggestions(word)
        
        result = {
            'word': word,
            'suggestions': suggestions[:Config.MAX_SUGGESTIONS],
            'timestamp': datetime.now().isoformat(),
            'cached': False
        }
        
        # Cache the result
        cache_manager.set(word, result, 'suggestions')
        
        success = True
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"❌ Lỗi lấy gợi ý: {str(e)}")
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500
    finally:
        # Record performance metrics
        performance_monitor.record_request('/api/suggestions', time.time() - start_time, success, cached)

@app.route('/api/stats')
def get_stats():
    """API lấy thống kê hệ thống"""
    try:
        uptime = time.time() - performance_stats['start_time']
        overall_stats = performance_monitor.get_overall_stats()
        recent_stats = performance_monitor.get_stats(3600)  # Last hour
        
        return jsonify({
            'total_requests': overall_stats['total_requests'],
            'average_processing_time': round(overall_stats['average_response_time'], 2),
            'spell_checker_status': 'ready' if spell_checker else 'not_ready',
            'uptime': round(uptime, 2),
            'timestamp': datetime.now().isoformat(),
            'cache_stats': cache_manager.get_stats(),
            'performance_stats': overall_stats,
            'recent_stats': recent_stats,
            'config': Config.get_config()
        })
    except Exception as e:
        logging.error(f"❌ Lỗi lấy thống kê: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/config')
def get_config():
    """API lấy cấu hình hệ thống"""
    try:
        return jsonify({
            'config': Config.get_config(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"❌ Lỗi lấy cấu hình: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """API xóa cache"""
    try:
        cache_manager.clear()
        logging.info("🗑️ Cache đã được xóa")
        return jsonify({
            'message': 'Cache đã được xóa thành công',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"❌ Lỗi xóa cache: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance', methods=['GET'])
def get_performance():
    """API lấy thông tin performance chi tiết"""
    try:
        time_window = request.args.get('window', 3600, type=int)
        endpoint = request.args.get('endpoint', None)
        
        if endpoint:
            stats = performance_monitor.get_endpoint_performance(endpoint, time_window)
        else:
            stats = performance_monitor.get_stats(time_window)
        
        return jsonify({
            'performance_stats': stats,
            'timestamp': datetime.now().isoformat(),
            'time_window': time_window
        })
    except Exception as e:
        logging.error(f"❌ Lỗi lấy performance: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auto_evaluate', methods=['POST'])
def auto_evaluate():
    """API chạy đánh giá tự động"""
    try:
        from test_auto_evaluation import AutoEvaluator
        
        # Khởi tạo evaluator
        evaluator = AutoEvaluator(base_url=f"http://{request.host}")
        
        # Chạy đánh giá
        results = evaluator.run_all_tests()
        
        # Lưu kết quả
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_results_{timestamp}.json"
        evaluator.save_results(results, filename)
        
        return jsonify({
            'success': True,
            'results': results,
            'filename': filename,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"❌ Lỗi auto evaluation: {str(e)}")
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """Xử lý lỗi 404"""
    return jsonify({'error': 'Endpoint không tồn tại'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Xử lý lỗi 500"""
    logging.error(f"❌ Lỗi server: {str(error)}")
    return jsonify({'error': 'Lỗi server nội bộ'}), 500

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Vietnamese Spell Checker with GPT-OSS')
    parser.add_argument('--model', type=str, help='Path to GGUF model file')
    parser.add_argument('--host', type=str, default=Config.HOST, help='Host to bind to')
    parser.add_argument('--port', type=int, default=Config.PORT, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Set model path if provided
    if args.model:
        os.environ['MODEL_PATH'] = args.model
        logging.info(f"📁 Sử dụng mô hình: {args.model}")
    
    # Khởi tạo spell checker trong thread riêng
    init_thread = threading.Thread(target=initialize_spell_checker)
    init_thread.start()
    
    logging.info("🚀 Khởi động Vietnamese Spell Checker...")
    logging.info(f"📝 Truy cập: http://{args.host}:{args.port}")
    logging.info(f"🔧 Cấu hình: {Config.get_config()}")
    logging.info(f"💾 Cache: {'Bật' if Config.ENABLE_CACHE else 'Tắt'}")
    logging.info(f"🗜️ Compression: {'Bật' if Config.ENABLE_COMPRESSION else 'Tắt'}")
    logging.info(f"📊 Performance Monitoring: {'Bật' if Config.ENABLE_METRICS else 'Tắt'}")
    
    app.run(debug=args.debug or Config.DEBUG, host=args.host, port=args.port) 