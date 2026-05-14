---
name: geo-technical
description: 具有 GEO 專屬檢查的技術 SEO 稽核 — 可爬取性 (crawlability)、可索引性 (indexability)、安全性、效能、SSR 與 AI 爬蟲存取
version: 1.0.0
author: geo-seo-claude
tags: [geo, technical-seo, core-web-vitals, ssr, crawlability, security, performance]
allowed-tools: [Read, Grep, Glob, Bash, WebFetch, Write]
---

# GEO 技術 SEO 稽核

## 目的

技術 SEO 是傳統搜尋能見度與 AI 搜尋引用 (AI search citation) 的共同基礎。技術上故障的網站無法被任何平台爬取、索引或引用。此技能會稽核 8 類技術健康度，並特別關注 GEO 需求；最關鍵的是 **伺服器端渲染 (server-side rendering, SSR)**（AI 爬蟲通常不會執行 JavaScript）與 **AI 爬蟲存取 (AI crawler access)**（許多網站會在 robots.txt 中無意間封鎖 AI 爬蟲）。

## 如何使用此技能

1. 收集目標 URL（首頁 + 2-3 個重要內頁）。
2. 使用 curl/WebFetch 抓取每個頁面的原始 HTML (raw HTML) 與 HTTP 標頭 (headers)。
3. 逐一檢查下方 8 個稽核分類。
4. 使用評分規則為每個分類評分。
5. 產生包含結果的 GEO-TECHNICAL-AUDIT.md。

---

## 分類 1: 可爬取性 (Crawlability)（15 分）

### 1.1 robots.txt 有效性
- 抓取 `https://[domain]/robots.txt`。
- 檢查語法有效性：正確的 `User-agent`、`Allow`、`Disallow` 指令。
- 檢查常見錯誤：缺少 User-agent、萬用字元封鎖重要路徑、Disallow: / 封鎖整站。
- 驗證是否引用 XML 網站地圖 (sitemap)：`Sitemap: https://[domain]/sitemap.xml`。

### 1.2 AI 爬蟲存取 (AI Crawler Access)（GEO 關鍵）
檢查 robots.txt 是否有針對以下 AI 爬蟲的指令：

| 爬蟲 (Crawler) | User-Agent | 平台 |
|---|---|---|
| GPTBot | GPTBot | ChatGPT / OpenAI |
| Google-Extended | Google-Extended | Gemini / Google AI 訓練 |
| Googlebot | Googlebot | Google 搜尋 + AI Overviews |
| Bingbot | bingbot | Bing Copilot + ChatGPT (透過 Bing) |
| PerplexityBot | PerplexityBot | Perplexity AI |
| ClaudeBot | ClaudeBot | Anthropic Claude |
| Amazonbot | Amazonbot | Alexa / Amazon AI |
| CCBot | CCBot | Common Crawl（許多 AI 模型使用） |
| FacebookBot | FacebookExternalHit | Meta AI |
| Bytespider | Bytespider | TikTok / 字節跳動 AI |
| Applebot-Extended | Applebot-Extended | Apple Intelligence |

**AI 爬蟲存取評分：**
- 所有主要 AI 爬蟲皆允許：5 分
- 部分被封鎖但 Googlebot + Bingbot 允許：3 分
- GPTBot 或 PerplexityBot 被封鎖：1 分（顯著 GEO 影響）
- Googlebot 被封鎖：0 分（致命）

**重要細節**：封鎖 Google-Extended 不會封鎖 Googlebot。Google-Extended 只控制 AI 訓練資料使用，不控制搜尋索引。不過，封鎖 Google-Extended 可能降低在 AI Overviews 中的存在感。除非有特定資料授權疑慮，否則建議允許 Google-Extended。

### 1.3 XML 網站地圖 (Sitemaps)
- 抓取 sitemap（檢查 robots.txt 的位置，或嘗試 `/sitemap.xml`、`/sitemap_index.xml`）。
- 驗證 XML 語法。
- 檢查 `<lastmod>` 日期（應存在且正確）。
- 計算 URL 數量 — 與預期可索引頁面數比較。
- 大型網站檢查是否使用 sitemap index（每個 sitemap 最多 50,000 個 URL）。
- 驗證所有 sitemap URL 皆回傳 200 狀態碼 (抽樣檢查)。

