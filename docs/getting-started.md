# 開始使用

## 需求

| 需求 | 為什麼需要 |
|---|---|
| Python 3.8+ | 執行工具 scripts（頁面抓取、引用性評分、PDF 產生等） |
| Claude Code CLI | 技能與 agents 會透過 Claude Code 載入並呼叫 |
| Git | 安裝程式會用它 clone repository |
| Playwright（選用） | 啟用截圖擷取；主安裝完成後另行安裝 |

如果尚未安裝 Claude Code：

```bash
npm install -g @anthropic-ai/claude-code
```

---

## 安裝

### macOS / Linux — 一行指令

```bash
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/main/install.sh | bash
```

### macOS / Linux — 手動

```bash
git clone https://github.com/zubair-trabzada/geo-seo-claude.git
cd geo-seo-claude
./install.sh
```

### Windows — Git Bash

不支援 PowerShell 與 Command Prompt。你必須使用 [Git Bash](https://git-scm.com/downloads)（Git for Windows 內含）。

```bash
# 一行指令（從 Git Bash 執行）
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/main/install-win.sh | bash

# 手動
git clone https://github.com/zubair-trabzada/geo-seo-claude.git
cd geo-seo-claude
./install-win.sh
```

在 clone 後的資料夾上按右鍵並選擇「Open Git Bash here」，或在既有 Git Bash session 中切換到該目錄。

### 安裝程式會做什麼

- 將 `geo` 協調器技能複製到 `~/.claude/skills/geo/`
- 將 13 個 sub-skill 複製到 `~/.claude/skills/geo-*/`
- 將 5 個 subagent 定義複製到 `~/.claude/agents/`
- 透過 `pip install --user` 安裝 Python 相依套件
- 選擇性安裝 Playwright Chromium browser 以支援截圖

---

## 驗證安裝

安裝後，在任意專案目錄開啟 Claude Code 並執行：

```
/geo quick https://example.com
```

如果技能已正確接上，Claude Code 會啟動 60 秒 GEO 可見度快照。如果看到 "unknown command" 或沒有反應，請重新啟動 Claude Code，因為它會在啟動時讀取技能與 agents。

確認檔案已放到正確位置：

```bash
ls ~/.claude/skills/geo/
ls ~/.claude/skills/ | grep geo
ls ~/.claude/agents/ | grep geo
```

---

## 你的第一次稽核

### 快速路徑 — 60 秒快照

```
/geo quick https://yoursite.com
```

回傳高層級 GEO 可見度分數與最主要問題。適合第一次查看，或快速檢查客戶。

### 完整路徑 — 完整稽核

```
/geo audit https://yoursite.com
```

啟動 5 個平行 subagent，涵蓋 AI 可見度、平台最佳化、技術 SEO、內容品質與結構化資料。產生含綜合 GEO score（0–100）的優先行動計畫。

完整稽核耗時取決於網站，通常需要數分鐘。分數計算方式請見 [scoring-methodology.md](scoring-methodology.md)，所有可用指令請見 [commands-reference.md](commands-reference.md)。

---

## 疑難排解

**安裝期間找不到 Python**
- 症狀：安裝程式以 `Python 3.8+ is required but not found` 結束
- 原因：未安裝 Python，或 Python 不在 `PATH` 上
- 修正：從 [python.org](https://www.python.org/downloads/) 安裝；Windows 安裝時勾選 "Add Python to PATH"；接著重新開啟終端機

**找不到 Claude Code CLI**
- 症狀：安裝程式警告 `Claude Code CLI not found in PATH`
- 原因：未安裝 `claude`，或它不在 `PATH` 上
- 修正：執行 `npm install -g @anthropic-ai/claude-code`；用 `claude --version` 確認

**Claude Code 中沒有顯示技能**
- 症狀：`/geo quick` 產生 "unknown command" 或沒有回應
- 原因：Claude Code 只在啟動時讀取技能；啟動後新增的檔案不會被看到
- 修正：完整退出並重新開啟 Claude Code

**執行 `./install.sh` 時 Permission denied**
- 症狀：`bash: ./install.sh: Permission denied`
- 原因：未設定可執行 bit
- 修正：`chmod +x install.sh && ./install.sh`

**Windows 上使用了錯誤 shell**
- 症狀：`curl` 無法辨識，或 script 語法錯誤
- 原因：在 PowerShell 或 Command Prompt 中執行 `install-win.sh`
- 修正：只使用 Git Bash，於資料夾按右鍵選擇「Open Git Bash here」

**Playwright 不可用 / 缺少截圖**
- 症狀：截圖相關步驟靜默跳過或出錯
- 原因：安裝時跳過 Playwright（非互動模式或回答 no）
- 修正：手動安裝：
  ```bash
  python3 -m playwright install chromium
  ```

**安裝期間 Python 相依套件失敗**
- 症狀：安裝程式印出 `Some Python dependencies failed to install`
- 原因：pip 錯誤（網路、權限或 virtualenv 衝突）
- 修正：從 clone 後的 repo 或 `~/.claude/skills/geo/` 手動執行：
  ```bash
  python3 -m pip install --user -r requirements.txt
  ```

---

## 解除安裝

### Scripted

從 clone 後的 repository 目錄執行：

```bash
./uninstall.sh
```

這會移除 `~/.claude/skills/geo/`、所有 `~/.claude/skills/geo-*/` sub-skills，以及所有 `~/.claude/agents/geo-*.md` agent 檔案。Python packages 不會被移除。

### 手動

```bash
rm -rf ~/.claude/skills/geo ~/.claude/skills/geo-* ~/.claude/agents/geo-*.md
```

### 執行期資料

`~/.geo-prospects/` 目錄（由 `/geo prospect`、`/geo proposal` 與 `/geo compare` 使用）**不會**被解除安裝程式移除。如果不再需要資料，請手動刪除：

```bash
rm -rf ~/.geo-prospects
```

---

另請參閱：[architecture.md](architecture.md) | [commands-reference.md](commands-reference.md) | [scoring-methodology.md](scoring-methodology.md) | [skills-and-agents.md](skills-and-agents.md)
