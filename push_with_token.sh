#!/bin/bash

# Vietnamese Spell Checker - Push with Token Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎯 Vietnamese Spell Checker - Push with Token${NC}"
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

# Ask for GitHub token
echo -e "${YELLOW}⚠️  Vui lòng nhập Personal Access Token của GitHub:${NC}"
echo -e "${BLUE}💡 Tạo token tại: https://github.com/settings/tokens${NC}"
read -p "GitHub Token: " GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ Token không được để trống${NC}"
    exit 1
fi

# Set remote URL with token
REMOTE_URL="https://${GITHUB_TOKEN}@github.com/Trunglq/vietnamese-spell-checker.git"

echo -e "${BLUE}🔗 Đang cập nhật remote với token...${NC}"
git remote set-url origin "$REMOTE_URL"

# Check if remote was updated successfully
if ! git remote get-url origin >/dev/null 2>&1; then
    echo -e "${RED}❌ Không thể cập nhật remote${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Remote đã được cập nhật thành công${NC}"

# Push to GitHub
echo -e "${BLUE}🚀 Đang push code lên GitHub...${NC}"
git push -u origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}🎉 Code đã được push thành công lên GitHub!${NC}"
    echo -e "${BLUE}📝 Repository URL: https://github.com/Trunglq/vietnamese-spell-checker${NC}"
    echo -e "${BLUE}🔗 Clone URL: https://github.com/Trunglq/vietnamese-spell-checker.git${NC}"
else
    echo -e "${RED}❌ Lỗi khi push code lên GitHub${NC}"
    echo -e "${YELLOW}💡 Hãy kiểm tra:${NC}"
    echo -e "  1. Repository đã được tạo trên GitHub chưa?"
    echo -e "  2. Token có đúng quyền không?"
    echo -e "  3. Token có hết hạn không?"
    exit 1
fi

echo -e "${GREEN}✅ Hoàn thành! Vietnamese Spell Checker đã được đẩy lên GitHub.${NC}"
