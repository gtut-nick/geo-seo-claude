---
name: geo-brand-mentions
description: 用於 AI 能見度的品牌提及與權威掃描器。分析品牌在 AI 模型用於實體識別與引用判斷的平台上的存在感。產出品牌權威分數 Brand Authority Score（0-100），並提供各平台專屬建議。
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# 品牌提及掃描技能

## 核心洞察

品牌提及與 AI 能見度的相關性，大約比傳統反向連結（Backlinks）高出 3 倍。Ahrefs 於 2025 年 12 月發布的一項研究分析了 75,000 個品牌在 AI 搜尋平台上的表現，發現 **未連結的品牌提及（Unlinked Brand Mentions）** —— 也就是沒有超連結的品牌名稱引用 —— 比網域評級（Domain Rating, DR）或反向連結數量更能預測 AI 系統是否會引用並推薦某個品牌。

關鍵發現是：**提及出現在哪個平台至關重要。** 並非所有提及的價值都相等。YouTube 或 Reddit 上的一次提及，對 AI 引用的權重可能遠高於低權威部落格上的提及，因為 AI 訓練資料與檢索系統會不成比例地索引高互動平台。

這顛覆了傳統 SEO 的核心假設。在傳統 SEO 中，來自高 DR 網站的反向連結是黃金標準。在 GEO（生成式引擎最佳化）中，Reddit 上未連結的一次提及，或 YouTube 影片描述中的一次提及，可能比 DR 70 部落格的 dofollow 反向連結更有價值。

---

## AI 引用的平台重要性排名

根據 Ahrefs 2025 年 12 月的研究，以及 Profound (2025) 與 Terakeet (2025) 的佐證研究：

### 1. YouTube 提及 —— 相關性約 0.737（最強）

**YouTube 為何最重要：**
- YouTube 是全球第二大搜尋引擎，也是最大的影片平台（每月使用者超過 25 億）。
- AI 訓練資料集大量納入 YouTube 逐字稿、描述與中繼資料。
- Google 的 Gemini 與 AI Overviews 會直接參考 YouTube 內容。
- Perplexity 與 ChatGPT 都會索引並引用 YouTube 影片內容。
- YouTube 逐字稿特別有價值，因為它們包含自然語言對話脈絡中的提及，這與 AI 模型處理與生成文字的方式一致。

**要檢查什麼：**
- **品牌 YouTube 頻道：** 品牌是否有活躍的 YouTube 頻道？訂閱者多少？影片數量？上傳頻率？
- **第三方影片提及：** 其他 YouTuber 或頻道是否提及該品牌？脈絡是什麼（評論、教學、比較）？
- **影片描述：** 品牌名稱是否出現在產業相關內容的影片描述中？
- **影片逐字稿：** 品牌是否在相關影片的口述內容中被提及？（AI 模型會索引逐字稿）
- **YouTube 搜尋存在感：** 在 YouTube 搜尋「[品牌名稱]」時是否出現結果？結果是否正面？
- **留言提及：** 品牌是否在相關產業影片的留言中被提及？

**YouTube 評分（0-100）：**

| 分數 | 標準 |
|---|---|
| 90-100 | 活躍頻道且有 10K+ 訂閱者、定期上傳、品牌在 20+ 支第三方影片被提及、會出現在產業詞的 YouTube 搜尋結果中 |
| 70-89 | 活躍頻道且有 1K+ 訂閱者、品牌在 10-19 支第三方影片被提及、有部分 YouTube 搜尋存在感 |
| 50-69 | 有頻道且有部分內容、品牌在 5-9 支第三方影片被提及、YouTube 搜尋存在感有限 |
| 30-49 | 有頻道但不活躍、品牌在 1-4 支第三方影片被提及 |
| 10-29 | 沒有頻道或空頻道，品牌僅在 1-2 支影片被提及 |
| 0-9 | 完全沒有 YouTube 存在感 |

---

### 2. Reddit 提及 —— 高相關性

**Reddit 為何重要：**
- Reddit 是 AI 訓練資料中最常被索引的平台之一（Google 於 2024 年每年 6,000 萬美元的 Reddit 授權協議已證實此點）。
- AI 系統在產品推薦、比較與使用者情緒上高度重視 Reddit。
- 估計有 10-15% 的 Google 搜尋會被使用者加上「Reddit」字眼，以尋找真實意見。
- Perplexity 經常引用 Reddit 討論串作為來源。
- ChatGPT 與 Claude 在回答產品/服務問題時都會參考 Reddit 討論。

