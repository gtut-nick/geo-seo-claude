#!/usr/bin/env python3
"""
GEO-SEO PDF 報告產生器
從 GEO 稽核資料中產生專業的、可交付給客戶的 PDF 報告。

用法:
    python generate_pdf_report.py <json_data_file> [output_file.pdf]

JSON 資料檔案應包含如下結構的稽核結果:
{
    "url": "https://example.com",
    "brand_name": "Example Co",
    "date": "2026-02-18",
    "geo_score": 62,
    "scores": { ... },
    "findings": { ... },
    ...
}

或透過 stdin 傳遞 JSON 資料:
    cat audit_data.json | python generate_pdf_report.py - output.pdf
"""

import sys
import json
import os
import platform
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch, mm
    from reportlab.lib.colors import (
        HexColor, black, white, grey, lightgrey, darkgrey,
        Color
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable, KeepTogether, Image as RLImage
    )
    from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line, Wedge
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics import renderPDF

    # 支援繁體中文的必要設定
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping  # 新增：用來綁定字體家族

    # 判斷作業系統，自動抓取內建字體路徑
    system = platform.system()
    if system == 'Windows':
        # Windows 內建：微軟正黑體 (一般 與 粗體)
        sys_font_path = 'C:\\Windows\\Fonts\\msjh.ttc'
        sys_font_bold_path = 'C:\\Windows\\Fonts\\msjhbd.ttc'
    elif system == 'Darwin':
        # macOS 內建：蘋方體 或 黑體
        sys_font_path = '/System/Library/Fonts/PingFang.ttc'
        sys_font_bold_path = '/System/Library/Fonts/PingFang.ttc'
        if not os.path.exists(sys_font_path):
            sys_font_path = '/System/Library/Fonts/STHeiti Light.ttc'
            sys_font_bold_path = '/System/Library/Fonts/STHeiti Medium.ttc'
    else:
        # Linux (通常需要安裝字體)
        sys_font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
        sys_font_bold_path = sys_font_path

    pdfmetrics.registerFont(TTFont('MSung-Light', sys_font_path))
    pdfmetrics.registerFont(TTFont('MSung-Bold', sys_font_bold_path))
except ImportError:
    print("錯誤：未安裝必要的套件。請執行：pip install -r requirements.txt")
    sys.exit(1)

addMapping('MSung-Light', 0, 0, 'MSung-Light')    # Normal
addMapping('MSung-Light', 1, 0, 'MSung-Bold')     # Bold

# ============================================================
# COLOR PALETTE
# ============================================================
PRIMARY = HexColor("#1a1a2e")       # Dark navy
SECONDARY = HexColor("#16213e")     # Slightly lighter navy
ACCENT = HexColor("#0f3460")        # Blue accent
HIGHLIGHT = HexColor("#e94560")     # Red/coral highlight
SUCCESS = HexColor("#00b894")       # Green
WARNING = HexColor("#fdcb6e")       # Yellow/amber
DANGER = HexColor("#d63031")        # Red
INFO = HexColor("#0984e3")          # Blue
LIGHT_BG = HexColor("#f8f9fa")      # Light background
MEDIUM_BG = HexColor("#e9ecef")     # Medium background
TEXT_PRIMARY = HexColor("#2d3436")   # Dark text
TEXT_SECONDARY = HexColor("#636e72") # Grey text
WHITE = white
BLACK = black


def get_score_color(score):
    """根據分數傳回顏色。"""
    if score >= 80:
        return SUCCESS
    elif score >= 60:
        return INFO
    elif score >= 40:
        return WARNING
    else:
        return DANGER


def get_score_label(score):
    """根據分數傳回標籤。"""
    if score >= 85:
        return "極佳"
    elif score >= 70:
        return "良好"
    elif score >= 55:
        return "中等"
    elif score >= 40:
        return "低於平均"
    else:
        return "需要注意"


