---
name: geo-report-pdf
description: 使用 ReportLab 從 GEO 稽核資料產生專業 PDF 報告。建立精緻、可直接交付客戶的 PDF，包含分數儀表、長條圖、平台準備度視覺化、顏色編碼表格與優先行動計畫。
version: 1.0.0
author: geo-seo-claude
tags: [geo, pdf, report, client-deliverable, professional]
allowed-tools: [Read, Grep, Glob, Bash, WebFetch, Write]
---

# GEO PDF 報告產生器

## 目的

此技能會從 GEO 稽核資料 (audit data) 產生視覺精緻的專業 PDF 報告。PDF 包含分數儀表 (score gauges)、長條圖、平台準備度視覺化、顏色編碼表格與優先行動計畫 (action plan)，可直接交付客戶。

## 前置條件

- 必須安裝 **ReportLab**：`pip install reportlab`
- PDF 產生指令碼位於：`~/.claude/skills/geo/scripts/generate_pdf_report.py`
- 需先執行完整的 GEO 稽核（使用 `/geo-audit`），以取得報告所需的資料。

## 如何產生 PDF 報告

### Step 1：收集稽核資料 (Audit Data)

完整執行 `/geo-audit` 後，將所有分數、發現事項與建議收集成 JSON 結構。JSON 資料必須遵循此架構 (Schema)：

```json
{
    "url": "https://example.com",
    "brand_name": "範例公司",
    "date": "2026-02-18",
    "geo_score": 65,
    "scores": {
        "ai_citability": 62,
        "brand_authority": 78,
        "content_eeat": 74,
        "technical": 72,
        "schema": 45,
        "platform_optimization": 59
    },
    "platforms": {
        "Google AI Overviews": 68,
        "ChatGPT": 62,
        "Perplexity": 55,
        "Gemini": 60,
        "Bing Copilot": 50
    },
    "executive_summary": "關於稽核發現的 4-6 句摘要...",
    "findings": [
        {
            "severity": "critical",
            "title": "發現事項標題",
            "description": "該發現事項及其影響的描述。"
        }
    ],
    "quick_wins": [
        "行動項目 1",
        "行動項目 2"
    ],
    "medium_term": [
        "行動項目 1",
        "行動項目 2"
    ],
    "strategic": [
        "行動項目 1",
        "行動項目 2"
    ],
    "crawler_access": {
        "GPTBot": {"platform": "ChatGPT", "status": "Allowed", "recommendation": "保持允許"},
        "ClaudeBot": {"platform": "Claude", "status": "Blocked", "recommendation": "解除封鎖以提升能見度"}
    }
}
```

### Step 2：將 JSON 資料寫入暫存檔

將收集到的稽核資料寫入暫存的 JSON 檔案：

```bash
# 將稽核資料寫入暫存檔
cat > /tmp/geo-audit-data.json << 'EOF'
{ ... 稽核 JSON 資料 ... }
EOF
```

### Step 3：產生 PDF

執行 PDF 產生指令碼：

```bash
python3 ~/.claude/skills/geo/scripts/generate_pdf_report.py /tmp/geo-audit-data.json GEO-REPORT-[brand].pdf
```

指令碼會產生專業的 PDF 報告，內容包含：
- **封面頁 (Cover Page)** — 品牌名稱、URL、日期、帶有視覺儀表的整體 GEO 分數。
- **執行摘要 (Executive Summary)** — 關鍵發現與首要建議。
- **分數細項 (Score Breakdown)** — 所有 6 個評分指標的表格與長條圖。
- **AI 平台準備度 (AI Platform Readiness)** — 每個平台的視覺化水平長條圖與分數。
- **AI 爬蟲存取 (AI Crawler Access)** — 顏色編碼表格（綠色=允許、紅色=封鎖）。
- **關鍵發現 (Key Findings)** — 依嚴重程度編碼的發現事項列表（關鍵/高/中/低）。
- **優先行動計畫 (Prioritized Action Plan)** — 快速獲勝 (Quick wins)、中期與策略性倡議。
- **附錄 (Appendix)** — 方法論、資料來源與詞彙表。

### Step 4：回傳 PDF 路徑

產生完成後，告知使用者 PDF 儲存位置與檔案大小。

## 完整工作流範例 (Workflow Example)

使用者執行此技能時，請依下列確切順序進行：

1. **檢查既有稽核資料** — 在目前目錄尋找近期的 GEO 稽核報告：
   - `GEO-CLIENT-REPORT.md`
   - `GEO-AUDIT-REPORT.md`
   - 或任何近期稽核產生的 `GEO-*.md` 檔案。

2. **若沒有稽核資料** — 告知使用者先執行 `/geo-audit <url>`，再回來產生 PDF。

3. **若有稽核資料** — 解析 Markdown 報告並擷取：
   - 整體 GEO 分數。
   - 類別分數（引用性、品牌權威、內容/E-E-A-T、技術、Schema、平台最佳化）。
   - 平台準備度分數（Google AIO、ChatGPT、Perplexity、Gemini、Bing Copilot）。
   - AI 爬蟲存取狀態。
   - 帶有嚴重程度等級的關鍵發現。
   - 快速獲勝、中期與策略性行動項目。
   - 執行摘要。

4. **建立 JSON** — 依上方 JSON 架構組織所有資料。

5. **將 JSON 寫入暫存檔** — 儲存到 `/tmp/geo-audit-data.json`。

6. **執行 PDF 產生器**：
   ```bash
   python3 ~/.claude/skills/geo/scripts/generate_pdf_report.py /tmp/geo-audit-data.json "GEO-REPORT-[品牌名稱].pdf"

```

7. **報告成功訊息** — 告知使用者 PDF 已產生、儲存位置與檔案大小。

## 如果使用者提供 URL

如果使用者執行 `/geo-report-pdf https://example.com` 並提供 URL：
1. 首先執行完整稽核：對該 URL 調用 `geo-audit` 技能。
2. 接著從產生的報告檔案中收集所有稽核資料。
3. 按照上述說明產生 PDF。

## 解析 Markdown 稽核資料

從既有的 GEO Markdown 報告擷取資料時，請尋找以下模式：

- **GEO 分數**：尋找 "GEO Score: XX/100"、"Overall: XX/100" 或 "GEO Readiness Score: XX"。
- **類別分數**：尋找包含 "Component | Score | Weight" 這些欄位的評分表格。
- **平台分數**：尋找包含 "Google AI Overviews"、"ChatGPT"、"Perplexity" 等內容的表格。
- **爬蟲狀態**：尋找 GPTBot、ClaudeBot 等爬蟲的 "Allowed" 或 "Blocked" 狀態表格。
- **發現事項**：尋找 "Key Findings"、"Critical Issues"、"Recommendations" 章節。
- **行動項目**：尋找 "Quick Wins"、"Action Plan"、"Recommendations" 章節。

## 備註

- 若未安裝 ReportLab，請執行：`pip install reportlab`。
- PDF 設計為 US Letter 尺寸（8.5" x 11"）。
- 調色盤：深藍主色 (#1a1a2e)、藍色點綴 (#0f3460)、珊瑚紅強調 (#e94560)、綠色成功色 (#00b894)。
- 每頁皆有頁首線、頁碼、"Confidential" (機密) 浮水印與產生日期。
- 分數儀表使用紅綠燈配色：綠色 (80+)、藍色 (60-79)、黃色 (40-59)、紅色 (40 以下)。