**要檢查什麼：**
- **Subreddit 存在感：** 品牌是否在相關 subreddit 中被討論？哪些 subreddit？
- **提及量：** 有多少 Reddit 討論串提及該品牌？趨勢如何（增加/減少）？
- **情緒：** 提及多為正面、負面或中立？常見讚賞點與抱怨是什麼？
- **官方存在感：** 品牌是否有官方 Reddit 帳號？是否參與討論？是否辦過 AMA（問我任何事）？
- **推薦討論串：** 品牌是否出現在「你會推薦什麼 X？」這類討論串中？它是首選推薦還是陪榜選項？
- **Subreddit 社群：** 品牌是否有自己的 subreddit？活躍程度如何？

**Reddit 評分（0-100）：**

| 分數 | 標準 |
|---|---|
| 90-100 | 在相關 subreddit 中經常被推薦、情緒以正面為主、有活躍官方存在感、自有 subreddit 且有 5K+ 成員、在產業查詢的主要推薦中出現 |
| 70-89 | 在相關 subreddit 中定期被提及、情緒多為正面、有部分官方存在感、出現在多個推薦討論串 |
| 50-69 | 在數個相關討論串中被提及、情緒混合、品牌名稱被社群成員辨識 |
| 30-49 | 偶爾被提及、限於 1-2 個 subreddit、沒有官方存在感 |
| 10-29 | 很少被提及，品牌在 Reddit 上大體上不具知名度 |
| 0-9 | 沒有 Reddit 存在感 |

---

### 3. Wikipedia 存在感 —— 高相關性

**Wikipedia 為何重要：**
- Wikipedia 是 AI 訓練資料中權威性最高的來源之一。所有主要 AI 模型都曾以 Wikipedia dump 進行訓練。
- AI 系統將 Wikipedia 作為實體識別（Entity Recognition）的主要來源，用來判斷品牌是否是值得被記錄的「真實」實體。
- Wikidata（Wikipedia 的結構化資料姊妹專案）提供機器可讀的事實，AI 模型會用於知識圖譜建構。
- 擁有 Wikipedia 頁面是知名度的強訊號，這與 AI 系統是否將品牌視為權威實體直接相關。

**要檢查什麼：**
- **Wikipedia 頁面：** 品牌或公司是否有自己的 Wikipedia 條目？是否被標記為刪除或品質問題？
- **創辦人頁面：** 創辦人/CEO 是否有 Wikipedia 頁面？（強權威訊號）
- **Wikipedia 引用：** 品牌網站是否在任何 Wikipedia 條目中被列為參考資料？
- **Wikidata 項目：** 品牌是否有 Wikidata 項目（Q-number）？完整度如何？
- **Wikipedia 提及：** 品牌是否在其他 Wikipedia 條目中被提及（產業條目、競品頁、分類頁）？
- **條目品質：** 如果存在 Wikipedia 頁面，它是小作品（stub）、初級（start-class），還是更高品質？

**Wikipedia 評分（0-100）：**

| 分數 | 標準 |
|---|---|
| 90-100 | 詳細 Wikipedia 條目（B-class 或更高）、Wikidata 項目屬性完整、品牌在多個條目中作為參考資料被引用、創辦人有 Wikipedia 頁面 |
| 70-89 | 有 Wikipedia 條目（初級或更高）、有 Wikidata 項目、品牌在 2+ 個其他 Wikipedia 條目中被提及 |
| 50-69 | 有 Wikipedia 條目（小作品或初級）、基本 Wikidata 項目、在其他條目中提及有限 |
| 30-49 | 沒有 Wikipedia 條目，但品牌在其他條目中被提及或作為參考資料被引用；可能有 Wikidata 項目 |
| 10-29 | 品牌僅在 1-2 個 Wikipedia 條目中被順帶提及 |
| 0-9 | 沒有任何 Wikipedia 或 Wikidata 存在感 |

---

### 4. LinkedIn 存在感 —— 中度相關性

**LinkedIn 為何重要：**
- LinkedIn 內容正越來越多地被 AI 系統索引用於專業與 B2B 脈絡。
- 公司 LinkedIn 頁面與員工的思想領導（Thought Leadership）內容會建立品牌實體訊號。
- AI 模型會參考 LinkedIn 取得公司資訊、團隊資歷與專業權威。
- LinkedIn 文章與貼文會被搜尋引擎與 AI 爬蟲索引。

