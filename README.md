<p align="center">
  <img src="assets/banner.svg" alt="GEO-SEO Claude Code 技能" width="900"/>
</p>

<p align="center">
  <strong>GEO 優先，SEO 輔助。</strong> 在維持傳統 SEO 基礎的同時，為 AI 驅動的搜尋引擎最佳化網站<br/>
  （ChatGPT、Claude、Perplexity、Gemini、Google AI Overviews）。
</p>

<p align="center">
  AI 搜尋正在取代傳統搜尋。這套工具最佳化的是流量正在前往的地方，而不是流量曾經所在的地方。
</p>

---

## 為什麼 GEO 很重要（2026）

| 指標                             | 數值                                       |
| -------------------------------- | ------------------------------------------ |
| GEO 服務市場                     | 8.5 億美元以上（預計 2031 年達 73 億美元） |
| AI 推薦流量成長                  | 年增 527%                                  |
| AI 流量轉換率相較自然流量        | 高出 4.4 倍                                |
| Gartner：到 2028 年搜尋流量下滑  | -50%                                       |
| 品牌提及相較反向連結對 AI 的影響 | 相關性強 3 倍                              |
| 正在投資 GEO 的行銷人員          | 僅 23%                                     |

---

## 快速開始

### 一行指令安裝（macOS/Linux）

```bash
curl -fsSL https://raw.githubusercontent.com/gtut-nick/geo-seo-claude/main/install.sh | bash
```

### 手動安裝

```bash
git clone https://github.com/gtut-nick/geo-seo-claude.git
cd geo-seo-claude
./install.sh
```

### Windows（Git Bash）

