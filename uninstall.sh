#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# GEO-SEO Claude Code 技能解除安裝工具
# ============================================================

CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"

# 偵測是否透過 curl pipe 執行 (無法使用互動式輸入)
INTERACTIVE=true
if [ ! -t 0 ]; then
    INTERACTIVE=false
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 確保未匹配的 glob 展開為空
shopt -s nullglob

echo ""
echo -e "${YELLOW}GEO-SEO Claude Code 技能解除安裝工具${NC}"
echo ""
echo "這將會移除以下項目："
echo ""

# 列出將被移除的項目
[ -d "$SKILLS_DIR/geo" ] && echo "  → ${SKILLS_DIR}/geo/"
for skill_dir in "$SKILLS_DIR"/geo-*/; do
    [ -d "$skill_dir" ] && echo "  → ${skill_dir}"
done
for agent_file in "$AGENTS_DIR"/geo-*.md; do
    [ -f "$agent_file" ] && echo "  → ${agent_file}"
done

echo ""
if [ "$INTERACTIVE" = true ]; then
    read -p "您確定要解除安裝嗎？(y/n)： " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "解除安裝已取消。"
        exit 0
    fi
else
    echo -e "${YELLOW}非互動模式 — 繼續解除安裝...${NC}"
fi

echo ""

# 移除主要技能
if [ -d "$SKILLS_DIR/geo" ]; then
    rm -rf "$SKILLS_DIR/geo"
    echo -e "${GREEN}✓ 已移除主要技能${NC}"
fi

# 移除子技能
for skill_dir in "$SKILLS_DIR"/geo-*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        rm -rf "$skill_dir"
        echo -e "${GREEN}✓ 已移除 ${skill_name}${NC}"
    fi
done

# 移除代理 (agents)
for agent_file in "$AGENTS_DIR"/geo-*.md; do
    if [ -f "$agent_file" ]; then
        agent_name=$(basename "$agent_file")
        rm -f "$agent_file"
        echo -e "${GREEN}✓ 已移除 ${agent_name}${NC}"
    fi
done

echo ""
echo -e "${GREEN}GEO-SEO 技能已成功解除安裝。${NC}"
echo ""
echo "注意：Python 相依套件存在於技能目錄內獨立的 venv 中，"
echo "因此它們已自動被移除。您的系統 Python 中"
echo "不需要清理任何東西。"
echo ""
echo "注意：位於 ~/.geo-prospects/ 的潛在客戶 (Prospect) 資料尚未移除。"
echo "若要手動移除它，請執行："
echo "  rm -rf ~/.geo-prospects"
echo ""
