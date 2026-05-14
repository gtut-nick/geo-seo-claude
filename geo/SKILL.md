---
name: geo
description: >
  GEO 優先的 SEO 分析工具。在維持傳統 SEO 基礎的同時，為 AI 驅動的搜尋引擎
  （ChatGPT、Claude、Perplexity、Gemini、Google AI Overviews）最佳化網站。
  執行完整 GEO 稽核、引用性評分、AI 爬蟲分析、llms.txt 產生、品牌提及掃描、
  特定平台最佳化、結構化資料 (Schema)、技術性 SEO、內容品質（E-E-A-T），
  以及可交付客戶的 GEO 報告產生。當使用者提到 "geo"、"seo"、"audit"、
  "AI search"、"AI visibility"、"optimize"、"citability"、"llms.txt"、
  "schema"、"brand mentions"、"GEO report"，或提供任何 URL 要分析時使用。
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
---

# GEO-SEO 分析工具 — Claude Code Skill（2026 年 2 月）

> **理念：** GEO 優先，SEO 輔助。AI 搜尋正在吞食傳統搜尋。
> 這個工具最佳化的是流量正在前往的地方，而不是流量曾經所在的地方。

---

## 快速參考

| 指令                     | 功能說明                                              |
| ------------------------ | ----------------------------------------------------- |
| `/geo audit <url>`       | 使用平行子代理 (subagents) 執行完整 GEO + SEO 稽核    |
| `/geo page <url>`        | 深入單頁 GEO 分析                                     |
| `/geo citability <url>`  | 評估內容的 AI 引用準備度                              |
| `/geo crawlers <url>`    | 檢查 AI 爬蟲存取權限（robots.txt 分析）               |
| `/geo llmstxt <url>`     | 分析或產生 llms.txt 檔案                              |
| `/geo brands <url>`      | 掃描 AI 引用平台上的品牌提及 (brand mentions)         |
| `/geo platforms <url>`   | 針對特定平台最佳化（ChatGPT、Perplexity、Google AIO） |
| `/geo schema <url>`      | 偵測、驗證並產生結構化資料                            |
| `/geo technical <url>`   | 傳統技術性 SEO 稽核                                   |
| `/geo content <url>`     | 內容品質與 E-E-A-T 評估                               |
| `/geo report <url>`      | 產生可交付客戶的 GEO 成果報告                         |
| `/geo report-pdf <url>`  | 產生含圖表與評分的專業 PDF 報告                       |
| `/geo quick <url>`       | 60 秒 GEO 可見度快照                                  |
| `/geo prospect <cmd>`    | 簡易 CRM：管理銷售流程中的潛在客戶                    |
| `/geo proposal <domain>` | 根據稽核數據自動產生客戶提案書                        |
| `/geo compare <domain>`  | 每月差異報告：向客戶展示評分進步狀況                  |
| `/geo update`            | 從上游拉取最新 GEO 技能更新                           |

---

## 市場脈絡（為什麼 GEO 重要）

| 指標                               | 數值                          | 來源                       |
| ---------------------------------- | ----------------------------- | -------------------------- |
| GEO 服務市場規模 (2025)            | 8.5 億 - 8.86 億美元          | Yahoo Finance / Superlines |
| 預測 GEO 市場規模 (2031)           | 73 億美元 (34% CAGR)          | 產業分析師                 |
| AI 轉單會話增長率                  | +527% (2025 年 1-5 月)        | SparkToro                  |
| AI 流量轉換率 vs 自然搜尋          | 高出 4.4 倍                   | 產業數據                   |
| Google AI Overviews 觸及人數       | 每月 15 億用戶，遍布 200 多國 | Google                     |
| ChatGPT 週活躍用戶                 | 9 億以上                      | OpenAI                     |
| Perplexity 月查詢量                | 5 億以上                      | Perplexity                 |
| Gartner 預測：2028 年搜尋流量降幅  | -50%                          | Gartner                    |
| 投入 GEO 的行銷人員比例            | 僅 23%                        | 產業調查                   |
| 品牌提及 vs 反向連結對 AI 的重要性 | 相關性強 3 倍                 | Ahrefs (2025 年 12 月)     |

---

## 協調邏輯

### 完整稽核 (`/geo audit <url>`)

**第一階段：探索 (Discovery) — 循序執行**

1. 抓取首頁 HTML（使用 curl 或 WebFetch）
2. 偵測業務類型（SaaS、在地服務、電子商務、出版商、代理商、其他）
3. 從 sitemap.xml 或內部連結擷取關鍵頁面（最多 50 頁）

**第二階段：平行分析 (Parallel Analysis) — 委派予子代理**
同時啟動以下 5 個子代理：

