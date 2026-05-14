---
name: geo-report
description: 產生專業、面向客戶的 GEO 報告，將所有稽核結果整合為單一交付文件，包含分數、發現事項與優先行動
version: 1.0.0
author: geo-seo-claude
tags: [geo, report, client-deliverable, executive-summary, action-plan]
allowed-tools: [Read, Grep, Glob, Bash, WebFetch, Write]
---

# GEO 客戶報告產生器

## 目的

此技能會將所有 GEO 稽核（Audit）技能的輸出彙整成一份可直接交付給客戶或利害關係人的專業報告。報告是寫給**企業主與行銷主管**，而非開發人員；技術發現會被轉譯為商業影響與清楚的行動項目，並標示優先級。

## 如何使用此技能

1. 先執行以下稽核（或使用既有報告資料）：
   - `geo-platform-optimizer` -> GEO-PLATFORM-OPTIMIZATION.md
   - `geo-schema` -> GEO-SCHEMA-REPORT.md
   - `geo-technical` -> GEO-TECHNICAL-AUDIT.md
   - `geo-content` -> GEO-CONTENT-ANALYSIS.md
   - （選用）`geo-llmstxt` -> llms.txt 評估
   - （選用）`geo-brand-mentions` -> 品牌權威數據
2. 收集所有分數與發現事項。
3. 計算綜合 GEO 準備度分數（GEO Readiness Score）。
4. 使用下方範本產生客戶報告。
5. 輸出：GEO-CLIENT-REPORT.md

---

## GEO 準備度分數（GEO Readiness Score）計算

### 元件權重

| 元件 | 權重 | 來源技能 |
|---|---|---|
| AI 平台準備度 | 25% | geo-platform-optimizer |
| 內容品質與 E-E-A-T | 25% | geo-content |
| 技術基礎 | 20% | geo-technical |
| 結構化資料（Schema） | 15% | geo-schema |
| 品牌權威與實體存在感 | 15% | geo-platform-optimizer (實體訊號) |

### 分數公式
```
GEO Score = (平台分數 * 0.25) + (內容分數 * 0.25) + (技術分數 * 0.20) + (結構化資料分數 * 0.15) + (品牌分數 * 0.15)
```

四捨五入到最接近的整數。最高為 100 分。

### 給客戶看的分數解讀

| 分數範圍 | 標籤 | 面向客戶的描述 |
|---|---|---|
| 85-100 | 優異 (Excellent) | 您的網站已為 AI 搜尋建立了絕佳位置。重點應放在維持並擴大優勢。 |
| 70-84 | 良好 (Good) | 基礎穩固，且有明確機會提升 AI 能見度。針對性最佳化將帶來顯著成果。 |
| 55-69 | 中等 (Moderate) | 您的網站在 AI 準備度上存在缺口，競爭對手可能正在利用這些缺口。結構化最佳化計畫可以彌補差距。 |
| 40-54 | 低於平均 (Below Average) | 存在明顯的 AI 搜尋能見度障礙。若不採取行動，品牌有在 AI 生成回答中「消聲匿跡」的風險。 |
| 0-39 | 需立即關注 (Needs Attention) | 關鍵 AI 準備度問題需要立即處理。競爭對手很可能正在奪取本應由您的品牌掌握的 AI 搜尋流量。 |

---

## 報告範本

完整報告需依照以下精確結構。每個章節都包含關於寫什麼與如何撰寫的指示。

---

### 第 1 節：執行摘要 (Executive Summary)

寫**剛好一段**（4-6 句），涵蓋：
- 分析內容（網域、頁面數、分析日期）。
- 整體 GEO 準備度分數與脈絡（例如：「XX/100，這使 [品牌] 處於 [標籤] 層級」）。
- 最具影響力的單一發現（正面或負面）。
- 以一句話列出前三個優先建議。
- 一句商業影響說明（例如：「執行這些建議預計可增加 AI 驅動流量約 XX%，根據目前的流量模式，這代表每月約 $X,XXX 的價值」）。

**語氣**：自信、直接、專業。避免使用術語。不要含糊其辭。寫作方式應像顧問交付發現，而非工具產生報告。

### 第 2 節：GEO 準備度分數 (GEO Readiness Score)

醒目呈現整體分數：