**要檢查什麼：**
- **公司頁面：** 品牌是否有 LinkedIn 公司頁面？追蹤者數？發文頻率？
- **員工思想領導：** 員工（尤其是領導層）是否發布提及品牌的思想領導內容？
- **公司提及：** 品牌是否被非員工、產業分析師或客戶在 LinkedIn 貼文中提及？
- **LinkedIn 文章：** 是否有關於或提及品牌的長篇 LinkedIn 文章？
- **員工個人檔案：** 員工是否列出公司並提供詳細描述？是否具備強大的專業檔案？
- **互動指標：** 公司貼文的一般互動（按讚、留言、分享）狀況如何？

**LinkedIn 評分（0-100）：**

| 分數 | 標準 |
|---|---|
| 90-100 | 活躍公司頁面且有 10K+ 追蹤者、領導層定期發布思想領導內容、品牌經常被產業專業人士提及、員工檔案完整強健 |
| 70-89 | 活躍公司頁面且有 5K+ 追蹤者、有部分員工思想領導內容、偶爾有第三方提及 |
| 50-69 | 有公司頁面且有 1K+ 追蹤者、發文不規律、第三方提及有限 |
| 30-49 | 有公司頁面但內容稀疏或不活躍、追蹤者少、沒有第三方提及 |
| 10-29 | 基本公司頁面，資訊很少 |
| 0-9 | 沒有 LinkedIn 公司頁面 |

---

### 5. 其他平台存在感 —— 補充訊號

這些平台與 AI 能見度的相關性較低，但仍具備意義：

#### Quora
- **相關性：** Quora 回答經常包含在 AI 訓練資料中，也會被 Perplexity 引用。
- **要檢查什麼：** 品牌是否在產業相關問題的 Quora 回答中被提及？品牌是否有官方 Quora 存在感？
- **訊號強度：** 對 B2C 為中等，對 B2B 較低。

#### Stack Overflow / Stack Exchange
- **相關性：** 對面向開發者的品牌（SaaS、開發工具、API）至關重要。
- **要檢查什麼：** 品牌產品是否在 Stack Overflow 問答中被討論？品牌是否有專屬標籤（Tag）？是否有官方帳號回答問題？
- **訊號強度：** 對技術產品高，對多數 B2C 無關。

#### GitHub
- **相關性：** 對開源與開發者導向品牌至關重要。
- **要檢查什麼：** 品牌是否有 GitHub 組織（Organization）？存放庫（Repository）的星數（Stars）？是否在其他 Repo 的文件或討論中被提及？
- **訊號強度：** 對開發工具與開源項目高，對非技術品牌低。

#### 產業論壇與社群
- **相關性：** AI 模型會從特定領域訓練資料中捕捉到利基權威（Niche Authority）訊號。
- **要檢查什麼：** 品牌是否在產業特定論壇被討論（例如科技領域的 Hacker News、新創領域的 ProductHunt、產業特定 Slack 社群）？
- **訊號強度：** 中等，但有助於建立利基權威。

#### 新聞與媒體
- **相關性：** 新聞提及會建立實體權威與新近性（Recency）訊號。
- **要檢查什麼：** 品牌是否被主流新聞媒體或產業出版物報導？多近期？脈絡是什麼？
- **訊號強度：** 中等。新近性很重要 —— 過去 6 個月內的提及，遠比 3 年前的一次提及更有價值。

#### Podcasts
- **相關性：** 正在成長的 AI 訓練資料來源。逐字稿越來越常被索引。
- **要檢查什麼：** 品牌或其領導層是否上過 Podcast？提及品牌的 Podcast 逐字稿是否被搜尋引擎索引？
- **訊號強度：** 中等且持續成長。

---

## 綜合品牌權威分數 (Brand Authority Score)

### 評分公式

| 平台 | 權重 | 理由 |
|---|---|---|
| YouTube 存在感 | 25% | 與 AI 引用的相關性最強（0.737） |
| Reddit 存在感 | 25% | 第二強相關性；對產品推薦至關重要 |
| Wikipedia / Wikidata | 20% | 實體識別基礎；AI 訓練資料基石 |
| LinkedIn 權威性 | 15% | 專業權威訊號；B2B 相關性 |
| 其他平台 | 15% | 來自 Quora、GitHub、新聞、論壇、Podcast 的補充訊號 |

