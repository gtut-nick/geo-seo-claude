# 指令參考

此文件記錄 `geo-seo-claude` 技能套件中的每個指令。指令會在 Claude Code 中以 `/geo` 前綴呼叫。`geo/SKILL.md` 的主技能會作為 router：讀取 `/geo` 之後的第一個參數，並委派給 `skills/` 底下相符的 sub-skill。所有指令都接受 URL 作為主要參數；CRM 指令則操作 domain names 或 prospect IDs。任何產生分數的指令都會參照 [scoring-methodology.md](scoring-methodology.md) 中描述的權重模型。`/geo audit` 使用的平行 subagent 架構請見 [architecture.md](architecture.md)。

---

## 指令類別

**Audit** — 全站與聚焦分析

| Command | Description |
|---------|-------------|
| `/geo audit <url>` | 使用平行 subagents 執行完整 GEO + SEO 稽核 |
| `/geo quick <url>` | 60 秒 GEO 可見度快照 |
| `/geo citability <url>` | 評估單一頁面的 AI 引用準備度 |
| `/geo crawlers <url>` | 透過 robots.txt 與 meta tags 檢查 AI crawler access |
| `/geo llmstxt <url>` | 分析既有 llms.txt 或從零產生 |
| `/geo brands <url>` | 掃描 AI 引用平台上的品牌提及 |
| `/geo platforms <url>` | 平台特定準備度分數（AIO、ChatGPT、Perplexity、Gemini、Copilot） |

**Diagnostics** — 目標式技術與內容檢查

| Command | Description |
|---------|-------------|
| `/geo schema <url>` | 偵測、驗證並產生 Schema.org structured data |
| `/geo technical <url>` | 含 GEO 特定檢查的技術 SEO 稽核 |
| `/geo content <url>` | 內容品質與 E-E-A-T 評估 |

**Reports** — 可交付客戶的成果

| Command | Description |
|---------|-------------|
| `/geo report <url>` | 產生可交付客戶的 Markdown GEO 報告 |
| `/geo report-pdf <url>` | 產生含圖表與視覺化的專業 PDF 報告 |

**CRM** — 潛在客戶與客戶流程管理

| Command | Description |
|---------|-------------|
| `/geo prospect <cmd>` | 管理銷售流程中的 prospects |
| `/geo proposal <domain>` | 從稽核資料自動產生客戶提案 |
| `/geo compare <domain>` | 顯示分數改善的每月差異報告 |

---

## /geo audit

使用五個平行 subagents 對網站執行完整 GEO + SEO 稽核。

**Usage**

```
/geo audit https://example.com
```

**What it does**

- Phase 1（sequential）：抓取首頁、偵測商業類型（SaaS、Local、E-commerce、Publisher、Agency），並從 sitemap 或 internal links 爬取最多 50 頁。
- Phase 2（parallel）：同時委派給五個專門 subagents：AI visibility、platform analysis、technical SEO、content E-E-A-T 與 schema markup。subagent flow 請見 [architecture.md](architecture.md)。
- Phase 3（sequential）：將 subagent scores 彙總成加權綜合 GEO Score（0–100）。權重公式請見 [scoring-methodology.md](scoring-methodology.md)。
- 將每個 issue 依嚴重度分類：Critical、High、Medium 或 Low。
- 產生以週為主題的 30-day action plan。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | 要稽核網站的首頁 URL |

**Output**

將 `GEO-AUDIT-REPORT.md` 寫入 working directory。內容包含：executive summary、score breakdown table、各類別 deep dives、按嚴重度排列的 issue list、quick wins，以及逐週 30-day action plan。terminal 也會印出 inline summary。

**When to use it**

對任何新客戶或新網站先執行此指令；它是所有其他分析的 entry point。

---

## /geo quick

提供 60 秒 GEO 可見度快照，不寫入任何輸出檔。

**Usage**

```
/geo quick https://example.com
```

**What it does**

- 抓取首頁與少量 key pages。
- 對主要 GEO signals 執行輕量 pass：AI crawler access、llms.txt presence、homepage schema，以及 hero content 的粗略 citability read。
- 產生 approximate GEO score 與最高影響缺口的短列表。
- 從 CRM workflow 呼叫時，直接餵入 `/geo prospect audit`。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | 要建立快照的 URL |

**Output**

