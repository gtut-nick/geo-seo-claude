# 評分方法

GEO Score 是 0 到 100 的單一綜合數字，用來概括網站針對 ChatGPT、Perplexity、Claude、Google AI Overviews 等 AI 系統的發現、引用與推薦最佳化程度。它以六個類別 sub-score 的加權平均計算，每個類別由專門 subagent 獨立評估。高分代表 generative-engine visibility 的準備度強；低分則指向具體缺口，並附上依優先順序排列的行動計畫。

---

## 權重表

| 類別 | 權重 |
|---|---|
| AI Citability & Visibility | 25% |
| Brand Authority Signals | 20% |
| Content Quality & E-E-A-T | 20% |
| Technical Foundations | 15% |
| Structured Data | 10% |
| Platform Optimization | 10% |

---

## 綜合分數如何計算

每個 subagent 都會回傳 0–100 scale 的 sub-score。[`skills/geo-audit/SKILL.md`](../skills/geo-audit/SKILL.md) 中的 orchestrator 會將每個 sub-score 乘以權重後加總。

**公式（來自 `skills/geo-audit/SKILL.md`）：**

```
GEO_Score = (Citability   * 0.25)
          + (Brand        * 0.20)
          + (EEAT         * 0.20)
          + (Technical    * 0.15)
          + (Schema       * 0.10)
          + (Platform     * 0.10)
```

**Pseudo-code：**

```python
weights = {
    "citability": 0.25,
    "brand":      0.20,
    "eeat":       0.20,
    "technical":  0.15,
    "schema":     0.10,
    "platform":   0.10,
}

geo_score = sum(sub_scores[k] * w for k, w in weights.items())
# geo_score is in [0, 100]
```

**分數解讀（來自 `skills/geo-audit/SKILL.md`）：**

| 範圍 | 評級 | 意義 |
|---|---|---|
| 90–100 | Excellent | 很可能被 AI 引用 |
| 75–89 | Good | 基礎強，但仍有改善空間 |
| 60–74 | Fair | 中等存在感；有顯著機會 |
| 40–59 | Poor | 訊號弱；AI 系統可能難以引用 |
| 0–39 | Critical | 大多對 AI 系統不可見 |

---

## AI Citability & Visibility（25%）

**由以下項目實作：** [`agents/geo-ai-visibility.md`](../agents/geo-ai-visibility.md) 與 [`scripts/citability_scorer.py`](../scripts/citability_scorer.py)

### 評分器檢查什麼

引用性 sub-score 本身也是四個組件的加權組合（權重來自 `agents/geo-ai-visibility.md`）：

| 組件 | 權重 |
|---|---|
| Citability Score | 35% |
| Brand Mention Score | 30% |
| Crawler Access Score | 25% |
| llms.txt Score | 10% |

**引用性評分**（`scripts/citability_scorer.py`）會分析頁面上每個實質內容區塊，也就是由 headings 分隔的 sections，並依五個維度評分：

| 維度 | 最高分 | 主要訊號 |
|---|---|---|
| Answer Block Quality | 30 | 定義模式（"X is a…"、"X refers to…"）、答案出現在前 60 words、question-based heading、短而清楚的句子（5–25 words）、有歸因的主張（"research shows…"） |
| Self-Containment | 25 | 字數落在 134–167 word 最佳範圍（10 pts）、100–200 word 範圍（7 pts）、80–250 word 範圍（4 pts）；代名詞密度低於 2%（8 pts）；3+ proper nouns（7 pts） |
| Structural Readability | 20 | 平均句長 10–20 words（8 pts）；list-like transition words（4 pts）；numbered items 或 step references（4 pts）；paragraph breaks（4 pts） |
| Statistical Density | 15 | 百分比（每個 3 pts，最高 6）；金額（每個 3 pts，最高 5）；含單位脈絡的數字（每個 2 pts，最高 4）；年份引用（2 pts）；具名來源（2 pts） |
| Uniqueness Signals | 10 | 原創研究語言（"our study found…"）（5 pts）；case study 或 real-world example references（3 pts）；特定 tool/product mentions（2 pts） |