**公式：**
```
Brand_Authority_Score = (YouTube * 0.25) + (Reddit * 0.25) + (Wikipedia * 0.20) + (LinkedIn * 0.15) + (Other * 0.15)
```

### 分數解讀

| 分數範圍 | 評級 | 解讀 |
|---|---|---|
| 85-100 | Dominant (主導) | 品牌在 AI 平台上是被充分識別的實體。極有可能被 AI 系統引用與推薦。 |
| 70-84 | Strong (強勁) | 品牌具備穩固的跨平台存在感。AI 系統可能會針對相關查詢辨識並引用它。 |
| 50-69 | Moderate (中等) | 品牌在部分平台有存在感，但仍有缺口。AI 引用不穩定。 |
| 30-49 | Weak (微弱) | 品牌平台存在感有限。AI 系統可能不會將其辨識為獨立實體。 |
| 0-29 | Minimal (極低) | 品牌平台存在感極低。AI 系統不太可能引用或推薦它。 |

---

## 分析流程

### Step 1: 識別品牌資訊

從使用者或網站蒐集以下資訊：
- **品牌名稱**（精確拼法，包含任何官方變體）
- **創辦人/CEO 姓名**
- **網域 URL**
- **產業/類別**
- **主要產品或服務**（前 3 項）
- **主要競爭對手**（用於比較脈絡）

### Step 2: 平台掃描

對每個平台使用 WebFetch 搜尋並評估存在感：

**YouTube 檢查:**
1. Search: `[brand name] site:youtube.com`
2. Check: `youtube.com/@[brand-name]` 或 `youtube.com/c/[brand-name]` 是否為官方頻道
3. Search: `"[brand name]"` site:youtube.com（精確比對描述中的提及）
4. 記錄：頻道訂閱數、影片數、最新上傳日期、第三方提及數量

**Reddit 檢查:**
1. Search: `[brand name] site:reddit.com`
2. Search: `"[brand name]"` site:reddit.com（精確比對）
3. Check: `reddit.com/r/[brand-name]` 是否為官方 subreddit
4. Check: `reddit.com/user/[brand-name]` 是否為官方帳號
5. 記錄：討論串數量、主要 subreddit、情緒（正面/負面/中立）、推薦頻率

**Wikipedia 檢查（重要 —— 使用兩種方法避免偽陰性）：**

**Method 1 —— Python API check（最可靠，優先執行）：**
```bash
python3 -c "
import requests, json
from urllib.parse import quote_plus
brand = '[Brand_Name]'
# 直接檢查 Wikipedia API
api_url = f'[https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=](https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=){quote_plus(brand)}&format=json'
r = requests.get(api_url, headers={'User-Agent': 'GEO-Audit/1.0'}, timeout=15)
data = r.json()
results = data.get('query', {}).get('search', [])
if results and brand.lower() in results[0].get('title', '').lower():
    print(f'WIKIPEDIA PAGE EXISTS: {results[0][\"title\"]}')
    print(f'URL: [https://en.wikipedia.org/wiki/](https://en.wikipedia.org/wiki/){results[0][\"title\"].replace(\" \", \"_\")}')
else:
    print('No direct Wikipedia page found')
# 檢查 Wikidata
wd_url = f'[https://www.wikidata.org/w/api.php?action=wbsearchentities&search=](https://www.wikidata.org/w/api.php?action=wbsearchentities&search=){quote_plus(brand)}&language=en&format=json'
r2 = requests.get(wd_url, headers={'User-Agent': 'GEO-Audit/1.0'}, timeout=15)
wd = r2.json()
entities = wd.get('search', [])
if entities:
    print(f'WIKIDATA ENTRY: {entities[0].get(\"id\", \"\")} — {entities[0].get(\"description\", \"\")}')
"
```

**Method 2 —— 直接 URL 檢查（備援驗證）：**
1. WebFetch: `https://en.wikipedia.org/wiki/[Brand_Name]` —— 檢查頁面是否載入（而不是重新導向到搜尋結果）
2. WebFetch: `https://en.wikipedia.org/wiki/[Founder_Name]` 檢查創辦人條目

**Method 3 —— 搜尋（最不可靠，僅用於補充資訊）：**
1. Search: `[brand name] site:wikipedia.org`
2. Search: `[brand name] site:wikidata.org`