def create_score_gauge(score, width=120, height=120):
    """建立一個視覺分數表。"""
    d = Drawing(width, height)

    # Background circle
    d.add(Circle(width/2, height/2, 50, fillColor=LIGHT_BG, strokeColor=lightgrey, strokeWidth=2))

    # Score arc (simplified as colored circle)
    color = get_score_color(score)
    d.add(Circle(width/2, height/2, 45, fillColor=color, strokeColor=None))

    # Inner white circle
    d.add(Circle(width/2, height/2, 35, fillColor=WHITE, strokeColor=None))

    # Score text
    d.add(String(width/2, height/2 + 5, str(score),
                 fontSize=24, fontName='MSung-Light',
                 fillColor=TEXT_PRIMARY, textAnchor='middle'))

    # Label
    d.add(String(width/2, height/2 - 12, "/100",
                 fontSize=10, fontName='MSung-Light',
                 fillColor=TEXT_SECONDARY, textAnchor='middle'))

    return d


def create_bar_chart(data, labels, width=400, height=200):
    """建立一個水平柱狀圖來顯示分數。"""
    d = Drawing(width, height)

    chart = VerticalBarChart()
    chart.x = 60
    chart.y = 30
    chart.height = height - 60
    chart.width = width - 80
    chart.data = [data]
    chart.categoryAxis.categoryNames = labels
    chart.categoryAxis.labels.angle = 0
    chart.categoryAxis.labels.fontSize = 8
    chart.categoryAxis.labels.fontName = 'MSung-Light'
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 100
    chart.valueAxis.valueStep = 20
    chart.valueAxis.labels.fontSize = 8
    chart.valueAxis.labels.fontName = 'MSung-Light'

    # Color each bar based on score
    for i, score in enumerate(data):
        chart.bars[0].fillColor = get_score_color(score)

    chart.bars[0].strokeColor = None
    chart.bars[0].strokeWidth = 0

    d.add(chart)
    return d


def create_platform_chart(platforms, width=450, height=180):
    """建立一個顯示平台就緒分數的圖表。"""
    d = Drawing(width, height)

    bar_height = 22
    bar_max_width = 280
    start_y = height - 30
    label_x = 10

    for i, (name, score) in enumerate(platforms.items()):
        y = start_y - (i * (bar_height + 10))

        # Platform name
        d.add(String(label_x, y + 5, name,
                     fontSize=9, fontName='MSung-Light',
                     fillColor=TEXT_PRIMARY, textAnchor='start'))

        # Background bar
        bar_x = 130
        d.add(Rect(bar_x, y, bar_max_width, bar_height,
                    fillColor=LIGHT_BG, strokeColor=None))

        # Score bar
        bar_width = (score / 100) * bar_max_width
        color = get_score_color(score)
        d.add(Rect(bar_x, y, bar_width, bar_height,
                    fillColor=color, strokeColor=None))

        # Score text
        d.add(String(bar_x + bar_max_width + 10, y + 6, f"{score}/100",
                     fontSize=9, fontName='MSung-Light',
                     fillColor=TEXT_PRIMARY, textAnchor='start'))

    return d


def build_styles():
    """建立自訂段落樣式。"""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='ReportTitle',
        fontName='MSung-Light',
        fontSize=28,
        textColor=PRIMARY,
        spaceAfter=6,
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name='ReportSubtitle',
        fontName='MSung-Light',
        fontSize=14,
        textColor=TEXT_SECONDARY,
        spaceAfter=20,
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontName='MSung-Light',
        fontSize=18,
        textColor=PRIMARY,
        spaceBefore=20,
        spaceAfter=10,
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name='SubHeader',
        fontName='MSung-Light',
        fontSize=13,
        textColor=ACCENT,
        spaceBefore=14,
        spaceAfter=6,
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name='BodyText_Custom',
        fontName='MSung-Light',
        fontSize=10,
        textColor=TEXT_PRIMARY,
        spaceBefore=4,
        spaceAfter=4,
        leading=14,
        alignment=TA_JUSTIFY,
    ))

    styles.add(ParagraphStyle(
        name='SmallText',
        fontName='MSung-Light',
        fontSize=8,
        textColor=TEXT_SECONDARY,
        spaceBefore=2,
        spaceAfter=2,
    ))

    styles.add(ParagraphStyle(
        name='ScoreLabel',
        fontName='MSung-Light',
        fontSize=36,
        textColor=PRIMARY,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name='HighlightBox',
        fontName='MSung-Light',
        fontSize=10,
        textColor=TEXT_PRIMARY,
        backColor=LIGHT_BG,
        borderPadding=10,
        spaceBefore=8,
        spaceAfter=8,
        leading=14,
    ))

    styles.add(ParagraphStyle(
        name='CriticalFinding',
        fontName='MSung-Light',
        fontSize=10,
        textColor=DANGER,
        spaceBefore=4,
        spaceAfter=2,
    ))

    styles.add(ParagraphStyle(
        name='Recommendation',
        fontName='MSung-Light',
        fontSize=10,
        textColor=TEXT_PRIMARY,
        leftIndent=15,
        spaceBefore=3,
        spaceAfter=3,
        bulletIndent=5,
        leading=14,
    ))

    styles.add(ParagraphStyle(
        name='Footer',
        fontName='MSung-Light',
        fontSize=8,
        textColor=TEXT_SECONDARY,
        alignment=TA_CENTER,
    ))

    return styles


