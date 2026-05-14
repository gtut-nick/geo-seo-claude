# 架構與設計

此 repository 的結構是為了透過 Claude 的工具能力、agents 與 Python 工具 scripts，順暢提供 GEO+SEO 支援。

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
└── README.md                     # 主要專案總覽
```

### 完整稽核流程

當你執行 `/geo audit https://example.com`：

1. **探索** — 抓取首頁、偵測商業類型、爬取 sitemap
2. **平行分析** — 同時啟動 5 個 subagent：
   - AI 可見度（引用性、爬蟲、llms.txt、品牌提及）
   - 平台分析（ChatGPT、Perplexity、Google AIO 準備度）
   - 技術 SEO（Core Web Vitals、SSR、安全性、行動裝置）
   - 內容品質（E-E-A-T、可讀性、新鮮度）
   - Schema 標記（偵測、驗證、產生）
3. **彙整** — 彙總分數，產生綜合 GEO Score（0-100）
4. **報告** — 輸出依優先順序排列的行動計畫與快速成效項目

### 資料儲存

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
