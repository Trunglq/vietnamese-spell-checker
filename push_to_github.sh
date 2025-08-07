#!/bin/bash

# Vietnamese Spell Checker - Push to GitHub Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎯 Vietnamese Spell Checker - Push to GitHub${NC}"
echo -e "${BLUE}==========================================${NC}"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Git repository chưa được khởi tạo${NC}"
    exit 1
fi

# Check if there are commits
if ! git rev-parse HEAD >/dev/null 2>&1; then
    echo -e "${RED}❌ Chưa có commit nào${NC}"
    exit 1
fi

# Get current status
echo -e "${BLUE}📊 Kiểm tra trạng thái git...${NC}"
git status

# Ask for GitHub username
echo -e "${YELLOW}⚠️  Vui lòng nhập username GitHub của bạn:${NC}"
read -p "GitHub Username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo -e "${RED}❌ Username không được để trống${NC}"
    exit 1
fi

# Set remote URL
REMOTE_URL="https://github.com/$GITHUB_USERNAME/vietnamese-spell-checker.git"

echo -e "${BLUE}🔗 Đang thêm remote: $REMOTE_URL${NC}"
git remote add origin "$REMOTE_URL"

# Check if remote was added successfully
if ! git remote get-url origin >/dev/null 2>&1; then
    echo -e "${RED}❌ Không thể thêm remote${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Remote đã được thêm thành công${NC}"

# Push to GitHub
echo -e "${BLUE}🚀 Đang push code lên GitHub...${NC}"
git push -u origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}🎉 Code đã được push thành công lên GitHub!${NC}"
    echo -e "${BLUE}📝 Repository URL: https://github.com/$GITHUB_USERNAME/vietnamese-spell-checker${NC}"
    echo -e "${BLUE}🔗 Clone URL: $REMOTE_URL${NC}"
else
    echo -e "${RED}❌ Lỗi khi push code lên GitHub${NC}"
    echo -e "${YELLOW}💡 Hãy kiểm tra:${NC}"
    echo -e "  1. Repository đã được tạo trên GitHub chưa?"
    echo -e "  2. Username GitHub có đúng không?"
    echo -e "  3. Bạn có quyền push vào repository không?"
    exit 1
fi

echo -e "${GREEN}✅ Hoàn thành! Vietnamese Spell Checker đã được đẩy lên GitHub.${NC}"