段落分數是五個維度的總和（最高 100）。頁面層級的 citability score 是最高分五個區塊的平均；若不足五個區塊，則取所有區塊平均。

**Crawler Access Score**（`agents/geo-ai-visibility.md`）從 100 開始並扣分：
- 每封鎖一個 critical crawler 扣 15 points（GPTBot、ClaudeBot、PerplexityBot、OAI-SearchBot、GoogleBot）
- 每封鎖一個 secondary crawler 扣 5 points
- robots.txt 未引用 sitemap 扣 10 points
- 最低為 0

**llms.txt Score**（`agents/geo-ai-visibility.md` 與 `scripts/llmstxt_generator.py`）：
- 0 — 不存在
- 30 — 存在但格式錯誤
- 50 — 存在、格式有效，但內容很少
- 70 — 存在、有效，且涵蓋主要內容區域
- 90–100 — 完整，且也提供 `/llms-full.txt`

### 好與壞的樣貌

良好的 AI Citability score（70+）表示頁面有多段可自成一體、事實密度高、並直接回答問題的內容；robots.txt 允許所有主要 AI crawlers；且存在結構良好的 llms.txt。低分（低於 40）通常代表內容薄弱或高度依賴上下文、AI crawlers 被封鎖，且沒有 llms.txt。

---

## Brand Authority Signals（20%）

**由以下項目實作：** [`agents/geo-ai-visibility.md`](../agents/geo-ai-visibility.md) 與 [`scripts/brand_scanner.py`](../scripts/brand_scanner.py)

### 評分器檢查什麼

品牌權威會檢查品牌是否存在於 AI 模型建立 entity knowledge 時高度依賴的平台。Brand Mention Score（作為上方 AI Visibility composite 的輸入）由下列項目構成：

| 平台 | 可得分數 | 方法 |
|---|---|---|
| Wikipedia | 30 | Wikipedia API search；Wikidata entity lookup（`scripts/brand_scanner.py`） |
| Industry / niche sources | 25 | Review platforms（G2、Trustpilot、Capterra）、press mentions、權威產業網站 |
| Reddit | 20 | 品牌討論的存在、近期性與情緒 |
| YouTube | 15 | 官方 channel 是否存在與第三方影片 coverage |
| LinkedIn | 10 | 公司頁存在與活動 |

`scripts/brand_scanner.py` 中引用的相關性數值來自 Ahrefs 2025 年 12 月對 75,000 個品牌的研究：YouTube 與 AI citations 的相關性最強（0.737）；domain rating / backlinks 的相關性較弱（0.266）。

### 好與壞的樣貌

強品牌權威分數需要活躍的 Wikipedia presence（權重最高的訊號）、Reddit 上的 community-level discussion，以及含教育或評論內容的 YouTube presence。沒有 Wikipedia page、沒有 Reddit discussion、沒有 YouTube presence 的品牌，即使在傳統搜尋中很知名，此 sub-score 仍會接近 0。

---

## Content Quality & E-E-A-T（20%）

**由以下項目實作：** [`agents/geo-content.md`](../agents/geo-content.md)

### 評分器檢查什麼

內容 agent 會依 Google 的 E-E-A-T framework 評估頁面。四個維度各自以 0–25 評分，然後正規化到 0–15 以納入 content score 權重：

| 維度 | 最高（raw） | 檢查的主要訊號 |
|---|---|---|
| Experience | 25 | 原創研究或資料、具有可衡量成果的 case studies、第一手描述、before/after comparisons、具體姓名與數字 |
| Expertise | 25 | 具名 author 與 credentials、含 biography 的 author page 連結、技術深度、methodology transparency、Person schema |
| Authoritativeness | 25 | About page 品質、外部 citations、產業 recognition、media mentions、sameAs schema links |
| Trustworthiness | 25 | HTTPS、可見 contact information、privacy policy、editorial standards、透明 sourcing、publication 與 update dates |

除了 E-E-A-T，完整 content score（0–100）也納入：

