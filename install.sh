#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# GEO-SEO Claude Code 技能安裝工具
# 安裝適用於 Claude Code 的「以 GEO 為優先」SEO 分析工具
# 並建立獨立的 Python 虛擬環境。
# ============================================================

REPO_URL="https://github.com/gtut-nick/geo-seo-claude.git"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"
INSTALL_DIR="${SKILLS_DIR}/geo"
VENV_DIR="${INSTALL_DIR}/.venv"
VENV_PY="${VENV_DIR}/bin/python3"
# 用於修補 skill/agent .md 檔案內部參考的波浪號路徑。
# 波浪號刻意保留字面意義 — Claude Code 的 Bash 在稍後執行指令時會展開它。
# 請勿在此處替換為 $HOME。
# shellcheck disable=SC2088
VENV_MD_PY='~/.claude/skills/geo/.venv/bin/python3'
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
    echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   GEO-SEO Claude Code 技能安裝工具       ║${NC}"
    echo -e "${BLUE}║   以 GEO 為優先的 AI 搜尋優化            ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_error()   { echo -e "${RED}✗ $1${NC}"; }
print_info()    { echo -e "${BLUE}→ $1${NC}"; }

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# 跨平台原地替換 sed (支援 GNU sed 與 BSD/macOS sed)。
# 會寫入一個 .bak 備份檔然後刪除它。
sed_inplace() {
    local pattern="$1"
    local file="$2"
    sed -i.bak "$pattern" "$file" && rm -f "${file}.bak"
}

