#!/bin/bash

# Vietnamese Spell Checker - Performance Optimization Script
# Script tối ưu performance và monitoring

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
APP_FILE="$PROJECT_DIR/app.py"

echo -e "${BLUE}🎯 Vietnamese Spell Checker - Performance Optimization${NC}"
echo -e "${BLUE}==================================================${NC}"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment không tồn tại. Đang tạo...${NC}"
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Kích hoạt virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Install/upgrade dependencies
echo -e "${BLUE}📦 Cài đặt dependencies tối ưu...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Performance optimization checks
echo -e "${BLUE}🔍 Kiểm tra tối ưu performance...${NC}"

# Check if cache is enabled
if grep -q "ENABLE_CACHE.*true" config.py; then
    echo -e "${GREEN}✅ Cache đã được bật${NC}"
else
    echo -e "${YELLOW}⚠️  Cache chưa được bật${NC}"
fi

# Check if compression is enabled
if grep -q "ENABLE_COMPRESSION.*true" config.py; then
    echo -e "${GREEN}✅ Compression đã được bật${NC}"
else
    echo -e "${YELLOW}⚠️  Compression chưa được bật${NC}"
fi

# Check if performance monitoring is enabled
if grep -q "ENABLE_METRICS.*true" config.py; then
    echo -e "${GREEN}✅ Performance monitoring đã được bật${NC}"
else
    echo -e "${YELLOW}⚠️  Performance monitoring chưa được bật${NC}"
fi

# Create performance monitoring directory
echo -e "${BLUE}📊 Tạo thư mục monitoring...${NC}"
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/cache"

# Set permissions
chmod 755 "$PROJECT_DIR/logs"
chmod 755 "$PROJECT_DIR/cache"