只有 inline terminal summary，不會寫檔。透過 `/geo prospect audit` 呼叫時，score 會儲存在 prospect record 中。

**When to use it**

完整稽核前用於快速 qualification check，或由 `/geo prospect audit` subcommand 自動呼叫時使用。

---

## /geo citability

使用五維 rubric 評估單一頁面的 AI citation readiness。

**Usage**

```
/geo citability https://example.com/blog/my-article
```

**What it does**

- 抓取頁面，並在每個 H2/H3 邊界將內容分段成 blocks。
- 依五個維度評估每個 block：answer block quality（30%）、passage self-containment（25%）、structural readability（20%）、statistical density（15%）與 uniqueness/original data（10%）。
- 找出前三個最強與三個最弱的 blocks。
- 對每個低於 60 分的 block 產生具體 rewrite suggestions，包括建議 opening sentence。rubric 細節請見 [scoring-methodology.md](scoring-methodology.md)。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | 要評分的特定頁面 URL |

**Output**

寫出 `GEO-CITABILITY-SCORE.md`。內容包含：overall citability score、weighted score table、含引用 excerpt 的 strongest/weakest block analysis、rewrite suggestions，以及 per-section score table。

**When to use it**

用於任何內容頁發布前，或用來決定哪些既有頁面應優先改寫以提高 AI citation。

---

## /geo crawlers

分析哪些 AI crawlers 能存取網站，並提供建議 robots.txt 設定。

**Usage**

```
/geo crawlers https://example.com
```

**What it does**

- 抓取並解析 `robots.txt`，將每個 User-agent directive 對應到 14 個已知 AI crawlers。
- 抽樣 key pages 檢查 `<meta name="robots">` overrides 與 `X-Robots-Tag` HTTP headers。
- 檢查 `/llms.txt` 與 `/.well-known/ai-plugin.json` 是否存在。
- 評估 key content 是否需要 JavaScript rendering（AI crawlers 不執行 JS）。
- 以三層級評估 crawler access：Tier 1（ChatGPT、Claude、Perplexity，對 AI search 關鍵）、Tier 2（Gemini、Copilot、Apple Intelligence、Meta AI）與 Tier 3（training-only crawlers）。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | Domain root URL |

**Output**

寫出 `GEO-CRAWLER-ACCESS.md`。內容包含：per crawler access summary table、AI visibility score（0–100）、critical issues list，以及一段可直接貼上的完整 robots.txt block，用於最大化 AI visibility。

**When to use it**

當客戶回報沒有出現在 AI search results 時，可作為快速獨立檢查；也可在部署 robots.txt 變更前驗證。

---

## /geo llmstxt

分析既有 `llms.txt` 的品質；若不存在，則從零產生新的檔案。

**Usage**

```
/geo llmstxt https://example.com
```

**What it does**

- 抓取 `https://example.com/llms.txt` 與 `llms-full.txt` 並檢查 HTTP status。
- **Analysis mode**（檔案存在）：驗證格式（H1 title、blockquote description、H2 sections、absolute URLs、entry descriptions、Key Facts、Contact section）；評估 completeness（40%）、accuracy（35%）與 usefulness（25%）；找出檔案中缺少的重要頁面。
- **Generation mode**（檔案不存在）：爬取 sitemap 與 homepage，依 page type 排序，為每個選中的頁面撰寫 10-30 word descriptions，收集 key business facts，並組裝可部署的完整 `llms.txt`。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | Domain root URL |

**Output**

- Analysis mode：寫出 `GEO-LLMSTXT-ANALYSIS.md`，含 validation results、missing pages 與 suggested updated file。
- Generation mode：寫出可部署的 `llms.txt` file，以及簡短 `GEO-LLMSTXT-GENERATION.md`，說明 prioritization decisions。

**When to use it**

用於任何網站，以驗證既有 `llms.txt` 或產生新的檔案。截至 2026 年初，少於 5% 網站擁有 `llms.txt`，因此它是容易取得的 quick win。

---

## /geo brands

掃描 AI 系統用於 entity recognition 與 citation decisions 的平台上的品牌提及。

**Usage**

```
/geo brands https://example.com
```

**What it does**