main() {
    print_header

    # ---- 檢查必備條件 ----
    print_info "正在檢查必備條件..."

    if ! command -v git &> /dev/null; then
        print_error "需要 Git 但尚未安裝。"
        echo "  安裝：https://git-scm.com/downloads"
        exit 1
    fi
    print_success "找到 Git：$(git --version)"

    PYTHON_CMD=""
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PY_VERSION=$(python --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        if [ -n "$PY_VERSION" ]; then
            MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
            MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
            if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
                PYTHON_CMD="python"
            fi
        fi
    fi

    if [ -z "$PYTHON_CMD" ]; then
        print_error "需要 Python 3.8+ 但尚未找到。"
        echo "  安裝：https://www.python.org/downloads/"
        exit 1
    fi
    print_success "找到 Python：$($PYTHON_CMD --version)"

    if ! command -v claude &> /dev/null; then
        print_warning "在 PATH 中找不到 Claude Code CLI。"
        echo "  此工具需要 Claude Code 才能運作。"
        echo "  安裝：npm install -g @anthropic-ai/claude-code"
        echo ""
        if [ "$INTERACTIVE" = true ]; then
            read -p "是否仍要繼續安裝？(y/n)：" -n 1 -r
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

    # 偵測是否安裝了 uv 以加快 venv 建立/安裝速度 (非必要，預設回退至 stdlib venv + pip)
    USE_UV=false
    if command -v uv &> /dev/null; then
        USE_UV=true
        print_success "偵測到 'uv' — 將使用它來加快安裝速度"
    fi

    # ---- 建立目錄 ----
    print_info "正在建立目錄..."

    mkdir -p "$SKILLS_DIR" "$AGENTS_DIR" "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR/scripts" "$INSTALL_DIR/schema" "$INSTALL_DIR/hooks"

    print_success "目錄結構建立完成"

    # ---- 解析來源目錄 (本機或遠端 clone) ----
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
    print_success "主要技能安裝完成 → ${INSTALL_DIR}/"

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
    echo "  → 已安裝 ${SKILL_COUNT} 個子技能"

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
    echo "  → 已安裝 ${AGENT_COUNT} 個子代理"

    # ---- 安裝腳本 ----
    print_info "正在安裝公用程式指令碼..."
    if [ -d "$SOURCE_DIR/scripts" ]; then
        cp -r "$SOURCE_DIR/scripts/"* "$INSTALL_DIR/scripts/"
        print_success "指令碼安裝完成 → ${INSTALL_DIR}/scripts/"
    fi

    # ---- 安裝 Schema 範本 ----
    print_info "正在安裝結構描述 (Schema) 範本..."
    if [ -d "$SOURCE_DIR/schema" ]; then
        cp -r "$SOURCE_DIR/schema/"* "$INSTALL_DIR/schema/"
        print_success "結構描述範本安裝完成 → ${INSTALL_DIR}/schema/"
    fi

    # ---- 安裝 Hooks ----
    if [ -d "$SOURCE_DIR/hooks" ] && [ "$(ls -A "$SOURCE_DIR/hooks" 2>/dev/null)" ]; then
        print_info "正在安裝掛鉤 (Hooks)..."
        cp -r "$SOURCE_DIR/hooks/"* "$INSTALL_DIR/hooks/"
        chmod +x "$INSTALL_DIR/hooks/"* 2>/dev/null || true
        print_success "掛鉤安裝完成 → ${INSTALL_DIR}/hooks/"
    fi

    # ---- 建立虛擬環境 ----
    print_info "正在建立獨立的 Python 環境 → ${VENV_DIR}"

    # 如果有先前安裝留下的舊 venv，先將其移除。
    rm -rf "$VENV_DIR"

    if [ "$USE_UV" = true ]; then
        uv venv "$VENV_DIR" --python "$PYTHON_CMD" --quiet || {
            print_error "uv venv 建立失敗。"
            exit 1
        }
    else
        if ! $PYTHON_CMD -m venv "$VENV_DIR" 2>/dev/null; then
            print_error "建立虛擬環境失敗。"
            echo ""
            echo "  您的 Python 可能缺少 'venv' 模組。請嘗試以下其中一種方法："
            echo "    • Debian/Ubuntu:  sudo apt install python3-venv"
            echo "    • Fedora/RHEL:    sudo dnf install python3-virtualenv"
            echo "    • 安裝 'uv':      https://docs.astral.sh/uv/  (不需要系統套件)"
            exit 1
        fi
    fi
    print_success "虛擬環境建立完成"

    # ---- 將 Python 相依套件安裝至 venv ----
    print_info "正在將 Python 相依套件安裝到 venv..."

    if [ ! -f "$SOURCE_DIR/requirements.txt" ]; then
        print_warning "缺少 requirements.txt — 略過相依套件安裝。"
    elif [ "$USE_UV" = true ]; then
        uv pip install --python "$VENV_PY" -r "$SOURCE_DIR/requirements.txt" --quiet || {
            print_error "透過 uv 安裝相依套件失敗。"
            exit 1
        }
    else
        "$VENV_PY" -m pip install --upgrade pip --quiet
        "$VENV_PY" -m pip install -r "$SOURCE_DIR/requirements.txt" --quiet || {
            print_error "安裝相依套件失敗。"
            exit 1
        }
    fi
    print_success "相依套件安裝完成 (已隔離 — 不會影響系統 Python)"

    # 在 venv 旁邊保留一份 requirements.txt 以供參考。
    cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/" 2>/dev/null || true

    # ---- 將腳本的 shebang 指向 venv 直譯器 ----
    print_info "正在將指令碼 shebang 指向 venv 直譯器..."
    SHEBANG_COUNT=0
    for f in "$INSTALL_DIR/scripts/"*.py; do
        [ -f "$f" ] || continue
        sed_inplace "1s|^#!.*|#!${VENV_PY}|" "$f"
        chmod +x "$f"
        SHEBANG_COUNT=$((SHEBANG_COUNT + 1))
    done
    print_success "${SHEBANG_COUNT} 個指令碼已指向 venv"

    # ---- 修補技能與代理的 markdown 參考 ----
    # 策略：
    #   1. "python3 ~/.claude/skills/geo/scripts/"  →  "~/.claude/skills/geo/scripts/"
    #      (腳本現在會透過其 shebang 自行執行)
    #   2. bare "python3 -c " / "python3 -m "  →  "<venv>/python3 -c " / " -m "
    #      (內嵌的片段仍需要 venv 直譯器來執行 requests 等套件)
    print_info "正在改寫技能與代理參考以使用 venv..."

    patch_md() {
        local f="$1"
        sed_inplace 's|python3 ~/\.claude/skills/geo/scripts/|~/.claude/skills/geo/scripts/|g' "$f"
        sed_inplace "s|python3 -c |${VENV_MD_PY} -c |g" "$f"
        sed_inplace "s|python3 -m |${VENV_MD_PY} -m |g" "$f"
    }

    PATCH_COUNT=0
    for f in "$INSTALL_DIR/SKILL.md" "$SKILLS_DIR"/geo-*/SKILL.md "$AGENTS_DIR"/geo-*.md; do
        if [ -f "$f" ]; then
            patch_md "$f"
            PATCH_COUNT=$((PATCH_COUNT + 1))
        fi
    done
    print_success "${PATCH_COUNT} 個 Markdown 檔案已改寫"

    # ---- 選用：安裝 Playwright 瀏覽器 ----
    if [ "$INTERACTIVE" = true ]; then
        echo ""
        read -p "是否安裝 Playwright 瀏覽器以支援網頁截圖？(y/n)：" -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "正在將 Playwright Chromium 安裝至 venv..."
            if "$VENV_PY" -m playwright install chromium 2>/dev/null; then
                print_success "Playwright Chromium 安裝完成"
            else
                print_warning "Playwright 安裝失敗 — 無法使用網頁截圖功能。"
                echo "  重試：${VENV_PY} -m playwright install chromium"
            fi
        fi
    else
        print_info "略過 Playwright (非互動模式)。您可以稍後執行："
        echo "    ${VENV_PY} -m playwright install chromium"
    fi

    # ---- 驗證安裝 ----
    echo ""
    print_info "正在驗證安裝..."
    VERIFY_OK=true

    verify() {
        local label="$1"
        shift
        if "$@"; then
            print_success "$label"
        else
            print_error "$label 遺失"
            VERIFY_OK=false
        fi
    }

    # 透過 glob 計算代理檔案數量 (不解析 ls)。
    agent_count=0
    for f in "$AGENTS_DIR"/geo-*.md; do
        [ -f "$f" ] && agent_count=$((agent_count + 1))
    done

    verify "主要技能檔案"          test -f "$INSTALL_DIR/SKILL.md"
    verify "子技能目錄"            test -d "$SKILLS_DIR/geo-audit"
    verify "代理檔案"              test "$agent_count" -gt 0
    verify "公用程式指令碼"        test -d "$INSTALL_DIR/scripts"
    verify "結構描述範本"          test -d "$INSTALL_DIR/schema"
    verify "Venv 直譯器"           test -x "$VENV_PY"

    if [ "$VERIFY_OK" = false ]; then
        echo ""
        print_warning "遺失一個或多個檔案。安裝可能不完整。"
    fi

    # ---- 列印摘要 ----
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║               安裝完成！                 ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
    echo ""
    echo "  安裝至：${INSTALL_DIR}"
    echo "  虛擬環境：${VENV_DIR}"
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
