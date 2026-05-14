---
name: geo-prospect
description: >
  用於管理 GEO 代理商潛在客戶 (Prospects) 與客戶 (Clients) 的輕量級 CRM。透過完整的銷售漏斗 (Sales Pipeline)
  追蹤線索：線索 (Lead) → 已開發 (Qualified) → 已寄送提案 (Proposal Sent) → 成交 (Won) → 遺失 (Lost)。
  儲存稽核歷史、筆記、交易價值，並產生漏斗摘要。
  當使用者提到 "prospect"、"lead"、"client"、"pipeline"、"crm"、
  "nuovo prospect"、"aggiungi cliente"，或管理 GEO 服務商業面時使用。
version: 1.0.0
tags: [geo, business, crm, prospect, pipeline, sales]
allowed-tools: [Read, Write, Bash, Glob]
---

# GEO 潛在客戶管理器

## 目的

管理 GEO 代理商潛在客戶與客戶的完整銷售生命週期。
所有資料都儲存在 `~/.geo-prospects/prospects.json` 中（跨工作階段持久保存）。

---

## 指令

| 指令 | 功能說明 |
|---------|-------------|
| `/geo prospect new <domain>` | 建立新潛在客戶（互動式提示） |
| `/geo prospect list` | 顯示所有潛在客戶與漏斗狀態 |
| `/geo prospect list <status>` | 依狀態篩選：lead, qualified, proposal, won, lost |
| `/geo prospect show <id-or-domain>` | 顯示完整的潛在客戶詳情與歷史紀錄 |
| `/geo prospect audit <id-or-domain>` | 執行快速 GEO 稽核並存入潛在客戶紀錄 |
| `/geo prospect note <id-or-domain> "<text>"` | 新增帶有時間戳記的互動筆記 |
| `/geo prospect status <id-or-domain> <new-status>` | 在漏斗階段中移動位置 |
| `/geo prospect won <id-or-domain> <monthly-value>` | 標記為成交，並設定合約價值 |
| `/geo prospect lost <id-or-domain> "<reason>"` | 標記為遺失並記錄原因 |
| `/geo prospect pipeline` | 顯示帶有營收預測的視覺化漏斗摘要 |

---

## 資料結構

每個潛在客戶都會儲存為一個 JSON 紀錄：

```json
{
  "id": "PRO-001",
  "company": "Electron Srl",
  "domain": "electron-srl.com",
  "contact_email": "info@electron-srl.com",
  "contact_name": "",
  "industry": "Educational Equipment Manufacturing",
  "country": "Italy",
  "status": "qualified",
  "geo_score": 32,
  "audit_date": "2026-03-12",
  "audit_file": "~/.geo-prospects/audits/electron-srl.com-2026-03-12.md",
  "proposal_file": "~/.geo-prospects/proposals/electron-srl.com-proposal.md",
  "monthly_value": 0,
  "contract_start": null,
  "contract_months": 0,
  "notes": [
    {
      "date": "2026-03-12",
      "text": "Initial GEO quick scan. Score 32/100 - Critical tier. Strong candidate for GEO services."
    }
  ],
  "created_at": "2026-03-12",
  "updated_at": "2026-03-12"
}
```

---

## 協調指示

### `/geo prospect new <domain>`

1. 檢查 `~/.geo-prospects/prospects.json` 是否存在；若不存在，建立空陣列 (Array)。
2. 從網域自動偵測公司名稱（例如 `electron-srl.com` → `Electron Srl`）。
3. 指派下一個順序 ID：`PRO-001`、`PRO-002` 等。
4. 詢問使用者：
   - 聯絡人姓名（選填）
   - 聯絡人電子郵件
   - 預估每月合約價值（選填）
5. 將狀態設為 `lead`。
6. 儲存到 JSON 檔案。
7. 建議下一步："執行 `/geo prospect audit electron-srl.com` 來為此潛在客戶評分。"

### `/geo prospect list`

讀取 `~/.geo-prospects/prospects.json` 並呈現摘要表格：

