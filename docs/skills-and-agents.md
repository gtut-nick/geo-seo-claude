# Skills、Agents、Scripts 與 Schemas

此參考文件說明 `geo-seo-claude` 技能套件中的每個組件。此套件會為 Generative Engine Optimization（GEO）最佳化網站，使內容能被 AI search platforms（ChatGPT、Perplexity、Google AI Overviews、Gemini、Bing Copilot）發現與引用，同時維持傳統 SEO 基礎。它由 1 個 orchestrator skill、14 個 sub-skills、5 個平行 subagents、6 個 Python helper scripts，以及 6 個 JSON-LD schema templates 組成。

完整 slash-command reference 請見 [commands-reference.md](commands-reference.md)，完整稽核時平行 subagent flow 如何運作請見 [architecture.md](architecture.md)。

---

## 協調器

- **geo**（`geo/SKILL.md`）— 所有 GEO 指令的 entry point。偵測商業類型、為個別指令 dispatch sub-skills，並協調三階段完整稽核流程：discovery、parallel subagent delegation 與 score synthesis。產生跨六個類別加權的綜合 GEO Score（0–100）。

---

## Sub-skills

### geo-audit

**Purpose:** 透過 discovery、委派五個平行 subagents，並將它們的分數彙總成單一綜合 GEO Score，協調完整 GEO + SEO 稽核。

**Inputs:** URL。可選：pre-crawled page data。

**Outputs:** `GEO-AUDIT-REPORT.md` — composite score、per-category breakdown、issue severity list（Critical / High / Medium / Low）、30-day action plan，以及 analyzed pages appendix。

**Scoring weights:**
- AI Citability 25%、Brand Authority 20%、Content E-E-A-T 20%、Technical GEO 15%、Structured Data 10%、Platform Optimization 10%

**Dependencies:** 委派給全部五個 subagents（`geo-ai-visibility`、`geo-platform-analysis`、`geo-technical`、`geo-content`、`geo-schema`）。

`/geo audit` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-citability

**Purpose:** 以 0–100 scale 評估個別內容段落的 AI citation readiness。衡量 AI system 直接擷取與引用段落的可能性。

**Inputs:** URL（以 WebFetch 抓取）。

**Outputs:** `GEO-CITABILITY-SCORE.md` — per-section scores、top citation-ready passages、含 rewrite suggestions 的 weakest blocks，以及 citability coverage percentage。

**Scoring dimensions（per passage）:** Answer Block Quality（30%）、Self-Containment（25%）、Structural Readability（20%）、Statistical Density（15%）、Uniqueness（10%）。

**Key threshold:** 最佳 AI-cited passages 長度為 134–167 words、自成一體、事實豐富，並在前 1–2 句回答問題。

`/geo citability` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-crawlers

**Purpose:** 透過解析 `robots.txt`、meta robots tags 與 HTTP `X-Robots-Tag` headers，稽核哪些 AI crawlers 能存取網站。產生跨三層級 14 個 crawlers 的完整 access map。

**Inputs:** Domain URL。

**Outputs:** `GEO-CRAWLER-ACCESS.md` — per-crawler status（Allowed / Blocked / Not Mentioned）、AI Visibility Score、建議 `robots.txt` configuration，以及 JavaScript rendering assessment。

**Crawler tiers:**
- Tier 1（search visibility）：GPTBot、OAI-SearchBot、ChatGPT-User、ClaudeBot、PerplexityBot
- Tier 2（broader AI ecosystem）：Google-Extended、GoogleOther、Applebot-Extended、Amazonbot、FacebookBot
- Tier 3（training-only）：CCBot、anthropic-ai、Bytespider、cohere-ai

`/geo crawlers` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-llmstxt

**Purpose:** 分析既有 `llms.txt` file 的格式合規性與完整度，或透過爬取網站從零產生新檔。`llms.txt` 標準會提供 AI systems 關於網站結構與 key pages 的明確 guidance。

