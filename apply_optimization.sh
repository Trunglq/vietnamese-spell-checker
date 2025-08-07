#!/bin/bash

# Vietnamese Spell Checker - Apply Optimization Script
# Generated on 2025-08-07 12:31:45

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎯 Vietnamese Spell Checker - Apply Optimization${NC}"
echo -e "${BLUE}==============================================${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment không tồn tại. Đang tạo...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Kích hoạt virtual environment...${NC}"
source venv/bin/activate

# Install dependencies if needed
echo -e "${BLUE}📦 Cài đặt dependencies...${NC}"
pip install -r requirements.txt

# Backup current config
echo -e "${BLUE}💾 Backup cấu hình hiện tại...${NC}"
if [ -f ".env" ]; then
    cp .env .env.backup
    echo -e "${GREEN}✅ Backup created: .env.backup${NC}"
fi

# Apply optimized config
echo -e "${BLUE}⚙️  Áp dụng cấu hình tối ưu...${NC}"
if [ -f ".env.optimized" ]; then
    cp .env.optimized .env
    echo -e "${GREEN}✅ Optimized config applied${NC}"
else
    echo -e "${RED}❌ File .env.optimized không tồn tại${NC}"
    exit 1
fi

# Restart application
echo -e "${BLUE}🔄 Khởi động lại ứng dụng...${NC}"
pkill -f "python app.py" || true
sleep 2

# Start application with optimized config
echo -e "${BLUE}🚀 Khởi động ứng dụng với cấu hình tối ưu...${NC}"
python app.py --port 3000 --host 127.0.0.1 &

# Wait for application to start
sleep 5

# Test application
echo -e "${BLUE}🧪 Test ứng dụng...${NC}"
if curl -s http://127.0.0.1:3000/api/health | grep -q "ok"; then
    echo -e "${GREEN}✅ Ứng dụng đã khởi động thành công${NC}"
else
    echo -e "${RED}❌ Ứng dụng khởi động thất bại${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Tối ưu hóa đã được áp dụng thành công!${NC}"
echo -e "${BLUE}📊 Truy cập: http://127.0.0.1:3000${NC}"