- 檢查 YouTube（channel existence、subscriber count、third-party video mentions）、Reddit（thread volume、sentiment、official presence、subreddit）、Wikipedia/Wikidata（article existence、Wikidata Q-number、quality class）與 LinkedIn（company page、follower count、post frequency）上的品牌 presence。
- 直接使用 Wikipedia API（`en.wikipedia.org/w/api.php`），避免 web search false negatives。
- 也掃描 supplementary platforms：Quora、Stack Overflow、GitHub、Hacker News 與 press/news。
- 計算 composite Brand Authority Score：YouTube 25%、Reddit 25%、Wikipedia/Wikidata 20%、LinkedIn 15%、其他平台 15%。請見 [scoring-methodology.md](scoring-methodology.md)。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | Domain URL（品牌名稱會從網站推斷） |

**Output**

寫出 `GEO-BRAND-MENTIONS.md`。內容包含：Brand Authority Score（0–100）、per-platform breakdown tables、sentiment assessment、competitive context table（若辨識出 competitors），以及依時間範圍分組的 priority recommendations（week 1–2、month 1–3、month 3–12）。

**When to use it**

當網站技術與內容都不差，卻沒有出現在 AI-generated recommendations 中時使用；也可作為 entity-building strategy 的一部分。

---

## /geo platforms

分別稽核各主要 AI search platform 的準備度並產生 per-platform scores。

**Usage**

```
/geo platforms https://example.com
```

**What it does**

- 對五個平台各自執行 checklist 與 scoring rubric：Google AI Overviews、ChatGPT Web Search、Perplexity AI、Google Gemini 與 Bing Copilot。
- Google AIO checklist 涵蓋：top-10 organic ranking、question-based headings、direct answer structure、tables、FAQ sections、statistics with attribution、author bylines 與 publication dates。
- ChatGPT checklist 涵蓋：Wikipedia/Wikidata entity、Bing index coverage、Reddit mentions、YouTube presence、entity consistency 與 content comprehensiveness。
- Perplexity checklist 涵蓋：Reddit presence、forum mentions、content freshness、original research、quotable paragraphs 與 multi-source claim validation。
- Gemini checklist 涵蓋：Google Knowledge Panel、Google Business Profile、YouTube strategy、Schema.org markup 與 Google ecosystem presence。
- Copilot checklist 涵蓋：Bing Webmaster Tools、IndexNow implementation、LinkedIn page、meta descriptions 與 page load speed。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | 網站首頁 URL |

**Output**

寫出 `GEO-PLATFORM-OPTIMIZATION.md`。內容包含：overall combined score、per-platform score table、含具體 actions 的 per-platform gap analysis，以及 priority action plan（quick wins、medium-term、strategic）。platform 在綜合分數中的權重請見 [scoring-methodology.md](scoring-methodology.md)。

**When to use it**

當你需要知道網站在哪些特定 AI platforms 表現不足，或要建立 platform-targeted optimization roadmap 時使用。

---

## /geo schema

偵測網站上的所有 structured data，依 Schema.org 規格驗證，並為缺少或不完整的 schemas 產生可直接貼上的 JSON-LD blocks。

**Usage**

```
/geo schema https://example.com
```

**What it does**

- 使用 `fetch_page.py` 抓取 raw HTML（不是 WebFetch，因為 WebFetch 會移除 `<head>` content），以抽出所有 JSON-LD、Microdata 與 RDFa blocks。
- 驗證每個 schema：JSON syntax、valid `@type`、required properties、recommended properties、`sameAs` links、URL validity、nesting，以及 schema 是 server-rendered 或 JS-injected。
- 檢查 GEO-critical schema types：Organization、LocalBusiness、Article with Author、Product、FAQPage、SoftwareApplication、WebSite with SearchAction 與 BreadcrumbList。
- 依 14 個平台的 priority list 稽核 `sameAs` property（Wikipedia、Wikidata、LinkedIn、YouTube、Twitter/X、GitHub、Crunchbase 等）。
- 使用 `@graph` pattern 為缺少或不完整的 schemas 產生完整 JSON-LD code blocks。schema score 如何餵入綜合 GEO Score，請見 [scoring-methodology.md](scoring-methodology.md)。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | 要稽核的頁面或 domain URL |

**Output**

寫出 `GEO-SCHEMA-REPORT.md`。內容包含：schema score（0–100）、detected schemas table、per-property validation results、missing schema list、sameAs audit table，以及含 implementation notes 的 ready-to-paste JSON-LD code blocks。

