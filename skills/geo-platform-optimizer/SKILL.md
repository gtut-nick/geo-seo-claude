---
name: geo-platform-optimizer
description: 針對平台的 AI 搜尋最佳化 (AI search optimization)，分別稽核與最佳化 Google AI Overviews、ChatGPT、Perplexity、Gemini 與 Bing Copilot
version: 1.0.0
author: geo-seo-claude
tags: [geo, ai-search, platform-optimization, chatgpt, perplexity, gemini, aio]
allowed-tools: [Read, Grep, Glob, Bash, WebFetch, Write]
---

# GEO 平台最佳化工具

## 核心洞察

只有 **11% 的網域 (Domains)** 會在同一個查詢 (Query) 中同時被 ChatGPT 與 Google AI Overviews 引用。每個 AI 搜尋平台使用不同的索引 (Index)、排名邏輯 (Ranking logic) 與來源偏好 (Source preferences)。為 Google AI Overviews 最佳化的頁面可能對 ChatGPT 不可見，反之亦然。平台特定最佳化 (Platform-specific optimization) 不是選配，而是任何嚴肅的 GEO 策略之基礎。

## 如何使用此技能

1. 收集目標 URL 與網站的主要主題/產業。
2. 針對該網站執行下方各平台的檢查清單 (Checklist)。
3. 依 0-100 的評分標準 (Rubric) 為各平台評分。
4. 產生 GEO-PLATFORM-OPTIMIZATION.md，包含各平台的分數、差距 (Gaps) 與行動項目 (Action items)。

---

## 平台 1: Google AI Overviews (AIO)

### AIO 如何選擇來源 (Sources)
- 92% 的 AIO 引用來自已排名在 **前 10 名自然搜尋結果 (Top 10 organic results)** 的頁面，傳統 SEO 是進入門檻。
- 但 47% 的引用來自排名**低於第 5 名**的頁面，表示 AIO 有自己的選擇邏輯，偏好清晰度 (Clarity) 與直接性 (Directness)，而不只是單純的排名。
- AIO 強烈偏好 **乾淨的結構 (Clean structure)、直接的回答 (Direct answers)、具備可掃描性的格式 (Scannable formatting)**。
- 精選摘要最佳化 (Featured snippet optimization) 與 AIO 最佳化約有 70% 的重疊。
- AIO 偏好 **簡潔、事實性、無歧義的答案**；避險語言 (Hedging) 與贅詞 (Filler) 會降低被引用的機率。

### 最佳化檢查清單

1. **問題式標題 (Question-Based Headings)**：使用以真實使用者查詢構成的 H2/H3 問題標題。檢查 Google 的「其他人也問了 (People Also Ask)」區塊，並鏡像模仿其精確措辭。
2. **第一段即直接回答 (Direct Answer in First Paragraph)**：在每個問題標題後立即提供清楚的 1-2 句回答，再展開支持性細節。第一句應可作為獨立引用。
3. **表格與結構化比較 (Tables and Structured Comparisons)**：AIO 高度引用表格。任何比較、定價、規格或功能數據都應轉成 HTML 表格，並使用清楚的欄位標題 (Column headers)。
4. **編號與項目清單 (Ordered and Unordered Lists)**：步驟流程使用編號清單。功能列表使用項目符號清單。AIO 會直接擷取這些結構。
5. **常見問題章節 (FAQ Sections)**：加入專屬的 FAQ 章節，包含 5-10 個真實問題。每個問題使用正確的 H3 標題。雖然 FAQPage schema 的複合搜尋結果自 2023 年 8 月起限制於政府/健康網站，但此內容模式仍有助於 AIO 擷取。
6. **定義與術語表方塊 (Definitions and Glossary Boxes)**：為任何產業專有名詞提供清楚定義。格式：「**[術語]** 是 [簡潔的定義]。」AIO 經常引用定義。
7. **具備來源的統計數據 (Statistics with Sources)**：加入具備歸屬說明 (Attribution) 的具體數字。「根據 [來源]，[統計數據]。」AIO 偏好可引用、具體的主張，而非模糊的斷言。
8. **發布日期 (Publication Date)**：包含可見的發布日期與最後更新日期。AIO 會降低無日期內容在時效性查詢中的優先度。
9. **作者署名 (Author Byline)**：顯示作者姓名與憑證 (Credentials)。連結到包含個人簡介、憑證與 sameAs 連結的作者頁面。
10. **頁面深度 (Page Depth)**：目標頁面保持在首頁點擊 3 次以內的距離。AIO 很少引用深層或孤立的內容。

### 評分標準 (0-100)

