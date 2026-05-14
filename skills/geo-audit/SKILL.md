---
name: geo-audit
description: 使用平行子代理委派（parallel subagent delegation）執行完整的網站 GEO+SEO 稽核。協調涵蓋 AI 可引用度（AI citability）、平台分析（platform analysis）、技術基礎設施（technical infrastructure）、內容品質（content quality）與結構化標記（schema markup）的完整生成式引擎最佳化（Generative Engine Optimization）稽核。產生綜合 GEO 分數（0-100）與優先行動計畫。
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# GEO 稽核協調技能

## 目的

此技能會對任意網站執行完整的生成式引擎最佳化（Generative Engine Optimization, GEO）稽核。GEO 是最佳化網站內容，使 AI 系統（ChatGPT、Claude、Perplexity、Gemini 等）能發現、理解、引用並推薦它。本稽核會衡量網站在所有 GEO 面向的表現，並產生可執行的改善計畫。

## 核心洞察

傳統 SEO 最佳化的是搜尋引擎排名（search engine rankings）。GEO 最佳化的是 AI 引用與推薦。GEO 指標高分的網站，在 AI 產生的回應中會增加 30-115% 的曝光度（Georgia Tech / Princeton / IIT Delhi 2024 研究）。兩者有重疊，但要求不同。

---

## 稽核工作流程

### 第一階段：發現與偵察

**步驟 1：抓取首頁並偵測業務類型**

1. 使用 WebFetch 取得所提供 URL 的首頁。
2. 擷取下列訊號：
   - 頁面標題（Page title）、中繼描述（meta description）、H1 標題
   - 導覽列選單項目（揭示網站架構）
   - 頁尾內容（揭示業務資訊、地點、法律聲明頁面）
   - 首頁上的 Schema.org 標記（如 Organization、LocalBusiness 等）
   - 定價頁面連結（SaaS 指標）
   - 產品列表模式（電子商務指標）
   - 部落格/資源區塊（發布者指標）
   - 服務頁面（代理商指標）
   - 地址/電話/Google 地圖嵌入（在地商家指標）

3. 使用下列模式分類業務類型：

| 業務類型 | 偵測訊號 |
|---|---|
| **SaaS（軟體即服務）** | 定價頁面、「註冊」/「免費試用」行動呼籲（CTA）、app.domain.com 子網域、功能比較表、整合頁面 |
| **在地商家** | 首頁上的實體地址、Google 地圖嵌入、「附近」內容、LocalBusiness schema、服務區域頁面 |
| **電子商務** | 產品列表、購物車、Product schema、分類頁面、價格顯示、「加入購物車」按鈕 |
| **發布者** | 導覽列以部落格為主、Article schema、作者頁面、以日期為基礎的彙整、RSS 摘要、高內容發布量 |
| **代理商/服務** | 案例研究、作品集、「我們的作品」區塊、團隊頁面、客戶商標、服務描述 |
| **混合型** | 上述訊號的組合，依主要模式進行分類 |

**步驟 2：爬取網站地圖與內部連結**

1. 嘗試抓取 `/sitemap.xml` 與 `/sitemap_index.xml`。
2. 若網站地圖（sitemap）存在，依下列優先順序擷取最多 50 個不重複的頁面 URL：
   - 首頁（永遠包含）
   - 頂層導覽頁面
   - 高價值頁面（定價、關於我們、聯絡資訊、關鍵服務/產品頁面）
   - 部落格文章（抽樣 5-10 篇最近文章）
   - 分類/到達頁面（landing pages）
3. 若沒有網站地圖，從首頁爬取內部連結：
   - 擷取所有指向同一個網域的 `<a href>` 連結
   - 最多追蹤 2 層深度
   - 優先處理主要導覽列連出的頁面
4. 尊重 `robots.txt` 指令，不抓取被禁止（disallowed）的路徑。
5. 強制上限為 50 個頁面，每次擷取逾時限制為 30 秒。

**步驟 3：收集頁面層級數據**

對爬取集合中的每個頁面記錄：
- URL、標題、中繼描述、標準網址（canonical URL）
- H1-H6 標題架構
- 主要內容字數
- 存在的 Schema.org 類型
- 內部/外部連結數量
- 有/無 alt 替代文字的圖片
- Open Graph 與 Twitter Card 中繼標籤（meta tags）
- 回應狀態碼（Response status code）
- 頁面是否有結構化資料（structured data）

---

### 第二階段：平行子代理委派

將分析委派給 5 個專門的子代理（subagents）。每個子代理都會使用收集到的頁面數據，並產生類別分數（0-100）與發現結果。

**子代理 1：AI 曝光度分析（geo-ai-visibility）**
- 分析內容區塊是否適合被 AI 系統引用（可引用度評分）
- 透過 `robots.txt` 與 `llms.txt` 的存在與否檢查 AI 爬蟲的存取權限
- 掃描 YouTube、Reddit、Wikipedia、LinkedIn 上的品牌能見度
- 評估 AI 模型用於實體識別（entity recognition）的品牌權威訊號