| 組件 | 權重 | 訊號 |
|---|---|---|
| E-E-A-T（combined, normalised） | 60% | 上述四個維度 |
| Content Metrics | 15% | 字數分類（thin < 300 words；deep-dive 3000+ words）、近似 Flesch readability、paragraph length、heading hierarchy |
| AI Content Assessment | 10% | 缺少 generic AI-pattern phrases、存在 authorial voice、original data |
| Topical Authority | 10% | 內容廣度（related pages）、internal linking depth、hub-and-cluster structure |
| Content Freshness | 5% | 可見 publication 與 modification dates、時間敏感主題的近期性 |

### 好與壞的樣貌

70+ 分需要可明確識別且 credentials 可驗證的 author、原創資料或 case studies、透明 sourcing、HTTPS，以及超越表層涵蓋的內容。低於 30 通常代表沒有 author attribution、沒有外部來源、沒有 HTTPS，且內容看起來任何沒有主題經驗的人都能寫出來。

---

## Technical Foundations（15%）

**由以下項目實作：** [`agents/geo-technical.md`](../agents/geo-technical.md)

### 評分器檢查什麼

技術 agent 會從九個加權組件計算分數：

| 組件 | 權重 |
|---|---|
| Server-Side Rendering / JS dependency | 25% |
| Meta tags & indexability | 15% |
| Crawlability（robots.txt, sitemap） | 15% |
| Security headers | 10% |
| Core Web Vitals risk | 10% |
| Mobile optimization | 10% |
| URL structure | 5% |
| Response headers & status | 5% |
| Additional checks | 5% |

Server-side rendering 權重最高，因為 AI crawlers（GPTBot、ClaudeBot、PerplexityBot）通常不執行 JavaScript。若頁面主要內容必須靠 JS render，無論內容本身寫得多好，對 AI crawlers 都等同不可見。

Security header 扣分（來自 `agents/geo-technical.md`）：
- No HTTPS: -30 points
- No HSTS: -10 points
- No CSP: -10 points
- No X-Frame-Options: -5 points
- No X-Content-Type-Options: -5 points
- No Referrer-Policy: -5 points
- No Permissions-Policy: -3 points

Core Web Vitals（LCP、INP、CLS）會從 static HTML analysis 評估為 Low / Medium / High risk。agent 會明確註明實際量測需要 field data（PageSpeed Insights 或 CrUX）。

### 好與壞的樣貌

高技術分數需要完整 server-side rendering、格式良好且允許 AI crawlers 的 robots.txt、被引用的 XML sitemap、具 HSTS 的 HTTPS，以及乾淨 meta tags。critical finding 是任何 client-side-only SPA：若 HTML body 在沒有 JavaScript execution 時是空的，再多內容最佳化也無法幫助 AI discoverability。

---

## Structured Data（10%）

**由以下項目實作：** [`agents/geo-schema.md`](../agents/geo-schema.md)

### 評分器檢查什麼

schema agent 會在 page source 中偵測 JSON-LD、Microdata 與 RDFa structured data，並依十個組件評估完整度：

| 組件 | 最高分 | Criteria |
|---|---|---|
| Organization / LocalBusiness | 20 | Present（10 pts）；sameAs linking to 3+ platforms（20 pts） |
| Article / content schema | 15 | Present（8 pts）；author as Person object（12 pts）；dateModified present（15 pts） |
| Person schema for author | 15 | Present（8 pts）；sameAs present（12 pts）；jobTitle and knowsAbout present（15 pts） |
| sameAs completeness | 15 | 1–2 platforms（5 pts）；3–4 platforms（10 pts）；5+ platforms including Wikipedia（15 pts） |
| speakable property | 10 | Present and targeting content sections（10 pts） |
| BreadcrumbList | 5 | Present and valid（5 pts） |
| WebSite + SearchAction | 5 | Present and valid（5 pts） |
| No deprecated schemas | 5 | No HowTo（removed Sep 2023）or SpecialAnnouncement schemas present |
| JSON-LD format | 5 | All schemas in JSON-LD rather than Microdata or RDFa |
| Validation（no errors） | 5 | All schemas pass syntax and property validation |

agent 也會標記由 JavaScript 注入、而不是存在於 initial HTML response 的 schemas，因為 AI crawlers 不會執行 JavaScript，會完全錯過這些 schemas。