| 準則 (Criterion) | 分數 | 如何評分 |
|---|---|---|
| 目標查詢排名在前 10 名 | 20 | 是得 20，前 20 得 10，其餘得 0 |
| 具備問題式標題 | 10 | 每個問題標題 2 分，最高 10 |
| 標題後有直接回答 | 15 | 每個直接回答 3 分，最高 15 |
| 比較數據使用表格呈現 | 10 | 適當使用表格得 10，部分使用得 5，未使用得 0 |
| 流程/功能使用清單呈現 | 10 | 有得 10，部分有得 5 |
| 具備 5 個以上問題的 FAQ 章節 | 10 | 5+ 得 10，1-4 得 5，無則得 0 |
| 具備引用的統計數據 | 10 | 每個被引用的數據 2 分，最高 10 |
| 可見發布/更新日期 | 5 | 兩個日期皆有得 5，有一個得 3，無則得 0 |
| 具備憑證的作者署名 | 5 | 完整署名得 5，僅姓名得 3，無則得 0 |
| 乾淨的 URL + 標題階層 | 5 | H1>H2>H3 結構乾淨得 5，輕微問題得 3，結構錯誤得 0 |

---

## 平台 2: ChatGPT Web Search

### ChatGPT 如何選擇來源
- 使用 **Bing 搜尋索引 (Bing search index)** 作為基礎（而非 Google）。
- 依網域佔比的前幾名引用來源：**維基百科 (47.9%)**、Reddit (11.3%)、YouTube、主要新聞媒體。
- ChatGPT 高度重視 **實體識別 (Entity recognition)**；若品牌是結構化實體（維基百科、Wikidata、Crunchbase），被引用機率大幅提高。
- 偏好 **權威、老牌的來源**，而非新網站或小眾網站。
- 較長、較全面的文章比短篇內容更常被引用。
- ChatGPT 傾向引用主張的 **最權威來源 (Most canonical source)**，而不一定是原始來源。

### 最佳化檢查清單

1. **維基百科存在感 (Wikipedia Presence)**：檢查品牌/個人/產品是否有維基百科條目。若沒有，評估知名度標準 (Notability criteria)。若具備知名度，建立草案。若已存在條目，確保資訊準確且為最新。
2. **Wikidata 實體 (Wikidata Entity)**：確認實體是否存在於 Wikidata。若沒有，建立 Wikidata 項目，包含關鍵屬性：實例 (Instance of)、官方網站、社群媒體連結、創立日期、總部位置。
3. **Bing 網站管理員工具 (Bing Webmaster Tools)**：確認網站已註冊 Bing Webmaster Tools。提交網站地圖 (Sitemap)。檢查抓取錯誤 (Crawl errors)。
4. **Bing 索引覆蓋率 (Bing Index Coverage)**：在 Bing 使用 `site:domain.com` 確認關鍵頁面已被索引。Bing 索引的頁面可能與 Google 不同。
5. **Reddit 權威性**：檢查 Reddit 上的品牌提及。找出相關的子版 (Subreddits)。評估品牌是否真實地參與討論。
6. **YouTube 存在感**：確認 YouTube 頻道是否存在且有相關內容。影片描述應包含完整的 URL 與實體資訊。
7. **權威反向連結 (Authoritative Backlinks)**：ChatGPT/Bing 高度重視 .edu、.gov 與主要媒體的反向連結。稽核反向連結設定檔中是否有這些來源。
8. **實體一致性 (Entity Consistency)**：品牌名稱、創立日期、領導團隊與關鍵事實必須在維基百科、Crunchbase、LinkedIn 與官方網站之間保持一致。
9. **內容全面性 (Comprehensive Content)**：針對 ChatGPT 引用的頁面應為 **2000 字以上** 且主題涵蓋透徹。ChatGPT 偏好單一權威來源，而非多個內容稀疏的頁面。
10. **清楚的歸屬 (Clear Attribution)**：包含「關於我們」章節、公司描述與創業故事。ChatGPT 用這些進行實體確認 (Entity grounding)。

### 評分標準 (0-100)