```
## GEO 準備度分數：XX/100 — [標籤]
```

接著用表格拆解各元件：

```markdown
| 元件 | 分數 | 權重 | 加權分數 |
|---|---|---|---|
| AI 平台準備度 | XX/100 | 25% | XX |
| 內容品質與 E-E-A-T | XX/100 | 25% | XX |
| 技術基礎 | XX/100 | 20% | XX |
| 結構化資料 | XX/100 | 15% | XX |
| 品牌權威 | XX/100 | 15% | XX |
| **總計** | | | **XX/100** |
```

### 第 3 節：AI 能見度儀表板 (AI Visibility Dashboard)

呈現各平台準備度分數：

```markdown
## AI 能見度儀表板

| AI 平台 | 準備度分數 | 關鍵缺口 | 優先行動 |
|---|---|---|---|
| Google AI Overviews | XX/100 | [單行缺口描述] | [單行行動建議] |
| ChatGPT Web Search | XX/100 | [單行缺口描述] | [單行行動建議] |
| Perplexity AI | XX/100 | [單行缺口描述] | [單行行動建議] |
| Google Gemini | XX/100 | [單行缺口描述] | [單行行動建議] |
| Bing Copilot | XX/100 | [單行缺口描述] | [單行行動建議] |
```

加上一段簡短說明這些分數的意義：「這些分數反映了您的內容被各個 AI 搜尋平台引用的可能性。分數低於 50 分表示在該平台上存在嚴重的引用障礙。」

### 第 4 節：AI 爬蟲存取狀態 (AI Crawler Access Status)

用清楚表格呈現：

```markdown
## AI 爬蟲存取

| AI 爬蟲 | 平台 | 狀態 | 影響等級 | 建議 |
|---|---|---|---|---|
| Googlebot | Google 搜尋 + AIO | 允許/封鎖 | 關鍵 (Critical) | [行動] |
| GPTBot | ChatGPT / OpenAI | 允許/封鎖 | 高 (High) | [行動] |
| Bingbot | Bing + Copilot + ChatGPT | 允許/封鎖 | 高 (High) | [行動] |
| PerplexityBot | Perplexity AI | 允許/封鎖 | 中 (Medium) | [行動] |
| Google-Extended | Gemini 訓練 | 允許/封鎖 | 中 (Medium) | [行動] |
| ClaudeBot | Anthropic Claude | 允許/封鎖 | 中 (Medium) | [行動] |
| Applebot-Extended | Apple Intelligence | 允許/封鎖 | 中 (Medium) | [行動] |
```

**為客戶轉譯**：「封鎖 AI 爬蟲就像在營業時間關閉門市。如果爬蟲無法存取您的網站，其支援的 AI 平台就無法引用您的內容。除非您有特定的數據授權考量，否則我們建議允許所有主要的 AI 爬蟲。」

### 第 5 節：品牌權威分析 (Brand Authority Analysis)

呈現各平台的實體存在感：

```markdown
## 品牌權威

| 平台 | 存在感 | 狀態 | 對 AI 能見度的影響 |
|---|---|---|---|
| 維基百科 (Wikipedia) | 是/否 | [細節] | 極高 — ChatGPT 引用中有 47.9% 來自維基百科 |
| Wikidata | 是/否 | [細節] | 高 — 機器可讀的實體數據 |
| LinkedIn | 是/否 | [細節] | 高 — Bing Copilot 與 ChatGPT 的重要訊號 |
| YouTube | 是/否 | [細節] | 高 — Gemini 與 Perplexity 的重要訊號 |
| Reddit | 是/否 | [細節] | 極高 — Perplexity 引用中有 46.7% 來自 Reddit |
| Google 知識面板 | 是/否 | [細節] | 高 — Gemini 實體識別 |
| Crunchbase | 是/否 | [細節] | 中 — 實體驗證 |
| GitHub | 是/否 | [細節] | 中 — 技術品牌訊號 |
```

**為客戶轉譯**：「AI 平台透過在多個權威來源中交叉比對您的品牌來建立信任。您的品牌在越多平台擁有準確且一致的存在感，就越有可能在 AI 回答中被引用。」

### 第 6 節：引用性分析 (Citability Analysis)

#### 前 5 個最容易被引用的頁面
每個頁面包含：
- URL
- 為何容易被引用（結構、深度、E-E-A-T 訊號）。
- 一項能讓它更容易被引用的具體改善。

