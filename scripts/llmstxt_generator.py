#!/usr/bin/env python3
"""
llms.txt 產生器 — 建立並驗證用於指引 AI 爬蟲的 llms.txt 檔案。

llms.txt 標準是一項新興規範，可協助 AI 爬蟲
了解您的網站架構並找出最重要的內容。

位置：/llms.txt (網域根目錄)
擴展版本：/llms-full.txt (詳細版本)
"""

import sys
import json
import re
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("錯誤：未安裝必要的套件。請執行：pip install -r requirements.txt")
    sys.exit(1)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def validate_llmstxt(url: str) -> dict:
    """檢查 llms.txt 是否存在並驗證其格式。"""
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    llms_url = f"{base_url}/llms.txt"
    llms_full_url = f"{base_url}/llms-full.txt"

    result = {
        "url": llms_url,
        "exists": False,
        "format_valid": False,
        "has_title": False,
        "has_description": False,
        "has_sections": False,
        "has_links": False,
        "section_count": 0,
        "link_count": 0,
        "content": "",
        "issues": [],
        "suggestions": [],
        "full_version": {
            "url": llms_full_url,
            "exists": False,
        },
    }

    # 檢查 llms.txt
    try:
        response = requests.get(llms_url, headers=DEFAULT_HEADERS, timeout=15)
        if response.status_code == 200:
            result["exists"] = True
            result["content"] = response.text
            content = response.text

            # 驗證格式
            lines = content.strip().split("\n")

            # 檢查標題（以 # 開頭）
            if lines and lines[0].startswith("# "):
                result["has_title"] = True
            else:
                result["issues"].append("缺少標題（應該以 '# 網站名稱' 開頭）")

            # 檢查描述（> 區塊引言）
            for line in lines:
                if line.startswith("> "):
                    result["has_description"] = True
                    break
            if not result["has_description"]:
                result["issues"].append("缺少描述（請使用 '> 簡短描述'）")

            # 檢查區塊（## 標題）
            sections = [l for l in lines if l.startswith("## ")]
            result["section_count"] = len(sections)
            result["has_sections"] = len(sections) > 0
            if not result["has_sections"]:
                result["issues"].append("未找到任何區塊（請使用 '## 區塊名稱'）")

            # 檢查連結
            link_pattern = r"- \[.+\]\(.+\)"
            links = re.findall(link_pattern, content)
            result["link_count"] = len(links)
            result["has_links"] = len(links) > 0
            if not result["has_links"]:
                result["issues"].append("未找到頁面連結（請使用 '- [頁面標題](url): 描述'）")

            # 整體格式有效性
            result["format_valid"] = (
                result["has_title"]
                and result["has_description"]
                and result["has_sections"]
                and result["has_links"]
            )

            # 建議
            if result["link_count"] < 5:
                result["suggestions"].append("考慮新增更多關鍵頁面（目標為 10-20 個）")
            if result["section_count"] < 2:
                result["suggestions"].append("新增更多區塊以組織內容類型")
            if "contact" not in content.lower():
                result["suggestions"].append("新增「聯絡方式」(Contact) 區塊，包含電子郵件和位置資訊")
            if "key fact" not in content.lower() and "about" not in content.lower():
                result["suggestions"].append("新增關於您的業務/服務的關鍵事實")

        else:
            result["issues"].append(f"llms.txt 回傳狀態碼 {response.status_code}")
    except Exception as e:
        result["issues"].append(f"取得 llms.txt 時發生錯誤：{str(e)}")

    # 檢查 llms-full.txt
    try:
        response = requests.get(llms_full_url, headers=DEFAULT_HEADERS, timeout=15)
        if response.status_code == 200:
            result["full_version"]["exists"] = True
    except Exception:
        pass

    return result


