"""
Simple Flask application to track Aiden's respiratory health, estimate risk,
and share teacher-facing instructions.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

from flask import Flask, flash, redirect, render_template, request, url_for

DATA_PATH = Path(__file__).parent / "data" / "health_log.json"
app = Flask(__name__)
app.secret_key = os.environ.get("AIDEN_HEALTH_SECRET", "dev-secret-key")


@app.context_processor
def inject_share_link() -> Dict[str, str]:
    """Expose the current base URL so users can copy/share the app link."""
    # request.url_root includes a trailing slash—strip it for a clean share URL.
    link = request.url_root.rstrip("/") if request else ""
    return {"share_link": link}


def _ensure_data_file() -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        DATA_PATH.write_text("[]", encoding="utf-8")


def load_entries() -> List[Dict]:
    _ensure_data_file()
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def save_entries(entries: List[Dict]) -> None:
    DATA_PATH.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def compute_risk(entry: Dict) -> Tuple[str, int]:
    """Return a qualitative risk label and numeric score."""
    score = 0
    score += int(entry.get("cough_severity", 0))
    if entry.get("asthma_trouble"):
        score += 2
    if entry.get("fever"):
        score += 3
    exposures = entry.get("exposures", "")
    if exposures:
        score += min(3, len(exposures.split(",")))
    if entry.get("peak_flow"):
        try:
            peak_flow = int(entry["peak_flow"])
            if peak_flow < 250:
                score += 3
            elif peak_flow < 325:
                score += 2
        except ValueError:
            pass

    if score >= 8:
        label = "High"
    elif score >= 4:
        label = "Moderate"
    else:
        label = "Low"
    return label, score


def demo_entries() -> List[Dict]:
    """Return a small set of demo entries for quick previews."""
    now = datetime.utcnow()
    sample_days = [now, now - timedelta(days=1), now - timedelta(days=2)]
    samples: List[Dict] = []
    exposure_options = ["Pollen", "Pollen, cold contact", "Smoke"]
    for offset, day in enumerate(sample_days):
        entry = {
            "timestamp": day.isoformat(),
            "date": day.strftime("%Y-%m-%d"),
            "cough_severity": min(5, offset * 2),
            "cough_notes": [
                "Clear daytime cough.",
                "Night cough with phlegm.",
                "Short bursts after recess.",
            ][offset],
            "asthma_trouble": offset != 0,
            "asthma_notes": [
                "Breathing normal.",
                "Used rescue inhaler once.",
                "Chest tightness during PE.",
            ][offset],
            "medication": "Controller inhaler AM/PM",
            "peak_flow": str(340 - (offset * 30)),
            "fever": offset == 2,
            "exposures": exposure_options[offset],
            "teacher_note": [
                "Encourage hydration and monitor cough frequency.",
                "Allow indoor recess and keep inhaler accessible.",
                "Send to nurse if breathing is labored; skip running.",
            ][offset],
        }
        samples.append(entry)
    samples.sort(key=lambda entry: entry["timestamp"])
    return samples


def build_entry(form: Dict) -> Dict:
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "date": form.get("date") or datetime.utcnow().strftime("%Y-%m-%d"),
        "cough_severity": int(form.get("cough_severity", 0)),
        "cough_notes": form.get("cough_notes", "").strip(),
        "asthma_trouble": bool(form.get("asthma_trouble")),
        "asthma_notes": form.get("asthma_notes", "").strip(),
        "medication": form.get("medication", "").strip(),
        "peak_flow": form.get("peak_flow", "").strip(),
        "fever": bool(form.get("fever")),
        "exposures": form.get("exposures", "").strip(),
        "teacher_note": form.get("teacher_note", "").strip(),
    }


@app.route("/")
def index():
    entries = load_entries()
    latest = entries[-1] if entries else None
    risk = compute_risk(latest)[0] if latest else None
    return render_template("index.html", entries=entries, latest=latest, risk=risk)


@app.route("/log")
def log_view():
    entries = load_entries()
    entries_with_risk = [
        {**entry, "risk": compute_risk(entry)[0], "risk_score": compute_risk(entry)[1]}
        for entry in entries
    ]
    entries_with_risk.sort(key=lambda e: e["timestamp"], reverse=True)
    return render_template("log.html", entries=entries_with_risk)


@app.route("/demo")
def load_demo():
    entries = load_entries()
    if entries:
        flash(
            "Demo data not added because you already have saved entries. Delete data/health_log.json to reload demo entries.",
            "warning",
        )
        return redirect(url_for("index"))

    samples = demo_entries()
    save_entries(samples)
    flash("Loaded demo entries so you can preview the dashboard and log.", "success")
    return redirect(url_for("index"))


@app.route("/entry", methods=["POST"])
def add_entry():
    entry = build_entry(request.form)
    entries = load_entries()
    entries.append(entry)
    save_entries(entries)
    risk_label, _ = compute_risk(entry)
    flash(f"Entry saved. Current risk: {risk_label}.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    host = os.environ.get("AIDEN_HOST", "127.0.0.1")
    port = int(os.environ.get("AIDEN_PORT", "5000"))
    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug_mode)
