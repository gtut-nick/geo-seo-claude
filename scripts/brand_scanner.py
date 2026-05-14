#!/usr/bin/env python3
"""
品牌提及掃描器 (Brand Mention Scanner) — 檢查品牌在 AI 引用平台上的存在感。

品牌提及與 AI 可見度的相關性是反向連結 (backlinks) 的 3 倍。
(Ahrefs 2025 年 12 月對 75,000 個品牌的研究)

AI 引用平台的重要性：
1. YouTube 提及 (~0.737 相關性 - 最強)
2. Reddit 提及 (高)
3. Wikipedia 存在感 (高)
4. LinkedIn 存在感 (中)
5. 網域評分/反向連結 (~0.266 - 弱)
"""

import sys
import json
import re
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("錯誤：未安裝必要的套件。請執行：pip install -r requirements.txt")
    sys.exit(1)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def check_youtube_presence(brand_name: str) -> dict:
    """檢查品牌在 YouTube 上的存在感。"""
    result = {
        "platform": "YouTube",
        "correlation": 0.737,
        "weight": "25%",
        "has_channel": False,
        "mentioned_in_videos": False,
        "search_url": f"https://www.youtube.com/results?search_query={quote_plus(brand_name)}",
        "recommendations": [],
    }

    # 注意：在生產環境中會使用實際的 YouTube API
    # 這裡提供了讓 Claude Code 使用 WebFetch 的框架
    result["check_instructions"] = [
        f"在 YouTube 搜尋 '{brand_name}' 並檢查：",
        "1. 該品牌是否有官方 YouTube 頻道？",
        "2. 是否有來自該品牌的影片（教學、示範、思想領導）？",
        "3. 是否有其他創作者製作關於該品牌的影片？",
        "4. 與品牌相關影片的觀看次數是多少？",
        "5. 是否有正面的評論或產品示範？",
    ]

    result["recommendations"] = [
        "如果尚未建立，請建立一個 YouTube 頻道",
        "發布與您的利基市場相關的教育/教學內容",
        "鼓勵客戶製作評論/示範影片",
        "使用品牌名稱最佳化影片標題和描述",
        "加入時間戳記和章節以提高 AI 解析能力",
        "包含逐字稿（YouTube 會自動產生，但需人工檢查準確性）",
    ]

    return result


def check_reddit_presence(brand_name: str) -> dict:
    """檢查品牌在 Reddit 上的存在感。"""
    result = {
        "platform": "Reddit",
        "correlation": "高",
        "weight": "25%",
        "has_subreddit": False,
        "mentioned_in_discussions": False,
        "search_url": f"https://www.reddit.com/search/?q={quote_plus(brand_name)}",
        "recommendations": [],
    }

    result["check_instructions"] = [
        f"在 Reddit 搜尋 '{brand_name}' 並檢查：",
        "1. 該品牌是否有自己的 subreddit (r/brandname)？",
        "2. 該品牌是否在相關產業的 subreddit 中被討論？",
        "3. 討論的情感傾向為何（正面、負面、中立）？",
        "4. 是否有推薦文章提及該品牌？",
        "5. 該品牌是否有官方的 Reddit 帳號？",
        "6. 提及是否為近期發生（過去 6 個月內）？",
    ]

    result["recommendations"] = [
        "監控相關 subreddit 中的品牌提及",
        "真誠地參與產業討論（切勿發送垃圾訊息）",
        "建立官方 Reddit 帳號以提供客戶支援",
        "分享有價值的內容（而不僅僅是自我推銷）",
        "回答有關您的產品/服務類別的問題",
        "Reddit 非常看重真實性 — 請勿使用行銷術語",
    ]

    return result


def check_wikipedia_presence(brand_name: str) -> dict:
    """檢查品牌/實體在 Wikipedia 和 Wikidata 上的存在感。"""
    result = {
        "platform": "Wikipedia",
        "correlation": "高",
        "weight": "20%",
        "has_wikipedia_page": False,
        "has_wikidata_entry": False,
        "cited_in_articles": False,
        "search_url": f"https://zh.wikipedia.org/wiki/Special:Search?search={quote_plus(brand_name)}",
        "wikidata_url": f"https://www.wikidata.org/w/index.php?search={quote_plus(brand_name)}",
        "recommendations": [],
    }

    # 檢查 Wikipedia API
    try:
        api_url = f"https://zh.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(brand_name)}&format=json"
        response = requests.get(api_url, headers=DEFAULT_HEADERS, timeout=15)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            if search_results:
                # 檢查第一個結果是否與品牌相關
                top_title = search_results[0].get("title", "").lower()
                if brand_name.lower() in top_title:
                    result["has_wikipedia_page"] = True
                result["wikipedia_search_results"] = len(search_results)
    except Exception:
        pass

    # 檢查 Wikidata
    try:
        wikidata_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={quote_plus(brand_name)}&language=zh&format=json"
        response = requests.get(wikidata_url, headers=DEFAULT_HEADERS, timeout=15)
        if response.status_code == 200:
            data = response.json()
            entities = data.get("search", [])
            if entities:
                result["has_wikidata_entry"] = True
                result["wikidata_id"] = entities[0].get("id", "")
                result["wikidata_description"] = entities[0].get("description", "")
    except Exception:
        pass

    result["recommendations"] = [
        "如果符合資格，請建立 Wikipedia 條目（需要符合知名度標準）",
        "確保 Wikidata 項目存在並具備完整的結構化資料",
        "在 schema 標記中加入指向 Wikipedia/Wikidata 的 sameAs 連結",
        "在現有的 Wikipedia 條目中被引用為來源",
        "透過新聞報導和獨立評論建立知名度",
        "注意：Wikipedia 有嚴格的知名度指南 — 公關報導有助於建立知名度",
    ]

    return result


