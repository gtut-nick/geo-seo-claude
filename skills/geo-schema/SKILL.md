---
name: geo-schema
description: 針對 AI 可發現性 (AI discoverability) 最佳化的 Schema.org 結構化資料稽核與產生，偵測、驗證並產生 JSON-LD 標記
version: 1.0.0
author: geo-seo-claude
tags: [geo, schema, structured-data, json-ld, entity-recognition, ai-discoverability]
allowed-tools: [Read, Grep, Glob, Bash, WebFetch, Write]
---

# GEO Schema 與結構化資料 (Structured Data)

## 目的

結構化資料是告訴 AI 系統「一個實體 (Entity) 是什麼、做什麼、如何與其他實體連結」的主要機器可讀訊號。傳統上 Schema 標記是為了取得 Google 複合搜尋結果 (Rich Results)，但它在 GEO 中的角色根本不同：**結構化資料是 AI 模型理解並信任您的實體的方式**。完整的實體圖譜 (Entity Graph) 會大幅提高所有 AI 搜尋平台引用的機率。

## 如何使用此技能

1. 使用 `fetch_page.py` 抓取目標頁面的 HTML（見下方註記）。
2. 偵測所有現有的結構化資料（JSON-LD、Microdata、RDFa）。
3. 依 Schema.org 規範驗證偵測到的 Schema。
4. 根據業務類型找出缺少的建議 Schema。
5. 產生可直接使用的 JSON-LD 程式碼區塊。
6. 輸出 GEO-SCHEMA-REPORT.md。

---

## Step 1: 偵測 (Detection)

**重要提示：** WebFetch 會將 HTML 轉換為 Markdown 並移除 `<head>` 內容，這會刪除 JSON-LD 區塊。請改用 `fetch_page.py`：
```bash
python3 ~/.claude/skills/geo/scripts/fetch_page.py <url> page
```
輸出會包含 `structured_data` 陣列，其中有從頁面解析出的所有 JSON-LD 區塊。

### 掃描 JSON-LD
在 HTML 中尋找 `<script type="application/ld+json">` 區塊。將每個區塊解析為 JSON。一個頁面可能包含多個 JSON-LD 區塊，請全部收集。

### 掃描 Microdata
尋找含有 `itemscope`、`itemtype` 與 `itemprop` 屬性的元素。映射嵌套項目的階層結構。註記：AI 爬蟲解析 Microdata 比 JSON-LD 困難。如果 Microdata 是唯一發現的格式，請標記建議遷移至 JSON-LD。

### 掃描 RDFa
尋找含有 `typeof`、`property` 與 `vocab` 屬性的元素。與 Microdata 類似，建議遷移至 JSON-LD。

### 優先順序
JSON-LD 是 GEO **強烈建議的格式**。Google、Bing 與 AI 平台都能最可靠地處理 JSON-LD。如果網站完全使用 Microdata 或 RDFa，請將其標記為高優先級遷移項目。

---

## Step 2: 驗證 (Validation)

對每個偵測到的 Schema 區塊進行驗證：

1. **有效的 JSON**：JSON-LD 語法是否有效？檢查結尾逗號、未加引號的鍵、格式錯誤的字串。
2. **有效的 @type**：`@type` 是否符合公認的 Schema.org 類型？對照 https://schema.org/docs/full.html。
3. **必填屬性**：Schema 是否包含該類型的所有必填屬性？（見下方各類型要求。）
4. **建議屬性**：Schema 是否包含能提高 AI 可發現性的建議屬性？
5. **sameAs 連結**：Schema 是否包含連結至其他平台存在感的 `sameAs` 屬性？
6. **URL 有效性**：Schema 中所有 URL 是否可解析（不是 404）？
7. **嵌套 (Nesting)**：Schema 是否正確嵌套（例如 Article 中的 author、Organization 中的 address）？
8. **渲染方式**：JSON-LD 是在伺服器渲染的 HTML 中，還是透過 JavaScript 注入的？依據 Google 2025 年 12 月的指南，**透過 JavaScript 注入的結構化資料處理可能會延遲**。標記任何需要執行 JS 的 Schema。

---

## Step 3: GEO 用的 Schema 類型