```
GEO 潛在客戶漏斗 (Pipeline) — 2026 年 3 月
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID       網域 (Domain)            公司名稱 (Company) 狀態 (Status)  分數  價值
───────  ──────────────────────  ────────────────  ──────────  ─────  ──────
PRO-001  electron-srl.com        Electron Srl      Qualified   32/100  €4.5K
PRO-002  acme.com                ACME Corp         Lead        —       —
PRO-003  bigshop.it              BigShop           Won         41/100  €6.0K

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
漏斗統計：1 lead | 1 qualified | 0 proposals | 1 won | 0 lost
已承諾 MRR (每月經常性收入)：€6,000 | 漏斗總價值：€4,500
```

### `/geo prospect audit <id-or-domain>`

1. 執行 `/geo quick <domain>` 以取得 GEO 快照分數。
2. 將分數存入潛在客戶紀錄：`geo_score`、`audit_date`。
3. 將稽核輸出存入 `~/.geo-prospects/audits/<domain>-<date>.md`。
4. 更新潛在客戶紀錄中的 `audit_file` 路徑。
5. 加入自動筆記："執行快速稽核。GEO 分數：XX/100。"
6. 若分數 < 55，建議："分數顯示有強烈的銷售機會。執行 `/geo proposal <domain>` 產生提案。"

### `/geo prospect note <id-or-domain> "<text>"`

1. 依 ID 或網域找到潛在客戶。
2. 附加含有目前 ISO 日期的筆記。
3. 儲存回 JSON。
4. 確認："已將筆記新增至 Electron Srl (PRO-001)。"

### `/geo prospect status <id-or-domain> <status>`

有效狀態：`lead`、`qualified`、`proposal`、`won`、`lost`

1. 更新狀態欄位。
2. 加入自動筆記："狀態已變更為 <status>"。
3. 儲存並確認。

### `/geo prospect pipeline`

以營收為核心的視覺化漏斗摘要：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEO 代理商銷售漏斗 (PIPELINE) 摘要 — 2026 年 3 月
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

階段 (STAGE)     數量 (COUNT)   潛在價值 (VALUE)   筆記 (NOTES)
─────────────  ─────   ───────────────   ─────────────────────
Lead             2      每月 €8,000      新發現
Qualified        1      每月 €4,500      可準備提案
Proposal Sent    1      每月 €6,000      等待簽署
Won              3      每月 €18,500     活躍客戶 (MRR)
Lost             1      —                預算凍結

已承諾 MRR:        €18,500
漏斗價值 (含合格以上): €10,500
總體潛在價值:      每月 €29,000 → 每年 €348,000

後續行動：
→ PRO-003 (acme.com): 寄送提案 — 分數 38/100（強力案例）
→ PRO-007 (shop.it): 追蹤 — 提案已寄出 8 天
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 儲存位置

所有資料都儲存在 `~/.geo-prospects/`：
```
~/.geo-prospects/
├── prospects.json          # 主要 CRM 資料庫
├── audits/                 # 快速稽核快照
│   └── electron-srl.com-2026-03-12.md
└── proposals/              # 產生的提案
    └── electron-srl.com-proposal.md
```

若目錄不存在，請建立：`mkdir -p ~/.geo-prospects/audits ~/.geo-prospects/proposals`

---

## 漏斗階段定義

| 狀態 (Status) | 意義 | 典型的後續行動 |
|--------|---------|---------------------|
| `lead` | 已發現，尚未聯繫 | 執行快速稽核，評估機會 |
| `qualified` | 已完成稽核，確認痛點 | 產生提案 (Proposal) |
| `proposal` | 提案已送出，等待決定 | 追蹤，回答客戶問題 |
| `won` | 已簽署合約，成為活躍客戶 | 執行全面稽核，開始引導上線 (Onboarding) |
| `lost` | 交易失敗結案 | 記錄原因供未來參考 |

---

## 輸出

- 所有指令都會在終端機印出確認訊息與目前的潛在客戶狀態。
- 除非明確儲存稽核或提案，否則不寫入外部檔案。
- JSON 資料庫是唯一的真實資料來源 (Single Source of Truth)。
