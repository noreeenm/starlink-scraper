import threading
import csv
import time
import os
import re
import logging
import html as htmllib
from datetime import date, timedelta

from flask import Flask, render_template, jsonify, send_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ── Shared state ──────────────────────────────────────────────────────────────
scraped_data  = []
scrape_status = {"running": False, "message": "Idle", "done": False, "error": None}

# ── Path to the provided local HTML file ─────────────────────────────────────
LOCAL_HTML = os.path.join(os.path.dirname(__file__), "Starlink_files", "Starlink.html")

# ── Core parsing logic ────────────────────────────────────────────────────────
def parse_starlink_html(html_content: str) -> list[dict]:
    """
    Parse daily data usage from a saved Starlink account HTML page.
    The chart is an SVG bar chart; each <rect> in the y_0 data-series
    represents one day. Bar height encodes GB used.

    Chart calibration (from the y-axis tick labels in the SVG):
      y = 130  →  0 GB
      y ≈ 43.13 →  20 GB
    """
    content = htmllib.unescape(html_content)

    # ── 1. Extract SVG bar heights ────────────────────────────────────────────
    y0_match = re.search(r'data-series="y_0"[^>]*>(.*?)</g>', content, re.DOTALL)
    if not y0_match:
        raise ValueError("Could not find data-series='y_0' in HTML — is this the correct page?")

    rects = re.findall(r'y="([0-9.]+)"[^>]*?height="([0-9.]+)"', y0_match.group(1))
    if not rects:
        raise ValueError("No <rect> elements found in the y_0 bar series.")

    # ── 2. Chart scale ────────────────────────────────────────────────────────
    Y_ZERO  = 130.0          # y-coordinate for 0 GB
    Y_20GB  = 43.134687002672486   # y-coordinate for 20 GB
    scale   = 20.0 / (Y_ZERO - Y_20GB)

    # ── 3. Find the total usage label to cross-validate and correct rounding ──
    total_match = re.search(r'Total Data Usage.*?([0-9,]+)\s*GB', content, re.DOTALL)
    reported_total = None
    if total_match:
        reported_total = float(total_match.group(1).replace(',', ''))
        logger.info(f"Reported total: {reported_total} GB")

    raw_gb = [(Y_ZERO - float(y)) * scale for y, h in rects]
    pixel_sum = sum(raw_gb)

    if reported_total and pixel_sum > 0:
        factor = reported_total / pixel_sum
    else:
        factor = 1.0

    gb_vals = [round(v * factor, 2) for v in raw_gb]

    # ── 4. Determine the month being shown ───────────────────────────────────
    # Find the highlighted (selected) month button — class mui-1bcwr2w
    selected_months = re.findall(
        r'class="MuiTypography-root MuiTypography-subtitle2 mui-1bcwr2w">(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)</h6>',
        content
    )
    logger.info(f"Selected months: {selected_months}")

    # Map to a start date; default to April 2026 based on the provided file
    month_map = {
        'Jan': (2026, 1), 'Feb': (2026, 2), 'Mar': (2026, 3),
        'Apr': (2026, 4), 'May': (2026, 5), 'Jun': (2026, 6),
        'Jul': (2026, 7), 'Aug': (2026, 8), 'Sep': (2026, 9),
        'Oct': (2025, 10), 'Nov': (2025, 11), 'Dec': (2025, 12),
    }
    # Use the first selected month
    if selected_months:
        year, month = month_map.get(selected_months[0], (2026, 4))
    else:
        year, month = 2026, 4

    start_date = date(year, month, 1)
    month_label = start_date.strftime('%B %Y')

    # ── 5. Build result rows ──────────────────────────────────────────────────
    rows = []
    for i, gb in enumerate(gb_vals):
        d = start_date + timedelta(days=i)
        rows.append({
            "day":        d.strftime('%Y-%m-%d'),
            "data_usage": f"{gb} GB",
            "extra":      d.strftime('%A') + f" | {month_label}",
        })

    return rows


def scrape_from_local_file():
    """Parse the bundled Starlink.html file."""
    global scraped_data, scrape_status
    scraped_data  = []
    scrape_status = {"running": True, "message": "Reading local HTML file…", "done": False, "error": None}

    try:
        html_path = os.path.join(os.path.dirname(__file__), "Starlink.html")
        if not os.path.exists(html_path):
            raise FileNotFoundError(
                f"Starlink.html not found at {html_path}. "
                "Place the saved Starlink page next to app.py."
            )

        scrape_status["message"] = "Parsing HTML…"
        with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
            html_content = f.read()

        scraped_data = parse_starlink_html(html_content)
        save_csv()

        scrape_status = {
            "running": False,
            "message": f"Done! {len(scraped_data)} daily records extracted.",
            "done":    True,
            "error":   None,
        }

    except Exception as e:
        logger.error(f"Parse error: {e}", exc_info=True)
        scrape_status = {
            "running": False,
            "message": "An error occurred.",
            "done":    True,
            "error":   str(e),
        }


# ── CSV helper ────────────────────────────────────────────────────────────────
def save_csv():
    path = os.path.join(os.path.dirname(__file__), "starlink_data_usage.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["day", "data_usage", "extra"])
        writer.writeheader()
        writer.writerows(scraped_data)
    logger.info(f"CSV saved → {path}")


# ── Flask routes ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scrape", methods=["POST"])
def start_scrape():
    if scrape_status.get("running"):
        return jsonify({"error": "Scraper already running"}), 400
    t = threading.Thread(target=scrape_from_local_file, daemon=True)
    t.start()
    return jsonify({"message": "Scraping started"})


@app.route("/api/status")
def status():
    return jsonify(scrape_status)


@app.route("/api/data")
def data():
    return jsonify(scraped_data)


@app.route("/api/download")
def download():
    path = os.path.join(os.path.dirname(__file__), "starlink_data_usage.csv")
    if not os.path.exists(path):
        return jsonify({"error": "CSV not generated yet"}), 404
    return send_file(
        path,
        as_attachment=True,
        download_name="starlink_data_usage.csv",
        mimetype="text/csv",
    )


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  🛰️  Starlink Data Usage Scraper")
    print("  Open  http://localhost:5000  in your browser")
    print("  Place Starlink.html next to app.py before scraping")
    print("=" * 55 + "\n")
    app.run(debug=False, port=5000)