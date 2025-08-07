#!/bin/bash

# Vietnamese Spell Checker - GPT-OSS
# Script khởi động cải tiến

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
PORT=${PORT:-3000}
HOST=${HOST:-127.0.0.1}

echo -e "${BLUE}🎯 Vietnamese Spell Checker - GPT-OSS${NC}"
echo -e "${BLUE}================================${NC}"

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

# Check if app.py exists
if [ ! -f "$APP_FILE" ]; then
    echo -e "${RED}❌ Không tìm thấy app.py${NC}"
    exit 1
fi

# Kill any existing processes
echo -e "${YELLOW}🔄 Dừng các process cũ...${NC}"
pkill -f "python.*app.py" || true
sleep 2

# Start the application
echo -e "${GREEN}🚀 Khởi động Vietnamese Spell Checker...${NC}"
echo -e "${BLUE}📝 Truy cập: http://$HOST:$PORT${NC}"
echo -e "${BLUE}🔍 Health check: http://$HOST:$PORT/api/health${NC}"
echo -e "${YELLOW}💡 Nhấn Ctrl+C để dừng${NC}"
echo ""

# Run the application
python "$APP_FILE" --port "$PORT" --host "$HOST" 