#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vietnamese Spell Checker - Demo Showcase
Script để demo tất cả các tính năng của ứng dụng
"""

import requests
import json
import time
from typing import Dict, List

class SpellCheckerDemo:
    def __init__(self, base_url: str = "http://127.0.0.1:3000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def print_header(self, title: str):
        """In header đẹp"""
        print(f"\n{'='*60}")
        print(f"🎯 {title}")
        print(f"{'='*60}")
    
    def print_success(self, message: str):
        """In thông báo thành công"""
        print(f"✅ {message}")
    
    def print_info(self, message: str):
        """In thông tin"""
        print(f"ℹ️  {message}")
    
    def demo_health_check(self):
        """Demo health check"""
        self.print_header("Health Check Demo")
        
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Server status: {data['status']}")
                self.print_info(f"Spell checker ready: {data['spell_checker_ready']}")
                self.print_info(f"Version: {data.get('version', 'N/A')}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def demo_spell_checking(self):
        """Demo spell checking"""
        self.print_header("Spell Checking Demo")
        
        test_cases = [
            {
                "title": "Văn bản đơn giản",
                "text": "toi dang hoc tieng viet",
                "expected_errors": 3
            },
            {
                "title": "Văn bản phức tạp",
                "text": "toi dang là sinh diên nam hai ở truong đạ hoc khoa jọc tự nhiên",
                "expected_errors": 8
            },
            {
                "title": "Văn bản có nhiều lỗi",
                "text": "tôii dangg họcc tiếngg việtt nam",
                "expected_errors": 5
            }
        ]
        
        for case in test_cases:
            print(f"\n📝 {case['title']}:")
            print(f"   Input: {case['text']}")
            
            try:
                data = {"text": case['text']}
                response = self.session.post(f"{self.base_url}/api/check_spelling", json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    error_count = result.get('error_count', 0)
                    corrected_text = result.get('corrected_text', '')
                    processing_time = result.get('processing_time_ms', 0)
                    
                    self.print_success(f"Found {error_count} errors in {processing_time}ms")
                    print(f"   Corrected: {corrected_text}")
                    
                    # Show some errors if any
                    errors = result.get('errors', [])
                    if errors:
                        print(f"   Sample errors:")
                        for error in errors[:3]:  # Show first 3 errors
                            print(f"     - '{error.get('word', '')}' → '{error.get('corrected', '')}' ({error.get('category', 'unknown')})")
                else:
                    print(f"❌ Spell check failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def demo_suggestions(self):
        """Demo suggestions"""
        self.print_header("Suggestions Demo")
        
        test_words = ["tôii", "họcc", "việtt", "nam", "truong"]
        
        for word in test_words:
            try:
                data = {"word": word}
                response = self.session.post(f"{self.base_url}/api/suggestions", json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    suggestions = result.get('suggestions', [])
                    self.print_success(f"Suggestions for '{word}': {suggestions}")
                else:
                    print(f"❌ Suggestions failed for '{word}': {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error getting suggestions for '{word}': {e}")
    
    def demo_config(self):
        """Demo config"""
        self.print_header("Configuration Demo")
        
        try:
            response = self.session.get(f"{self.base_url}/api/config")
            if response.status_code == 200:
                data = response.json()
                config = data.get('config', {})
                
                self.print_success("Configuration retrieved:")
                print(f"   Host: {config.get('host', 'N/A')}")
                print(f"   Port: {config.get('port', 'N/A')}")
                print(f"   Debug: {config.get('debug', 'N/A')}")
                print(f"   Max text length: {config.get('max_text_length', 'N/A')}")
                print(f"   Processing timeout: {config.get('processing_timeout', 'N/A')}")
                print(f"   Confidence threshold: {config.get('confidence_threshold', 'N/A')}")
            else:
                print(f"❌ Config failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Config error: {e}")
    
    def demo_stats(self):
        """Demo stats"""
        self.print_header("Statistics Demo")
        
        try:
            response = self.session.get(f"{self.base_url}/api/stats")
            if response.status_code == 200:
                data = response.json()
                
                self.print_success("Statistics retrieved:")
                print(f"   Spell checker status: {data.get('spell_checker_status', 'N/A')}")
                print(f"   Total requests: {data.get('total_requests', 'N/A')}")
                print(f"   Average processing time: {data.get('average_processing_time', 'N/A')}")
            else:
                print(f"❌ Stats failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Stats error: {e}")
    
    def demo_performance(self):
        """Demo performance"""
        self.print_header("Performance Demo")
        
        test_text = "toi dang hoc tieng viet va rat thich chuong trinh nay"
        
        print(f"📊 Testing performance with text: {test_text}")
        
        times = []
        for i in range(5):
            try:
                start_time = time.time()
                data = {"text": test_text}
                response = self.session.post(f"{self.base_url}/api/check_spelling", json=data)
                end_time = time.time()
                
                if response.status_code == 200:
                    processing_time = (end_time - start_time) * 1000
                    times.append(processing_time)
                    print(f"   Run {i+1}: {processing_time:.2f}ms")
                else:
                    print(f"   Run {i+1}: Failed")
                    
            except Exception as e:
                print(f"   Run {i+1}: Error - {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            self.print_success(f"Performance summary:")
            print(f"   Average time: {avg_time:.2f}ms")
            print(f"   Min time: {min_time:.2f}ms")
            print(f"   Max time: {max_time:.2f}ms")
    
    def run_full_demo(self):
        """Chạy toàn bộ demo"""
        print("🎯 Vietnamese Spell Checker - Full Demo Showcase")
        print("=" * 60)
        print("🚀 Starting comprehensive demo...")
        
        # Check if server is running
        if not self.demo_health_check():
            print("❌ Server is not running. Please start the server first:")
            print("   python app.py --port 3000 --host 127.0.0.1")
            return
        
        # Run all demos
        self.demo_spell_checking()
        self.demo_suggestions()
        self.demo_config()
        self.demo_stats()
        self.demo_performance()
        
        print(f"\n{'='*60}")
        print("🎉 Demo completed successfully!")
        print("🌐 Access the web interface at: http://127.0.0.1:3000")
        print("📚 Check the README.md for more information")
        print(f"{'='*60}")

def main():
    """Main function"""
    import sys
    
    base_url = "http://127.0.0.1:3000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    demo = SpellCheckerDemo(base_url)
    demo.run_full_demo()

if __name__ == "__main__":
    main() 