### 1.4 爬取深度 (Crawl Depth)
- 首頁 = 深度 0。檢查所有重要頁面是否能在 **3 次點擊**內到達（深度 3）。
- 位於深度 4 以上的頁面會獲得明顯較少的爬取預算 (crawl budget)，也較不可能被 AI 引用。
- 檢查內部連結 (internal linking)：重要內容頁是否從首頁或主選單連結？

### 1.5 Noindex 管理
- 檢查應被索引的頁面是否有 `<meta name="robots" content="noindex">`。
- 檢查是否有 `X-Robots-Tag: noindex` HTTP 標頭。
- 常見錯誤：在分頁 (pagination)、分類頁或重要到達網頁 (landing pages) 上設定 noindex。

**分類評分：**
| 檢查項目 | 分數 |
|---|---|
| robots.txt 有效且完整 | 3 |
| 允許 AI 爬蟲存取 | 5 |
| XML sitemap 存在且有效 | 3 |
| 爬取深度在 3 次點擊內 | 2 |
| 無錯誤的 noindex 指令 | 2 |

---

## 分類 2: 可索引性 (Indexability)（12 分）

### 2.1 標準連結標籤 (Canonical Tags)
- 每個可索引頁面都必須有 `<link rel="canonical" href="...">` 標籤。
- 權威版本 (authoritative version) 的 canonical 必須指向自己 (self-referencing)。
- 檢查衝突的 canonical（HTML 標籤 vs. HTTP 標頭）。
- 檢查標準連結鏈 (canonical chains)（A 指向 B，B 指向 C -- 應修正為 A 直接指向 C）。

### 2.2 重複內容 (Duplicate Content)
- 檢查 www vs. non-www（兩者都應可解析，其中一個應重新導向）。
- 檢查 HTTP vs. HTTPS（HTTP 應 301 導向至 HTTPS）。
- 檢查結尾斜線 (trailing slash) 一致性（選定一種模式，另一種重新導向）。
- 檢查參數造成的重複頁面（例如 `?sort=price` 建立重複內容）。

### 2.3 分頁 (Pagination)
- 若存在分頁內容，檢查 `rel="next"` / `rel="prev"`（注意：Google 自 2019 年起忽略這些，但 Bing 仍使用）。
- 偏好做法：在分頁頁面使用 `rel="canonical"` 指向「查看全部」頁面或第一頁。
- 確保含有獨特內容的分頁頁面不要設定 noindex。

### 2.4 Hreflang（國際化網站）
- 檢查 `<link rel="alternate" hreflang="xx">` 標籤。
- 驗證對等 hreflang（若頁面 A 指向頁面 B，B 必須指回 A）。
- 驗證 x-default 回退機制是否存在。
- 檢查語言/地區代碼有效性（ISO 639-1 / ISO 3166-1）。

### 2.5 索引膨脹 (Index Bloat)
- 估算已索引頁面數（檢查 sitemap 數量，使用 `site:domain.com` 估算）。
- 將已索引頁面與實際有價值的內容頁比較。
- 若已索引頁面明顯超過內容頁，標記為索引膨脹（通常來自內容貧乏頁/重複頁/參數頁）。

**分類評分：**
| 檢查項目 | 分數 |
|---|---|
| 所有頁面的 Canonical 標籤正確 | 3 |
| 無重複內容問題 | 3 |
| 分頁處理正確 | 2 |
| Hreflang 正確 (如適用) | 2 |
| 無索引膨脹問題 | 2 |

---

## 分類 3: 安全性 (Security)（10 分）

### 3.1 強制 HTTPS
- 網站必須透過 HTTPS 載入。
- HTTP 必須重新導向到 HTTPS（301 重新導向）。
- 不可有混合內容警告 (mixed content warnings)（HTTPS 頁面中的 HTTP 資源）。
- SSL/TLS 憑證必須有效且未過期。

### 3.2 安全標頭 (Security Headers)
檢查 HTTP 回應標頭：

