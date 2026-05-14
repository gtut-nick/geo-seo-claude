# Agent-Readiness Checks：測試結果

針對 Content Signals 檢查測試了 2 個 URL。所有 HTTP 請求都透過 Playwright `page.request`（原生 Node.js context，不是 browser fetch）發出，以擷取真實 response headers。

## 測試網站

| Site | Check | Result | Notes |
|---|---|---|---|
| contentsignals.org | Content Signals | Pass | 存在 `Content-Signal:` 指令，含 3 組 key=value 配對 |
| tradewater.co | Content Signals | Recommendation | 沒有 `Content-Signal:` 指令；標準 WordPress robots.txt |

---

## 詳細發現

### 內容訊號

**contentsignals.org/robots.txt**

找到完整指令：
```
Content-Signal: ai-train=yes, search=yes, ai-input=yes
```

解析後的值：
| Signal Key | Value | Meaning | Valid per spec? |
|---|---|---|---|
| ai-train | yes | 允許用於 AI model training | Yes |
| search | yes | 允許用於 AI-powered search results | Yes |
| ai-input | yes | 允許作為 AI input 使用 | Warning — `ai-input` 不在已知 key set（`ai-train`、`search`、`ai-personalization`、`ai-retrieval`）中 |

結果：**Pass with warning** — 指令存在且大多有效。`ai-input` 是未知 key；規格仍是 IETF 草案，因此未知 key 應被標記為 warnings，但不應視為 errors。

**tradewater.co/robots.txt**

未找到 `Content-Signal:` 指令。標準 WordPress 設定會封鎖 admin paths、WooCommerce logs 與 REST API endpoints。存在 `Crawl-delay: 10`。有引用 sitemap。

結果：**Recommendation** — 加入 `Content-Signal:` 以宣告 AI 使用偏好。

---

## 驗證備註

**contentsignals.org 上的 `ai-input` key。** 規格作者自己的網站使用 `ai-input=yes`，而這不在規格中定義的已知 key set（`ai-train`、`search`、`ai-personalization`、`ai-retrieval`）內。這是真實世界訊號，顯示 IETF 草案仍在演進。實作正確地將未知 key 標記為 warnings，而不是讓檢查失敗。

**WebFetch 無法擷取 HTTP response headers。** WebFetch 只會回傳 rendered body content。所有 header-level tests 都需要 Playwright `page.request`（原生 Node context）。這與 aeo-scan skill 有關，任何在 production tools 中實作這些檢查的方式都應使用 Playwright 或 direct HTTP requests，而不是 WebFetch。