**子代理 2：平台最佳化（geo-platform-analysis）**
- 評估 Google AI Overviews、ChatGPT、Perplexity、Gemini、Bing Copilot 的準備度
- 檢查特定平台的排名因素與最佳化機會

**子代理 3：技術 GEO 基礎設施（geo-technical）**
- 分析 `robots.txt` 中的 AI 爬蟲存取權限
- 驗證中繼標籤、標頭（headers）與 AI 系統的技術可存取性
- 檢查頁面載入速度、伺服器端渲染（SSR）與網站核心指標（Core Web Vitals）
- 評估安全標頭與行動裝置最佳化

**子代理 4：內容 E-E-A-T 品質（geo-content）**
- 評估經驗（Experience）、專業度（Expertise）、權威性（Authoritativeness）、可信度（Trustworthiness）訊號
- 檢查作者簡介、資歷證明、來源引用
- 評估內容的新鮮度、深度與原創性
- 驗證「關於我們」頁面品質與團隊資歷

**子代理 5：Schema 與結構化資料（geo-schema）**
- 驗證所有 schema.org 標記
- 檢查對 GEO 至關重要的 schema 類型（FAQ、HowTo、Organization、Product、Article）
- 評估 schema 的完整性與準確性
- 找出缺失的 schema 機會

---

### 第三階段：分數彙總與報告產生

#### 綜合 GEO 分數計算

整體 GEO 分數（0-100）是六個類別分數的加權平均：

| 類別 | 權重 | 衡量內容 |
|---|---|---|
| **AI 可引用度 (AI Citability)** | 25% | 內容對 AI 系統的可引用/可擷取程度 |
| **品牌權威 (Brand Authority)** | 20% | 第三方提及、實體識別訊號 |
| **內容 E-E-A-T (Content E-E-A-T)** | 20% | 經驗、專業度、權威性、可信度 |
| **技術 GEO (Technical GEO)** | 15% | AI 爬蟲存取權限、llms.txt、渲染、速度 |
| **Schema 與結構化資料** | 10% | Schema.org 標記品質與完整性 |
| **平台最佳化 (Platform Optimization)** | 10% | 在 AI 模型訓練與引用平台上的能見度 |

**公式:**
```
GEO分數 = (可引用度 * 0.25) + (品牌 * 0.20) + (EEAT * 0.20) + (技術 * 0.15) + (Schema * 0.10) + (平台 * 0.10)
```

#### 分數解讀

| 分數範圍 | 評等 | 解讀 |
|---|---|---|
| 90-100 | 極佳 (Excellent) | 頂級 GEO 最佳化；網站極度可能被 AI 引用 |
| 75-89 | 良好 (Good) | GEO 基礎穩固，但仍有改善空間 |
| 60-74 | 尚可 (Fair) | 中等 GEO 能見度；有顯著的最佳化機會 |
| 40-59 | 差劣 (Poor) | GEO 訊號弱；AI 系統可能難以引用或推薦 |
| 0-39 | 危急 (Critical) | GEO 最佳化極少；網站大多對 AI 系統不可見 |

---

## 問題嚴重度分類

稽核期間找到的每個問題都依嚴重度分類：

### 嚴重 (Critical)（立即修復）
- `robots.txt` 封鎖所有 AI 爬蟲
- 沒有可索引的內容（僅依賴 JavaScript 渲染且無伺服器端渲染 SSR）
- 網域層級的 noindex 指令
- 關鍵頁面回傳 5xx 錯誤
- 完全沒有任何結構化資料
- 品牌未被任何 AI 系統視為實體（entity）

### 高 (High)（1 週內修復）
- 關鍵 AI 爬蟲（GPTBot、ClaudeBot、PerplexityBot）被封鎖
- 沒有 `llms.txt` 檔案
- 關鍵頁面上沒有問答（question-answering）內容區塊
- 缺少 Organization 或 LocalBusiness schema
- 內容頁面沒有作者署名
- 所有內容都在登入/付費牆後，且無預覽內容

### 中 (Medium)（1 個月內修復）
- 部分 AI 爬蟲封鎖（部分允許、部分封鎖）
- `llms.txt` 存在但不完整或格式錯誤
- 內容區塊平均低於 50 分的可引用度分數
- 有 FAQ 內容的頁面缺少 FAQ schema
- 作者簡介很單薄且無資歷證明
- 沒有 Wikipedia 或 Reddit 品牌能見度

### 低 (Low)（可行時最佳化）
- 輕微的 schema 驗證錯誤
- 部分圖片缺少 alt 替代文字
- 非關鍵頁面有內容新鮮度問題
- 缺少 Open Graph 標籤
- 部分頁面的標題層級（heading hierarchy）不理想
- LinkedIn 公司頁面存在但不完整

---

## 輸出格式

產生名為 `GEO-AUDIT-REPORT.md` 的檔案，結構如下：

