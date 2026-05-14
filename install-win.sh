#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# GEO-SEO Claude Code 技能安裝工具 — Windows (Git Bash)
# 請從 Git Bash 執行此腳本，不要使用 PowerShell 或 CMD。
# ============================================================

REPO_URL="https://github.com/gtut-nick/geo-seo-claude.git"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"
INSTALL_DIR="${SKILLS_DIR}/geo"
TEMP_DIR=$(mktemp -d)

# 偵測是否透過 curl pipe 執行 (無法使用互動式輸入)
INTERACTIVE=true
if [ ! -t 0 ]; then
    INTERACTIVE=false
fi

# 輸出顏色設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 無顏色

print_header() {
    echo ""
    echo -e "${BLUE}+------------------------------------------+${NC}"
    echo -e "${BLUE}|   GEO-SEO Claude Code 技能安裝工具       |${NC}"
    echo -e "${BLUE}|   以 GEO 為優先的 AI 搜尋優化            |${NC}"
    echo -e "${BLUE}|   Windows / Git Bash 版本                |${NC}"
    echo -e "${BLUE}+------------------------------------------+${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!!] $1${NC}"
}

print_error() {
    echo -e "${RED}[XX] $1${NC}"
}

print_info() {
    echo -e "${BLUE}[>>] $1${NC}"
}