**關鍵提醒 (CRITICAL)：** 單靠網頁搜尋無法可靠判斷 Wikipedia 存在感。務必先執行 Python API 檢查。如果 API 顯示頁面存在，它就確實存在 —— 不要因為搜尋結果找不到而推翻此結論。

5. 記錄：條目是否存在、品質、編輯歷史、Wikidata 完整度

**LinkedIn 檢查:**
1. Search: `[brand name] site:linkedin.com`
2. Check: `linkedin.com/company/[brand-name]` 是否為公司頁面
3. 記錄：追蹤者數、發文頻率、列出的員工數、互動程度

**其他平台：**
1. Search: `[brand name] site:quora.com`
2. Search: `[brand name] site:stackoverflow.com`（若為技術品牌）
3. Search: `[brand name] site:github.com`（若為技術品牌）
4. Search: `[brand name] site:news.ycombinator.com`（Hacker News）
5. Search: `"[brand name]"` 廣泛搜尋新聞提及（篩選過去 6 個月）
6. 記錄：各平台是否存在，以及提及品質

### Step 3: 情緒評估

針對 Reddit 與其他討論平台，分析最新且最突出的提及來評估情緒：

| 情緒 | 指標 |
|---|---|
| **正面 (Positive)** | 推薦（"我愛 [品牌名]", "我們換成了 [品牌名] 然後...", "強力推薦"）、高票提及、相對於競品的正面比較 |
| **中立 (Neutral)** | 事實性提及（"我們使用 [品牌名] 來做...", "[品牌名] 提供..."）、關於品牌的問題、平衡的比較 |
| **負面 (Negative)** | 抱怨（"避開 [品牌名]", "[品牌名] 的支援很糟"）、被負評 (downvote) 的推薦、負面比較 |
| **混合 (Mixed)** | 正面與負面混合。記錄比例與主要主題。 |

### Step 4: 競爭比較（選用）

如果已識別競爭對手，快速掃描他們的平台存在感作為脈絡。這有助於校正分數 —— 如果某品牌在 Reddit 的存在感屬「中等」，但同產業競品幾乎沒有 Reddit 存在感，則相對而言仍然很強。

### Step 5: 分數計算

1. 使用上方量表為每個平台評分（0-100）。
2. 套用權重計算綜合品牌權威分數 (Brand Authority Score)。
3. 識別最強與最弱的平台。
4. 針對最弱的平台產生具體、可執行的建議。

---

## 輸出格式

產生名為 `GEO-BRAND-MENTIONS.md` 的檔案：

```markdown
# 品牌權威報告：[Brand Name]

**分析日期 (Analysis Date):** [Date]
**品牌 (Brand):** [Brand Name]
**網域 (Domain):** [URL]
**產業 (Industry):** [Industry]

---

## 品牌權威分數：[X]/100（[Rating]）

### 平台細項

| 平台 | 分數 | 權重 | 加權得分 | 狀態 |
|---|---|---|---|---|
| YouTube | [X]/100 | 25% | [X] | [活躍頻道 / 有提及 / 缺席] |
| Reddit | [X]/100 | 25% | [X] | [活躍 / 有討論 / 缺席] |
| Wikipedia | [X]/100 | 20% | [X] | [條目 / 有提及 / 缺席] |
| LinkedIn | [X]/100 | 15% | [X] | [活躍 / 基本 / 缺席] |
| 其他平台 | [X]/100 | 15% | [X] | [摘要] |
| **總計** | | | **[X]/100** | |

---

## 平台詳細資料

### YouTube ([X]/100)

**官方頻道:** [是/否] | [若存在則提供網址]
**訂閱者:** [數量或不適用]
**影片數:** [數量或不適用]
**最後上傳:** [日期或不適用]
**第三方提及:** [估計數量]
**關鍵發現:**
- [發現 1]
- [發現 2]

### Reddit ([X]/100)

**官方帳號:** [是/否] | [若存在則提供網址]
**自有 Subreddit:** [是/否] | [若存在則提供網址與成員數]
**提及量:** [估計討論串數量]
**主要 Subreddits:** [討論品牌的主要 subreddit 列表]
**情緒:** [正面/負面/中立/混合]
**關鍵發現:**
- [發現 1]
- [發現 2]

### Wikipedia ([X]/100)

**公司條目:** [是/否] | [若存在則提供網址]
**創辦人條目:** [是/否] | [若存在則提供網址]
**Wikidata 項目:** [是/否] | [若存在則提供 Q 編號]
**在其他條目被引用:** [是/否] | [哪些條目]
**關鍵發現:**
- [發現 1]
- [發現 2]

### LinkedIn ([X]/100)

**公司頁面:** [是/否] | [若存在則提供網址]
**追蹤者:** [數量或不適用]
**發文頻率:** [每週/每月/罕見/從不]
**關鍵發現:**
- [發現 1]
- [發現 2]

### 其他平台 ([X]/100)

| 平台 | 存在感 | 備註 |
|---|---|---|
| Quora | [是/否] | [簡短說明] |
| Stack Overflow | [是/否] | [簡短說明] |
| GitHub | [是/否] | [簡短說明] |
| Hacker News | [是/否] | [簡短說明] |
| 新聞/媒體 | [是/否] | [簡短說明] |
| Podcasts | [是/否] | [簡短說明] |

---

## 建議

### 立即行動 (第 1-2 週)

1. **[平台]:** [具體行動與預期影響]
2. **[平台]:** [具體行動]

### 短期策略 (第 1-3 個月)

1. **[平台]:** [策略與戰術]
2. **[平台]:** [策略與戰術]

### 長期權威建立 (第 3-12 個月)

1. **[平台]:** [長期策略]
2. **[平台]:** [長期策略]

---

## 競爭脈絡

[若有分析競爭對手，顯示簡要比較表]

| 品牌 | YouTube | Reddit | Wikipedia | LinkedIn | 其他 | 總分 |
|---|---|---|---|---|---|---|
| [受評品牌] | [X] | [X] | [X] | [X] | [X] | **[X]** |
| [競爭對手 1] | [X] | [X] | [X] | [X] | [X] | **[X]** |
| [競爭對手 2] | [X] | [X] | [X] | [X] | [X] | **[X]** |

## 關鍵結論

[1-2 句話總結品牌的 AI 能見度現狀，以及單一最具影響力的行動建議]
```