| 標頭 (Header) | 要求值 | 目的 |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | 強制使用 HTTPS (HSTS) |
| `Content-Security-Policy` | 適當的政策值 | 防止 XSS 攻擊 |
| `X-Content-Type-Options` | `nosniff` | 防止 MIME 類型嗅探 |
| `X-Frame-Options` | `DENY` 或 `SAMEORIGIN` | 防止點擊劫持 (Clickjacking) |
| `Referrer-Policy` | `strict-origin-when-cross-origin` 或更嚴格 | 控制參照位址資料 |
| `Permissions-Policy` | 適當的限制值 | 控制瀏覽器功能權限 |

**分類評分：**
| 檢查項目 | 分數 |
|---|---|
| 強制使用 HTTPS 並具備有效憑證 | 4 |
| 具備 HSTS 標頭 | 2 |
| X-Content-Type-Options | 1 |
| X-Frame-Options | 1 |
| Referrer-Policy | 1 |
| Content-Security-Policy | 1 |

---

## 分類 4: URL 結構（8 分）

### 4.1 乾淨的 URL (Clean URLs)
- URL 應具備可讀性：`/blog/seo-guide`，而非 `/blog?id=12345`。
- URL 中不可包含工作階段 ID (session IDs)。
- 僅使用小寫字母（不要大小寫混用）。
- 使用連字號 (hyphens) 分隔單字（不要用底線 underscores）。
- 不使用特殊字元或編碼後的空白。

### 4.2 邏輯階層
- URL 路徑應反映網站架構：`/category/subcategory/page`。
- 適合時保持扁平化結構 — 避免不必要的深層嵌套。
- 全站使用一致的命名模式。

### 4.3 重新導向鏈 (Redirect Chains)
- 檢查重新導向鏈（A 導向 B 再導向 C）。
- 建議最多 1 次跳轉 (1 hop)（A 直接導向 C）。
- 檢查重新導向迴圈 (redirect loops)。
- 除非是刻意的暫時性用途，所有重新導向都應為 301（永久），而非 302（暫時）。

### 4.4 參數處理
- URL 參數不應建立重複的可索引頁面。
- 對於參數變體使用 canonical 標籤或 `robots.txt` Disallow。
- 在 Google Search Console 與 Bing Webmaster Tools 設定參數處理規則。

**分類評分：**
| 檢查項目 | 分數 |
|---|---|
| 乾淨且具可讀性的 URL | 2 |
| 邏輯架構階層 | 2 |
| 無重新導向鏈 (最多 1 次跳轉) | 2 |
| 已配置參數處理規則 | 2 |

---

## 分類 5: 行動裝置最佳化 (Mobile Optimization)（10 分）

### 關鍵脈絡
自 **2024 年 7 月** 起，Google 只使用行動裝置 Googlebot (mobile Googlebot) 爬取所有網站。不再進行電腦版爬取。如果網站在行動裝置上無法運作，它對 Google 來說就是無效的。

### 5.1 回應式設計 (Responsive Design)
- 檢查 `<meta name="viewport" content="width=device-width, initial-scale=1">`。
- 內容在行動裝置上不得需要水平捲動。
- 不可有寬於視窗 (viewport) 的固定寬度版面 (fixed-width layouts)。

### 5.2 點擊目標 (Tap Targets)
- 互動元素（按鈕、連結）至少必須為 48x48 CSS 像素。
- 點擊目標之間至少應有 8 像素的間距。
- 檢查導覽列 (navigation) 在行動裝置上是否易於操作。

### 5.3 字體大小
- 基礎字體大小應至少為 16 像素。
- 文字不應需要縮放即可閱讀。
- 對比度充足（WCAG AA 標準：一般文字 4.5:1，大字 3:1）。

### 5.4 行動裝置內容對等性 (Mobile Content Parity)
- 電腦版可見的所有內容也必須在行動裝置上可見。
- 不要把內容隱藏在 Googlebot 無法展開的「閱讀更多」切換開關後面（雖然截至 2025 年 Google 已更擅長處理這些內容）。
- 圖片與媒體必須能在行動裝置上正常載入。

**分類評分：**
| 檢查項目 | 分數 |
|---|---|
| Viewport meta 標籤正確 | 3 |
| 回應式版面 (無水平捲動) | 3 |
| 點擊目標尺寸適中 | 2 |
| 字體大小清晰易讀 | 2 |