### Organization (組織)（關鍵 — 每個業務網站必備）
這對所有 AI 平台的實體識別都至關重要。AI 模型透過它識別業務本體。

**必填屬性：**
- `@type`: "Organization"（或子類型：Corporation、LocalBusiness 等）
- `name`: 官方業務名稱
- `url`: 官方網站 URL
- `logo`: 標誌圖片 URL（偏好使用 ImageObject）

**GEO 建議屬性：**
- `sameAs`: 所有平台 URL 的陣列（見 sameAs 策略）
- `description`: 組織的 1-2 句描述
- `foundingDate`: ISO 8601 日期
- `founder`: Person (人物) Schema
- `address`: PostalAddress (郵寄地址) Schema
- `contactPoint`: 包含電話、電子郵件、聯絡類型的 ContactPoint
- `areaServed`: 服務地理區域
- `numberOfEmployees`: 員工人數 (QuantitativeValue)
- `industry`: 產業文字或定義術語
- `award`: 獲得的獎項陣列
- `knowsAbout`: 組織具備專業知識的主題陣列（強大的 GEO 訊號）

### LocalBusiness (在地商家)（有實體據點的業務）
擴展自 Organization。對在地 AI 搜尋結果與 Google Gemini 非常重要。

**額外必填屬性：**
- `address`: 完整郵寄地址
- `telephone`: 電話號碼
- `openingHoursSpecification`: 營業時間

**GEO 建議屬性：**
- `geo`: 地理座標 (GeoCoordinates)（緯度、經度）
- `priceRange`: 價格區間標示
- `aggregateRating`: 綜合評分 Schema
- `review`: 評論 Schema 陣列
- `hasMap`: Google 地圖 URL

### Article (文章) + Author (作者)（出版商必備關鍵）
作者 Schema 是 AI 平台最強大的 E-E-A-T 訊號之一。

**Article 必填項目：**
- `@type`: "Article"（或 NewsArticle、BlogPosting、TechArticle）
- `headline`: 文章標題
- `datePublished`: ISO 8601 發布日期
- `dateModified`: ISO 8601 修改日期（對新鮮度訊號至關重要）
- `author`: Person 或 Organization Schema
- `publisher`: 包含標誌的 Organization Schema
- `image`: 代表性圖片

**GEO 要求的作者 (Person) 屬性：**
- `name`: 全名
- `url`: 網站上的作者頁面 URL
- `sameAs`: LinkedIn、Twitter、個人網站、Google Scholar、ORCID
- `jobTitle`: 職稱
- `worksFor`: Organization Schema
- `knowsAbout`: 專業領域陣列
- `alumniOf`: 畢業院校
- `award`: 專業獎項

### Product (產品)（電子商務用）
**必填項目：**
- `name`、`description`、`image`
- `offers`: 包含價格、幣別、存貨狀態的報價
- `brand`: 品牌 Schema
- `sku` 或 `gtin`/`mpn`

**GEO 建議項目：**
- `aggregateRating`: 綜合評分
- `review`: 個別評論陣列
- `category`: 產品類別
- `material`、`weight`、`width`、`height`（如適用）

### FAQPage (常見問題頁面)
**截至 2024 年的狀態**：Google 將 FAQ 複合搜尋結果限制於政府和衛生網站。但 FAQPage Schema 仍具有 GEO 用途；AI 平台會解析 FAQ 結構化資料以進行問答擷取。即使複合搜尋結果可能不顯示，仍建議為了 AI 可讀性進行實作。

**結構：**
- `@type`: "FAQPage"
- `mainEntity`: Question Schema 陣列，每個 Question 包含 `acceptedAnswer`，其中包含 Answer Schema

### SoftwareApplication (軟體應用程式)（SaaS 用）
**必填項目：**
- `name`、`description`
- `applicationCategory`: 例如 "BusinessApplication"
- `operatingSystem`: 支援的平台
- `offers`: 定價

**GEO 建議項目：**
- `aggregateRating`: 使用者評分
- `featureList`: 功能列表陣列（強大的引用訊號）
- `screenshot`: 螢幕截圖
- `softwareVersion`: 當前版本
- `releaseNotes`: 更新日誌連結