| 準則 (Criterion) | 分數 | 如何評分 |
|---|---|---|
| 維基百科條目存在且準確 | 20 | 存在得 20，小作品 (Stub) 得 10，無則得 0 |
| Wikidata 實體具備 5 個以上屬性 | 10 | 完整得 10，基本得 5，無則得 0 |
| 關鍵頁面的 Bing 索引覆蓋率 | 10 | 全面得 10，部分得 5，極少得 0 |
| Reddit 品牌提及（正面） | 10 | 活躍討論得 10，有提及得 5，無則得 0 |
| 具備相關內容的 YouTube 頻道 | 10 | 活躍得 10，存在但稀疏得 5，無則得 0 |
| 權威反向連結 (.edu、.gov、媒體) | 15 | 每個權威連結類別 3 分，最高 15 |
| 跨平台的實體一致性 | 10 | 一致得 10，輕微差異得 5，重大差異得 0 |
| 內容全面性 (2000 字以上) | 10 | 透徹得 10，足夠得 5，稀疏得 0 |
| 已配置 Bing 網站管理員工具 | 5 | 已驗證得 5，未驗證得 0 |

---

## 平台 3: Perplexity AI

### Perplexity 如何選擇來源
- 前幾名引用來源：**Reddit (46.7%)**、維基百科、YouTube、主要出版物。
- 在所有 AI 搜尋平台中，Perplexity 最重視 **社群驗證 (Community validation)**。
- 強烈偏好由多位參與者辯論、驗證或擴展主張的 **討論串 (Discussion threads)**。
- 偏好新近內容；發布日期是強大的排名訊號。
- 每個回答會引用 **多個來源**（通常 5-15 個），因此中等權威的網站有更多機會出現。
- 除了搜尋 API 外，也使用自己的抓取基礎架構 (Crawling infrastructure)。

### 最佳化檢查清單

1. **活躍的 Reddit 存在感**：品牌或代表應在相關的 Reddit 子版討論中真實參與。不要進行推銷，要提供幫助、具體且以社群為導向。
2. **Reddit AMAs 與討論串**：鼓勵或參與 AMA (問我任何事)、詳細的討論串與社群問答。Perplexity 會將這些視為高訊號內容。
3. **論壇與社群存在感**：除 Reddit 外，檢查 Hacker News、Stack Overflow、Quora 與小眾產業論壇。Perplexity 大量索引這些平台。
4. **討論友善內容 (Discussion-Friendly Content)**：發布會引發討論的內容，例如評論文章、研究結果、反直覺觀點、原始數據。會被社群分享與討論的內容排名更好。
5. **新鮮度訊號 (Freshness Signals)**：內容需有清楚日期。定期更新內容。Perplexity 比其他平台更積極降低陳舊內容的優先度。
6. **多來源驗證 (Multiple Source Validation)**：內容中的主張應由其他來源支持。Perplexity 會進行交叉比對，並偏好能由多個來源驗證的主張。
7. **YouTube 影片內容**：建立 Perplexity 可引用的影片內容。確保影片標題、描述與逐字稿包含目標資訊。
8. **直接、可引用的段落**：撰寫可作為獨立引用的段落。每段應有一個清楚的觀點與支持證據。
9. **原始數據與研究**：發布原始調查、基準測試、案例研究或數據集。Perplexity 高度偏好第一手來源 (Primary sources)。
10. **Perplexity 頁面 (Pages)**：檢查 Perplexity 是否已建立關於你的主題/品牌的「頁面」。這些策展摘要會影響未來的引用。

### 評分標準 (0-100)

| 準則 (Criterion) | 分數 | 如何評分 |
|---|---|---|
| 在相關子版有活躍 Reddit 存在感 | 20 | 活躍貢獻者得 20，被提及得 10，無則得 0 |
| 論壇/社群提及 (HN、SO、Quora) | 10 | 多平台得 10，單一平台得 5，無則得 0 |
| 內容新鮮度（6 個月內更新） | 10 | 近期得 10，一年內得 5，更久得 0 |
| 發布原始研究/數據 | 15 | 原始研究得 15，案例研究得 10，部分數據得 5，無則得 0 |
| 具備逐字稿的 YouTube 內容 | 10 | 活躍頻道得 10，部分影片得 5，無則得 0 |
| 具備結構、可獨立引用的段落 | 10 | 每個良好的可引用段落 2 分，最高 10 |
| 主張具備多來源驗證 | 10 | 來源充足得 10，部分來源得 5，無則得 0 |
| 會引發討論的內容 | 10 | 被分享/討論得 10，部分互動得 5，無則得 0 |
| 維基百科/Wikidata 存在感 | 5 | 存在得 5，無則得 0 |

---

## 平台 4: Google Gemini

### Gemini 如何選擇來源
- 使用 **Google 搜尋索引**，並強烈加權 **Google 自家產品 (Google-owned properties)**。
- YouTube 內容比標準 Google 搜尋中更受重視。
- Google 商家檔案 (Google Business Profile) 數據可被 Gemini 直接存取。
- Gemini 直接使用 Google 知識圖譜 (Knowledge Graph)；具備知識圖譜實體是重大優勢。
- 結構化資料 (Schema.org) 會被 Gemini 直接用於實體理解。
- Gemini 是多模態 (Multi-modal)：可同時參考圖片、影片與文字。