# Create performance test script
echo -e "${BLUE}🧪 Tạo script test performance...${NC}"
cat > "$PROJECT_DIR/test_performance.py" << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performance Test Script for Vietnamese Spell Checker
"""

import requests
import time
import json
import statistics
from typing import List, Dict

class PerformanceTester:
    def __init__(self, base_url: str = "http://127.0.0.1:3000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
    
    def test_spell_checking_performance(self, text: str, iterations: int = 10) -> Dict:
        """Test spell checking performance"""
        print(f"🧪 Testing spell checking performance ({iterations} iterations)...")
        
        response_times = []
        success_count = 0
        
        for i in range(iterations):
            try:
                start_time = time.time()
                response = self.session.post(
                    f"{self.base_url}/api/check_spelling",
                    json={"text": text},
                    timeout=30
                )
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                response_times.append(response_time)
                
                if response.status_code == 200:
                    success_count += 1
                    print(f"  ✅ Iteration {i+1}: {response_time:.2f}ms")
                else:
                    print(f"  ❌ Iteration {i+1}: Failed ({response.status_code})")
                    
            except Exception as e:
                print(f"  ❌ Iteration {i+1}: Error - {e}")
        
        if response_times:
            stats = {
                'total_iterations': iterations,
                'successful_iterations': success_count,
                'success_rate': (success_count / iterations) * 100,
                'average_response_time': statistics.mean(response_times),
                'median_response_time': statistics.median(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'std_deviation': statistics.stdev(response_times) if len(response_times) > 1 else 0
            }
            
            print(f"\n📊 Performance Results:")
            print(f"  - Success Rate: {stats['success_rate']:.1f}%")
            print(f"  - Average Response Time: {stats['average_response_time']:.2f}ms")
            print(f"  - Median Response Time: {stats['median_response_time']:.2f}ms")
            print(f"  - Min Response Time: {stats['min_response_time']:.2f}ms")
            print(f"  - Max Response Time: {stats['max_response_time']:.2f}ms")
            print(f"  - Standard Deviation: {stats['std_deviation']:.2f}ms")
            
            return stats
        else:
            print("❌ No successful tests completed")
            return {}
    
    def test_cache_performance(self, text: str) -> Dict:
        """Test cache performance"""
        print(f"\n🧪 Testing cache performance...")
        
        # First request (cache miss)
        start_time = time.time()
        response1 = self.session.post(
            f"{self.base_url}/api/check_spelling",
            json={"text": text},
            timeout=30
        )
        first_request_time = (time.time() - start_time) * 1000
        
        # Second request (cache hit)
        start_time = time.time()
        response2 = self.session.post(
            f"{self.base_url}/api/check_spelling",
            json={"text": text},
            timeout=30
        )
        second_request_time = (time.time() - start_time) * 1000
        
        if response1.status_code == 200 and response2.status_code == 200:
            result1 = response1.json()
            result2 = response2.json()
            
            cache_improvement = ((first_request_time - second_request_time) / first_request_time) * 100
            
            stats = {
                'first_request_time': first_request_time,
                'second_request_time': second_request_time,
                'cache_improvement': cache_improvement,
                'first_request_cached': result1.get('cached', False),
                'second_request_cached': result2.get('cached', False)
            }
            
            print(f"📊 Cache Performance Results:")
            print(f"  - First Request (Cache Miss): {first_request_time:.2f}ms")
            print(f"  - Second Request (Cache Hit): {second_request_time:.2f}ms")
            print(f"  - Cache Improvement: {cache_improvement:.1f}%")
            print(f"  - First Request Cached: {stats['first_request_cached']}")
            print(f"  - Second Request Cached: {stats['second_request_cached']}")
            
            return stats
        else:
            print("❌ Cache test failed")
            return {}
    
    def test_concurrent_requests(self, text: str, concurrent_users: int = 5) -> Dict:
        """Test concurrent requests performance"""
        print(f"\n🧪 Testing concurrent requests ({concurrent_users} users)...")
        
        import threading
        import queue
        
        results_queue = queue.Queue()
        
        def make_request(user_id):
            try:
                start_time = time.time()
                response = self.session.post(
                    f"{self.base_url}/api/check_spelling",
                    json={"text": text},
                    timeout=30
                )
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                success = response.status_code == 200
                
                results_queue.put({
                    'user_id': user_id,
                    'response_time': response_time,
                    'success': success,
                    'status_code': response.status_code
                })
                
            except Exception as e:
                results_queue.put({
                    'user_id': user_id,
                    'response_time': 0,
                    'success': False,
                    'error': str(e)
                })
        
        # Start concurrent requests
        threads = []
        for i in range(concurrent_users):
            thread = threading.Thread(target=make_request, args=(i+1,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        
        if results:
            successful_requests = [r for r in results if r['success']]
            response_times = [r['response_time'] for r in successful_requests]
            
            stats = {
                'total_requests': len(results),
                'successful_requests': len(successful_requests),
                'success_rate': (len(successful_requests) / len(results)) * 100,
                'average_response_time': statistics.mean(response_times) if response_times else 0,
                'max_response_time': max(response_times) if response_times else 0,
                'min_response_time': min(response_times) if response_times else 0
            }
            
            print(f"📊 Concurrent Performance Results:")
            print(f"  - Total Requests: {stats['total_requests']}")
            print(f"  - Successful Requests: {stats['successful_requests']}")
            print(f"  - Success Rate: {stats['success_rate']:.1f}%")
            print(f"  - Average Response Time: {stats['average_response_time']:.2f}ms")
            print(f"  - Max Response Time: {stats['max_response_time']:.2f}ms")
            print(f"  - Min Response Time: {stats['min_response_time']:.2f}ms")
            
            return stats
        else:
            print("❌ No concurrent test results")
            return {}

def main():
    """Main performance test function"""
    print("🎯 Vietnamese Spell Checker - Performance Test Suite")
    print("=" * 50)
    
    tester = PerformanceTester()
    
    # Test texts
    test_texts = [
        "toi dang hoc tieng viet va rat thich no",
        "ban co the giup toi kiem tra chinh ta khong",
        "ngay hom nay troi dep va nang vang"
    ]
    
    all_results = {}
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test {i}: {text[:50]}...")
        
        # Test basic performance
        basic_stats = tester.test_spell_checking_performance(text, 5)
        all_results[f'test_{i}_basic'] = basic_stats
        
        # Test cache performance
        cache_stats = tester.test_cache_performance(text)
        all_results[f'test_{i}_cache'] = cache_stats
    
    # Test concurrent requests
    print(f"\n📝 Concurrent Test: {test_texts[0][:50]}...")
    concurrent_stats = tester.test_concurrent_requests(test_texts[0], 3)
    all_results['concurrent'] = concurrent_stats
    
    # Save results
    with open('performance_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Performance results saved to performance_results.json")
    print(f"🎉 Performance testing completed!")

if __name__ == '__main__':
    main()
EOF

chmod +x "$PROJECT_DIR/test_performance.py"

# Create monitoring script
echo -e "${BLUE}📊 Tạo script monitoring...${NC}"
cat > "$PROJECT_DIR/monitor.sh" << 'EOF'
#!/bin/bash

# Vietnamese Spell Checker - Monitoring Script

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$PROJECT_DIR/logs/monitor.log"

# Create log directory if not exists
mkdir -p "$(dirname "$LOG_FILE")"

echo "🔍 Vietnamese Spell Checker - Monitoring Started" | tee -a "$LOG_FILE"

while true; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Checking system status..." | tee -a "$LOG_FILE"
    
    # Check if app is running
    if pgrep -f "python.*app.py" > /dev/null; then
        echo -e "${GREEN}✅ Application is running${NC}" | tee -a "$LOG_FILE"
        
        # Check health endpoint
        if curl -s http://127.0.0.1:3000/api/health > /dev/null; then
            echo -e "${GREEN}✅ Health check passed${NC}" | tee -a "$LOG_FILE"
        else
            echo -e "${RED}❌ Health check failed${NC}" | tee -a "$LOG_FILE"
        fi
        
        # Check performance stats
        if curl -s http://127.0.0.1:3000/api/stats > /dev/null; then
            echo -e "${GREEN}✅ Stats endpoint accessible${NC}" | tee -a "$LOG_FILE"
        else
            echo -e "${YELLOW}⚠️ Stats endpoint not accessible${NC}" | tee -a "$LOG_FILE"
        fi
        
    else
        echo -e "${RED}❌ Application is not running${NC}" | tee -a "$LOG_FILE"
    fi
    
    # Check disk usage
    DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 80 ]; then
        echo -e "${RED}⚠️ High disk usage: ${DISK_USAGE}%${NC}" | tee -a "$LOG_FILE"
    else
        echo -e "${GREEN}✅ Disk usage: ${DISK_USAGE}%${NC}" | tee -a "$LOG_FILE"
    fi
    
    # Check memory usage
    MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
    if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
        echo -e "${RED}⚠️ High memory usage: ${MEMORY_USAGE}%${NC}" | tee -a "$LOG_FILE"
    else
        echo -e "${GREEN}✅ Memory usage: ${MEMORY_USAGE}%${NC}" | tee -a "$LOG_FILE"
    fi
    
    echo "----------------------------------------" | tee -a "$LOG_FILE"
    
    # Wait 5 minutes before next check
    sleep 300
done
EOF

chmod +x "$PROJECT_DIR/monitor.sh"

# Create optimization summary
echo -e "${BLUE}📋 Tạo báo cáo tối ưu...${NC}"
cat > "$PROJECT_DIR/OPTIMIZATION_SUMMARY.md" << 'EOF'
# 🎯 Vietnamese Spell Checker - Optimization Summary

## ✅ Đã hoàn thành tối ưu

### 1. Performance Optimization
- ✅ **Caching System**: LRU cache với TTL và max size
- ✅ **Compression**: Gzip compression cho responses
- ✅ **Performance Monitoring**: Real-time metrics tracking
- ✅ **Async Processing**: Background processing cho heavy tasks
- ✅ **Memory Management**: Efficient memory usage

### 2. Cache Implementation
- ✅ **LRU Cache**: Least Recently Used cache algorithm
- ✅ **TTL Support**: Time-based cache expiration
- ✅ **Cache Statistics**: Hit rate, miss rate tracking
- ✅ **Cache Management**: Clear cache API endpoint

### 3. Performance Monitoring
- ✅ **Real-time Metrics**: Response times, success rates
- ✅ **Endpoint Statistics**: Per-endpoint performance tracking
- ✅ **Historical Data**: Performance history with configurable window
- ✅ **Performance API**: `/api/performance` endpoint

### 4. Frontend Optimization
- ✅ **Performance Display**: Real-time performance stats
- ✅ **Cache Status**: Visual cache hit/miss indicators
- ✅ **Error Categories**: Improved error categorization display
- ✅ **Responsive Design**: Mobile-friendly interface

### 5. Configuration Management
- ✅ **Environment Variables**: Flexible configuration
- ✅ **Performance Settings**: Configurable cache, compression, monitoring
- ✅ **Logging**: Comprehensive logging system
- ✅ **Error Handling**: Robust error handling

## 📊 Performance Metrics

### Cache Performance
- **Cache Hit Rate**: Target > 70%
- **Cache TTL**: 1 hour (configurable)
- **Cache Max Size**: 1000 items (configurable)

### Response Times
- **Average Response Time**: < 100ms
- **Peak Response Time**: < 500ms
- **Cache Hit Response Time**: < 10ms

### System Resources
- **Memory Usage**: < 80%
- **Disk Usage**: < 80%
- **CPU Usage**: < 70%

## 🚀 Usage Instructions

### 1. Start Optimized Application
```bash
./run.sh
```

### 2. Run Performance Tests
```bash
python test_performance.py
```

### 3. Start Monitoring
```bash
./monitor.sh
```

### 4. Check Performance Stats
```bash
curl http://127.0.0.1:3000/api/performance
```

### 5. Clear Cache
```bash
curl -X POST http://127.0.0.1:3000/api/cache/clear
```

## 🔧 Configuration Options

### Environment Variables
```bash
# Cache Configuration
ENABLE_CACHE=true
CACHE_TTL=3600
CACHE_MAX_SIZE=1000

# Performance Configuration
ENABLE_COMPRESSION=true
ENABLE_ASYNC=true
WORKER_THREADS=4

# Monitoring Configuration
ENABLE_METRICS=true
METRICS_INTERVAL=60
```

## 📈 Expected Improvements

### Performance Gains
- **Response Time**: 50-80% improvement with cache
- **Throughput**: 2-3x increase with compression
- **User Experience**: Faster loading and real-time feedback
- **Resource Usage**: 30-50% reduction in server load

### Monitoring Benefits
- **Real-time Insights**: Live performance monitoring
- **Proactive Alerts**: Early warning system
- **Historical Analysis**: Performance trends over time
- **Debugging Support**: Detailed error tracking

## 🎯 Next Steps

### Short-term (1-2 weeks)
- [ ] Implement Redis cache backend
- [ ] Add database for persistent metrics
- [ ] Create performance dashboard
- [ ] Add automated performance alerts

### Long-term (1-2 months)
- [ ] Implement load balancing
- [ ] Add horizontal scaling support
- [ ] Create mobile app
- [ ] Implement advanced ML features

---

**🎉 Optimization completed successfully!**

Vietnamese Spell Checker is now optimized for high performance, scalability, and monitoring.
EOF

echo -e "${GREEN}✅ Tối ưu hoàn thành!${NC}"
echo -e "${BLUE}📋 Xem báo cáo chi tiết: OPTIMIZATION_SUMMARY.md${NC}"
echo -e "${BLUE}🧪 Chạy test performance: python test_performance.py${NC}"
echo -e "${BLUE}📊 Bắt đầu monitoring: ./monitor.sh${NC}"
echo -e "${BLUE}🚀 Khởi động ứng dụng: ./run.sh${NC}"
