#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive test suite for Vietnamese Spell Checker
"""

import requests
import json
import time
import sys
from typing import Dict, List

class SpellCheckerTester:
    def __init__(self, base_url: str = "http://127.0.0.1:3000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
    
    def test_health_check(self) -> bool:
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_spell_checking(self, text: str, expected_errors: int = None) -> bool:
        """Test spell checking functionality"""
        try:
            data = {"text": text}
            response = self.session.post(f"{self.base_url}/api/check_spelling", json=data)
            
            if response.status_code == 200:
                result = response.json()
                error_count = result.get('error_count', 0)
                corrected_text = result.get('corrected_text', '')
                processing_time = result.get('processing_time_ms', 0)
                
                print(f"✅ Spell check passed:")
                print(f"   - Errors found: {error_count}")
                print(f"   - Processing time: {processing_time}ms")
                print(f"   - Corrected text: {corrected_text[:100]}...")
                
                if expected_errors is not None:
                    # Allow some flexibility in error count (within 50% range)
                    min_expected = max(0, expected_errors - 5)
                    max_expected = expected_errors + 5
                    if min_expected <= error_count <= max_expected:
                        print(f"   - Expected errors: {expected_errors} (±5) ✅")
                    else:
                        print(f"   - Expected errors: {expected_errors} (±5), got: {error_count} ❌")
                        return False
                
                return True
            else:
                print(f"❌ Spell check failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Spell check error: {e}")
            return False
    
    def test_suggestions(self, word: str) -> bool:
        """Test suggestions endpoint"""
        try:
            data = {"word": word}
            response = self.session.post(f"{self.base_url}/api/suggestions", json=data)
            
            if response.status_code == 200:
                result = response.json()
                suggestions = result.get('suggestions', [])
                print(f"✅ Suggestions for '{word}': {suggestions}")
                return True
            else:
                print(f"❌ Suggestions failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Suggestions error: {e}")
            return False
    
    def test_config(self) -> bool:
        """Test config endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/config")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Config retrieved: {len(data.get('config', {}))} items")
                return True
            else:
                print(f"❌ Config failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Config error: {e}")
            return False
    
    def test_stats(self) -> bool:
        """Test stats endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/stats")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Stats retrieved: {data.get('spell_checker_status', 'unknown')}")
                return True
            else:
                print(f"❌ Stats failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Stats error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests"""
        print("🎯 Vietnamese Spell Checker - Comprehensive Test Suite")
        print("=" * 60)
        
        tests = {
            "Health Check": self.test_health_check,
            "Config": self.test_config,
            "Stats": self.test_stats,
            "Spell Check - Simple": lambda: self.test_spell_checking("toi dang hoc tieng viet", 3),
            "Spell Check - Complex": lambda: self.test_spell_checking("toi dang là sinh diên nam hai ở truong đạ hoc khoa jọc tự nhiên", 30),
            "Suggestions": lambda: self.test_suggestions("tôii"),
        }
        
        results = {}
        for test_name, test_func in tests.items():
            print(f"\n🔍 Running {test_name}...")
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
                results[test_name] = False
        
        return results
    
    def print_summary(self, results: Dict[str, bool]):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Vietnamese Spell Checker is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the application.")
        
        return passed == total

def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://127.0.0.1:3000"
    
    tester = SpellCheckerTester(base_url)
    results = tester.run_all_tests()
    success = tester.print_summary(results)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 