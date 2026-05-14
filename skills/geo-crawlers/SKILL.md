---
name: geo-crawlers
description: AI 爬蟲存取分析 (AI crawler access analysis)。檢查 robots.txt、Meta 標籤與 HTTP 標頭，以判斷哪些 AI 爬蟲能存取網站。提供完整的存取地圖與建議，在維持適當控制的同時最大化 AI 能見度 (AI visibility)。
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# AI 爬蟲存取分析技能

## 目的

此技能分析網站對 AI 爬蟲 (AI crawlers) 的可存取性。AI 爬蟲是 AI 公司用來發現、索引 (index) 與訓練網頁內容的機器人 (bots)。若 AI 爬蟲被封鎖，無論網站內容品質多高，都無法出現在 AI 生成的回答 (AI-generated responses) 中。爬蟲存取是 GEO (生成式引擎最佳化) 的基礎技術需求。

## 核心洞察

截至 2026 年初，許多網站因繼承傳統 SEO 設定中過度激進的 robots.txt 規則，而意外封鎖了 AI 爬蟲。Originality.ai 2025 年的研究發現，前 1,000 大網站中超過 35% 至少封鎖了一個主要 AI 爬蟲，5-10% 封鎖了所有 AI 爬蟲。封鎖 AI 爬蟲是在 AI 生成的搜尋結果中變得「不可見」最快的方式。

---

## 完整 AI 爬蟲參考

### 第一梯隊 (Tier 1)：AI 搜尋能見度的關鍵（建議：允許 ALLOW）

這些爬蟲支援使用者主動尋找答案的 AI 搜尋產品。封鎖它們會直接降低你在 AI 生成回答中的能見度。

#### GPTBot
- **操作者：** OpenAI
- **使用者代理 (User-Agent)：** `GPTBot`
- **完整 User-Agent 字串：** `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)`
- **目的：** 抓取 ChatGPT 網頁瀏覽 (web browsing)、外掛程式與搜尋功能的內容。GPTBot 存取的內容可能用於改善 OpenAI 模型。
- **封鎖影響：** 內容不會出現在 ChatGPT 搜尋結果中，也無法在使用者要求 ChatGPT 瀏覽網頁時被存取。這是最應允許的高影響力 AI 爬蟲。
- **建議：** **允許 (ALLOW)** — ChatGPT 在 2025 年擁有超過 3 億週活躍用戶。封鎖 GPTBot 會讓內容離開最大的 AI 搜尋介面之一。

#### OAI-SearchBot
- **操作者：** OpenAI
- **使用者代理 (User-Agent)：** `OAI-SearchBot`
- **完整 User-Agent 字串：** `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; OAI-SearchBot/1.0; +https://docs.openai.com/bots/overview)`
- **目的：** 專門支援 ChatGPT 搜尋功能。不同於 GPTBot，OAI-SearchBot 存取的內容**不**用於模型訓練，僅用於即時搜尋結果。
- **封鎖影響：** 即使允許 GPTBot，內容仍不會出現在 ChatGPT 搜尋結果中。
- **建議：** **允許 (ALLOW)** — 這是僅限搜尋的爬蟲，不涉及訓練問題。沒有策略性的封鎖理由。

#### ChatGPT-User
- **操作者：** OpenAI
- **使用者代理 (User-Agent)：** `ChatGPT-User`
- **完整 User-Agent 字串：** `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ChatGPT-User/1.0; +https://openai.com/bot)`
- **目的：** 當 ChatGPT 使用者明確要求模型存取特定 URL 時使用。它代表使用者像瀏覽器代理一樣行動。
- **封鎖影響：** 使用者要求 ChatGPT 閱讀或摘要頁面時，ChatGPT 無法訪問。這會阻止使用者發起的直接流量。
- **建議：** **允許 (ALLOW)** — 封鎖此機器人會阻止正嘗試透過 ChatGPT 使用你內容的使用者。

#### ClaudeBot
- **操作者：** Anthropic
- **使用者代理 (User-Agent)：** `ClaudeBot`
- **完整 User-Agent 字串：** `ClaudeBot/1.0; +https://www.anthropic.com/claude-bot`
- **目的：** 抓取 Claude 功能所需的網頁內容，包括網頁搜尋、引用與分析工具。
- **封鎖影響：** Claude 無法在網頁搜尋或使用者要求分析特定 URL 時存取內容。
- **建議：** **允許 (ALLOW)** — Claude 是重要且市佔成長中的 AI 助手。封鎖 ClaudeBot 會降低 AI 搜尋足跡。