**When to use it**

用於給開發團隊一張 self-contained implementation ticket，或在 CMS migration 後驗證 schema quality。

---

## /geo technical

跨八個類別執行技術 SEO 稽核，特別重視 server-side rendering 與 AI crawler access。

**Usage**

```
/geo technical https://example.com
```

**What it does**

- Crawlability（15 pts）：robots.txt validity、11 個 named bots 的 AI crawler access、XML sitemap presence and validity、crawl depth、noindex directives。
- Indexability（12 pts）：canonical tags、duplicate content（www/HTTP/trailing-slash）、pagination、hreflang。
- Security（10 pts）：HTTPS enforcement、HSTS、`X-Content-Type-Options`、`X-Frame-Options`、`Referrer-Policy`、CSP。
- URL structure（8 pts）：clean readable URLs、logical hierarchy、redirect chains、parameter handling。
- Mobile optimization（10 pts）：viewport meta tag、responsive layout、tap target sizing、font legibility。
- Core Web Vitals（15 pts）：依 2026 thresholds 檢查 LCP < 2.5s、INP < 200ms、CLS < 0.1。
- Server-side rendering（15 pts）：比較 `curl` output 與 rendered DOM；標記 AI crawlers 無法讀取的 client-rendered content。
- Page speed and server performance（15 pts）：TTFB、page weight、image optimization、JS bundle size、compression、caching、CDN。technical score 如何餵入 composite，請見 [scoring-methodology.md](scoring-methodology.md)。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | Domain root URL |

**Output**

寫出 `GEO-TECHNICAL-AUDIT.md`。內容包含：technical score（0–100）、含 Pass/Warn/Fail status 的 per-category score table、AI crawler access table、critical issues list、warnings 與 recommendations。

**When to use it**

當網站內容很強但 AI visibility 很弱時使用，或用於產生 developer-facing remediation checklist。

---

## /geo content

透過 E-E-A-T framework（Experience、Expertise、Authoritativeness、Trustworthiness）評估內容品質，並評估 AI citability 與 topical authority。

**Usage**

```
/geo content https://example.com
```

**What it does**

- 以 25-point scale 評估四個 E-E-A-T dimensions：Experience（first-person accounts、original data、case studies）、Expertise（author credentials、technical depth、methodology、data-backed claims）、Authoritativeness（inbound citations、press mentions、awards、Wikipedia presence）、Trustworthiness（contact info、privacy policy、HTTPS、editorial standards、accurate claims）。
- 套用 topical authority modifier：20+ 頁且 clustering 強加 +10，低到少於 5 頁則 -5。
- 評估每頁 content freshness（< 3 months 到 no-date/24+ months）。
- 標記 low-quality AI-generated content patterns（generic phrasing、no original insight、hedging overload）並辨識 high-quality signals。
- 檢查每種 page type 的 word count benchmarks 與 AI extraction 需要的 paragraph structure。content score 如何餵入 composite，請見 [scoring-methodology.md](scoring-methodology.md)。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | Domain root URL（分析 homepage 與 key content pages） |

**Output**

寫出 `GEO-CONTENT-ANALYSIS.md`。內容包含：content score（0–100）、E-E-A-T breakdown table、pages-analyzed table、每個 dimension 的 detailed findings、含 rewrite suggestions 的 content quality issues、AI content concerns、freshness assessment、最可引用與最不可引用 passages、content gap recommendations，以及 E-E-A-T improvement steps。

**When to use it**

當網站技術基礎良好，但沒有被 AI systems 引用，顯示內容品質有問題時使用。

---

## /geo report

將所有 audit skills 的輸出彙總成單一專業、面向客戶的 Markdown report。

**Usage**

```
/geo report https://example.com
```

**What it does**

- 讀取 working directory 中既有 `GEO-*.md` audit files；必要時自動執行缺少的 audits。
- 計算 composite GEO Readiness Score：AI Platform Readiness 25%、Content E-E-A-T 25%、Technical Foundation 20%、Schema 15%、Brand Authority 15%。請見 [scoring-methodology.md](scoring-methodology.md)。
- 將所有 technical findings 翻譯成面向 business owners 與 marketing leaders 的 business-impact language，而不是面向 developers。
- 產生 12 個結構化 sections：executive summary、score dashboard、AI visibility dashboard（per platform）、AI crawler access table、brand authority analysis、citability analysis（top 5 / bottom 5 pages）、technical health summary、schema status、llms.txt status、prioritized action plan（quick wins / medium / strategic）、competitor comparison（若分析 competitors）與 glossary appendix。
- 包含與 score improvements 相關的保守 traffic 與 revenue impact estimates。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | Domain URL；working directory 中既有 audit files 會被自動使用 |