### WebSite + SearchAction（用於站內搜尋框）
**結構：**
```json
{
  "@type": "WebSite",
  "name": "網站名稱",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

### Person (人物)（獨立型 — 用於個人品牌、作者、思想領袖）
在「關於/簡介」頁面上作為獨立 Schema 使用。這會為個人專業知識建立實體圖譜。

**必填：** `name`、`url`
**GEO 建議項目：** `sameAs`、`jobTitle`、`worksFor`、`knowsAbout`、`alumniOf`、`award`、`description`、`image`

### speakable 屬性（針對語音/AI 助手）
`speakable` 屬性標記特別適合語音與 AI 助手讀取的內容區段。加入 Article 或 WebPage Schema 中。

```json
{
  "@type": "Article",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-summary", ".key-takeaway"]
  }
}
```
這會向 AI 助手指出哪些段落最適合引用或朗讀。

---

## Step 4: 標記已棄用/已變更的 Schema

| Schema | 狀態 | 註記 |
|---|---|---|
| HowTo | 2023 年 8 月棄用複合搜尋結果 | 仍可用於 AI 解析，但不要承諾複合結果 |
| FAQPage | 2023 年 8 月限制於政府/衛生網站 | 仍可用於 AI 解析（見上方） |
| SpecialAnnouncement | 2023 年棄用 | COVID 用途；若仍存在請移除 |
| CourseInfo | 2024 年被 Course 更新取代 | 使用更新後的 Course Schema 屬性 |
| VideoObject `contentUrl` | 2024 年變更行為 | 必須指向實際影片檔案，而非頁面 URL |
| Review snippet | 2024 年執行更嚴格 | 產品頁面上的自我推薦評論可能不顯示 |

標記任何發現的已棄用 Schema 並建議替代方案。

---

## Step 5: sameAs 策略（實體識別的關鍵）

`sameAs` 屬性是 GEO 最重要的結構化資料屬性。它告訴 AI 系統：「我網站上的這個實體與其他地方的這些個人資料是同一個實體。」這會建立 AI 平台用來驗證、信任與引用來源的實體圖譜。

### 建議的 sameAs 連結（依優先順序）

1. **維基百科條目 (Wikipedia article)** — 最高權威的實體連結
2. **Wikidata 項目** — 機器可讀的實體識別碼（例如 `https://www.wikidata.org/wiki/Q12345`）
3. **LinkedIn** — 公司專頁或個人檔案
4. **YouTube** — 頻道 URL
5. **Twitter/X** — 個人資料 URL
6. **Facebook** — 專頁 URL
7. **Crunchbase** — 公司檔案（針對新創/技術公司）
8. **GitHub** — 組織或個人檔案（針對技術領域）
9. **Google Scholar** — 作者檔案（針對研究人員/學者）
10. **ORCID** — 研究人員識別碼（針對學者）
11. **Instagram** — 個人資料 URL
12. **Apple App Store / Google Play** — 應用程式清單（針對軟體）
13. **BBB** — 商業改進局清單（針對美國業務）
14. **產業目錄** — 相關的垂直產業目錄

### sameAs 稽核流程
1. 收集實體的所有已知網路存在感。
2. 檢查每個 URL 是否可解析（非 404 或被重新導向）。
3. 確認 Organization/Person Schema 包含全部 URL。
4. 檢查每個平台上資訊是否一致（名稱、描述、創立日期等）。
5. 標記實體應該存在但目前不存在的平台。

---

## Step 6: JSON-LD 產生

根據偵測到的業務類型，產生可直接貼上的 JSON-LD 區塊。務必產生：

1. **Organization 或 Person**（取決於實體類型）— 必備
2. **包含 SearchAction 的 WebSite** — 首頁必備
3. **業務類型特定 Schema** — 出版商用 Article，電子商務用 Product，在地商家用 LocalBusiness，SaaS 用 SoftwareApplication
4. **BreadcrumbList (麵包屑清單)** — 任何深於首頁的頁面