cleanup() {
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

main() {
    print_header

    # ---- 驗證 Git Bash 環境 ----
    if [[ "${OSTYPE:-}" != "msys" && "${OSTYPE:-}" != "cygwin" && -z "${WINDIR:-}" ]]; then
        print_warning "無法確認是否為 Windows/Git Bash 環境。"
        print_warning "如果您使用的是 Linux/macOS，請改用 install.sh。"
        echo ""
    fi

    if [[ "$(uname -s 2>/dev/null)" != MINGW* ]] && \
       [[ "$(uname -s 2>/dev/null)" != CYGWIN* ]] && \
       [[ "$(uname -s 2>/dev/null)" != MSYS* ]] && \
       [[ -z "${WINDIR:-}" ]]; then
        print_info "偵測到非 Windows 環境 — 建議使用 install.sh"
    fi

    # ---- 檢查必備條件 ----
    print_info "正在檢查必備條件..."

    # 檢查 Git
    if ! command -v git &> /dev/null; then
        print_error "需要 Git 但尚未安裝。"
        echo "  安裝 Git for Windows：https://git-scm.com/downloads"
        exit 1
    fi
    print_success "找到 Git：$(git --version)"

    # 檢查 Python 3
    # 在 Windows 上，'python' 通常就是 Python 3；'python3' 可能不存在。
    PYTHON_CMD=""
    for cmd in python3 python py; do
        if command -v "$cmd" &> /dev/null; then
            _ver=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1 || true)
            if [ -n "$_ver" ]; then
                _major=$(echo "$_ver" | cut -d. -f1)
                _minor=$(echo "$_ver" | cut -d. -f2)
                if [ "$_major" -ge 3 ] && [ "$_minor" -ge 8 ]; then
                    PYTHON_CMD="$cmd"
                    break
                fi
            fi
        fi
    done

    if [ -z "$PYTHON_CMD" ]; then
        print_error "需要 Python 3.8+ 但尚未找到。"
        echo "  安裝：https://www.python.org/downloads/"
        echo "  安裝時請務必勾選 'Add Python to PATH' (將 Python 加入 PATH)。"
        exit 1
    fi
    print_success "找到 Python：$($PYTHON_CMD --version)"

    # 檢查 Claude Code
    if ! command -v claude &> /dev/null; then
        print_warning "在 PATH 中找不到 Claude Code CLI。"
        echo "  此工具需要 Claude Code 才能運作。"
        echo "  安裝：npm install -g @anthropic-ai/claude-code"
        echo ""
        if [ "$INTERACTIVE" = true ]; then
            read -r -p "是否仍要繼續安裝？(y/n)：" REPLY
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        else
            print_info "非互動模式 — 繼續安裝..."
        fi
    else
        print_success "找到 Claude Code CLI"
    fi

    # ---- 建立目錄 ----
    print_info "正在建立目錄..."

    mkdir -p "$SKILLS_DIR"
    mkdir -p "$AGENTS_DIR"
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR/scripts"
    mkdir -p "$INSTALL_DIR/schema"
    mkdir -p "$INSTALL_DIR/hooks"

    print_success "目錄結構建立完成於：$CLAUDE_DIR"

    # ---- 複製或拷貝儲存庫 ----
    print_info "正在取得 GEO-SEO 技能檔案..."

    SCRIPT_DIR=""
    if [ -n "${BASH_SOURCE[0]:-}" ] && [ "${BASH_SOURCE[0]}" != "bash" ]; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)" || true
    fi

    if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/geo/SKILL.md" ]; then
        print_info "從本機目錄安裝..."
        SOURCE_DIR="$SCRIPT_DIR"
    else
        print_info "從儲存庫複製 (Clone)..."
        git clone --depth 1 "$REPO_URL" "$TEMP_DIR/repo" || {
            print_error "複製儲存庫失敗。請檢查您的網路連線。"
            exit 1
        }
        SOURCE_DIR="${TEMP_DIR}/repo"
    fi

    # ---- 安裝主要技能 ----
    print_info "正在安裝主要 GEO 技能..."

    cp -r "$SOURCE_DIR/geo/"* "$INSTALL_DIR/"
    print_success "主要技能安裝完成 -> ${INSTALL_DIR}/"

    # ---- 安裝子技能 ----
    print_info "正在安裝子技能..."

    SKILL_COUNT=0
    for skill_dir in "$SOURCE_DIR/skills"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            target_dir="${SKILLS_DIR}/${skill_name}"
            mkdir -p "$target_dir"
            cp -r "$skill_dir"* "$target_dir/"
            SKILL_COUNT=$((SKILL_COUNT + 1))
            print_success "  ${skill_name}"
        fi
    done
    echo "  -> 已安裝 ${SKILL_COUNT} 個子技能"

    # ---- 安裝代理 (Agents) ----
    print_info "正在安裝子代理 (Subagents)..."

    AGENT_COUNT=0
    for agent_file in "$SOURCE_DIR/agents/"*.md; do
        if [ -f "$agent_file" ]; then
            cp "$agent_file" "$AGENTS_DIR/"
            AGENT_COUNT=$((AGENT_COUNT + 1))
            print_success "  $(basename "$agent_file")"
        fi
    done
    echo "  -> 已安裝 ${AGENT_COUNT} 個子代理"

    # ---- 安裝腳本 ----
    print_info "正在安裝公用程式指令碼..."

    if [ -d "$SOURCE_DIR/scripts" ]; then
        cp -r "$SOURCE_DIR/scripts/"* "$INSTALL_DIR/scripts/"
        # chmod 在 Windows 上無作用但無害
        chmod +x "$INSTALL_DIR/scripts/"*.py 2>/dev/null || true
        print_success "指令碼安裝完成 -> ${INSTALL_DIR}/scripts/"
    fi

    # ---- 安裝 Schema 範本 ----
    print_info "正在安裝結構描述 (Schema) 範本..."

    if [ -d "$SOURCE_DIR/schema" ]; then
        cp -r "$SOURCE_DIR/schema/"* "$INSTALL_DIR/schema/"
        print_success "結構描述範本安裝完成 -> ${INSTALL_DIR}/schema/"
    fi

    # ---- 安裝 Hooks ----
    if [ -d "$SOURCE_DIR/hooks" ] && [ "$(ls -A "$SOURCE_DIR/hooks" 2>/dev/null)" ]; then
        print_info "正在安裝掛鉤 (Hooks)..."
        cp -r "$SOURCE_DIR/hooks/"* "$INSTALL_DIR/hooks/"
        chmod +x "$INSTALL_DIR/hooks/"* 2>/dev/null || true
        print_success "掛鉤安裝完成 -> ${INSTALL_DIR}/hooks/"
    fi

    # ---- 安裝 Python 相依套件 ----
    print_info "正在安裝 Python 相依套件..."

    if [ -f "$SOURCE_DIR/requirements.txt" ]; then
        # 使用 --user 以避免需要管理員權限；使用 -q 抑制不必要的輸出
        $PYTHON_CMD -m pip install --user -r "$SOURCE_DIR/requirements.txt" -q 2>/dev/null && {
            print_success "Python 相依套件安裝完成"
        } || {
            print_warning "部分 Python 相依套件安裝失敗。"
            echo "  請手動執行：$PYTHON_CMD -m pip install --user -r requirements.txt"
            cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/"
        }
    fi

    # ---- 選用：安裝 Playwright ----
    if [ "$INTERACTIVE" = true ]; then
        echo ""
        read -r -p "是否安裝 Playwright 瀏覽器以支援網頁截圖？(y/n)：" REPLY
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "正在安裝 Playwright 瀏覽器..."
            $PYTHON_CMD -m playwright install chromium 2>/dev/null && {
                print_success "Playwright Chromium 安裝完成"
            } || {
                print_warning "Playwright 安裝失敗。無法使用網頁截圖功能。"
                echo "  手動重試：$PYTHON_CMD -m playwright install chromium"
            }
        fi
    else
        print_info "略過 Playwright (非互動模式)。"
        echo "  稍後安裝：$PYTHON_CMD -m playwright install chromium"
    fi

    # ---- 驗證安裝 ----
    echo ""
    print_info "正在驗證安裝..."

    VERIFY_OK=true

    [ -f "$INSTALL_DIR/SKILL.md" ]       && print_success "主要技能檔案"         || { print_error "主要技能檔案遺失";   VERIFY_OK=false; }
    [ -d "$SKILLS_DIR/geo-audit" ]       && print_success "子技能目錄"           || { print_error "子技能目錄遺失";        VERIFY_OK=false; }
    [ "$(ls "$AGENTS_DIR"/geo-*.md 2>/dev/null | wc -l)" -gt 0 ] \
                                         && print_success "代理檔案"             || { print_error "代理檔案遺失";       VERIFY_OK=false; }
    [ -d "$INSTALL_DIR/scripts" ]        && print_success "公用程式指令碼"       || { print_error "指令碼遺失";           VERIFY_OK=false; }
    [ -d "$INSTALL_DIR/schema" ]         && print_success "結構描述範本"         || { print_error "結構描述範本遺失";  VERIFY_OK=false; }

    if [ "$VERIFY_OK" = false ]; then
        echo ""
        print_warning "遺失一個或多個檔案。安裝可能不完整。"
    fi

    # ---- 列印摘要 ----
    echo ""
    echo -e "${GREEN}+------------------------------------------+${NC}"
    echo -e "${GREEN}|               安裝完成！                 |${NC}"
    echo -e "${GREEN}+------------------------------------------+${NC}"
    echo ""
    echo "  安裝至：${INSTALL_DIR}"
    echo "  技能：${SKILL_COUNT} 個子技能"
    echo "  代理：${AGENT_COUNT} 個子代理"
    echo ""
    echo -e "${BLUE}快速開始：${NC}"
    echo "  打開 Claude Code 並嘗試："
    echo ""
    echo "    /geo audit https://example.com"
    echo "    /geo quick https://example.com"
    echo "    /geo citability https://example.com/blog/article"
    echo "    /geo crawlers https://example.com"
    echo "    /geo report https://example.com"
    echo ""
    echo -e "${BLUE}可用指令：${NC}"
    echo "    /geo audit <url>      完整的 GEO + SEO 稽核"
    echo "    /geo quick <url>      60 秒可見度快照"
    echo "    /geo citability <url> AI 引用準備度分數"
    echo "    /geo crawlers <url>   AI 爬蟲存取檢查"
    echo "    /geo llmstxt <url>    分析/產生 llms.txt"
    echo "    /geo brands <url>     品牌提及掃描"
    echo "    /geo platforms <url>  特定平台優化"
    echo "    /geo schema <url>     結構化資料分析"
    echo "    /geo technical <url>  技術 SEO 稽核"
    echo "    /geo content <url>    內容品質與 E-E-A-T"
    echo "    /geo report <url>     可交付客戶的 GEO 報告"
    echo "    /geo report-pdf       從稽核資料產生 PDF 報告"
    echo ""
    echo "  文件：https://github.com/gtut-nick/geo-seo-claude"
    echo ""
}

main "$@"