**Output**

寫出 `GEO-CLIENT-REPORT.md`。報告長度為 3,000–6,000 words，self-contained，可直接交付，不需要再編輯。

**When to use it**

完整 audit suite 執行後，或每月 engagement cycle 結束時，用於產生最終交付成果。

---

## /geo report-pdf

將 GEO audit data 轉成具專業格式的 PDF，包含 charts、score gauges 與 color-coded tables。

**Usage**

```
/geo report-pdf https://example.com
```

**What it does**

- 檢查 working directory 中是否有既有 `GEO-CLIENT-REPORT.md` 或 `GEO-AUDIT-REPORT.md`；若沒有，先執行 full audit。
- 解析 Markdown report，抽出 scores、platform readiness numbers、crawler status、findings 與 action items。
- 將資料組裝成 PDF generation script 預期的 JSON schema。
- 呼叫 `python3 ~/.claude/skills/geo/scripts/generate_pdf_report.py`（需要 `pip install reportlab`）。
- PDF 使用 US Letter size，navy/blue/coral 色盤；score gauges 使用 traffic-light colors（green 80+、blue 60–79、yellow 40–59、red below 40）。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<url>` | Yes | Domain URL；用於定位或產生 audit data |

**Output**

將 `GEO-REPORT-<brand>.pdf` 寫入 working directory。PDF 包含：含 score gauge 的封面、executive summary、score breakdown bar chart、AI platform readiness horizontal bar chart、crawler access color-coded table、依嚴重度排列的 key findings、prioritized action plan，以及 methodology/glossary appendix。完成時會回報 file path 與 size。

**When to use it**

當交付成果需要直接 email 給期待 polished document 而不是 Markdown 檔案的客戶時使用。

---

## /geo prospect

一個 CRM-lite pipeline manager，用於追蹤 prospects 與 clients，從 initial discovery 到 contract。

**Usage**

```
/geo prospect new <domain>
/geo prospect list [<status>]
/geo prospect show <id-or-domain>
/geo prospect audit <id-or-domain>
/geo prospect note <id-or-domain> "<text>"
/geo prospect status <id-or-domain> <new-status>
/geo prospect won <id-or-domain> <monthly-value>
/geo prospect lost <id-or-domain> "<reason>"
/geo prospect pipeline
```

**What it does**

- 將所有 prospect data 儲存在 `~/.geo-prospects/prospects.json`，作為持久 JSON records，包含 ID、company、domain、status、GEO score、audit file path、proposal file path、monthly contract value 與 timestamped notes。
- 追蹤五個 pipeline stages：`lead`、`qualified`、`proposal`、`won`、`lost`。
- `prospect audit` 呼叫 `/geo quick`，並將 resulting score 儲存到 prospect record。
- `prospect pipeline` 印出 revenue-focused summary，顯示 committed MRR、pipeline value 與每筆 record 的 suggested next actions。
- 所有 subcommands 都會在 terminal 印出 confirmation 與 current prospect status；除了 audit snapshots 與 proposals 外，不會寫入外部檔案。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<cmd>` | Yes | Subcommand：`new`、`list`、`show`、`audit`、`note`、`status`、`won`、`lost`、`pipeline` |
| `<id-or-domain>` | Contextual | Prospect ID（例如 `PRO-001`）或 domain name |
| `<status>` | For `status`, `list` | Pipeline stage：`lead`、`qualified`、`proposal`、`won`、`lost` |
| `<monthly-value>` | For `won` | Numeric monthly contract value |
| `"<text>"` | For `note`, `lost` | Free-text note 或 lost reason |

**Output**

更新 `~/.geo-prospects/prospects.json`。Audit snapshots 儲存到 `~/.geo-prospects/audits/`。所有 subcommands 都有 terminal output。

**When to use it**

用於管理持續進行的 GEO agency sales pipeline，並跨 sessions 追蹤 client history。

---

## /geo proposal