### 最佳化檢查清單

1. **Google 知識面板 (Knowledge Panel)**：檢查品牌是否有 Google 知識面板。若沒有，透過 Google 商家檔案或結構化資料進行宣告。確保所有資訊準確。
2. **Google 商家檔案 (Google Business Profile)**：完整最佳化 GBP：營業時間、服務、照片、貼文、問答。Gemini 對於在地查詢會直接從 GBP 擷取。
3. **YouTube 策略**：為每個關鍵主題建立 YouTube 內容。最佳化標題、描述、時間戳記與閉路字幕 (Closed captions)。Gemini 引用 YouTube 的頻率高於任何其他 AI 平台。
4. **YouTube 章節與時間戳記**：使用章節（在描述中使用時間戳記），讓 Gemini 可以參考影片的特定片段。
5. **Google 商家中心 (Google Merchant Center)**：電子商務需確保產品已進入 Google Merchant Center。Gemini 會直接參考產品數據。
6. **結構化資料 (Schema.org)**：實作完整的 Schema.org 標記。Gemini 使用此訊號進行實體理解的積極程度高於其他平台。
7. **Google 網站生態系統**：確保存在於 Google 生態系統中：Google 學術搜尋 (研究)、Google 新聞 (發布者)、Google 地圖 (在地)。
8. **圖片最佳化**：Gemini 是多模態。使用描述性的替代文字 (Alt text)、結構化的圖片檔名與高品質圖片。每篇內容都加入相關圖片。
9. **Google E-E-A-T 訊號**：所有標準 Google E-E-A-T 訊號都適用且權重更高。作者頁面、關於頁面、編輯政策、專業展示。
10. **Chrome 線上應用程式商店 / Google Workspace Marketplace**：軟體公司若存在於 Google 平台，會增加實體訊號。

### 評分標準 (0-100)

| 準則 (Criterion) | 分數 | 如何評分 |
|---|---|---|
| Google 知識面板存在 | 15 | 完整得 15，部分得 10，無則得 0 |
| Google 商家檔案完整 | 10 | 完全最佳化得 10，基本得 5，無則得 0 |
| 具備主題相關內容的 YouTube 頻道 | 20 | 活躍且有章節得 20，存在得 10，無則得 0 |
| 已實作 Schema.org 結構化資料 | 15 | 全面得 15，基本得 10，極少得 5，無則得 0 |
| Google 生態系統存在感 (學術、新聞、地圖) | 10 | 3+ 得 10，1-2 得 5，無則得 0 |
| 圖片最佳化 (替代文字、檔名) | 10 | 全部圖片皆最佳化得 10，部分得 5，無則得 0 |
| E-E-A-T 訊號 (作者頁、關於頁、編輯政策) | 10 | 強得 10，部分得 5，弱則得 0 |
| Google 商家中心（若為電商） | 5 | 適用且活躍得 5，不適用則 N/A |
| 多模態內容 (文字 + 圖片 + 影片) | 5 | 豐富的多模態得 5，部分得 3，僅文字則得 0 |

---

## 平台 5: Bing Copilot

### Copilot 如何選擇來源
- 使用 **Bing 搜尋索引**（與 ChatGPT 共用基礎架構，但排名/選擇邏輯不同）。
- 支援 **IndexNow 協定**，可近乎即時地索引新內容與更新內容。
- Copilot 傾向每個回答引用**較少來源**（通常 3-5 個），但來源歸屬 (Attribution) 更突出。
- 微軟生態系統整合：LinkedIn、GitHub、Microsoft Learn 內容被加權。
- Copilot 偏好頁面清晰、具備結構化標記與載入速度快的頁面。

### 最佳化檢查清單