def generate_llmstxt(url: str, max_pages: int = 30) -> dict:
    """透過爬取網站來產生 llms.txt 檔案。"""
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    result = {
        "generated_llmstxt": "",
        "generated_llmstxt_full": "",
        "pages_analyzed": 0,
        "sections": {},
    }

    # 抓取首頁
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "lxml")
    except Exception as e:
        result["error"] = f"抓取首頁失敗：{str(e)}"
        return result

    # 擷取網站名稱與描述
    title = soup.find("title")
    site_name = title.get_text(strip=True).split("|")[0].split("-")[0].strip() if title else parsed.netloc
    meta_desc = soup.find("meta", attrs={"name": "description"})
    site_description = meta_desc.get("content", "") if meta_desc else f"{site_name} 的官方網站"

    # 發現並分類頁面
    pages = {
        "主要頁面": [],
        "產品與服務": [],
        "資源與部落格": [],
        "公司資訊": [],
        "支援與幫助": [],
    }

    # 爬取內部連結
    seen_urls = set()
    for link in soup.find_all("a", href=True):
        href = urljoin(base_url, link["href"])
        link_text = link.get_text(strip=True)

        if not link_text or len(link_text) < 2:
            continue

        parsed_href = urlparse(href)
        if parsed_href.netloc != parsed.netloc:
            continue
        if href in seen_urls:
            continue
        if any(ext in href for ext in [".pdf", ".jpg", ".png", ".gif", ".css", ".js"]):
            continue
        if "#" in href and href.split("#")[0] in seen_urls:
            continue

        seen_urls.add(href)
        path = parsed_href.path.lower()

        # 分類
        page_entry = {"url": href, "title": link_text}

        if any(kw in path for kw in ["/pricing", "/feature", "/product", "/solution", "/demo"]):
            pages["產品與服務"].append(page_entry)
        elif any(kw in path for kw in ["/blog", "/article", "/resource", "/guide", "/learn", "/docs", "/documentation"]):
            pages["資源與部落格"].append(page_entry)
        elif any(kw in path for kw in ["/about", "/team", "/career", "/contact", "/press", "/partner"]):
            pages["公司資訊"].append(page_entry)
        elif any(kw in path for kw in ["/help", "/support", "/faq", "/status"]):
            pages["支援與幫助"].append(page_entry)
        elif path in ["/", ""] or any(kw in path for kw in ["/home", "/index"]):
            if href != base_url and href != base_url + "/":
                pages["主要頁面"].append(page_entry)
        else:
            pages["主要頁面"].append(page_entry)

        if len(seen_urls) >= max_pages:
            break

    result["pages_analyzed"] = len(seen_urls)

    # 產生 llms.txt（簡潔版）
    llms_lines = [
        f"# {site_name}",
        f"> {site_description}",
        "",
    ]

    for section, section_pages in pages.items():
        if section_pages:
            llms_lines.append(f"## {section}")
            # 簡潔版每個區塊限制最多前 10 個
            for page in section_pages[:10]:
                llms_lines.append(f"- [{page['title']}]({page['url']})")
            llms_lines.append("")

    # 新增聯絡方式區塊佔位符
    llms_lines.extend([
        "## 聯絡方式",
        f"- 網站：{base_url}",
        f"- 電子郵件：contact@{parsed.netloc}",
        "",
    ])

    result["generated_llmstxt"] = "\n".join(llms_lines)

    # 產生 llms-full.txt（包含描述的詳細版）
    full_lines = [
        f"# {site_name}",
        f"> {site_description}",
        "",
    ]

    for section, section_pages in pages.items():
        if section_pages:
            full_lines.append(f"## {section}")
            for page in section_pages:
                # 略過跨來源 URL 以防止透過重新導向鏈發生 SSRF
                if urlparse(page["url"]).netloc != parsed.netloc:
                    full_lines.append(f"- [{page['title']}]({page['url']})")
                    continue

                # 嘗試抓取頁面描述
                try:
                    page_resp = requests.get(page["url"], headers=DEFAULT_HEADERS, timeout=10)
                    page_soup = BeautifulSoup(page_resp.text, "lxml")
                    page_meta = page_soup.find("meta", attrs={"name": "description"})
                    page_desc = page_meta.get("content", "") if page_meta else ""
                    if page_desc:
                        full_lines.append(f"- [{page['title']}]({page['url']}): {page_desc}")
                    else:
                        full_lines.append(f"- [{page['title']}]({page['url']})")
                except Exception:
                    full_lines.append(f"- [{page['title']}]({page['url']})")
            full_lines.append("")

    full_lines.extend([
        "## 聯絡方式",
        f"- 網站：{base_url}",
        f"- 電子郵件：contact@{parsed.netloc}",
        "",
    ])

    result["generated_llmstxt_full"] = "\n".join(full_lines)
    result["sections"] = {k: len(v) for k, v in pages.items()}

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python llmstxt_generator.py <url> [模式]")
        print("模式：validate (預設), generate")
        sys.exit(1)

    target_url = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "validate"

    if mode == "validate":
        data = validate_llmstxt(target_url)
    elif mode == "generate":
        data = generate_llmstxt(target_url)
    else:
        print(f"未知的模式：{mode}。請使用 'validate' 或 'generate'。")
        sys.exit(1)

    print(json.dumps(data, indent=2, default=str, ensure_ascii=False))