**Inputs:** Domain URL。以 analysis mode（檔案存在）或 generation mode（檔案不存在）運作。

**Outputs（analysis mode）:** `GEO-LLMSTXT-ANALYSIS.md` — format validation table、missing pages、overall llms.txt score（Completeness 40%、Accuracy 35%、Usefulness 25%）。

**Outputs（generation mode）:** 可部署的 `llms.txt` file 與 `GEO-LLMSTXT-GENERATION.md`，說明 page selection rationale。

**Dependencies:** `scripts/llmstxt_generator.py` 提供 validation 與 generation helpers。

`/geo llmstxt` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-brand-mentions

**Purpose:** 掃描品牌在 AI models 用於 entity recognition 與 citation decisions 的平台上的 presence。依 platform-weighted presence 產生 Brand Authority Score。

**Inputs:** Brand name、domain URL、industry（若未提供，從網站收集）。

**Outputs:** `GEO-BRAND-MENTIONS.md` — per-platform scores（YouTube 25%、Reddit 25%、Wikipedia/Wikidata 20%、LinkedIn 15%、Other 15%）、sentiment assessment、composite Brand Authority Score，以及 prioritized recommendations。

**Key insight:** YouTube mentions 與 AI citation 的相關性約 0.737；Domain Rating correlation 約 0.266（Ahrefs，2025 年 12 月，75,000 brands study）。

**Dependencies:** `scripts/brand_scanner.py` 提供 platform-check framework。Wikipedia checks 會透過 Bash 直接使用 Wikipedia API（只用 web search 容易產生 false negatives）。

`/geo brands` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-platform-optimizer

**Purpose:** 分別稽核五個主要 AI search platforms 的準備度，因為同一 query 中只有 11% domains 同時被 ChatGPT 與 Google AI Overviews 引用。

**Inputs:** URL 與網站主要 topic 或 industry。

**Outputs:** `GEO-PLATFORM-OPTIMIZATION.md` — Google AI Overviews、ChatGPT Web Search、Perplexity AI、Google Gemini、Bing Copilot 的 per-platform scores 與 gaps；cross-platform priority action plan。

**Platform-specific top factors:** AIO → top-10 ranking + Q&A structure；ChatGPT → Wikipedia entity；Perplexity → Reddit presence + original research；Gemini → YouTube + Knowledge Panel；Bing Copilot → IndexNow + Bing Webmaster Tools。

`/geo platforms` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-schema

**Purpose:** 偵測、驗證並產生 Schema.org structured data（偏好 JSON-LD）。Structured data 是 AI models 用來識別與信任 entities 的主要 machine-readable signal。

**Inputs:** URL。使用 `scripts/fetch_page.py` 取得包含 `<head>` content 的 raw HTML（WebFetch 會移除它）。

**Outputs:** `GEO-SCHEMA-REPORT.md` — detected schemas 與 validation results、`sameAs` entity-linking audit、deprecated schema flags（HowTo removed Sep 2023、FAQPage restricted Aug 2023），以及 ready-to-paste JSON-LD code blocks。

**GEO-critical schemas:** Organization + `sameAs`、Article + Author（Person）、speakable property、BreadcrumbList、WebSite + SearchAction。

**Dependencies:** `scripts/fetch_page.py`（raw HTML extraction）；`schema/*.json` templates（作為 generation references）。

`/geo schema` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-technical

**Purpose:** 稽核八個 technical health categories，重點放在獨特影響 AI crawler visibility 的因素：server-side rendering 與 AI crawler access。

**Inputs:** Homepage URL 加上 2–3 個 key inner pages。

**Outputs:** `GEO-TECHNICAL-AUDIT.md` — category scores、AI crawler access table、SSR assessment、Core Web Vitals risk（LCP / INP / CLS）、security headers 與 mobile optimization status。