#### PerplexityBot
- **操作者：** Perplexity AI
- **使用者代理 (User-Agent)：** `PerplexityBot`
- **完整 User-Agent 字串：** `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)`
- **目的：** 支援 Perplexity AI 搜尋引擎，提供帶有來源引用與回連原始頁面的具名回答。
- **封鎖影響：** 內容不會出現在 Perplexity 搜尋結果中。Perplexity 是 AI 搜尋產品中最好的推薦流量 (referral traffic) 來源之一，因為它始終顯示來源連結。
- **建議：** **允許 (ALLOW)** — Perplexity 會帶來實際推薦流量，且總是會標註引用來源。對發布者與企業來說是高價值的 AI 爬蟲。

---

### 第二梯隊 (Tier 2)：較廣大 AI 生態系統的重要爬蟲（建議：允許 ALLOW）

這些爬蟲服務於大型 AI 平台或搜尋生態系統。允許它們會增加內容的觸及率。

#### Google-Extended
- **操作者：** Google
- **使用者代理 (User-Agent)：** `Google-Extended`
- **目的：** 控制 Google 是否使用你的內容進行 Gemini 模型訓練與 AI Overviews 改良。**關鍵註記：** 封鎖 Google-Extended **不會**影響 Google 搜尋排名或在 Google 搜尋結果中的呈現；該部分由標準 Googlebot 控制。
- **封鎖影響：** 內容可能不會用於 Gemini 訓練或改良 AI Overviews。然而，你的內容仍可基於標準搜尋索引出現在 AI Overviews 中。
- **建議：** **允許 (ALLOW)** — 封鎖提供的內容保護價值極小，卻會降低在 Google AI 功能中的能見度。既然不影響標準搜尋排名，唯一封鎖理由通常是對訓練數據使用的哲學性反對。

#### GoogleOther
- **操作者：** Google
- **使用者代理 (User-Agent)：** `GoogleOther`
- **目的：** Google 用於各種非搜尋排名目的，包括研究、一次性抓取與 AI 相關數據收集。
- **封鎖影響：** 對搜尋排名影響很小。可能降低在 Google AI 研究與實驗性功能中的能見度。
- **建議：** **允許 (ALLOW)** — 低風險，對被納入 AI 功能有中度的潛在效益。

#### Applebot-Extended
- **操作者：** Apple
- **使用者代理 (User-Agent)：** `Applebot-Extended`
- **目的：** Apple 用來訓練與改善 Apple Intelligence 功能、Siri 與 Apple AI 產品。與標準 Applebot（支援 Siri 搜尋與 Spotlight 建議）分開。
- **封鎖影響：** 內容可能不會被用於 Apple Intelligence 功能。標準 Siri 與 Spotlight 功能不受影響（由 Applebot 控制）。
- **建議：** **允許 (ALLOW)** — Apple Intelligence 整合到所有 Apple 裝置（超過 20 億台活躍裝置）。在 Apple AI 功能中存在的策略價值正在增加。

#### Amazonbot
- **操作者：** Amazon
- **使用者代理 (User-Agent)：** `Amazonbot`
- **完整 User-Agent 字串：** `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5 (compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot)`
- **目的：** 為 Alexa 回答與 Amazon AI 功能索引內容。
- **封鎖影響：** 內容不會出現在 Alexa 語音回答或 Amazon AI 驅動的搜尋功能中。
- **建議：** **允許 (ALLOW)** — 與語音搜尋最佳化 (Voice Search Optimization) 相關。優先級低於第一梯隊爬蟲，但允許它沒有壞處。

#### FacebookBot
- **操作者：** Meta
- **使用者代理 (User-Agent)：** `FacebookBot`
- **目的：** Meta 用於 Facebook、Instagram、WhatsApp 與 Meta AI 助手的 AI 功能。
- **封鎖影響：** 內容可能無法供 Meta AI 存取。Facebook/Instagram 的連結預覽 (link previews) 由不同爬蟲處理，不受影響。
- **建議：** **允許 (ALLOW)** — Meta AI 嵌入在總計超過 30 億用戶的應用程式中。對 AI 能見度的重要性日益增加。