從 audit data 自動產生完全客製、可交付客戶的 GEO service proposal。

**Usage**

```
/geo proposal <domain>
/geo proposal <domain> --tier basic|standard|premium --client-name "Name" --monthly EUR
```

**Examples**

```
/geo proposal example.com
/geo proposal example.com --tier standard --client-name "Acme Corp"
/geo proposal ~/.geo-prospects/audits/example.com-2026-03-12.md
```

**What it does**

- 從 `~/.geo-prospects/audits/<domain>*.md` 載入最新 audit file（若不存在則執行 `/geo quick`）。
- 依 GEO score 選擇建議 service tier：0–40 → Premium，41–60 → Standard，61–75 → Basic。
- 填入 12-section proposal template：executive summary、market context tables、audit findings、含 pricing 的 three-tier service packages（Basic €2,500/mo、Standard €5,000/mo、Premium €9,500/mo）、ROI projection table、six-month engagement timeline、investment summary 與 terms。
- 將 prospect record status 更新為 `proposal`，並儲存 proposal file path。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<domain>` | Yes | Domain name 或 audit file path |
| `--tier` | No | 強制使用指定 tier，而不是 score-based recommendation |
| `--client-name` | No | 覆寫自動偵測出的 company name |
| `--monthly` | No | 覆寫 estimated monthly contract value |

**Output**

寫出 `~/.geo-prospects/proposals/<domain>-proposal-<date>.md`。印出 confirmation，含 recommended package 與 price。proposal 不需編輯即可送出。

**When to use it**

在 prospect audit 後立即使用，尤其當 GEO score 顯示明確銷售機會（score below 75）時。

---

## /geo compare

產生每月差異報告，將 baseline audit 與 current audit 比較，向客戶顯示 score improvements。

**Usage**

```
/geo compare <domain>
/geo compare <baseline-file> <current-file>
/geo compare <domain> --month march-2026
```

**What it does**

- 在 `~/.geo-prospects/audits/` 中尋找符合 domain 的 audit files；最舊作為 baseline，最新作為 current。若只有一個檔案，會執行新的 quick audit 作為 current snapshot。
- 從兩個檔案抽出 overall GEO score、六個 category scores、五個 platform scores，以及 AI crawler status。
- 計算 deltas 並指定 trend symbols（▲▲ strong improvement、▲ improvement、── unchanged、▼ decline、▼▼ significant decline）。
- 追蹤 quick wins、medium-term 與 strategic action items 的完成狀態。
- 包含 six-month trajectory table 與保守 business impact estimate（AI citation likelihood change、crawler coverage、estimated traffic value）。

**Inputs**

| Argument | Required | Description |
|----------|----------|-------------|
| `<domain>` | Yes（或 two file paths） | Domain name，或 baseline 與 current audit files 的明確 paths |
| `--month` | No | 報告檔名的 month label |

**Output**

寫出 `~/.geo-prospects/reports/<domain>-monthly-<YYYY-MM>.md`。terminal 會印出 summary，顯示 score change、quick wins completion rate、new issues found，以及 six-month target 是否 on track。

**When to use it**

每月第一天對每個 active client 執行，產生證明 retainer 價值的 progress report。

---

## 差異

在 `geo/SKILL.md` 與 `skills/` 目錄之間發現以下差異：

- **`/geo quick`**：列在 `geo/SKILL.md`，並在整個 codebase 中被 `geo-prospect` 與 `geo-compare` 引用，但沒有 `skills/geo-quick/SKILL.md`。quick-scan 行為只透過 `geo/SKILL.md` 與 `geo-prospect` skill 中的 orchestration instructions 記錄。以上文件是根據這些引用撰寫。
- **`/geo page`**：列在 `geo/SKILL.md` 的 quick reference table（作為 `/geo page <url>` — deep single-page GEO analysis），也列在 output files table（產生 `GEO-PAGE-ANALYSIS.md`），但沒有 `skills/geo-page/SKILL.md`。不存在實作。因沒有 skill file 可參照，此指令**未在上方 reference 中記錄**。
- **原始 `docs/commands-reference.md` 中的 `/geo quick`**：舊表列出 `/geo quick`，但 `geo/SKILL.md` 未在 sub-skills table 中列出（只在 quick reference table 中）。由於 prospect 與 compare skills 將它作為真實行為引用，因此上方保留它。