---

## 分類 6: 網站核心指標 (Core Web Vitals)（15 分）

### 2026 指標與門檻
網站核心指標使用真實使用者資料 (field data) 的 **第 75 百分位數** 作為基準。實驗室資料 (Lab data) 對除錯有用，但真實使用者資料決定排名訊號。

| 指標 | 良好 (Good) | 待改善 (NI) | 不佳 (Poor) | 說明 |
|---|---|---|---|---|
| **LCP** (最大內容繪製) | < 2.5s | 2.5s - 4.0s | > 4.0s | 測量載入效能 — 最大可見元素完成渲染的時間 |
| **INP** (下次繪製互動) | < 200ms | 200ms - 500ms | > 500ms | 2024 年 3 月取代 FID。測量所有互動的回應性 |
| **CLS** (累計版面配置位移) | < 0.1 | 0.1 - 0.25 | > 0.25 | 測量視覺穩定性 — 非預期的版面位移 |

### 沒有 CrUX 資料時如何評估
當無法取得真實使用者資料時，依頁面特徵進行估算：
- **LCP**：檢查首屏 (above-fold) 最大元素。是圖片嗎（檢查尺寸/格式）？是文字嗎（檢查字體載入效能）？伺服器回應時間 (TTFB) 如何？
- **INP**：檢查頁面是否有沉重的 JavaScript。長工作 (Long tasks, >50ms) 會阻塞互動。檢查第三方指令碼。
- **CLS**：檢查圖片是否缺少明確的寬高屬性。檢查首屏是否有動態插入的內容。檢查網路字體是否造成版面位移 (FOUT/FOIT)。

### 常見 LCP 修正建議
1. 最佳化主視覺圖片：使用 WebP/AVIF 格式、正確尺寸、並用 `<link rel="preload">` 預載。
2. 降低伺服器回應時間（目標 TTFB < 800ms）。
3. 移除阻礙渲染的 CSS/JS。
4. 預先連線 (Preconnect) 到關鍵第三方網域。

### 常見 INP 修正建議
1. 使用 `requestIdleCallback` 或 `scheduler.yield()` 將長工作 (>50ms) 拆分成較小片段。
2. 減少第三方 JavaScript 的使用。
3. 對螢幕外的內容使用 `content-visibility: auto`。
4. 對事件處理程式進行防震 (debounce) 或節流 (throttle) 處理。

### 常見 CLS 修正建議
1. 一律在圖片與影片標籤上包含 `width` 和 `height` 屬性。
2. 使用 CSS `aspect-ratio` 或明確尺寸為廣告與嵌入內容預留空間。
3. 使用 `font-display: swap` 並搭配調整過尺寸的備用字體。
4. 避免在頁面載入後，於現有內容上方動態插入新內容。

**分類評分：**
| 檢查項目 | 分數 |
|---|---|
| LCP < 2.5s | 5 |
| INP < 200ms | 5 |
| CLS < 0.1 | 5 |

---

## 分類 7: 伺服器端渲染 (Server-Side Rendering, SSR)（15 分）— GEO 關鍵

### 為何 SSR 是 AI 能見度的必要條件
大多數 AI 爬蟲（GPTBot、PerplexityBot、ClaudeBot 等）**不會執行 JavaScript**。它們直接抓取原始 HTML 並進行解析。如果內容是由 React、Vue、Angular 或任何其他 JS 框架在用戶端 (client-side) 渲染，AI 爬蟲看到的將會是空白頁面。

即使是會執行 JavaScript 的 Googlebot，也會因額外的爬取預算需求而降低 JS 渲染內容的優先級。Google 會在獨立的「渲染佇列」(rendering queue) 中處理 JS 渲染，這可能導致索引延遲數天甚至數週。

### 偵測方法
1. 使用 curl 抓取頁面（不執行 JS）：`curl -s [URL]`。
2. 將原始 HTML 與渲染後的 DOM（透過瀏覽器查看）進行比較。
3. 如果 curl 輸出中缺少關鍵內容（標題、段落、產品資訊、文章正文），則網站過度依賴用戶端渲染。