---

### 第三梯隊 (Tier 3)：僅限訓練的爬蟲（依策略 允許 或 封鎖）

這些爬蟲主要用於 AI 模型訓練，而非即時搜尋功能。封鎖它們不影響 AI 搜尋能見度。

#### CCBot
- **操作者：** Common Crawl（非營利組織）
- **使用者代理 (User-Agent)：** `CCBot`
- **完整 User-Agent 字串：** `CCBot/2.0 (https://commoncrawl.org/faq/)`
- **目的：** 建立 Common Crawl 數據集，被許多 AI 公司（Google、Meta、Stability AI 等）用作訓練數據。
- **封鎖影響：** 內容不會出現在未來的 Common Crawl 數據集中。不影響任何即時 AI 搜尋產品。
- **建議：** **視情況而定 (CONTEXT-DEPENDENT)** — 若想最大化長期 AI 訓練能見度，請允許。若想控制訓練數據使用，請封鎖。對搜尋能見度無影響。

#### anthropic-ai
- **操作者：** Anthropic
- **使用者代理 (User-Agent)：** `anthropic-ai`
- **目的：** Anthropic 用於 AI 安全研究與 Claude 模型訓練。與支援即時功能的 ClaudeBot 分開。
- **封鎖影響：** 內容不會用於 Claude 訓練。不影響 Claude 即時搜尋或網頁瀏覽功能（由 ClaudeBot 控制）。
- **建議：** **視情況而定 (CONTEXT-DEPENDENT)** — 類似 CCBot。允許以取得訓練能見度，或封鎖以控制訓練數據。對即時 AI 搜尋無影響。

#### Bytespider
- **操作者：** 字節跳動 (ByteDance)
- **使用者代理 (User-Agent)：** `Bytespider`
- **目的：** 字節跳動用於各種 AI 產品，包括 TikTok AI 功能與豆包 (Doubao，其在中國的 ChatGPT 競爭對手)。
- **封鎖影響：** 內容不會用於字節跳動 AI 產品。對西方市場企業影響很小。
- **建議：** 多數西方企業 **封鎖 (BLOCK)**（據報有激進抓取行為、能見度效益小）。若目標是中國/亞洲市場則 **允許 (ALLOW)**。

#### cohere-ai
- **操作者：** Cohere
- **使用者代理 (User-Agent)：** `cohere-ai`
- **目的：** Cohere 用於模型訓練。Cohere 支援企業 AI 解決方案與 Coral 對話產品。
- **封鎖影響：** 內容不會用於 Cohere 模型訓練。對直接面向消費者的影響很小。
- **建議：** **視情況而定 (CONTEXT-DEPENDENT)** — 低優先級。依據對訓練數據使用的一般立場來決定允許或封鎖。

---

## 建議矩陣摘要

| 爬蟲 (Crawler) | 梯隊 | 建議 | 原因 |
|---|---|---|---|
| GPTBot | 1 | **允許 (ALLOW)** | 支援 ChatGPT 搜尋（3 億以上用戶） |
| OAI-SearchBot | 1 | **允許 (ALLOW)** | 僅限搜尋，不用於訓練 |
| ChatGPT-User | 1 | **允許 (ALLOW)** | 使用者啟動的瀏覽 |
| ClaudeBot | 1 | **允許 (ALLOW)** | Claude 網頁搜尋與分析 |
| PerplexityBot | 1 | **允許 (ALLOW)** | 最佳推薦流量 AI 搜尋 |
| Google-Extended | 2 | **允許 (ALLOW)** | Gemini 功能；不影響搜尋排名 |
| GoogleOther | 2 | **允許 (ALLOW)** | Google AI 研究 |
| Applebot-Extended | 2 | **允許 (ALLOW)** | Apple Intelligence（20 億台裝置） |
| Amazonbot | 2 | **允許 (ALLOW)** | Alexa 與 Amazon AI |
| FacebookBot | 2 | **允許 (ALLOW)** | Meta AI（30 億 App 用戶） |
| CCBot | 3 | 視情況 | 僅限訓練數據 |
| anthropic-ai | 3 | 視情況 | 僅限訓練數據 |
| Bytespider | 3 | **封鎖 (BLOCK)** | 激進爬蟲，效益低 |
| cohere-ai | 3 | 視情況 | 僅限訓練數據 |