#### 前 5 個最不容易被引用的頁面
每個頁面包含：
- URL
- 為何不太可能被引用（內容薄弱、結構差、缺少訊號）。
- 具體重寫或重構建議。

**商業影響框架**：「您最具引用性的頁面是出現在 AI 生成回答中的最佳候選者。改善引用性最低的 5 個頁面，是提升 AI 能見度中投資報酬率（ROI）最高的內容投資。」

### 第 7 節：技術健康度摘要 (Technical Health Summary)

用商業友善的語言呈現關鍵技術發現：

```markdown
## 技術健康度

| 領域 | 狀態 | 商業影響 |
|---|---|---|
| 網站核心指標 (Core Web Vitals) | 良好/需改進/不佳 | [對使用者體驗與排名的影響] |
| 伺服器端渲染 (SSR) | 是/部分/否 | [對 AI 爬蟲能見度的影響] |
| 行動裝置最佳化 | 良好/需改進/不佳 | [對 Google 行動優先索引的影響] |
| 安全性 (HTTPS + 標頭) | 良好/需改進/不佳 | [對信任訊號的影響] |
| 網頁速度 | 快/平均/慢 | [對使用者體驗與爬取預算的影響] |
| IndexNow 協定 | 已實作/未實作 | [對 Bing/ChatGPT 索引速度的影響] |
```

**關鍵發現提示**：如果缺少 SSR 或只有部分 SSR，請醒目標示：「您的網站使用用戶端渲染（Client-side rendering），這意味著 AI 爬蟲訪問時會看到一個空白頁面。這是影響 AI 搜尋能見度最單一且最具影響力的技術問題。在解決此問題之前，大多數 AI 平台無法引用您的內容。」

### 第 8 節：結構化資料（Schema & Structured Data）

```markdown
## 結構化資料 (Schema & Structured Data)

### 目前實作情況
| Schema 類型 | 是否存在 | 狀態 | 對 AI 影響 |
|---|---|---|---|
| Organization (組織) | 是/否 | [有效/有問題] | 關鍵 — 實體識別 |
| Article + Author | 是/否 | [有效/有問題] | 高 — E-E-A-T 訊號 |
| sameAs (實體連結) | 是/否 | [計數] 個連結 | 關鍵 — 跨平台實體圖譜 |
| [業務特定類型] | 是/否 | [有效/有問題] | [影響說明] |
| WebSite + SearchAction | 是/否 | [有效/有問題] | 中 — 站內搜尋結果 |
| BreadcrumbList | 是/否 | [有效/有問題] | 低至中 — 導航脈絡 |
```

如果缺少 Schema，請註明：「隨插即用的結構化資料程式碼已準備妥當，並包含在技術附錄中。您的開發團隊只需花費極少體力即可將其加入網站。」

### 第 9 節：llms.txt 狀態

```markdown
## llms.txt — AI 內容指南

| 檔案 | 狀態 | 建議 |
|---|---|---|
| /llms.txt | 存在/缺失 | [行動建議] |
| /llms-full.txt | 存在/缺失 | [行動建議] |
```

**為客戶轉譯**：「llms.txt 是一種新興標準（類似於 robots.txt），它告訴 AI 系統您的網站主題以及哪些頁面最重要。雖然尚未被普遍採用，但實作它能讓您的品牌領先競爭對手，並為 AI 平台提供直接引導。」

### 第 10 節：優先行動計畫 (Prioritized Action Plan)

這是報告中最重要的章節。依時程與影響程度組織行動。

```markdown
## 優先行動計畫

### 快速獲勝 (Quick Wins) — 本週
*影響力高、體力消耗低 — 可立即執行*

| # | 行動項目 | 影響程度 | 預估體力 | 受影響平台 |
|---|---|---|---|---|
| 1 | [具體行動] | [高/中] | [小時預估] | [哪些 AI 平台] |
| 2 | [具體行動] | [高/中] | [小時預估] | [哪些 AI 平台] |
```

**快速獲勝 (Quick Win) 標準**：一個人可在 4 小時內完成。範例：
- 在 robots.txt 中解除 AI 爬蟲封鎖。
- 為既有內容加入發布日期。
- 加入具備資歷說明的作者署名。
- 修正損壞的元描述 (Meta descriptions)。
- 在既有 Organization Schema 中加入 sameAs 屬性。
- 建立/宣告 llms.txt 檔案。