**Scoring categories（max points）:** Server-Side Rendering 15、Core Web Vitals 15、Crawlability 15、Indexability 12、Security 10、Mobile 10、Page Speed 15、URL Structure 8。

**Critical check:** AI crawlers 不執行 JavaScript。沒有 SSR 的 client-side SPA 會對 GPTBot、ClaudeBot 與 PerplexityBot 呈現空頁。

`/geo technical` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-content

**Purpose:** 透過 E-E-A-T framework（Experience、Expertise、Authoritativeness、Trustworthiness）評估內容品質，並衡量 content depth、readability、AI content indicators 與 topical authority。

**Inputs:** URL（以 WebFetch 抓取）。

**Outputs:** `GEO-CONTENT-ANALYSIS.md` — E-E-A-T scores（各 25 points）、content metrics table、AI content assessment、topical authority rating、freshness assessment 與 rewrite recommendations。

**Score modifiers:** Topical authority 會在 base 100-point E-E-A-T score 上加 +10 到 -5 points。

`/geo content` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-report

**Purpose:** 將所有 audit sub-skills 的輸出彙總為單一 client-facing deliverable，寫給 business owners 而不是 developers；technical findings 會轉成 business impact 與 dollar-value framing。

**Inputs:** `geo-platform-optimizer`、`geo-schema`、`geo-technical`、`geo-content` 的輸出檔，以及選用的 `geo-llmstxt` 與 `geo-brand-mentions`。

**Outputs:** `GEO-CLIENT-REPORT.md` — executive summary、GEO Readiness Score、AI Visibility Dashboard、crawler access table、brand authority table、citability analysis、technical health summary、schema status、含 effort 與 platform impact 的 action plan，以及完整 glossary appendix。目標長度：3,000–6,000 words。

`/geo report` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-report-pdf

**Purpose:** 使用 ReportLab 從 GEO audit data 產生專業格式、可交付客戶的 PDF。包含 score gauges、bar charts 與 color-coded tables。

**Inputs:** 目前目錄中的既有 `GEO-AUDIT-REPORT.md` 或 `GEO-CLIENT-REPORT.md` files。若傳入 URL，會先執行 full audit。

**Outputs:** `GEO-REPORT-[brand].pdf` — 含 score gauge 的 cover page、含 bar chart 的 score breakdown、AI platform readiness chart、crawler access table（green/red coded）、依嚴重度整理的 findings、action plan 與 methodology appendix。

**Dependencies:** `scripts/generate_pdf_report.py`（需要 `pip install reportlab`）。

`/geo report-pdf` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-prospect

**Purpose:** 管理 GEO agency prospects 的 CRM-lite，透過五階段 sales pipeline（lead → qualified → proposal → won → lost）追蹤。所有資料持久化在 `~/.geo-prospects/prospects.json`。

**Inputs:** 透過 sub-commands 輸入的 domain names、contact details、status updates 與 notes。

**Outputs:** 更新 `prospects.json`；audit snapshots 位於 `~/.geo-prospects/audits/`；terminal 會印出 pipeline summary table。

**Key sub-commands:** `new`、`list`、`show`、`audit`、`note`、`status`、`won`、`lost`、`pipeline`。

**Dependencies:** `scripts/crm_dashboard.py` 提供 rich terminal dashboard（需要 `pip install rich`）。

`/geo prospect` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-proposal

**Purpose:** 從 audit data 自動產生可交付客戶的 GEO service proposal，包含 executive summary、score breakdown、三個 service tiers 與 pricing、ROI projection、engagement timeline。

**Inputs:** Domain name 或既有 audit file path。若可用，會讀取 `~/.geo-prospects/prospects.json` 中的 prospect record。

**Outputs:** `~/.geo-prospects/proposals/<domain>-proposal-<date>.md` — 完整且可直接送出的 proposal。也會將 prospect record status 更新為 `proposal`。