---

## 參考資料

### 相關強度（Ahrefs 2025 年 12 月，針對 75K 個品牌）

| 訊號 | 與 AI 引用的相關性 | 傳統 SEO 價值 |
|---|---|---|
| YouTube 提及 | ~0.737 | 低（非排名因素） |
| Reddit 提及 | 高（未公布精確係數） | 低 |
| Wikipedia 存在感 | 高 | 中等（信任訊號） |
| LinkedIn 存在感 | 中等 | 低 |
| 網域評級 (DR) | ~0.266 | 極高 |
| 反向連結數量 | ~0.266 | 極高 |
| 自然流量 (Organic traffic) | 中等 | 極高 |

**關鍵洞察：** 對 AI 能見度最重要的訊號（YouTube、Reddit）在傳統 SEO 中幾乎無關，而傳統 SEO 最重要的訊號（反向連結、DR）對 AI 能見度的預測力較弱。這需要一套根本不同的最佳化策略。

### 建立平台存在感的平台專屬提示

**YouTube 快速獲勝法 (Quick Wins):**
- 建立頻道並上傳 3-5 支說明核心主題的解說影片。
- 確保品牌名稱出現在影片標題、描述與口述內容中。
- 爭取登上相關產業 YouTube 頻道擔任來賓。
- 製作比較或「替代方案 (alternatives)」影片（這類影片常被 AI 用於比較查詢的引用）。

**Reddit 快速獲勝法:**
- 找出 3-5 個目標受眾活躍的 subreddit。
- 真誠參與（不要硬性推銷 —— Reddit 社群會偵測並懲罰這種行為）。
- 若適合品牌，舉辦 AMA（問我任何事）。
- 監測並回應品牌提及。
- 建立真正有幫助、自然提及品牌專業領域的貼文。

**Wikipedia 策略:**
- 聘請熟悉 Wikipedia 的顧問 —— 不要自行編輯自己的條目（利益衝突）。
- 先透過媒體報導、學術引用與產業認可建立知名度 (Notability)。
- 即使沒有 Wikipedia 條目，也要確保 Wikidata 項目完整。
- 貢獻產業相關條目，讓品牌能自然地作為來源被引用。

**LinkedIn 快速獲勝法:**
- 使用完整資訊與定期發文最佳化公司頁面。
- 鼓勵領導層每週發布思想領導內容。
- 針對品牌具備獨特專業的主題發布 LinkedIn 文章。
- 參與產業討論，提升品牌在專業脈絡中的能見度。