```markdown
### 中期改進 (Medium-Term Improvements) — 本月
*影響力顯著、體力消耗中等 — 需要內容或技術變更*

| # | 行動項目 | 影響程度 | 預估體力 | 受影響平台 |
|---|---|---|---|---|
| 1 | [具體行動] | [高/中] | [天數預估] | [哪些 AI 平台] |
```

**中期 (Medium-Term) 標準**：1-5 天工作量。範例：
- 用問題式標題與直接答案重構前 10 個頁面。
- 實作完整 Schema.org 標記。
- 建立具備資歷與 sameAs 連結的作者頁。
- 最佳化網站核心指標 (Core Web Vitals)（圖片壓縮、程式碼拆分）。
- 註冊並設定 Bing 網站管理員工具。
- 實作 IndexNow 協定。

```markdown
### 策略性倡議 (Strategic Initiatives) — 本季
*長期競爭優勢、需要持續投入*

| # | 行動項目 | 影響程度 | 預估體力 | 受影響平台 |
|---|---|---|---|---|
| 1 | [具體行動] | [高/中] | [週數預估] | [哪些 AI 平台] |
```

**策略性 (Strategic) 標準**：跨週/月的持續投入。範例：
- 建立維基百科/Wikidata 實體存在感。
- 發展主動的 Reddit 社群參與策略。
- 建立與搜尋查詢一致的 YouTube 內容策略。
- 實作伺服器端渲染 (SSR)（若目前為用戶端渲染）。
- 透過完整內容策略建立主題權威 (Topical Authority)。
- 建立原創研究/數據發布計畫。

### 預估影響
在行動計畫後，加入影響預估：

「根據產業基準以及本次稽核中識別出的具體缺口：
- **僅執行快速獲勝 (Quick Wins)** 即可讓您的 GEO 分數提升約 [X-Y] 分。
- **全面執行**此行動計畫可讓您的 GEO 分數提升至約 [XX]/100。
- 以目前的流量水準與轉換率計算，提升的 AI 能見度預計代表每月 **$X,XXX - $XX,XXX** 的額外自然價值。」

使用保守估計。金額數字基於：
- 目前預估的自然流量價值（若有 Analytics 則使用，否則以產業基準估算）。
- 預計到 2026 年底，AI 搜尋將驅動 25-40% 的自然探索。
- GEO 分數每提升 10 分，通常與 AI 引用頻率增加 15-25% 相關。

### 第 11 節：競爭對手比較 (Competitor Comparison)（若提供競爭對手 URL）

如果已與主要網域一起分析競爭對手 URL：

```markdown
## 競爭對手比較

| 指標 | [您的品牌] | [競爭對手 1] | [競爭對手 2] |
|---|---|---|---|
| 整體 GEO 分數 | XX/100 | XX/100 | XX/100 |
| Google AIO 準備度 | XX/100 | XX/100 | XX/100 |
| ChatGPT 準備度 | XX/100 | XX/100 | XX/100 |
| Perplexity 準備度 | XX/100 | XX/100 | XX/100 |
| Schema 覆蓋率 | [詳情] | [詳情] | [詳情] |
| 維基百科存在感 | 是/否 | 是/否 | 是/否 |
| Reddit 權威性 | [詳情] | [詳情] | [詳情] |
| SSR 狀態 | 是/否 | 是/否 | 是/否 |

### 您的領先之處
[品牌優於競爭對手的具體領域]

### 您的落後之處
[競爭對手具備優勢的具體領域，以及縮短差距的行動]
```

### 第 12 節：附錄 (Appendix)