### 稽核重點
- **主要內容文字**：文章本文 / 產品描述 / 頁面內容是否出現在原始 HTML 中？
- **標題 (Headings)**：H1、H2、H3 標籤是否位於原始 HTML 中？
- **導覽列**：主導覽選單是否為伺服器端渲染？
- **結構化資料 (Schema)**：JSON-LD 是直接在原始 HTML 中，還是由 JS 注入？
- **Meta 標籤**：標題、描述、canonical、OG 標籤是否在原始 HTML 中？
- **內部連結**：導覽與內容連結是否在原始 HTML 中？（這對可爬取性至關重要）

### 建議的 SSR 解決方案
| 框架 | SSR 解決方案 |
|---|---|
| React | Next.js (SSR/SSG), Remix, Gatsby (SSG) |
| Vue | Nuxt.js (SSR/SSG) |
| Angular | Angular Universal |
| Svelte | SvelteKit |
| 通用型 | Prerender.io (預渲染服務), Rendertron |

### 評分細節
- 所有關鍵內容皆為伺服器端渲染：15 分
- 主要內容為伺服器渲染，但部分元素僅靠 JS：10 分
- 關鍵內容需要執行 JS 才能顯示（如產品資訊、正文）：5 分
- 整頁皆為用戶端渲染（原始 HTML 中 body 為空）：0 分

**分類評分：**
| 檢查項目 | 分數 |
|---|---|
| 原始 HTML 中包含主要內容 | 8 |
| 原始 HTML 中包含 Meta 標籤與結構化資料 | 4 |
| 原始 HTML 中包含內部連結 | 3 |

---

## 分類 8: 網頁速度與伺服器效能（15 分）

### 8.1 首位元組時間 (Time to First Byte, TTFB)
- 目標：**< 800ms**（理想值 < 200ms）。
- 使用 curl 測量：`curl -o /dev/null -s -w 'TTFB: %{time_starttransfer}s\n' [URL]`。
- 若 TTFB > 800ms：檢查伺服器地理位置、快取機制、資料庫查詢效能、CDN 使用情況。

### 8.2 資源最佳化
- 總頁面重量目標：**< 2MB**（關鍵頁面應 < 1MB）。
- 檢查未壓縮資源（應啟用 gzip 或 brotli 壓縮）。
- 檢查未縮減 (minify) 的 CSS 與 JavaScript。
- 檢查未使用的 CSS/JS（許多網站下載的內容中有 50% 以上是多餘的）。

### 8.3 圖片最佳化
- 檢查圖片格式：WebP 或 AVIF 優於 JPEG/PNG。
- 檢查過大圖片 (oversized images)（圖片實體尺寸大於顯示尺寸）。
- 檢查延遲載入 (lazy loading)：首屏以下的圖片應具備 `loading="lazy"`。
- 檢查明確尺寸：包含寬高屬性以防止 CLS 位移。
- 首屏 (above-fold) 圖片**不應**使用延遲載入（這會傷害 LCP）。

### 8.4 程式碼拆分 (Code Splitting) 與延遲載入
- JavaScript 應進行程式碼拆分，確保每個頁面只載入所需的內容。
- 檢查大型 JS 套件（壓縮後 > 200KB 為警訊，> 500KB 為關鍵問題）。
- 第三方指令碼應非同步載入（使用 `async` 或 `defer`）。
- 檢查 `<head>` 中是否存在阻礙渲染的資源。

### 8.5 快取機制 (Caching)
- 檢查靜態資源（圖片、CSS、JS）的 `Cache-Control` 標頭。
- 靜態資產應使用長效快取：`max-age=31536000`（1 年）並搭配內容雜湊 (content-hashed) 檔名。
- HTML 頁面應使用較短的快取，或搭配驗證機制（如 `ETag` 或 `Last-Modified`）的 `no-cache`。

### 8.6 CDN 使用
- 檢查靜態資源是否由 CDN 提供（透過不同網域或 CDN 專屬標頭判斷）。
- 對於全球受眾，CDN 是確保效能一致性的關鍵。
- 檢查 CDN 特定標頭：`CF-Ray` (Cloudflare), `X-Cache` (AWS CloudFront), `X-Served-By` (Fastly)。