| 子代理                | 檔案名稱                          | 職責                                             |
| --------------------- | --------------------------------- | ------------------------------------------------ |
| geo-ai-visibility     | `agents/geo-ai-visibility.md`     | GEO 稽核、引用性、AI 爬蟲、llms.txt、品牌提及    |
| geo-platform-analysis | `agents/geo-platform-analysis.md` | 特定平台最佳化 (ChatGPT, Perplexity, Google AIO) |
| geo-technical         | `agents/geo-technical.md`         | 技術性 SEO、核心網頁指標、可爬取性、可索引性     |
| geo-content           | `agents/geo-content.md`           | 內容品質、E-E-A-T、可讀性、AI 內容偵測           |
| geo-schema            | `agents/geo-schema.md`            | 結構化資料偵測、驗證、產生                       |

**第三階段：綜合彙整 (Synthesis) — 循序執行**

1. 收集所有子代理報告
2. 計算綜合 GEO 分數 (0-100)
3. 產生優先行動計畫
4. 輸出可交付客戶的報告

### 評分方法

| 類別               | 權重 | 衡量標準                                                 |
| ------------------ | ---- | -------------------------------------------------------- |
| AI 引用性與可見度  | 25%  | 段落評分、答案區塊品質、AI 爬蟲存取權限                  |
| 品牌權威訊號       | 20%  | Reddit、YouTube、維基百科、LinkedIn 上的提及；實體存在感 |
| 內容品質與 E-E-A-T | 20%  | 專業訊號、原始數據、作者資歷                             |
| 技術基礎           | 15%  | SSR、核心網頁指標、可爬取性、行動裝置友善、安全性        |
| 結構化資料         | 10%  | Schema 完整性、JSON-LD 驗證、複合搜尋結果資格            |
| 平台最佳化         | 10%  | 各平台就緒程度 (Google AIO, ChatGPT, Perplexity)         |

---

## 業務類型偵測

分析首頁模式：

| 類型                   | 偵測訊號                                                   |
| ---------------------- | ---------------------------------------------------------- |
| **SaaS**               | 價格頁、"註冊"、"免費試用"、"/app"、"/dashboard"、API 文件 |
| **在地服務 (Local)**   | 電話號碼、地址、"附近"、Google 地圖嵌入、服務區域          |
| **電子商務**           | 產品頁、購物車、"加入購物車"、價格元素、產品 Schema        |
| **出版商 (Publisher)** | 部落格、文章、作者欄、發布日期、文章 Schema                |
| **代理商 (Agency)**    | 作品集、案例研究、"我們的服務"、客戶標誌、見證             |
| **其他**               | 預設值 — 套用一般性 GEO 最佳實踐                           |

系統會依據偵測到的類型調整建議。例如：在地企業需要 LocalBusiness Schema 與 Google 商家檔案最佳化；SaaS 需要 SoftwareApplication Schema 與比較頁策略；電商則需要產品 Schema 與評論彙整。

---

## 子技能 (Sub-Skills — 14 個專業組件)

| #   | 技能名稱               | 目錄                             | 用途                         |
| --- | ---------------------- | -------------------------------- | ---------------------------- |
| 1   | geo-audit              | `skills/geo-audit/`              | 完整稽核協調與評分           |
| 2   | geo-citability         | `skills/geo-citability/`         | 段落級別的 AI 引用就緒度     |
| 3   | geo-crawlers           | `skills/geo-crawlers/`           | AI 爬蟲存取與 robots.txt     |
| 4   | geo-llmstxt            | `skills/geo-llmstxt/`            | llms.txt 標準分析與產生      |
| 5   | geo-brand-mentions     | `skills/geo-brand-mentions/`     | AI 引用平台上的品牌存在感    |
| 6   | geo-platform-optimizer | `skills/geo-platform-optimizer/` | 特定 AI 搜尋平台最佳化       |
| 7   | geo-schema             | `skills/geo-schema/`             | 用於 AI 可探索性的結構化資料 |
| 8   | geo-technical          | `skills/geo-technical/`          | 技術性 SEO 基礎              |
| 9   | geo-content            | `skills/geo-content/`            | 內容品質與 E-E-A-T           |
| 10  | geo-report             | `skills/geo-report/`             | 產生可交付客戶的成果物       |
| 11  | geo-prospect           | `skills/geo-prospect/`           | 簡易 CRM 潛在客戶與案源管理  |
| 12  | geo-proposal           | `skills/geo-proposal/`           | 根據稽核數據自動產生客戶提案 |
| 13  | geo-compare            | `skills/geo-compare/`            | 每月差異追蹤與進度報告       |
| 14  | geo-update             | `skills/geo-update/`             | 從上游儲存庫拉取最新更新     |

