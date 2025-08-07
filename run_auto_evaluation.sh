#!/bin/bash

# Vietnamese Spell Checker - Auto Evaluation Runner
# Script chạy đánh giá tự động và hiển thị kết quả

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
TEST_FILE="$PROJECT_DIR/test_auto_evaluation.py"

echo -e "${BLUE}🎯 Vietnamese Spell Checker - Auto Evaluation Runner${NC}"
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
echo -e "${BLUE}📦 Cài đặt dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Check if server is running
echo -e "${BLUE}🔍 Kiểm tra server...${NC}"
if curl -s http://127.0.0.1:3000/api/health > /dev/null; then
    echo -e "${GREEN}✅ Server đang chạy${NC}"
else
    echo -e "${YELLOW}⚠️  Server chưa chạy. Đang khởi động...${NC}"
    echo -e "${BLUE}💡 Chạy lệnh sau trong terminal khác:${NC}"
    echo -e "${GREEN}   ./run.sh${NC}"
    echo -e "${BLUE}   Hoặc: python app.py${NC}"
    echo ""
    read -p "Nhấn Enter khi server đã chạy..."
fi

# Run auto evaluation
echo -e "${BLUE}🧪 Chạy đánh giá tự động...${NC}"
python "$TEST_FILE"

echo -e "${GREEN}✅ Hoàn thành đánh giá tự động!${NC}"
echo -e "${BLUE}📁 Kết quả chi tiết đã được lưu trong thư mục hiện tại${NC}"