**分類評分：**
| 檢查項目 | 分數 |
|---|---|
| TTFB < 800ms | 3 |
| 頁面總重量 < 2MB | 2 |
| 圖片已最佳化 (格式、尺寸、延遲載入) | 3 |
| JS 套件大小合理 (壓縮後 < 200KB) | 2 |
| 已啟用壓縮 (gzip/brotli) | 2 |
| 靜態資源具備快取標頭 | 2 |
| 已使用 CDN | 1 |

---

## IndexNow 協定

### 這是什麼
IndexNow 是一個開放協定，允許網站在內容建立、更新或刪除時立即通知搜尋引擎。Bing、Yandex、Seznam 與 Naver 皆支援此協定。Google 目前不支援，但會監測此協定。

### 為何對 GEO 重要
ChatGPT 使用 Bing 的索引。Bing Copilot 亦然。更快的 Bing 索引代表在兩個主要平台上的 AI 能見度也會更新得更快。

### 實作檢查
1. 檢查 IndexNow 金鑰檔案：`https://[domain]/.well-known/indexnow-key.txt` 或類似位置。
2. 檢查 CMS 是否安裝 IndexNow 外掛（例如 WordPress 的 IndexNow 外掛；許多現代 CMS 已原生支援）。
3. 若未實作，建議加入並提供指示。

---

## 整體評分摘要

| 分類 | 最高分 | 權重意義 |
|---|---|---|
| 可爬取性 (Crawlability) | 15 | 核心基礎 |
| 可索引性 (Indexability) | 12 | 核心基礎 |
| 安全性 (Security) | 10 | 信任訊號 |
| URL 結構 | 8 | 爬取效率 |
| 行動裝置最佳化 | 10 | Google 必要條件 |
| 網站核心指標 (CWV) | 15 | 排名訊號 |
| 伺服器端渲染 (SSR) | 15 | GEO 關鍵需求 |
| 網頁速度與伺服器效能 | 15 | 效能表現 |
| **總分** | **100** | |

### 分數解讀
- **90-100**：卓越 (Excellent) — 傳統 SEO 與 GEO 的技術基礎均非常健全。
- **70-89**：良好 (Good) — 雖然有小問題需處理，但基礎穩固。
- **50-69**：需改進 (Needs Work) — 明顯的技術債正影響能見度。
- **30-49**：差 (Poor) — 重大問題阻礙了爬取、索引或 AI 能見度。
- **0-29**：關鍵 (Critical) — 根本性的技術失效，需要立即處理。

---

## 輸出格式

產生 **GEO-TECHNICAL-AUDIT.md**，內容包含：

```markdown
# GEO 技術 SEO 稽核報告 — [網域]
日期：[日期]

## 技術分數：XX/100

## 分數細項
| 分類 | 分數 | 狀態 |
|---|---|---|
| 可爬取性 | XX/15 | 通過/警告/失敗 |
| 可索引性 | XX/12 | 通過/警告/失敗 |
| 安全性 | XX/10 | 通過/警告/失敗 |
| URL 結構 | XX/8 | 通過/警告/失敗 |
| 行動裝置最佳化 | XX/10 | 通過/警告/失敗 |
| 網站核心指標 | XX/15 | 通過/警告/失敗 |
| 伺服器端渲染 (SSR) | XX/15 | 通過/警告/失敗 |
| 網頁速度與伺服器效能 | XX/15 | 通過/警告/失敗 |

狀態定義：通過 = 取得該分類 80% 以上分數，警告 = 50-79%，失敗 = < 50%

## AI 爬蟲存取狀態
| 爬蟲 (Crawler) | User-Agent | 狀態 | 建議 |
|---|---|---|---|
| GPTBot | GPTBot | 允許/封鎖 | [行動建議] |
| Googlebot | Googlebot | 允許/封鎖 | [行動建議] |
[針對所有 AI 爬蟲繼續列出]

## 關鍵問題 (Critical Issues - 需立即修復)
[列出具體頁面 URL 及其問題]

## 警告項目 (Warnings - 建議本月修復)
[列出詳細資訊]

## 最佳化建議 (Recommendations - 建議本季最佳化)
[列出詳細資訊]

## 詳細調查結果
[依分類列出證據與細節]
```