**Tier recommendation logic:** Score 0–40 → Premium（€9,500/mo）；41–60 → Standard（€5,000/mo）；61–75 → Basic（€2,500/mo）。

`/geo proposal` 請見 [commands-reference.md](commands-reference.md)。

---

### geo-compare

**Purpose:** 產生每月 delta report，比較兩份 GEO audits（baseline vs. current），追蹤所有類別的 score improvements 與 action-item completion status。

**Inputs:** Domain name 或兩個 audit file paths。若只提供 domain，會讀取 `~/.geo-prospects/audits/` 中依日期排序的檔案。

**Outputs:** `~/.geo-prospects/reports/<domain>-monthly-<YYYY-MM>.md` — score progress bar、before/after breakdown table、platform and crawler delta tables、action plan status、wins section、new issues discovered 與 6-month trajectory。

`/geo compare` 請見 [commands-reference.md](commands-reference.md)。

---

## 平行 Subagents

這五個 agents 會在 `/geo audit` 期間同時執行，以降低總執行時間。每個都會回傳 structured markdown section 與 category score（0–100），並餵入 composite GEO Score。平行流程圖請見 [architecture.md](architecture.md)。

### geo-ai-visibility

**File:** `agents/geo-ai-visibility.md`

**Role:** GEO specialist，涵蓋四個最高權重的 AI visibility dimensions。

**Dispatched when:** `/geo audit` 的 Phase 2 開始。

**What it does:** 依 citability（5-dimension rubric）評估每個 content block、解析 `robots.txt` 中的 12 個 AI crawlers、驗證 `llms.txt` format 與 completeness，並掃描 YouTube、Reddit、Wikipedia 與 LinkedIn 上的 brand presence。

**Returns:** AI Visibility Score = Citability（35%）+ Brand Mentions（30%）+ Crawler Access（25%）+ llms.txt（10%）。

**Sub-skills used:** geo-citability、geo-crawlers、geo-llmstxt、geo-brand-mentions。

---

### geo-platform-analysis

**File:** `agents/geo-platform-analysis.md`

**Role:** Platform optimization specialist。

**Dispatched when:** `/geo audit` 的 Phase 2 開始（與其他 agents 同時）。

**What it does:** 使用 platform-specific scoring rubrics 與 signal checks，評估五個 AI search platforms 的準備度：Google AI Overviews、ChatGPT Web Search、Perplexity AI、Google Gemini 與 Bing Copilot。

**Returns:** Per-platform scores（各 0–100）與 Platform Readiness Average；cross-platform synergy actions。

**Sub-skill used:** geo-platform-optimizer。

---

### geo-technical

**File:** `agents/geo-technical.md`

**Role:** Technical SEO specialist。

**Dispatched when:** `/geo audit` 的 Phase 2 開始（與其他 agents 同時）。

**What it does:** 抓取 raw HTML 與 response headers；稽核 SSR vs. CSR rendering（最高權重檢查）、crawlability、meta tags、security headers、Core Web Vitals risk indicators、mobile optimization 與 URL structure。

**Returns:** Technical Score（0–100）與 per-category breakdown；SSR severity rating（Critical / High / Medium / Low）。

**Sub-skill used:** geo-technical。

---

### geo-content

**File:** `agents/geo-content.md`

**Role:** Content quality specialist。

**Dispatched when:** `/geo audit` 的 Phase 2 開始（與其他 agents 同時）。

**What it does:** 依四個 dimensions（各 25 points）評估 E-E-A-T、衡量 word count、readability（Flesch）、heading structure 與 internal linking、偵測 AI content quality signals、評估 topical authority 與 content freshness。

**Returns:** Content Score（0–100）；E-E-A-T breakdown；AI content assessment label。

**Sub-skill used:** geo-content。

---

### geo-schema

**File:** `agents/geo-schema.md`

**Role:** Schema markup specialist。

**Dispatched when:** `/geo audit` 的 Phase 2 開始（與其他 agents 同時）。