def check_linkedin_presence(brand_name: str) -> dict:
    """檢查品牌在 LinkedIn 上的存在感。"""
    result = {
        "platform": "LinkedIn",
        "correlation": "中等",
        "weight": "15%",
        "has_company_page": False,
        "employee_thought_leadership": False,
        "search_url": f"https://www.linkedin.com/search/results/companies/?keywords={quote_plus(brand_name)}",
        "recommendations": [],
    }

    result["check_instructions"] = [
        f"在 LinkedIn 搜尋 '{brand_name}' 並檢查：",
        "1. 公司是否有 LinkedIn 專頁？",
        "2. 有多少追蹤者？",
        "3. 專頁是否活躍並有近期貼文？",
        "4. 員工是否發布思想領導內容？",
        "5. 是否有關於該品牌的 LinkedIn 文章？",
        "6. 貼文是否有互動（按讚、留言、分享）？",
    ]

    result["recommendations"] = [
        "建立/最佳化 LinkedIn 公司專頁",
        "定期發布思想領導內容",
        "鼓勵員工分享公司內容",
        "發布長篇 LinkedIn 文章",
        "參與產業討論並留言互動",
        "將公司 LinkedIn 網址加入 schema 的 sameAs 屬性中",
    ]

    return result


def check_other_platforms(brand_name: str) -> dict:
    """檢查品牌在其他平台上的存在感。"""
    result = {
        "platform": "其他平台",
        "weight": "15%",
        "platforms_checked": {},
        "recommendations": [],
    }

    platforms = {
        "Quora": f"https://www.quora.com/search?q={quote_plus(brand_name)}",
        "Stack Overflow": f"https://stackoverflow.com/search?q={quote_plus(brand_name)}",
        "GitHub": f"https://github.com/search?q={quote_plus(brand_name)}",
        "Crunchbase": f"https://www.crunchbase.com/textsearch?q={quote_plus(brand_name)}",
        "Product Hunt": f"https://www.producthunt.com/search?q={quote_plus(brand_name)}",
        "G2": f"https://www.g2.com/search?utf8=&query={quote_plus(brand_name)}",
        "Trustpilot": f"https://www.trustpilot.com/search?query={quote_plus(brand_name)}",
    }

    result["platforms_checked"] = {
        name: {
            "search_url": url,
            "check_instruction": f"在 {name} 上搜尋 '{brand_name}'",
        }
        for name, url in platforms.items()
    }

    result["recommendations"] = [
        "在與產業相關的平台上維護個人檔案/專頁",
        "在 Quora 和 Stack Overflow 上回答問題",
        "鼓勵客戶在 G2 和 Trustpilot 上留下評論",
        "保持 Crunchbase 個人檔案更新（對 B2B 來說很重要）",
        "在 GitHub 上貢獻開源專案能提升開發者品牌的權威性",
        "在 Product Hunt 上發布可以產生巨大的初期迴響",
    ]

    return result


def generate_brand_report(brand_name: str, domain: str = None) -> dict:
    """產生全面的品牌提及報告。"""
    report = {
        "brand_name": brand_name,
        "domain": domain,
        "analysis_date": "由 GEO-SEO Claude 工具產生",
        "key_insight": "關鍵洞察：品牌提及與 AI 可見度的相關性是反向連結的 3 倍 (Ahrefs 2025 年 12 月對 7.5 萬個品牌的研究)",
        "platforms": {},
        "overall_recommendations": [],
    }

    # 檢查所有平台
    report["platforms"]["youtube"] = check_youtube_presence(brand_name)
    report["platforms"]["reddit"] = check_reddit_presence(brand_name)
    report["platforms"]["wikipedia"] = check_wikipedia_presence(brand_name)
    report["platforms"]["linkedin"] = check_linkedin_presence(brand_name)
    report["platforms"]["other"] = check_other_platforms(brand_name)

    # 整體建議
    report["overall_recommendations"] = [
        "優先事項 1: YouTube — 與 AI 引用的相關性最高 (0.737)。請建立教育內容。",
        "優先事項 2: Reddit — 在產業 subreddit 中建立真實的存在感。切勿使用行銷術語。",
        "優先事項 3: Wikipedia — 透過新聞報導建立知名度，然後建立/改善維基百科條目。",
        "優先事項 4: LinkedIn — 來自創辦人和員工的思想領導內容。",
        "優先事項 5: 評論平台 — G2、Trustpilot、Capterra 等提供社會認同訊號的平台。",
        "跨平台：確保所有平台上的 NAP（名稱、地址、電話）保持一致。",
        "Schema 標記：加入 sameAs 屬性，連結到「所有」平台設定檔。",
        "監控：在所有平台上設定品牌提及通知 (alerts)。",
    ]

    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python brand_scanner.py <品牌名稱> [網域]")
        print("範例: python brand_scanner.py 'Acme Corp' acmecorp.com")
        sys.exit(1)

    brand = sys.argv[1]
    domain = sys.argv[2] if len(sys.argv) > 2 else None

    result = generate_brand_report(brand, domain)
    print(json.dumps(result, indent=2, default=str))
