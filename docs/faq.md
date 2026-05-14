# 常見問題

---

## 一般問題

### 什麼是 GEO？它和 SEO 有什麼不同？

SEO（Search Engine Optimization）目標是在 Google 藍色連結結果等傳統搜尋引擎中取得排名。GEO（Generative Engine Optimization）目標是在 ChatGPT、Perplexity、Claude、Gemini 與 Google AI Overviews 等系統產生的 AI 答案中提高可見度。兩者有所重疊，技術基礎與內容品質都很重要，但 GEO 額外關注 AI retrieval 特有的議題：引用性評分、品牌提及密度、llms.txt，以及 AI 引用平台上的實體識別。

### 這是付費工具或服務嗎？

工具本身免費，採 MIT 授權。它完全在你自己的 Claude Code session 中執行，使用既有 Anthropic subscription。技能套件本身沒有額外 API key、用量計或訂閱費。

### 這適合誰使用？

適合執行客戶稽核的 GEO 代理商、監控 AI 搜尋可見度的內部行銷團隊、為 AI 引用最佳化單頁內容的內容創作者，以及想取得可行 GEO 與 SEO 回饋、但不想訂閱 SaaS 的網站開發與維護者。

### 這會取代我現有的 SEO 工具組嗎？

不會。它是補充既有工具。`/geo technical` 指令涵蓋技術 SEO 基礎，但本工具不會取代 Screaming Frog 這類 crawler、關鍵字研究平台或排名追蹤工具。它的主要價值在 GEO layer，也就是多數傳統 SEO 工具尚未涵蓋的 AI 引用性、爬蟲存取、品牌訊號與平台準備度。

---

## 安裝與設定

### 為什麼我需要 Claude Code CLI？

技能套件是以 Claude Code slash commands 實作。所有指令（`/geo audit`、`/geo quick` 等）都透過 Claude Code 的 skill 與 agent 系統路由。CLI 是執行環境；沒有它，就沒有東西能執行技能檔案。請用 `npm install -g @anthropic-ai/claude-code` 安裝。

### 我可以在沒有 WSL 的 Windows 上執行嗎？

可以，但你必須使用 Git Bash，而不是 PowerShell 或 Command Prompt。Windows 安裝程式是 `install-win.sh`，需要 Git for Windows（內含 Git Bash）。在 repo 資料夾上按右鍵選擇「Open Git Bash here」，再執行 `./install-win.sh`。不需要 WSL。

### `install.sh` 實際上會做什麼？

它會檢查 Git、Python 3.8+ 與 Claude Code CLI，接著將檔案複製到你的 Claude 設定目錄（`~/.claude/`）。具體來說：主技能會放到 `~/.claude/skills/geo/`，13 個 sub-skill 各自放到 `~/.claude/skills/geo-<name>/`，5 個 agent 檔案放到 `~/.claude/agents/`。接著使用 `pip install --user` 從 `requirements.txt` 安裝 Python 相依套件。如果你以互動模式執行，它也會詢問是否安裝 Playwright Chromium browser 以支援截圖。安裝程式可從 clone 後的本機目錄執行，也可透過 repository URL 的 `curl | bash` pipe 執行。

### 我需要 Playwright 嗎？

Playwright 是選用。安裝程式會提示是否安裝它（`python3 -m playwright install chromium`）。沒有它時，截圖型功能不可用，但其他所有稽核與分析指令都能正常運作。你可以稍後隨時安裝。

---

## 使用方式

### `/geo quick` 和 `/geo audit` 有什麼差別？

`/geo quick` 會產生 60 秒 inline 可見度快照，不寫入任何輸出檔。它適合在投入完整執行前快速判讀 URL，或用於快速客戶檢查。`/geo audit` 是完整流程：抓取網站、偵測商業類型、啟動 5 個平行 subagent、彙總所有類別分數，並寫出含優先行動計畫的 `GEO-AUDIT-REPORT.md`。完整指令列表請見 [commands-reference.md](commands-reference.md)。

### 綜合 GEO Score 從哪裡來？

分數（0-100）是六個類別的加權彙總：AI Citability & Visibility（25%）、Brand Authority Signals（20%）、Content Quality & E-E-A-T（20%）、Technical Foundations（15%）、Structured Data（10%）與 Platform Optimization（10%）。每個類別內的個別訊號如何衡量，請見 [scoring-methodology.md](scoring-methodology.md)。

### 平行 subagents 如何運作？

完整稽核時，初始探索階段完成後，五個 subagent 會同時執行：`geo-ai-visibility`、`geo-platform-analysis`、`geo-technical`、`geo-content` 與 `geo-schema`。每個 subagent 對應 `~/.claude/agents/` 中的一個 agent definition file，負責分析的不同切片。Claude Code 的 agent 系統負責平行 dispatch；orchestrator 之後收集五份報告並彙整成綜合分數。完整流程請見 [architecture.md](architecture.md)。

### prospect、proposal 與 report 資料儲存在哪裡？

`/geo prospect`、`/geo proposal` 與 `/geo compare` 的資料會寫入 Claude Code 目錄之外的 `~/.geo-prospects/`。結構如下：

```
~/.geo-prospects/
├── prospects.json
├── proposals/<domain>-proposal-<date>.md
└── reports/<domain>-monthly-<YYYY-MM>.md
```

此目錄刻意不會被 `uninstall.sh` 移除。如果想丟棄潛在客戶資料，請用 `rm -rf ~/.geo-prospects` 手動刪除。

---

## 貢獻

### 如何新增 sub-skill？

在 `skills/` 底下依 `geo-<skill-name>/` 命名模式建立新目錄。於其中加入 `SKILL.md`，定義該技能的名稱、描述與邏輯。如果該技能應參與完整稽核，請在 `agents/` 底下適當的 agent 檔案中註冊它。可參考既有 sub-skill，例如 `skills/geo-citability/` 的結構。技能與 agents 的關係圖請見 [skills-and-agents.md](skills-and-agents.md)。

### 開 PR 前如何測試我的變更？

從本機 clone 執行 `./install.sh`，script 會偵測本機 `geo/SKILL.md` 並從 working directory 安裝，而不是從 GitHub clone。開啟 Claude Code，針對真實 URL 執行受影響的指令。提交 pull request 前，確認所有狀態檢查都已通過，這點也記載於 `CONTRIBUTING.md`。

### 我要在哪裡回報 bug 或提出功能請求？

請在 GitHub 開 issue。Bug 請包含清楚描述、你稽核的 URL（若相關），以及任何錯誤輸出。功能請求請說明使用情境與它的重要性。請先搜尋既有 issues 以避免重複。兩者都在 repository 的 Issues tab 中追蹤。

---

## 限制

### 這個工具能保證 AI 引用或排名嗎？

不能。此工具稽核與 AI 可見度相關的訊號，並提供改善建議，但沒有任何工具能保證任何 AI 系統會引用或顯示特定網域。AI retrieval 具有機率性，會依 query、平台與模型版本而變化。

### 它會把資料提交到第三方服務嗎？

技能會使用 `WebFetch` 與 `Bash`（透過 `curl`）抓取你提供的 URL，品牌提及掃描器也會檢查公開可存取平台（YouTube、Reddit、Wikipedia、LinkedIn 等）的品牌訊號。沒有稽核資料會被送到 Anthropic-operated 或第三方 analytics endpoint。你的資料會留在你的 Claude Code session 與本機檔案系統中。