**What it does:** 使用 `fetch_page.py` 取得 raw HTML，偵測所有 JSON-LD / Microdata / RDFa blocks，依 Schema.org specifications 驗證，稽核 `sameAs` entity links，標記 deprecated 或 JS-injected schemas，並為缺少的 schemas 產生可直接貼上的 JSON-LD templates。

**Returns:** Schema Score（0–100）；validated schema inventory；generated JSON-LD code blocks。

**Sub-skill used:** geo-schema。

---

## Python Scripts

| Script | Purpose | Used by |
|--------|---------|---------|
| `scripts/fetch_page.py` | 抓取 URL 並回傳 structured data，包含 raw HTML、meta tags、heading structure、word count 與 parsed JSON-LD blocks。繞過 WebFetch 套用的 markdown conversion，保留 `<head>` content。 | geo-schema（skill + agent）、geo-technical |
| `scripts/citability_scorer.py` | 使用五個加權維度（answer quality、self-containment、structure、statistical density、uniqueness）評估個別 text passages 的 AI citation readiness。提供 `score_passage()` 作為 callable function。 | geo-citability |
| `scripts/brand_scanner.py` | 檢查 AI-cited platforms（YouTube、Reddit、Wikipedia、LinkedIn）上的 brand presence。提供 per-platform check functions 與 WebFetch-based verification instructions。需要 `requests` 與 `beautifulsoup4`。 | geo-brand-mentions |
| `scripts/llmstxt_generator.py` | 依 spec（H1 title、blockquote description、H2 sections、absolute URLs、descriptions）驗證既有 `llms.txt`，並從 site crawl data 產生新檔。 | geo-llmstxt |
| `scripts/generate_pdf_report.py` | 使用 ReportLab 從 JSON audit data file 產生 multi-page PDF。render score gauges、bar charts、color-coded tables 與 action plan。接受 JSON file path 作為 CLI argument 或 stdin。需要 `reportlab`。 | geo-report-pdf |
| `scripts/crm_dashboard.py` | render prospect CRM 的 rich terminal dashboard。讀取 `~/.geo-prospects/prospects.json`，並顯示 pipeline stages、MRR 與 prospect detail views。需要 `rich`。 | geo-prospect |

---

## Schema 範本

`schema/` 中的這些 JSON-LD files 是 `geo-schema` 或 `geo-report` 需要產生可直接貼上的 structured data 時使用的 generation references。所有 placeholders 都遵循 `YOUR_FIELD_NAME` 或 `REPLACE_WITH_VALUE` pattern。

| Template | When to use |
|----------|-------------|
| `schema/organization.json` | 任意 business site；提供完整 Organization type，含連到 Wikipedia、Wikidata、LinkedIn、YouTube、GitHub 與 Crunchbase 的 `sameAs` links，以及用於 entity topic signals 的 `knowsAbout`。 |
| `schema/local-business.json` | 有實體 location 的 businesses；以 address、`geo` coordinates、opening hours、service area、aggregate rating 與 offer catalog 擴充 Organization。 |
| `schema/article-author.json` | Publisher 與 blog pages；Article type 搭配完整 Person author（credentials、`sameAs`、`alumniOf`、`knowsAbout`），以及供 AI assistant readability 使用的 `speakable` specification。 |
| `schema/product-ecommerce.json` | E-commerce product pages；Product type 搭配 Offer（含 shipping details 與 return policy）、AggregateRating 與 individual Review entries。 |
| `schema/software-saas.json` | SaaS product pages；SoftwareApplication type 搭配 tiered AggregateOffer pricing、`featureList`、screenshot，以及連到 G2、Capterra、ProductHunt 與 GitHub 的 `sameAs` links。 |
| `schema/website-searchaction.json` | 每個網站首頁；WebSite type 搭配 SearchAction `potentialAction`，用於啟用 sitelinks search box，並提供 AI systems 該網站的 search endpoint。 |
