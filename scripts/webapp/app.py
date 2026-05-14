#!/usr/bin/env python3
"""
GEO-SEO CRM — 網頁介面 (Flask + HTMX)
用法:
    pip install flask
    python app.py
    打開 http://localhost:5050
"""

import json
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, send_file, abort, jsonify

app = Flask(__name__)


@app.context_processor
def inject_now():
    return {"now": datetime.now().strftime("%Y-%m-%d %H:%M")}

CRM_PATH = Path.home() / ".geo-prospects" / "prospects.json"
PROPOSALS_DIR = Path.home() / ".geo-prospects" / "proposals"
AUDITS_DIR = Path.home() / ".geo-prospects" / "audits"


# ── 輔助函式 (Helpers) ────────────────────────────────────────────────────────────

def load_prospects() -> list[dict]:
    if not CRM_PATH.exists():
        return []
    with open(CRM_PATH) as f:
        return json.load(f)

def save_prospects(prospects: list[dict]):
    with open(CRM_PATH, "w") as f:
        json.dump(prospects, f, indent=2, ensure_ascii=False)

def score_tier(score: int) -> str:
    if score >= 80: return "good"
    if score >= 60: return "moderate"
    if score >= 40: return "poor"
    return "critical"

def score_label(score: int) -> str:
    if score >= 80: return "良好"
    if score >= 60: return "中等"
    if score >= 40: return "不佳"
    return "危急"

def format_eur(value) -> str:
    if not value:
        return "—"
    return f"€{int(value):,}".replace(",", ".")

def crm_stats(prospects: list[dict]) -> dict:
    total = len(prospects)
    active = [p for p in prospects if p.get("status") == "active"]
    proposals = [p for p in prospects if p.get("status") == "proposal"]
    mrr = sum(p.get("monthly_value", 0) for p in active)
    pipeline = sum(p.get("monthly_value", 0) for p in proposals)
    avg_score = round(sum(p.get("geo_score", 0) for p in prospects) / total) if total else 0
    return {
        "total": total,
        "active": len(active),
        "mrr": format_eur(mrr),
        "pipeline": format_eur(pipeline),
        "avg_score": avg_score,
        "avg_tier": score_tier(avg_score),
    }

def find_pdf(prospect: dict) -> Path | None:
    """尋找特定潛在客戶的 PDF 檔案。"""
    domain = prospect.get("domain", "")
    for f in sorted(PROPOSALS_DIR.glob(f"{domain}*.pdf"), reverse=True):
        return f
    return None


# ── 模板過濾器 (Template filters) ────────────────────────────────────────────────────

app.jinja_env.filters["score_tier"] = score_tier
app.jinja_env.filters["score_label"] = score_label
app.jinja_env.filters["format_eur"] = format_eur

STATUS_META = {
    "lead":     {"icon": "⬜", "badge": "secondary",  "label": "潛在客戶"},
    "audit":    {"icon": "🔍", "badge": "warning",    "label": "稽核"},
    "proposal": {"icon": "📄", "badge": "info",       "label": "提案"},
    "active":   {"icon": "✅", "badge": "success",    "label": "活躍"},
    "churned":  {"icon": "❌", "badge": "danger",     "label": "已流失"},
    "lost":     {"icon": "💀", "badge": "dark",       "label": "未成交"},
}

@app.template_filter("status_meta")
def status_meta_filter(status: str) -> dict:
    return STATUS_META.get(status, {"icon": "?", "badge": "secondary", "label": status})


# ── 路由 (Routes) ─────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    prospects = load_prospects()
    status_filter = request.args.get("status", "")
    sort = request.args.get("sort", "score")

    filtered = [p for p in prospects if not status_filter or p.get("status") == status_filter]

    if sort == "score":
        filtered.sort(key=lambda x: x.get("geo_score", 0))
    elif sort == "company":
        filtered.sort(key=lambda x: x.get("company", "").lower())
    elif sort == "mrr":
        filtered.sort(key=lambda x: x.get("monthly_value", 0), reverse=True)

    stats = crm_stats(prospects)
    statuses = list(STATUS_META.keys())

    return render_template(
        "dashboard.html",
        prospects=filtered,
        stats=stats,
        status_filter=status_filter,
        sort=sort,
        statuses=statuses,
        STATUS_META=STATUS_META,
    )


@app.route("/prospect/<pid>")
def prospect_detail(pid):
    prospects = load_prospects()
    p = next((x for x in prospects if x.get("id") == pid), None)
    if not p:
        abort(404)

    pdf_path = find_pdf(p)
    has_pdf = pdf_path is not None

    return render_template(
        "prospect.html",
        p=p,
        has_pdf=has_pdf,
        STATUS_META=STATUS_META,
        statuses=list(STATUS_META.keys()),
    )


@app.route("/prospect/<pid>/note", methods=["POST"])
def add_note(pid):
    """HTMX 端點 — 回傳更新後的備註片段。"""
    prospects = load_prospects()
    p = next((x for x in prospects if x.get("id") == pid), None)
    if not p:
        abort(404)

    text = request.form.get("text", "").strip()
    if text:
        if "notes" not in p:
            p["notes"] = []
        p["notes"].append({
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "text": text,
        })
        p["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        save_prospects(prospects)

    return render_template("_notes.html", p=p)


@app.route("/prospect/<pid>/status", methods=["POST"])
def update_status(pid):
    """HTMX 端點 — 更新狀態，回傳徽章片段。"""
    prospects = load_prospects()
    p = next((x for x in prospects if x.get("id") == pid), None)
    if not p:
        abort(404)

    new_status = request.form.get("status", "").strip()
    if new_status in STATUS_META:
        p["status"] = new_status
        p["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        save_prospects(prospects)

    meta = STATUS_META.get(p["status"], {})
    return f'<span class="badge bg-{meta["badge"]} fs-6">{meta["icon"]} {meta["label"]}</span>'


@app.route("/prospect/<pid>/pdf")
def download_pdf(pid):
    prospects = load_prospects()
    p = next((x for x in prospects if x.get("id") == pid), None)
    if not p:
        abort(404)

    pdf_path = find_pdf(p)
    if not pdf_path:
        abort(404)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=pdf_path.name,
        mimetype="application/pdf",
    )


# ── 執行 (Run) ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, port=5050)
