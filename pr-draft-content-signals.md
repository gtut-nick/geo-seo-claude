# PR：將 Content Signals 檢查加入 geo-crawlers 與 geo-ai-visibility

## 這個 PR 做了什麼

將 **Content Signals** 檢查加入 `geo-crawlers`（新的 Step 6）與 `geo-ai-visibility`（擴充 Step 3）。這兩個技能本來就會抓取 `robots.txt`，因此這項檢查會掃描既有抓取結果中的 `Content-Signal:` 指令，不需要額外 HTTP 請求。

## 原因

這是在稽核 [isitagentready.com](https://isitagentready.com/) 時發現的。該網站是 Cloudflare 用來評估 agent-layer 準備度的工具，並會檢查 Content Signals；但 geo-seo-claude 尚未包含這項檢查。

Content Signals（`draft-romm-aipref-contentsignals`，[contentsignals.org](https://contentsignals.org/)）是一份 IETF 草案，讓網站擁有者能直接在 `robots.txt` 中宣告 AI 使用偏好，並與爬蟲存取規則分開。指令形式如下：

```
Content-Signal: ai-train=no, search=yes, ai-retrieval=yes
```

這會告訴 AI operators 下游能或不能如何使用內容（訓練模型、顯示於搜尋、用於檢索），而既有的 `User-agent`/`Disallow` 指令則控制爬蟲是否能存取內容本身。多數網站目前尚未加入這項指令。

## 變更內容

- **`skills/geo-crawlers/SKILL.md`** — 在 Analysis Procedure 中新增 Step 6：掃描 robots.txt 中的 `Content-Signal:` 指令。解析 key=value 配對，依已知 key（`ai-train`、`search`、`ai-personalization`、`ai-retrieval`）與 value（`yes`/`no`）驗證。未知 key 標記為 warning（草案仍在演進）。在輸出範本中加入 Content Signals 區段。
- **`agents/geo-ai-visibility.md`** — 擴充 Step 3（AI Crawler Access Check），從已抓取的 robots.txt 另外解析 Content Signals。此為非計分旗標，不影響 Crawler Access Score。
- **`specs/agent-readiness-checks.md`** — 此檢查的完整規格（另外兩項 HTTP-level 檢查在另一個 PR 中）。
- **`tests/agent-readiness-test-results.md`** — 覆蓋 2 個網站 Content Signals 的測試結果。

## 評分

這項檢查**不計分**。它只會產生 pass 或 recommendation，不會扣分。該標準仍是 IETF 草案；因缺少它而懲罰網站並不公平。

| 狀態 | 處理方式 |
|---|---|
| 存在且有效 | Pass — 回報解析後的值與白話意義 |
| 存在但有未知 key 或無效 value | Warning — 標出具體問題與修正方式 |
| 不存在 | Recommendation — 說明應加入的內容 |

## 測試結果

| Site | Check | Result | Notes |
|---|---|---|---|
| contentsignals.org | Content Signals | Pass | 存在 `Content-Signal:` 指令，含 3 組 key=value 配對 |
| tradewater.co | Content Signals | Recommendation | 沒有 `Content-Signal:` 指令；標準 WordPress robots.txt |

值得注意的發現：規格作者自己的網站（`contentsignals.org`）使用了一個未知 key（`ai-input=yes`）。這證實草案仍在演進，也表示將未知 key 標記為 warnings（不是 failures）是正確行為。

## 此 PR 中的檔案

- `skills/geo-crawlers/SKILL.md`
- `agents/geo-ai-visibility.md`
- `specs/agent-readiness-checks.md`
- `tests/agent-readiness-test-results.md`