### 產生規則
- 使用 `@graph` 模式，在一個 JSON-LD 區塊中包含多個 Schema。
- 所有 URL 必須使用絕對路徑（非相對路徑）。
- 包含 `@id` 屬性，以便 Schema 之間進行交叉引用。
- 所有日期使用 ISO 8601。
- 在 Article Schema 中加入 `speakable`，CSS 選擇器指向關鍵內容區段。
- 將 JSON-LD 放在 `<head>` 區段，**不要**透過 JavaScript 注入。

### 範本：含完整 GEO 訊號的 Organization
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "公司名稱",
  "url": "https://example.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://example.com/logo.png",
    "width": 600,
    "height": 60
  },
  "description": "關於公司業務的簡明描述。",
  "foundingDate": "2020-01-15",
  "founder": {
    "@type": "Person",
    "name": "創辦人姓名",
    "sameAs": "https://www.linkedin.com/in/founder"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service",
    "email": "support@example.com"
  },
  "sameAs": [
    "https://en.wikipedia.org/wiki/Company_Name",
    "https://www.wikidata.org/wiki/Q12345",
    "https://www.linkedin.com/company/company-name",
    "https://www.youtube.com/@companyname",
    "https://twitter.com/companyname",
    "https://github.com/companyname",
    "https://www.crunchbase.com/organization/company-name"
  ],
  "knowsAbout": [
    "主題 1",
    "主題 2",
    "主題 3"
  ]
}
```

---

## 評分標準 (0-100)

| 準則 | 分數 | 如何評分 |
|---|---|---|
| Organization/Person Schema 存在且完整 | 15 | 完整得 15，基本得 10，無則得 0 |
| sameAs 連結（5 個平台以上） | 15 | 每個有效的 sameAs 連結得 3 分，最高 15 |
| Article Schema 包含作者詳情 | 10 | 完整的作者 Schema 得 10，僅有姓名得 5，無則得 0 |
| 業務類型特定 Schema 存在 | 10 | 完整得 10，部分得 5，缺失得 0 |
| WebSite + SearchAction | 5 | 存在得 5，無則得 0 |
| 內頁具備 BreadcrumbList | 5 | 存在得 5，無則得 0 |
| 使用 JSON-LD 格式（非 Microdata/RDFa） | 5 | 僅 JSON-LD 得 5，混合得 3，僅 Microdata/RDFa 得 0 |
| 伺服器渲染（非 JS 注入） | 10 | 位於 HTML 源碼中得 10，JS 但在 head 中得 5，動態 JS 注入得 0 |
| 文章具備 speakable 屬性 | 5 | 存在得 5，無則得 0 |
| 有效的 JSON + 有效的 Schema.org 類型 | 10 | 無錯誤得 10，輕微問題得 5，重大錯誤得 0 |
| Organization/Person 具備 knowsAbout 屬性 | 5 | 具備 3 個以上主題得 5，缺失得 0 |
| 未發現已棄用的 Schema | 5 | 乾淨得 5，發現已棄用 Schema 得 0 |

---

## 輸出格式

產生 **GEO-SCHEMA-REPORT.md**，內容包含：

```markdown
# GEO Schema 與結構化資料報告 — [網域 Domain]
日期：[Date]

## Schema 分數：XX/100

## 偵測到的 Schema
| 頁面 | Schema 類型 | 格式 | 狀態 | 問題 |
|---|---|---|---|---|
| / | Organization | JSON-LD | 有效 | 缺少 sameAs |
| /blog/post-1 | Article | JSON-LD | 有效 | 無作者 Schema |

## 驗證結果
[依屬性列出每個 Schema 的通過/失敗情況]

## 缺少的建議 Schema
[根據業務類型列出應存在但實際缺失的 Schema]

## sameAs 稽核
| 平台 | URL | 狀態 |
|---|---|---|
| Wikipedia | [URL 或 "未找到"] | 存在/缺失 |
| LinkedIn | [URL 或 "未找到"] | 存在/缺失 |
[針對所有建議平台繼續列出]

## 產生的 JSON-LD 程式碼
[為每個缺失或不完整的 Schema 提供可直接貼上的 JSON-LD 區塊]

## 實作備註
- 每個 JSON-LD 區塊應放置的位置
- 伺服器渲染要求
- 使用 Google 複合搜尋結果測試與 Schema.org 驗證器進行測試
```