### 最大化 AI 能見度設定 (robots.txt)

適合想最大化 AI 搜尋能見度的網站：

```
# AI Crawlers - ALLOWED for AI search visibility
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: GoogleOther
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: FacebookBot
Allow: /

# AI Crawlers - BLOCKED (aggressive/low value)
User-agent: Bytespider
Disallow: /

User-agent: CCBot
Disallow: /
```

---

## 分析流程

### Step 1：抓取並解析 robots.txt

1. 使用 WebFetch 取得 `[網域]/robots.txt`。
2. 解析所有 User-agent 指令與其關聯的 Allow/Disallow 規則。
3. 對參考清單中的每個 AI 爬蟲：
   - 檢查是否有該爬蟲特定的 User-agent 封鎖。
   - 檢查是否有適用的萬用字元（`User-agent: *`）封鎖。
   - 判斷有效存取：**允許 (Allowed)**、**封鎖 (Blocked)** 或 **未提及 (Not Mentioned)**（繼承萬用字元規則）。
4. 記錄任何會拖慢 AI 爬蟲存取速度的 `Crawl-delay` 指令。
5. 檢查 `Sitemap` 指令（AI 爬蟲會用它們來進行探索）。

### Step 2：檢查 Meta Robots 標籤

1. 對 5-10 個關鍵頁面抽樣抓取 HTML 並檢查：
   - `<meta name="robots" content="noindex">` -- 封鎖所有機器人。
   - `<meta name="robots" content="nofollow">` -- 阻止追蹤連結。
   - `<meta name="robots" content="noai">` -- 封鎖 AI 使用的新興標籤。
   - `<meta name="robots" content="noimageai">` -- 封鎖 AI 圖片訓練。
   - 特定機器人標籤：`<meta name="GPTBot" content="noindex">`
2. 記錄任何會覆寫 robots.txt 指令的頁面級設定。

### Step 3：檢查 HTTP 標頭 (HTTP Headers)

1. 對相同的抽樣頁面檢查回應標頭：
   - `X-Robots-Tag: noindex` -- 相當於 Meta noindex 的 HTTP 標頭。
   - `X-Robots-Tag: noai` -- 封鎖 AI 使用的 HTTP 標頭。
   - `X-Robots-Tag: noimageai` -- 封鎖 AI 圖片訓練。
   - 特定機器人標頭：`X-Robots-Tag: GPTBot: noindex`
2. 註記：HTTP 標頭會覆寫 Meta 標籤，也適用於非 HTML 資源。

### Step 4：檢查 AI 專用檔案

1. 檢查 `/llms.txt`（AI 爬蟲引導的新興標準）。
2. 檢查 `/.well-known/ai-plugin.json`（OpenAI 外掛程式宣告檔）。
3. 檢查 `/ai.txt`（提案中的標準，類似 AI 版的 ads.txt）。
4. 記錄每個檔案的存在與品質。

### Step 5：評估 JavaScript 渲染需求

1. 檢查網站是否為單頁應用程式 (SPA) 或高度依賴 JavaScript 渲染。
2. 不同 AI 爬蟲的 JavaScript 渲染能力各異：
   - GPTBot：JS 渲染能力有限。
   - ClaudeBot：JS 渲染能力有限。
   - PerplexityBot：JS 渲染能力有限。
   - Googlebot：具備完整 JS 渲染能力（Google-Extended 繼承此能力）。
3. 若關鍵內容需要 JS 渲染才能顯示，將其標記為潛在問題。
4. 檢查是否有伺服器端渲染 (SSR) 或靜態網站生成 (SSG) 作為緩解措施。

### Step 6：解析內容訊號 (Content Signals)

使用 Step 1 已抓取的 robots.txt，掃描 `Content-Signal:` 指令 (IETF 草案 `draft-romm-aipref-contentsignals`)。

1. 掃描每一行，找出以 `Content-Signal:` 開頭的行（不分大小寫）。
2. 若找到：
   - 解析所有鍵值對 (key=value pairs)（先以 `,` 分割，再以 `=` 分割）。
   - 依已知集合驗證鍵 (keys)：`ai-train`、`search`、`ai-personalization`、`ai-retrieval`。
   - 驗證值 (values)：僅 `yes` 與 `no` 有效。
   - 將任何未知鍵或無效值標記為警告，因為規格仍處於 IETF 草案階段。
   - 將結果記錄為 **通過 (Pass)**，並以口語意義顯示解析後的值。