需要 [Git for Windows](https://git-scm.com/downloads)，其中包含 Git Bash。

```bash
# 選項 1：一行指令安裝（請從 Git Bash 執行，不要用 PowerShell/CMD）
curl -fsSL https://raw.githubusercontent.com/gtut-nick/geo-seo-claude/main/install-win.sh | bash

# 選項 2：手動安裝
git clone https://github.com/gtut-nick/geo-seo-claude.git
cd geo-seo-claude
./install-win.sh
```

> **注意：** 在資料夾上按右鍵並選擇「Open Git Bash here」，或開啟 Git Bash 後切換到該目錄。請不要使用 PowerShell 或命令提示字元。

### 需求

- Python 3.8+（Debian/Ubuntu 也需要 `python3-venv`）
- Claude Code CLI
- Git
- 選用：[`uv`](https://docs.astral.sh/uv/) — 如果可用，安裝程式會用它更快地安裝相依套件
- 選用：Playwright（用於截圖）

### 隔離式安裝

Python 相依套件會安裝到專用虛擬環境：
`~/.claude/skills/geo/.venv/`。系統 Python **不會**被修改，
而且解除安裝技能時，會連同其餘檔案一起移除該 venv。

技能與 agent 檔案會直接參照該 venv，因此無論 `PATH` 上的
`python3` 解析到哪裡，工具都能正常運作。

---

## 指令

開啟 Claude Code 並使用以下指令：

| 指令                    | 功能                                      |
| ----------------------- | ----------------------------------------- |
| `/geo audit <url>`      | 使用平行 subagent 執行完整 GEO + SEO 稽核 |
| `/geo quick <url>`      | 60 秒 GEO 可見度快照                      |
| `/geo citability <url>` | 評估內容是否適合被 AI 引用                |
| `/geo crawlers <url>`   | 檢查 AI 爬蟲存取權限（robots.txt）        |
| `/geo llmstxt <url>`    | 分析或產生 llms.txt                       |
| `/geo brands <url>`     | 掃描 AI 引用平台上的品牌提及              |
| `/geo platforms <url>`  | 針對特定平台進行最佳化                    |
| `/geo schema <url>`     | 結構化資料分析與產生                      |
| `/geo technical <url>`  | 技術 SEO 稽核                             |
| `/geo content <url>`    | 內容品質與 E-E-A-T 評估                   |
| `/geo report <url>`     | 產生可直接交付客戶的 GEO 報告             |
| `/geo report-pdf`       | 產生含圖表與視覺化的專業 PDF 報告         |

---

## 架構

```
geo-seo-claude/
├── geo/                          # 主要技能協調器
│   └── SKILL.md                  # 含指令與路由的主要技能檔
├── skills/                       # 13 個專門 sub-skill
│   ├── geo-audit/                # 完整稽核協調與評分
│   ├── geo-citability/           # AI 引用準備度評分
│   ├── geo-crawlers/             # AI 爬蟲存取分析
│   ├── geo-llmstxt/              # llms.txt 標準分析與產生
│   ├── geo-brand-mentions/       # AI 引用平台上的品牌存在感
│   ├── geo-platform-optimizer/   # 針對平台的 AI 搜尋最佳化
│   ├── geo-schema/               # 用於 AI 可發現性的結構化資料
│   ├── geo-technical/            # 技術 SEO 基礎
│   ├── geo-content/              # 內容品質與 E-E-A-T
│   ├── geo-report/               # 可交付客戶的 markdown 報告產生
│   ├── geo-report-pdf/           # 含圖表的專業 PDF 報告
│   ├── geo-prospect/             # 輕量 CRM 潛在客戶流程管理
│   ├── geo-proposal/             # 自動產生客戶提案
│   └── geo-compare/              # 每月差異追蹤與進度報告
├── agents/                       # 5 個平行 subagent
│   ├── geo-ai-visibility.md      # GEO 稽核、引用性、爬蟲、品牌
│   ├── geo-platform-analysis.md  # 平台特定最佳化
│   ├── geo-technical.md          # 技術 SEO 分析
│   ├── geo-content.md            # 內容與 E-E-A-T 分析
│   └── geo-schema.md             # Schema 標記分析
├── scripts/                      # Python 工具程式
│   ├── fetch_page.py             # 頁面抓取與解析
│   ├── citability_scorer.py      # AI 引用性評分引擎
│   ├── brand_scanner.py          # 品牌提及偵測
│   ├── llmstxt_generator.py      # llms.txt 驗證與產生
│   └── generate_pdf_report.py    # PDF 報告產生器（ReportLab）
├── schema/                       # JSON-LD 範本
│   ├── organization.json         # Organization schema（含 sameAs）
│   ├── local-business.json       # LocalBusiness schema
│   ├── article-author.json       # Article + Person schema（E-E-A-T）
│   ├── software-saas.json        # SoftwareApplication schema
│   ├── product-ecommerce.json    # 含 offers 的 Product schema
│   └── website-searchaction.json # WebSite + SearchAction schema
├── install.sh                    # 一行指令安裝程式
├── uninstall.sh                  # 解除安裝程式
├── requirements.txt              # Python 相依套件
└── README.md                     # 本檔案
```

---

## 資料儲存

CRM 與報告技能（`/geo prospect`、`/geo proposal`、`/geo compare`）會將執行期間資料儲存在 Claude Code 目錄之外：

```
~/.geo-prospects/
├── prospects.json              # 客戶/潛在客戶流程資料
├── proposals/                  # 產生的提案文件
│   └── <domain>-proposal-<date>.md
└── reports/                    # 每月差異報告
    └── <domain>-monthly-<YYYY-MM>.md
```

解除安裝程式**不會移除**這個目錄。如果不再需要潛在客戶資料，請手動刪除。

---

## 運作方式

### 完整稽核流程

當你執行 `/geo audit https://example.com`：

1. **探索** — 抓取首頁、偵測商業類型、爬取 sitemap
2. **平行分析** — 同時啟動 5 個 subagent：
   - AI 可見度（引用性、爬蟲、llms.txt、品牌提及）
   - 平台分析（ChatGPT、Perplexity、Google AIO 準備度）
   - 技術 SEO（Core Web Vitals、SSR、安全性、行動裝置）
   - 內容品質（E-E-A-T、可讀性、新鮮度）
   - Schema 標記（偵測、驗證、產生）
3. **彙整** — 彙總分數，產生綜合 GEO 分數（0-100）
4. **報告** — 輸出依優先順序排列的行動計畫與快速成效項目

### 評分方法

| 類別               | 權重 |
| ------------------ | ---- |
| AI 引用性與可見度  | 25%  |
| 品牌權威訊號       | 20%  |
| 內容品質與 E-E-A-T | 20%  |
| 技術基礎           | 15%  |
| 結構化資料         | 10%  |
| 平台最佳化         | 10%  |

---

## 主要功能

### 引用性評分

分析內容區塊是否適合被 AI 引用。理想的 AI 引用段落長度為 134-167 個字，應該自成一體、包含大量事實，並直接回答問題。

### AI 爬蟲分析

檢查 robots.txt 中 14 種以上 AI 爬蟲（GPTBot、ClaudeBot、PerplexityBot 等）的設定，並提供具體的允許/封鎖建議。

### 品牌提及掃描

品牌提及與 AI 可見度的相關性比反向連結強 3 倍。會掃描 YouTube、Reddit、Wikipedia、LinkedIn，以及其他 7 個以上平台。

### 平台特定最佳化

只有 11% 的網域會在同一查詢中同時被 ChatGPT 與 Google AI Overviews 引用。本工具會針對各平台提供客製化建議。

### llms.txt 產生

產生新興的 llms.txt 標準檔案，協助 AI 爬蟲理解你的網站結構。

### 可交付客戶的報告

產生 markdown 或 PDF 格式的專業 GEO 報告。PDF 報告包含分數儀表、長條圖、平台準備度視覺化、色彩標記表格，以及依優先順序排列的行動計畫，可直接交付客戶。

---

## 使用情境

- **GEO 代理商** — 執行客戶稽核並產生交付成果
- **行銷團隊** — 監控並改善 AI 搜尋可見度
- **內容創作者** — 為 AI 引用最佳化內容
- **在地商家** — 讓 AI 助理找得到你
- **SaaS 公司** — 改善各 AI 平台上的實體識別
- **電子商務** — 為 AI 購物推薦最佳化商品頁

---

## 解除安裝

```bash
./uninstall.sh
```

或手動執行：

```bash
rm -rf ~/.claude/skills/geo ~/.claude/skills/geo-* ~/.claude/agents/geo-*.md
```

---

## 想把這套工具變成一門生意？

這套工具是免費的。如何將它商業化，才是社群能幫上忙的地方。

**[加入 AI Workshop 社群 →](https://skool.com/aiworkshop)**

加入後你會獲得：

- **影片逐步教學** — 從設定、執行稽核到解讀結果的完整流程
- **客戶開發手冊** — 如何尋找潛在客戶、推廣 GEO 服務並成交
- **線上 office hours** — 帶著你的稽核結果來，獲得直接協助
- **GEO 代理商定價與範本** — 提案文件、陌生開發腳本、客戶 onboarding 流程

GEO 代理商收費每月 2,000-12,000 美元。這套工具負責稽核，社群教你如何銷售它。

---

## 授權

MIT License

---

## 貢獻

歡迎貢獻！

---

為 AI 搜尋時代而打造。