def header_footer(canvas, doc):
    """為每個頁面新增頁首和頁尾。"""
    canvas.saveState()

    # Header line
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(2)
    canvas.line(50, letter[1] - 40, letter[0] - 50, letter[1] - 40)

    # Header text
    canvas.setFont('MSung-Light', 8)
    canvas.setFillColor(TEXT_SECONDARY)
    canvas.drawString(50, letter[1] - 35, "GEO-SEO 分析報告")

    # Footer
    canvas.setStrokeColor(lightgrey)
    canvas.setLineWidth(0.5)
    canvas.line(50, 40, letter[0] - 50, 40)

    canvas.setFont('MSung-Light', 8)
    canvas.setFillColor(TEXT_SECONDARY)
    canvas.drawString(50, 28, f"產生於 {datetime.now().strftime('%Y年%m月%d日')}")
    canvas.drawRightString(letter[0] - 50, 28, f"第 {doc.page} 頁")
    canvas.drawCentredString(letter[0] / 2, 28, "機密")

    canvas.restoreState()


def make_table_style(header_color=PRIMARY):
    """建立一致的表格樣式。"""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'MSung-Light'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'MSung-Light'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, lightgrey),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ])


def generate_report(data, output_path="GEO-REPORT.pdf"):
    """根據審核資料產生完整的 PDF 報告。"""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=55,
        bottomMargin=55,
        leftMargin=50,
        rightMargin=50,
    )

    styles = build_styles()
    elements = []

    # Extract data with defaults
    url = data.get("url", "https://example.com")
    brand_name = data.get("brand_name", url.replace("https://", "").replace("http://", "").split("/")[0])
    date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    geo_score = data.get("geo_score", 0)

    scores = data.get("scores", {})
    ai_citability = scores.get("ai_citability", 0)
    brand_authority = scores.get("brand_authority", 0)
    content_eeat = scores.get("content_eeat", 0)
    technical = scores.get("technical", 0)
    schema_score = scores.get("schema", 0)
    platform_optimization = scores.get("platform_optimization", 0)

    platforms = data.get("platforms", {
        "Google AI Overviews": 0,
        "ChatGPT": 0,
        "Perplexity": 0,
        "Gemini": 0,
        "Bing Copilot": 0,
    })

    crawlers = data.get("crawlers", [])
    findings = data.get("findings", [])
    quick_wins = data.get("quick_wins", [])
    medium_term = data.get("medium_term", [])
    strategic = data.get("strategic", [])
    executive_summary = data.get("executive_summary", "")
    crawler_access = data.get("crawler_access", {})
    schema_findings = data.get("schema_findings", {})
    content_findings = data.get("content_findings", {})
    technical_findings = data.get("technical_findings", {})
    brand_findings = data.get("brand_findings", {})

    # ============================================================
    # COVER PAGE
    # ============================================================
    elements.append(Spacer(1, 100))

    # Title
    elements.append(Paragraph("GEO 分析報告", styles['ReportTitle']))
    elements.append(Spacer(1, 8))

    # Subtitle
    elements.append(Paragraph(
        f"<b>{brand_name}</b> 的生成式引擎優化 (GEO) 稽核",
        styles['ReportSubtitle']
    ))

    elements.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=20))

    # Key details table
    details_data = [
        ["網站", url],
        ["分析日期", datetime.strptime(date, "%Y-%m-%d").strftime("%Y年%m月%d日") if "-" in date else date],
        ["GEO 分數", f"{geo_score}/100 — {get_score_label(geo_score)}"],
    ]

    details_table = Table(details_data, colWidths=[120, 350])
    details_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'MSung-Light'),
        ('FONTNAME', (1, 0), (1, -1), 'MSung-Light'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), ACCENT),
        ('TEXTCOLOR', (1, 0), (1, -1), TEXT_PRIMARY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, lightgrey),
    ]))
    elements.append(details_table)

    elements.append(Spacer(1, 30))

    # Score gauge
    gauge = create_score_gauge(geo_score, 200, 200)
    elements.append(gauge)

    elements.append(Spacer(1, 20))

    # Score label
    score_color = get_score_color(geo_score)
    elements.append(Paragraph(
        f'<font color="{score_color.hexval()}">{get_score_label(geo_score)}</font>',
        ParagraphStyle('ScoreLabelColored', parent=styles['SectionHeader'],
                       alignment=TA_CENTER, fontSize=20)
    ))

    elements.append(PageBreak())

    # ============================================================
    # EXECUTIVE SUMMARY
    # ============================================================
    elements.append(Paragraph("執行摘要", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))

    if executive_summary:
        elements.append(Paragraph(executive_summary, styles['BodyText_Custom']))
    else:
        elements.append(Paragraph(
            f"本報告呈現對 <b>{brand_name}</b> ({url}) 進行的生成式引擎優化 (GEO) 綜合稽核結果。"
            f"分析評估了該網站對 AI 驅動的搜尋引擎（包括 Google AI Overviews、ChatGPT、Perplexity、Gemini 及 Bing Copilot）的準備情況。"
            f"整體 GEO 準備度分數為 <b>{geo_score}/100</b>，"
            f"使該網站在 <b>{get_score_label(geo_score)}</b> 等級。",
            styles['BodyText_Custom']
        ))

    elements.append(Spacer(1, 16))

    # ============================================================
    # SCORE BREAKDOWN
    # ============================================================
    elements.append(Paragraph("GEO 分數解析", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))

    score_data = [
        ["項目", "分數", "權重", "加權分數"],
        ["AI 引用率與可見度", f"{ai_citability}/100", "25%", f"{round(ai_citability * 0.25, 1)}"],
        ["品牌權威訊號", f"{brand_authority}/100", "20%", f"{round(brand_authority * 0.20, 1)}"],
        ["內容品質與 E-E-A-T", f"{content_eeat}/100", "20%", f"{round(content_eeat * 0.20, 1)}"],
        ["技術基礎", f"{technical}/100", "15%", f"{round(technical * 0.15, 1)}"],
        ["結構化資料", f"{schema_score}/100", "10%", f"{round(schema_score * 0.10, 1)}"],
        ["平台優化", f"{platform_optimization}/100", "10%", f"{round(platform_optimization * 0.10, 1)}"],
        ["整體分數", f"{geo_score}/100", "100%", f"{geo_score}"],
    ]

    score_table = Table(score_data, colWidths=[200, 80, 60, 80])
    style = make_table_style()

    # Bold the last row
    style.add('FONTNAME', (0, -1), (-1, -1), 'MSung-Light')
    style.add('BACKGROUND', (0, -1), (-1, -1), MEDIUM_BG)

    # Color-code score cells
    for i in range(1, len(score_data) - 1):
        score_val = int(score_data[i][1].split("/")[0])
        color = get_score_color(score_val)
        style.add('TEXTCOLOR', (1, i), (1, i), color)

    score_table.setStyle(style)
    elements.append(score_table)

    elements.append(Spacer(1, 16))

    # Score bar chart
    chart_scores = [ai_citability, brand_authority, content_eeat, technical, schema_score, platform_optimization]
    chart_labels = ["引用率", "品牌", "內容", "技術", "結構化", "平台"]
    elements.append(create_bar_chart(chart_scores, chart_labels))

    elements.append(PageBreak())

    # ============================================================
    # AI PLATFORM READINESS
    # ============================================================
    elements.append(Paragraph("AI 平台準備度", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))

    elements.append(Paragraph(
        "這些分數反映了您的內容被各大 AI 搜尋平台引用的可能性。"
        "低於 50 分表示在該平台上存在明顯的引用障礙。",
        styles['BodyText_Custom']
    ))
    elements.append(Spacer(1, 10))

    # Platform chart
    if platforms:
        elements.append(create_platform_chart(platforms))

    elements.append(Spacer(1, 10))

    # Platform table
    platform_table_data = [["AI 平台", "分數", "狀態"]]
    for name, score in platforms.items():
        status = get_score_label(score)
        platform_table_data.append([name, f"{score}/100", status])

    pt = Table(platform_table_data, colWidths=[180, 80, 150])
    pt_style = make_table_style()
    for i in range(1, len(platform_table_data)):
        score_val = int(platform_table_data[i][1].split("/")[0])
        color = get_score_color(score_val)
        pt_style.add('TEXTCOLOR', (1, i), (1, i), color)
    pt.setStyle(pt_style)
    elements.append(pt)

    elements.append(PageBreak())

    # ============================================================
    # AI CRAWLER ACCESS
    # ============================================================
    elements.append(Paragraph("AI 爬蟲存取狀態", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))

    elements.append(Paragraph(
        "阻擋 AI 爬蟲會導致 AI 平台無法引用您的內容。"
        "下表顯示目前哪些 AI 爬蟲可以存取您的網站。",
        styles['BodyText_Custom']
    ))
    elements.append(Spacer(1, 8))

    if crawler_access:
        # Use Paragraph objects for text wrapping in cells
        cell_style = ParagraphStyle(
            'CrawlerCell', fontName='MSung-Light', fontSize=9,
            textColor=TEXT_PRIMARY, leading=12,
        )
        header_cell_style = ParagraphStyle(
            'CrawlerHeaderCell', fontName='MSung-Light', fontSize=9,
            textColor=WHITE, leading=12,
        )
        status_style_allowed = ParagraphStyle(
            'StatusAllowed', fontName='MSung-Light', fontSize=9,
            textColor=SUCCESS, leading=12,
        )
        status_style_blocked = ParagraphStyle(
            'StatusBlocked', fontName='MSung-Light', fontSize=9,
            textColor=DANGER, leading=12,
        )
        status_style_restricted = ParagraphStyle(
            'StatusRestricted', fontName='MSung-Light', fontSize=9,
            textColor=WARNING, leading=12,
        )
        status_style_default = ParagraphStyle(
            'StatusDefault', fontName='MSung-Light', fontSize=9,
            textColor=TEXT_PRIMARY, leading=12,
        )

        crawler_data = [[
            Paragraph("爬蟲", header_cell_style),
            Paragraph("平台", header_cell_style),
            Paragraph("狀態", header_cell_style),
            Paragraph("建議", header_cell_style),
        ]]
        for crawler_name, info in crawler_access.items():
            if isinstance(info, dict):
                status_text = info.get("status", "Unknown")

                # 中文化狀態文字
                display_status = status_text
                status_upper = status_text.upper()
                if "ALLOW" in status_upper:
                    s_style = status_style_allowed
                    display_status = "允許"
                elif "BLOCK" in status_upper:
                    s_style = status_style_blocked
                    display_status = "阻擋"
                elif "RESTRICT" in status_upper:
                    s_style = status_style_restricted
                    display_status = "受限"
                else:
                    s_style = status_style_default

                crawler_data.append([
                    Paragraph(crawler_name, cell_style),
                    Paragraph(info.get("platform", ""), cell_style),
                    Paragraph(display_status, s_style),
                    Paragraph(info.get("recommendation", ""), cell_style),
                ])
            else:
                crawler_data.append([
                    Paragraph(crawler_name, cell_style),
                    Paragraph("", cell_style),
                    Paragraph(str(info), cell_style),
                    Paragraph("", cell_style),
                ])

        # Full page width: letter (612pt) - 50pt margins each side = 512pt
        ct = Table(crawler_data, colWidths=[90, 110, 72, 240])
        ct_style = make_table_style()
        ct_style.add('VALIGN', (0, 0), (-1, -1), 'TOP')

        ct.setStyle(ct_style)
        elements.append(ct)
    else:
        elements.append(Paragraph(
            "<i>執行 /geo crawlers 以在此區塊填入 AI 爬蟲存取資料。</i>",
            styles['BodyText_Custom']
        ))

    elements.append(PageBreak())

    # ============================================================
    # KEY FINDINGS
    # ============================================================
    elements.append(Paragraph("關鍵發現", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))

    if findings:
        for finding in findings:
            severity = finding.get("severity", "info").upper()
            title = finding.get("title", "")
            description = finding.get("description", "")

            if severity == "CRITICAL":
                sev_color = DANGER
            elif severity == "HIGH":
                sev_color = WARNING
            elif severity == "MEDIUM":
                sev_color = INFO
            else:
                sev_color = TEXT_SECONDARY

            elements.append(Paragraph(
                f'<font color="{sev_color.hexval()}">[{severity}]</font> <b>{title}</b>',
                styles['BodyText_Custom']
            ))
            if description:
                elements.append(Paragraph(description, styles['Recommendation']))
            elements.append(Spacer(1, 4))
    else:
        elements.append(Paragraph(
            "<i>執行完整的 /geo 稽核以填入發現結果。</i>",
            styles['BodyText_Custom']
        ))

    elements.append(PageBreak())

    # ============================================================
    # PRIORITIZED ACTION PLAN
    # ============================================================
    elements.append(Paragraph("優先行動計畫", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))

    # Quick Wins
    elements.append(Paragraph("速贏方案（本週）", styles['SubHeader']))
    elements.append(Paragraph(
        "高影響力、低工作量 — 可立即實施。",
        styles['SmallText']
    ))

    if quick_wins:
        for i, action in enumerate(quick_wins, 1):
            if isinstance(action, dict):
                text = f"<b>{i}.</b> {action.get('action', '')} — <i>{action.get('impact', '')}</i>"
            else:
                text = f"<b>{i}.</b> {action}"
            elements.append(Paragraph(text, styles['Recommendation']))
    else:
        default_wins = [
            "在 robots.txt 中允許所有第一線 AI 爬蟲 (GPTBot, ClaudeBot, PerplexityBot)",
            "在所有內容頁面加入發布及最後更新日期",
            "在部落格文章與新聞中加入帶有資歷的作者署名",
            "建立 llms.txt 檔案以引導 AI 系統找到您的關鍵內容",
            "在 Organization 結構化資料中加入 sameAs 屬性，連結所有平台設定檔",
        ]
        for i, action in enumerate(default_wins, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {action}", styles['Recommendation']))

    elements.append(Spacer(1, 12))

    # Medium-Term
    elements.append(Paragraph("中期改善計畫（本月）", styles['SubHeader']))
    elements.append(Paragraph(
        "顯著影響力、中等工作量 — 需要內容或技術上的修改。",
        styles['SmallText']
    ))

    if medium_term:
        for i, action in enumerate(medium_term, 1):
            if isinstance(action, dict):
                text = f"<b>{i}.</b> {action.get('action', '')} — <i>{action.get('impact', '')}</i>"
            else:
                text = f"<b>{i}.</b> {action}"
            elements.append(Paragraph(text, styles['Recommendation']))
    else:
        default_medium = [
            "使用問題導向的標題與直接回答區塊重構前 10 大頁面",
            "實作完整的 Organization + Article + Person 結構化資料標記",
            "優化內容區塊以提升 AI 引用率 (134-167 字的獨立段落)",
            "確保所有公開內容頁面皆使用伺服器端渲染 (SSR)",
            "實作 IndexNow 協定以提升 Bing/Copilot 索引速度",
        ]
        for i, action in enumerate(default_medium, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {action}", styles['Recommendation']))

    elements.append(Spacer(1, 12))

    # Strategic
    elements.append(Paragraph("戰略性倡議（本季）", styles['SubHeader']))
    elements.append(Paragraph(
        "長期競爭優勢 — 需要持續投入。",
        styles['SmallText']
    ))

    if strategic:
        for i, action in enumerate(strategic, 1):
            if isinstance(action, dict):
                text = f"<b>{i}.</b> {action.get('action', '')} — <i>{action.get('impact', '')}</i>"
            else:
                text = f"<b>{i}.</b> {action}"
            elements.append(Paragraph(text, styles['Recommendation']))
    else:
        default_strategic = [
            "透過新聞報導與知名度，建立 Wikipedia/Wikidata 實體存在感",
            "制定相關 Reddit 子版塊的活躍社群參與策略",
            "建立符合 AI 搜尋意圖的 YouTube 內容策略",
            "建立原創研究/數據發布計畫，以獲得獨特的引用率",
            "透過全面的內容叢集 (Content Clusters) 建立主題權威",
        ]
        for i, action in enumerate(default_strategic, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {action}", styles['Recommendation']))

    elements.append(PageBreak())

    # ============================================================
    # METHODOLOGY & GLOSSARY
    # ============================================================
    elements.append(Paragraph("附錄：方法論", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))

    elements.append(Paragraph(
        f"本次 GEO 稽核於 {date} 進行，分析目標為 {url}。"
        "分析評估了該網站的六個維度：AI 引用率與可見度 (25%)、"
        "品牌權威訊號 (20%)、內容品質與 E-E-A-T (20%)、技術基礎 (15%)、"
        "結構化資料 (10%)，以及平台優化 (10%)。",
        styles['BodyText_Custom']
    ))

    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        "<b>評估的平台：</b> Google AI Overviews、ChatGPT 網頁搜尋、Perplexity AI、"
        "Google Gemini、Bing Copilot",
        styles['BodyText_Custom']
    ))

    elements.append(Paragraph(
        "<b>參考標準：</b> Google 搜尋品質評分指南 (2025年12月)、"
        "Schema.org 規範、核心網頁指標 (Core Web Vitals，2026年標準)、"
        "llms.txt 新興標準、RSL 1.0 授權框架",
        styles['BodyText_Custom']
    ))

    elements.append(Spacer(1, 16))

    # Glossary
    elements.append(Paragraph("詞彙表", styles['SubHeader']))

    glossary = [
        ["術語", "定義"],
        ["GEO", "生成式引擎優化 (Generative Engine Optimization) — 為 AI 搜尋引用優化內容"],
        ["AIO", "AI Overviews — Google 搜尋結果中的 AI 生成答案區塊"],
        ["E-E-A-T", "經驗 (Experience)、專業度 (Expertise)、權威性 (Authoritativeness)、可信度 (Trustworthiness)"],
        ["SSR", "伺服器端渲染 (Server-Side Rendering) — 在伺服器上生成 HTML 以供爬蟲讀取"],
        ["CWV", "核心網頁指標 (Core Web Vitals) — Google 的網頁體驗指標 (LCP, INP, CLS)"],
        ["INP", "與下一個畫面的互動 (Interaction to Next Paint) — 響應速度指標 (取代 FID)"],
        ["JSON-LD", "連結資料的 JavaScript 物件表示法 — 首選的結構化資料格式"],
        ["sameAs", "Schema.org 的屬性，用於將實體連結至其在其他平台上的設定檔"],
        ["llms.txt", "擬議的標準檔案，用於引導 AI 系統了解網站內容"],
        ["IndexNow", "可立即通知搜尋引擎內容變更的協定"],
    ]

    gt = Table(glossary, colWidths=[80, 380])
    gt.setStyle(make_table_style())
    elements.append(gt)

    elements.append(Spacer(1, 30))

    # Footer disclaimer
    elements.append(HRFlowable(width="100%", thickness=0.5, color=lightgrey, spaceAfter=8))
    elements.append(Paragraph(
        "本報告由 GEO-SEO 程式碼分析工具產生。"
        "分數與建議基於自動化分析及業界基準。結果應透過特定平台測試進行驗證。",
        styles['SmallText']
    ))

    # ============================================================
    # BUILD PDF
    # ============================================================
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Generate a sample report for demonstration
        sample_data = {
            "url": "https://example.com",
            "brand_name": "Example Company",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "geo_score": 58,
            "scores": {
                "ai_citability": 45,
                "brand_authority": 62,
                "content_eeat": 70,
                "technical": 55,
                "schema": 30,
                "platform_optimization": 48,
            },
            "platforms": {
                "Google AI Overviews": 65,
                "ChatGPT": 52,
                "Perplexity": 48,
                "Gemini": 60,
                "Bing Copilot": 45,
            },
            "executive_summary": (
                "本報告呈現對 Example Company (https://example.com) 進行的 GEO 綜合稽核結果。"
                "該網站的整體 GEO 準備度分數為 58/100，處於中等等級。"
                "最強的領域是內容品質 (70/100)，而結構化資料 (30/100) 則是最大的改善機會。"
                "實作結構化資料標記、允許 AI 爬蟲存取，並優化內容結構，預計能在 90 天內將分數提升至約 78/100。"
            ),
            "findings": [
                {"severity": "critical", "title": "未偵測到結構化資料標記",
                 "description": "網站缺乏 JSON-LD 結構化資料，導致 AI 模型難以理解實體關聯。"},
                {"severity": "high", "title": "純 JavaScript 渲染",
                 "description": "關鍵內容頁面使用客戶端渲染，這對無法執行 JavaScript 的 AI 爬蟲來說是隱形的。"},
                {"severity": "high", "title": "缺少 llms.txt",
                 "description": "不存在 llms.txt 檔案來引導 AI 系統找到最重要的內容。"},
                {"severity": "medium", "title": "品牌實體存在感薄弱",
                 "description": "品牌未出現在 Wikipedia 或 Wikidata 上，限制了 AI 模型的實體識別能力。"},
                {"severity": "medium", "title": "內容未針對引用率進行優化",
                 "description": "大多數內容區塊太短或太長，不利於 AI 引用（目標：134-167 字）。"},
            ],
            "quick_wins": [
                "在 robots.txt 中允許所有第一線 AI 爬蟲",
                "在所有內容頁面加入發布日期",
                "建立包含關鍵頁面參考的 llms.txt 檔案",
                "加入帶有資歷的作者署名",
                "修復前 10 大頁面的 meta 描述",
            ],
            "medium_term": [
                "實作帶有 sameAs 連結的 Organization 結構化資料",
                "在所有部落格文章加入 Article + Person 結構化資料",
                "使用問題導向的 H2 標題重構內容",
                "優化內容區塊以符合 134-167 字的引用標準",
                "為內容頁面實作伺服器端渲染 (SSR)",
            ],
            "strategic": [
                "建立 Wikipedia/Wikidata 的實體存在感",
                "制定 Reddit 社群參與策略",
                "建立符合 AI 搜尋意圖的 YouTube 內容",
                "建立原創研究發布計畫",
                "建立全面的主題權威內容叢集",
            ],
            "crawler_access": {
                "GPTBot": {"platform": "ChatGPT", "status": "Allowed", "recommendation": "保持允許"},
                "ClaudeBot": {"platform": "Claude", "status": "Allowed", "recommendation": "保持允許"},
                "PerplexityBot": {"platform": "Perplexity", "status": "Blocked", "recommendation": "解除阻擋以提升可見度"},
                "Google-Extended": {"platform": "Gemini", "status": "Allowed", "recommendation": "保持允許"},
                "Bingbot": {"platform": "Bing Copilot", "status": "Allowed", "recommendation": "保持允許"},
            },
        }

        output_file = "GEO-REPORT-sample.pdf"
        result = generate_report(sample_data, output_file)
        print(f"Report generated: {result}")

    else:
        # Load data from file or stdin
        input_path = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "GEO-REPORT.pdf"

        if input_path == "-":
            MAX_STDIN_BYTES = 10_000_000
            raw = sys.stdin.buffer.read(MAX_STDIN_BYTES + 1)
            if len(raw) > MAX_STDIN_BYTES:
                print("ERROR: stdin input exceeds 10 MB limit", file=sys.stderr)
                sys.exit(1)
            data = json.loads(raw)
        else:
            with open(input_path) as f:
                data = json.load(f)

        result = generate_report(data, output_file)
        print(f"Report generated: {result}")
