# 🛰️ Starlink Data Scraper

A local web app that logs into your Starlink account, scrapes your monthly data usage from the chart, and exports it as a clean CSV report.

---

## Project Structure

```
starlink-scraper/
├── app.py                  # Flask web server
├── scraper.py              # Chrome automation + data extraction
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Browser UI
├── output/
│   └── starlink_usage.csv  # Generated after each scrape
└── static/                 # (unused) placeholder for future CSS/JS assets
```

---

## Requirements

- Python 3.8+
- Google Chrome installed
- A Starlink account with access to the usage dashboard

---

## Setup

**1. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python app.py
```

**4. Open your browser and go to**
```
http://127.0.0.1:5001
```

---

## How to Use

1. Click **START ACCURATE SYNC** in the browser UI
2. A Chrome window will open automatically and navigate to the Starlink login page
3. **Log in manually** — solve any CAPTCHAs if prompted
4. Once logged in, the scraper takes over automatically:
   - Navigates to your usage dashboard
   - Clicks through each month tab (Nov–Dec, Jan, Feb, Mar, Apr, May–Jun)
   - Extracts daily usage data from the chart bars
5. When finished, the table populates in the UI and your **Total Data Usage** is displayed
6. Click **DOWNLOAD CSV REPORT** to save `starlink_usage.csv`

> ⏱️ The full scrape takes **2–4 minutes**. Do not close the Chrome window while it runs.