3. 若不存在：記錄為 **建議 (Recommendation)** — 該網站尚未宣告其 AI 使用偏好。

不需要額外的 HTTP 請求。robots.txt 已在 Step 1 抓取。

---

## 輸出格式

產生名為 `GEO-CRAWLER-ACCESS.md` 的檔案：

```markdown
# AI 爬蟲存取報告：[網域]

**分析日期：** [Date]
**網域：** [Domain]
**robots.txt 狀態：** [Found/Not Found/Error]

---

## 爬蟲存取摘要

| 爬蟲 (Crawler) | 操作者 | 梯隊 | 狀態 | 影響 |
|---|---|---|---|---|
| GPTBot | OpenAI | 1 | [允許/封鎖/未提及] | [影響描述] |
| OAI-SearchBot | OpenAI | 1 | [狀態] | [影響] |
| ChatGPT-User | OpenAI | 1 | [狀態] | [影響] |
| ClaudeBot | Anthropic | 1 | [狀態] | [影響] |
| PerplexityBot | Perplexity | 1 | [狀態] | [影響] |
| Google-Extended | Google | 2 | [狀態] | [影響] |
| GoogleOther | Google | 2 | [狀態] | [影響] |
| Applebot-Extended | Apple | 2 | [狀態] | [影響] |
| Amazonbot | Amazon | 2 | [狀態] | [影響] |
| FacebookBot | Meta | 2 | [狀態] | [影響] |
| CCBot | Common Crawl | 3 | [狀態] | [影響] |
| anthropic-ai | Anthropic | 3 | [狀態] | [影響] |
| Bytespider | ByteDance | 3 | [狀態] | [影響] |
| cohere-ai | Cohere | 3 | [狀態] | [影響] |

## AI 能見度分數：[X]/100

**第一梯隊存取：** [X/5 個爬蟲已允許]
**第二梯隊存取：** [X/5 個爬蟲已允許]
**第三梯隊存取：** [X/4 個爬蟲已允許]

---

## 關鍵問題

[列出任何被封鎖的第一梯隊爬蟲]

## 建議

### 立即行動
[需要對 robots.txt 進行的具體變更]

### 建議的 robots.txt
```
[針對 AI 爬蟲最佳化的完整建議 robots.txt 內容]
```

### 其他技術發現
- **Meta Robots 標籤：** [發現內容]
- **X-Robots-Tag 標頭：** [發現內容]
- **JavaScript 渲染：** [評估結果]
- **llms.txt：** [存在/不存在]
- **Sitemap 可存取性：** [評估結果]

### 內容訊號 (Content Signals - IETF 草案)

**狀態：** 存在 / 不存在

<!-- 若存在： -->
| 訊號鍵 (Signal Key) | 值 | 意義 |
|---|---|---|
| ai-train | no | 已選擇退出 AI 模型訓練 |
| search | yes | 允許用於 AI 驅動的搜尋結果 |

<!-- 若不存在： -->
**建議：** 在 robots.txt 中加入 `Content-Signal:` 指令，以明確宣告 AI 使用偏好。例如：

`Content-Signal: ai-train=no, search=yes, ai-retrieval=yes`

完整規格請參閱 [https://contentsignals.org/](https://contentsignals.org/)。
```

---

## 爬蟲存取評分

AI 爬蟲存取分數 (AI Crawler Access Score) 計算方式如下：

| 組成部分 | 權重 | 評分方式 |
|---|---|---|
| 允許第一梯隊爬蟲 | 50% | 每個允許的第一梯隊爬蟲得 20 分（5 個爬蟲滿分 100 分，依比例調整至 50 分） |
| 允許第二梯隊爬蟲 | 25% | 每個允許的第二梯隊爬蟲得 20 分（5 個爬蟲滿分 100 分，依比例調整至 25 分） |
| 無地毯式 AI 封鎖 | 15% | 沒有 `User-agent: *` 配合 Disallow: / 且沒有 noai Meta 標籤即得滿分 |
| 具備 AI 專用檔案 | 10% | 有 llms.txt 得 5 分，AI 爬蟲可存取 Sitemap 得 5 分 |

最終分數 = 所有權重組件加總，最高 100 分。