檢查的 deprecated 與 restricted 狀態（來自 `agents/geo-schema.md`）：
- HowTo：自 2023 年 9 月起從 Google rich results 移除
- FAQPage：自 2023 年 8 月起限制於政府與健康權威網站
- SpecialAnnouncement：deprecated

### 好與壞的樣貌

高 schema 分數需要 Organization schema，且 sameAs links 至少連到五個平台（包含 Wikipedia）；所有內容 author 都有正確巢狀的 Person schemas；Article schema 含 dateModified；所有 schemas 都以 server-rendered JSON-LD 交付。接近 0 分代表完全沒有 structured data，這會移除 AI models 可用的任何明確 entity-linking signal。

---

## Platform Optimization（10%）

**由以下項目實作：** [`agents/geo-platform-analysis.md`](../agents/geo-platform-analysis.md)

### 評分器檢查什麼

平台 agent 會分別評估五個 AI search platforms 的準備度並加總。每個平台有自己的 sub-scoring breakdown：

**Google AI Overviews：** Content structure（40 pts）— question-based headings、direct answer paragraphs、comparison tables；source authority signals（30 pts）；technical signals（30 pts）。

**ChatGPT web search：** Entity recognition（35 pts）— Wikipedia 與 Wikidata presence、sameAs schema；content preferences（40 pts）— factual, citable statements with attribution；crawler access（25 pts）— robots.txt 允許 OAI-SearchBot 與 ChatGPT-User。

**Perplexity AI：** Community validation（Reddit、Quora、Stack Overflow）與 source directness 分開評分。

**Google Gemini 與 Bing Copilot：** 各平台依其 documented sourcing 與 ranking signals 評估。

README 提到只有 11% 網域會在同一 query 中同時被 ChatGPT 與 Google AI Overviews 引用，這也是將 platform readiness 視為獨立評分維度，而不是併入 technical 或 content categories 的原因。

### 好與壞的樣貌

強 platform score 需要通過其他類別也會出現的 crawler-access 與 entity-recognition 檢查，並具備平台特定結構模式：Google AIO 需要 question-answering headings 與 direct-answer paragraphs；ChatGPT 需要 Wikipedia 與 Wikidata presence；Perplexity 需要 community-platform presence。因為此類別與多個其他類別重疊，AI Citability 與 Brand Authority 表現好的網站，通常此處也會有合理分數。

---

## 注意事項

**確定性 vs LLM-judged scoring。** citability scorer（`scripts/citability_scorer.py`）與 llms.txt validator（`scripts/llmstxt_generator.py`）完全 deterministic：給定相同 HTML，每次都會回傳相同數值結果。Brand Authority、Content E-E-A-T、Technical、Schema 與 Platform 分數由 LLM subagents 依 documented rubrics 產生；它們是 guided evaluations，而不是可重現計算。同一 URL 兩次執行，在 LLM-judged categories 中可能有小幅差異。

**權重帶有主觀判斷。** 25/20/20/15/10/10 的權重分布反映工具作者在撰寫時，對各類別對 AI citation likelihood 相對重要性的判斷。這些權重不是來自 controlled study，並會隨 AI search platforms 演進而改變。

**診斷工具，不是保證。** GEO Score 是診斷工具。高分能改善 AI citation 的結構條件，但不能保證任何特定 AI system 會引用或推薦該網站。AI model behaviour 取決於許多工具範圍外的因素，包括 model training data、query phrasing 與 competitor content。

**Schema validation 是結構性，不是語意性。** schema agent 會檢查 JSON-LD 語法有效、使用 recognized Schema.org types 與 properties，並包含 required fields。它不會驗證值是否準確，也不會驗證描述的 entity 是否符合實際 organization 或 person。通過 validation 的 schema block 仍可能包含錯誤資訊。

**llms.txt 是新興標準。** `scripts/llmstxt_generator.py` 與 `agents/geo-ai-visibility.md` 引用的 llms.txt 規格尚未被 AI crawlers 普遍採用。目前它的存在與否不能保證任何特定 crawler behaviour。