```markdown
# GEO 稽核報告：[網站名稱]

**稽核日期:** [日期]
**網址 (URL):** [網址]
**業務類型:** [偵測到的類型]
**已分析頁面數:** [數量]

---

## 執行摘要

**整體 GEO 分數: [X]/100 ([評等])**

[用 2-3 句話總結網站的 GEO 健康狀況、最大優勢以及最關鍵的缺口。]

### 分數細項

| 類別 | 分數 | 權重 | 加權分數 |
|---|---|---|---|
| AI 可引用度 | [X]/100 | 25% | [X] |
| 品牌權威 | [X]/100 | 20% | [X] |
| 內容 E-E-A-T | [X]/100 | 20% | [X] |
| 技術 GEO | [X]/100 | 15% | [X] |
| Schema 與結構化資料 | [X]/100 | 10% | [X] |
| 平台最佳化 | [X]/100 | 10% | [X] |
| **整體 GEO 分數** | | | **[X]/100** |

---

## 嚴重問題 (立即修復)

[列出每個嚴重問題，包含特定頁面 URL 與建議的修復方式]

## 高優先級問題

[列出每個高優先級問題的詳細資訊]

## 中優先級問題

[列出每個中優先級問題]

## 低優先級問題

[列出每個低優先級問題]

---

## 分類深入分析

### AI 可引用度 ([X]/100)
[詳細發現結果、優良/不良段落範例、改寫建議]

### 品牌權威 ([X]/100)
[平台能見度地圖、提及量、情緒分析]

### 內容 E-E-A-T ([X]/100)
[作者品質、來源引用、新鮮度、深度]

### 技術 GEO ([X]/100)
[爬蟲存取權限、llms.txt、渲染、標頭]

### Schema 與結構化資料 ([X]/100)
[找到的 Schema 類型、驗證結果、缺失的機會]

### 平台最佳化 ([X]/100)
[在 YouTube、Reddit、Wikipedia 等平台的能見度]

---

## 快速致勝 (Quick Wins - 本週實施)

1. [具體、可執行的快速致勝方案與預期影響]
2. [另一個快速致勝方案]
3. [另一個快速致勝方案]
4. [另一個快速致勝方案]
5. [另一個快速致勝方案]

## 30 天行動計畫

### 第 1 週: [主題]
- [ ] 行動項目 1
- [ ] 行動項目 2

### 第 2 週: [主題]
- [ ] 行動項目 1
- [ ] 行動項目 2

### 第 3 週: [主題]
- [ ] 行動項目 1
- [ ] 行動項目 2

### 第 4 週: [主題]
- [ ] 行動項目 1
- [ ] 行動項目 2

---

## 附錄：已分析頁面

| URL | 標題 | GEO 問題數量 |
|---|---|---|
| [url] | [title] | [issue count] |
```

---

## 品質門檻

- **頁面限制 (Page Limit)：** 每次稽核（audit）不超過 50 個頁面。優先處理高價值頁面。
- **逾時 (Timeout)：** 每次頁面擷取（fetch）最多 30 秒。超時頁面跳過。
- **Robots.txt：** 爬取前永遠檢查並尊重 robots.txt。註明任何針對 AI 的特定指令（AI-specific directives）。
- **速率限制 (Rate Limiting)：** 頁面擷取間至少等待 1 秒，避免讓伺服器（server）過載。
- **錯誤處理 (Error Handling)：** 記錄失敗的擷取，但繼續執行稽核。在附錄（appendix）回報擷取失敗的項目。
- **內容類型 (Content Type)：** 只分析 HTML 頁面。跳過 PDF、圖片（images）與其他二進位內容（binary content）。
- **去重複化 (Deduplication)：** 爬取前將 URL 標準化（canonicalize）。跳過重複內容（例如 HTTP vs HTTPS、www vs non-www、結尾斜線等差異）。

---

## 特定業務類型的稽核調整 (Business-Type-Specific Audit Adjustments)

### SaaS 網站
- **額外加重權重於：** 功能比較表（高可引用度）、整合頁面、文件品質
- **檢查重點：** API 文件架構、更新日誌（changelog）頁面、知識庫組織
- **關鍵 Schema：** SoftwareApplication、FAQPage、HowTo

### 在地商家
- **額外加重權重於：** NAP（名稱、地址、電話）一致性、Google 商家檔案（Google Business Profile）訊號、在地 Schema
- **檢查重點：** 服務區域頁面、特定地點內容、評論標記
- **關鍵 Schema：** LocalBusiness、GeoCoordinates、OpeningHoursSpecification

### 電子商務網站 (E-commerce Sites)
- **額外加重權重於：** 產品描述（可引用度）、比較內容、購買指南
- **檢查重點：** Product Schema 完整性、評論彙總、產品頁面上的 FAQ 區塊
- **關鍵 Schema：** Product、AggregateRating、Offer、BreadcrumbList

### 出版者
- **額外加重權重於：** 文章品質、作者資歷證明、來源引用實務
- **檢查重點：** Article Schema、作者頁面、發布日期新鮮度、原創研究
- **關鍵 Schema：** Article、NewsArticle、Person（作者）、ClaimReview

### 代理商/服務 (Agency/Services)
- **額外加重權重於：** 案例研究（可引用度）、專業度展現、思想領導力（thought leadership）
- **檢查重點：** 作品集（portfolio）Schema、團隊資歷證明、特定產業專業度訊號
- **關鍵 Schema：** Organization、Service、Person（團隊）、Review