---

## 子代理 (Subagents — 5 個平行作業員)

| 代理名稱              | 檔案路徑                          | 使用技能                                                      |
| --------------------- | --------------------------------- | ------------------------------------------------------------- |
| geo-ai-visibility     | `agents/geo-ai-visibility.md`     | geo-citability, geo-crawlers, geo-llmstxt, geo-brand-mentions |
| geo-platform-analysis | `agents/geo-platform-analysis.md` | geo-platform-optimizer                                        |
| geo-technical         | `agents/geo-technical.md`         | geo-technical                                                 |
| geo-content           | `agents/geo-content.md`           | geo-content                                                   |
| geo-schema            | `agents/geo-schema.md`            | geo-schema                                                    |

---

## 輸出檔案

所有指令都會產生結構化輸出：

| 指令              | 輸出檔案                                                 |
| ----------------- | -------------------------------------------------------- |
| `/geo audit`      | `GEO-AUDIT-REPORT.md`                                    |
| `/geo page`       | `GEO-PAGE-ANALYSIS.md`                                   |
| `/geo citability` | `GEO-CITABILITY-SCORE.md`                                |
| `/geo crawlers`   | `GEO-CRAWLER-ACCESS.md`                                  |
| `/geo llmstxt`    | `llms.txt` (可直接部署)                                  |
| `/geo brands`     | `GEO-BRAND-MENTIONS.md`                                  |
| `/geo platforms`  | `GEO-PLATFORM-OPTIMIZATION.md`                           |
| `/geo schema`     | `GEO-SCHEMA-REPORT.md` + 產生的 JSON-LD                  |
| `/geo technical`  | `GEO-TECHNICAL-AUDIT.md`                                 |
| `/geo content`    | `GEO-CONTENT-ANALYSIS.md`                                |
| `/geo report`     | `GEO-CLIENT-REPORT.md` (簡報就緒)                        |
| `/geo report-pdf` | `GEO-REPORT.pdf` (含圖表的專業 PDF)                      |
| `/geo quick`      | 行內摘要 (不寫入檔案)                                    |
| `/geo prospect`   | 更新 `~/.geo-prospects/prospects.json`                   |
| `/geo proposal`   | `~/.geo-prospects/proposals/<domain>-proposal-<date>.md` |
| `/geo compare`    | `~/.geo-prospects/reports/<domain>-monthly-<YYYY-MM>.md` |

---

## PDF 報告產生

`/geo report-pdf <url>` 指令會產生專業、具品牌感的 PDF 報告：

### 運作方式

1. 先執行完整稽核或個別分析。
2. 將所有評分與發現收集成 JSON 結構。
3. 執行 PDF 產生器：`python3 ~/.claude/skills/geo/scripts/generate_pdf_report.py data.json GEO-REPORT.pdf`

### PDF 包含內容

- **封面頁**：含 GEO 分數儀表板視覺化。
- **評分詳解**：含顏色標記的長條圖。
- **AI 平台就緒度**：橫向長條圖儀表板。
- **爬蟲存取狀態**：含顏色標記 (Allow/Block) 的列表。
- **關鍵發現**：依嚴重程度分類（致命/高/中/低）。
- **優先行動計畫**：快速取勝 (Quick Wins)、中期計畫、策略建議。
- **方法論與術語表**：附錄說明。

### 工作流程

1. 執行 `/geo audit <url>` 收集完整數據。
2. 執行 `/geo report-pdf <url>` 產生 PDF。
3. 工具編譯 JSON 數據並生成 PDF 檔案。
4. 輸出：目前目錄下的 `GEO-REPORT.pdf`。

---

## 品質門檻

- **爬取限制**：每次稽核最多 50 頁（重質不重量）。
- **逾時設定**：單頁抓取最多 30 秒。
- **頻率限制**：請求間隔 1 秒，最多 5 個併發請求。
- **Robots.txt**：始終尊重，始終檢查。
- **重複偵測**：跳過內容相似度超過 80% 的頁面。

---

## 快速入門範例

```bash
# 對網站執行完整 GEO 稽核
/geo audit [https://example.com](https://example.com)

# 檢查 AI 機器人是否能抓取您的網站
/geo crawlers [https://example.com](https://example.com)

# 為特定頁面的 AI 引用性打分
/geo citability [https://example.com/blog/best-article](https://example.com/blog/best-article)

# 為您的網站產生 llms.txt 檔案
/geo llmstxt [https://example.com](https://example.com)

# 獲取 60 秒可見度快照
/geo quick [https://example.com](https://example.com)

# 產生可交付給客戶的報告
/geo report [https://example.com](https://example.com)
```