```markdown
## 附錄

### 方法論
本次 GEO 稽核使用以下方法執行：
- **已分析頁面**：[稽核的具體 URL 列表]
- **已評估平台**：Google AI Overviews, ChatGPT, Perplexity AI, Google Gemini, Bing Copilot
- **技術檢查**：HTTP 標頭, robots.txt, HTML 原始碼分析, 結構化資料驗證
- **內容評估**：依據 Google 2025 年 12 月《品質評分者指南》的 E-E-A-T 框架（經驗、專業、權威、信任）
- **Schema 驗證**：JSON-LD 解析與 Schema.org 規範合規性
- **分析日期**：[日期]

### 資料來源
- Google 搜尋品質評分者指南（2025 年 12 月更新）
- Schema.org 完整類型階層
- 產業引用研究（Zyppy, Authoritas, Semrush AI search research, 2025-2026）
- 網站核心指標門檻（web.dev, 2026 標準）
- AI 爬蟲 User-agent 文件（各平台官方文件）

### 詞彙表

| 術語 | 定義 |
|---|---|
| GEO | 生成式引擎最佳化 (Generative Engine Optimization) — 最佳化內容以利被 AI 搜尋平台引用 |
| AIO | AI Overviews — Google 在搜尋結果頂端產生的 AI 生成回答方塊 |
| E-E-A-T | 經驗、專業、權威、信任 (Experience, Expertise, Authoritativeness, Trustworthiness) — Google 的內容品質框架 |
| SSR | 伺服器端渲染 (Server-Side Rendering) — 在伺服器產生 HTML，讓爬蟲不需執行 JavaScript 即可讀取內容 |
| CWV | 網站核心指標 (Core Web Vitals) — Google 的網頁體驗指標 (LCP, INP, CLS) |
| LCP | 最大內容繪製 (Largest Contentful Paint) — 最大可見元素渲染完成所需時間 |
| INP | 下次繪製互動 (Interaction to Next Paint) — 回應性指標（2024 年 3 月取代 FID） |
| CLS | 累計版面配置位移 (Cumulative Layout Shift) — 視覺穩定性指標 |
| JSON-LD | 連結資料的 JavaScript 物件標記法 — 偏好的結構化資料格式 |
| sameAs | Schema.org 屬性，將實體連結到其他平台上的個人資料 (Profiles) |
| IndexNow | 內容變更時即時通知搜尋引擎的協定 |
| llms.txt | 用來指引 AI 系統理解網站內容的提案標準檔案 |
| YMYL | 攸關金錢或生命 (Your Money or Your Life) — 需要最高 E-E-A-T 標準的主題 |
| SERP | 搜尋引擎結果頁面 (Search Engine Results Page) |
| 主題權威 | 網站對核心主題涵蓋的深度與廣度 |
```

---

## 格式與語氣指南

### 格式
- 全文使用乾淨的 Markdown：表格、標題（H2/H3）、項目符號、粗體強調。
- 用表格呈現資料，用項目符號呈現建議，用粗體標示關鍵術語。
- 章節之間留一個空白行以利閱讀。
- 使用水平線（---）分隔主要章節。
- 所有 URL 都應為絕對 URL（非相對 URL）。

### 語氣
- **專業但易懂** —— 寫給企業主，而非開發人員。
- **自信且直接** —— 將發現寫成結論，而非可能性。
- **行動導向** —— 每個發現都應連結到具體行動。
- **聚焦商業影響** —— 將技術問題轉譯為商業結果。
- 避免：未解釋的術語、模糊保留語、被動語態、過多聲明。
- 使用：「您的網站 [是/否]...」、「我們建議...」、「這會影響...」。

### 金額價值框架
盡可能將建議連結到商業價值：
- 「將您的 Google AIO 準備度從 35 提升到 70，預計可增加您在 AI Overviews 中 50% 的存在感，以目前的搜尋量計算，這代表每月約增加 2,000 名訪客。」
- 「伺服器端渲染將使 ChatGPT、Perplexity 以及其他 AI 平台能夠存取您的內容 — 這代表了您的競爭對手已經觸及的受眾群體。」
- 「在結構化資料標記上的投資（預計開發人員需花費 8-16 小時）可將您的實體識別分數從 20 提升到 75，顯著改善被引用的機率。」

估算務必保守。清楚說明假設。絕不保證特定結果。

---

## 輸出

使用上方完整範本產生 **GEO-CLIENT-REPORT.md**，並填入實際稽核資料。報告應該：
- 詳細程度相當於 40-80 頁（3,000-6,000 字）。
- 無需編輯即可直接寄給客戶。
- 自成一體（不要引用其他報告檔案 — 所有相關資料都包含在內）。
- 可列印且適合簡報呈現（乾淨的 Markdown 格式）。