1. **Bing 網站管理員工具 (Bing Webmaster Tools)**：註冊並驗證網站。提交 XML 網站地圖。檢閱並修復抓取問題。
2. **IndexNow 實作**：實作 IndexNow 協定，即時通知 Bing 內容變動。在 `/.well-known/indexnow-key.txt` 放置金鑰檔案，並於內容發布/更新時 ping IndexNow API。
3. **LinkedIn 公司專頁**：確保公司 LinkedIn 頁面完整，包含準確描述、員工連結與定期貼文。Copilot 會索引 LinkedIn 內容。
4. **GitHub 存在感**：技術公司應維持活躍的 GitHub 存在感。Copilot 會參考 GitHub 儲存庫、文件與 README 檔案。
5. **Microsoft Learn / 文件**：若相關，貢獻 Microsoft Learn 或確保文件符合微軟文件標準。
6. **Bing Places for Business**：相當於 Google 商家檔案。Copilot 中的在地搜尋能見度需要填寫完整欄位。
7. **清楚的元描述 (Meta Descriptions)**：Bing/Copilot 對元描述的權重高於 Google。為每個頁面撰寫引人入勝、富含關鍵字的元描述。
8. **社群訊號 (Social Signals)**：Bing 在歷史上比 Google 更重視社群訊號（分享、按讚、互動）。維持活躍的社群媒體存在感。
9. **精確匹配關鍵字 (Exact-Match Keywords)**：Bing 演算法對關鍵字匹配的精確度要求比 Google 更直接。在標題、標題與正文內容中包含精確的目標短語。
10. **快速頁面載入**：Copilot 會降低慢速頁面的優先度。目標為 2 秒以下的載入時間。最佳化圖片、啟用壓縮、減少阻礙渲染的資源。

### 評分標準 (0-100)

| 準則 (Criterion) | 分數 | 如何評分 |
|---|---|---|
| Bing 網站管理員工具已驗證 + 網站地圖 | 15 | 已驗證得 15，部分得 5，未驗證得 0 |
| 已實作 IndexNow 協定 | 15 | 活躍得 15，未實作得 0 |
| 關鍵頁面的 Bing 索引覆蓋率 | 10 | 全面得 10，部分得 5，極少得 0 |
| LinkedIn 公司專頁 (完整) | 10 | 完整得 10，基本得 5，無則得 0 |
| GitHub 存在感 (若適用) | 5 | 活躍得 5，不適用則 N/A |
| 元描述已最佳化 | 10 | 全部關鍵頁面皆有得 10，部分得 5，缺失得 0 |
| 社群媒體互動訊號 | 10 | 活躍互動得 10，存在得 5，無則得 0 |
| 標題/標題中有精確匹配關鍵字 | 10 | 最佳化良好得 10，部分得 5，未最佳化得 0 |
| 頁面載入速度 < 2 秒 | 10 | < 2s 得 10，< 4s 得 5，> 4s 得 0 |
| Bing Places 已配置 (若為在地) | 5 | 完整得 5，非在地則 N/A |

---

## 跨平台總結

### 通用最佳化行動（幫助所有平台）
1. 維基百科/Wikidata 實體存在。
2. 具備相關內容的 YouTube 頻道。
3. 全面、結構良好且具備清楚標題的內容。
4. Schema.org 結構化資料（特別是 Organization + sameAs）。
5. 快速的頁面載入與乾淨的 HTML。
6. 具備憑證與 sameAs 連結的作者頁面。
7. 定期更新內容並標註可見日期。

### 平台特定優先順序
| 優先順序 | Google AIO | ChatGPT | Perplexity | Gemini | Copilot |
|---|---|---|---|---|---|
| #1 | 前 10 名排名 | 維基百科 | Reddit 存在感 | YouTube | IndexNow |
| #2 | 問答結構 | 實體圖譜 | 原始研究 | 知識面板 | Bing WMT |
| #3 | 表格/清單 | Bing SEO | 新鮮度 | Schema.org | LinkedIn |
| #4 | 精選摘要 | Reddit | 社群論壇 | GBP | 元描述 |

---

## 輸出格式

產生 **GEO-PLATFORM-OPTIMIZATION.md**，結構如下：

```markdown
# GEO 平台最佳化報告 — [網域 Domain]
日期：[Date]

## 整體平台準備度
- 綜合 GEO 分數: XX/100 (所有平台分數的平均值)

## 平台分數
| 平台 (Platform) | 分數 | 狀態 |
|---|---|---|
| Google AI Overviews | XX/100 | [強/中等/弱] |
| ChatGPT Web Search | XX/100 | [強/中等/弱] |
| Perplexity AI | XX/100 | [強/中等/弱] |
| Google Gemini | XX/100 | [強/中等/弱] |
| Bing Copilot | XX/100 | [強/中等/弱] |

狀態門檻：強 (Strong) = 70+，中等 (Moderate) = 40-69，弱 (Weak) = 0-39

## 平台詳細資料
[各平台的詳細分解，包含分數、發現的差距、具體行動]

## 優先行動計畫
### 快速獲勝 (本週)
[只需極少努力即可改善多個平台分數的行動]

### 中期計畫 (本月)
[需要內容創作或技術變動的行動]

### 策略計畫 (本季)
[需要實體建立、社群經營或平台存在感的行動]
```
