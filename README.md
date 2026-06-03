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
│   └── starlink_usage.csv  # Generated after each scrape (auto-created)

```

---

## Requirements

- Python 3.8 or higher — download at https://www.python.org/downloads/
- Google Chrome browser installed
- A Starlink account with access to the usage dashboard

---create a folder name it templates and put the index.html inside the folder

## Setup (Run Once on a New Device)

**1. Open a terminal inside the project folder**
```
cd starlink-scraper
```
**2. Allow scripts to run (first time only)**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**3. Create a virtual environment**
```bash
python -m venv venv
```

**4. Activate the virtual environment**
```bash
# Windows
venv\Scripts\activate
```

**5. Install dependencies**
```bash
pip install -r requirements.txt
```

**6. Run the app**
```bash
python app.py
```

**7. Open your browser and go to**
```
http://127.0.0.1:5001
```

---

## How to Use

1. Click **START ACCURATE SYNC** in the browser UI
2. A Chrome window will open automatically and navigate to the Starlink login page if its shows an error select the Go Home 
3. if not navigated to the sign in kindly select the three dots and select the SIGN IN
4. **Log in manually** using the following credentials:
   - **Username:** fundamentalssystem@gmail.com
   - **Password:** systemfundamentals2026
5. Solve any CAPTCHAs if prompted
6. Once logged in, the scraper takes over automatically:
   - Navigates to your usage dashboard
   - Clicks through each month tab (Nov–Dec, Jan, Feb, Mar, Apr, May–Jun)
   - Extracts daily usage data from the chart bars
7. When finished, the table populates in the UI and your **Total Data Usage** is displayed
8. Click **DOWNLOAD CSV REPORT** to save `starlink_usage.csv`
