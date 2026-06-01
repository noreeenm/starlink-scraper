# 🛰️ Starlink Data Usage Scraper

A Flask web application that reads a saved Starlink account page, extracts daily data usage records, displays them in a Web UI, and exports them to CSV.

---

## 📁 Project Structure

```
starlink-scraper/
├── app.py                   # Flask backend + HTML parser
├── requirements.txt         # Python dependencies
├── Starlink.html            # Saved Starlink account page (source file)
├── starlink_data_usage.csv  # Output CSV file (generated after scraping)
└── templates/
    └── index.html           # Frontend Web UI
```

---

## ✅ Requirements

- Python 3.9 or higher
- pip (Python package manager)

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```
git clone https://github.com/noreeenm/starlink-scraper.git
cd starlink-scraper
```

### 2. Create a virtual environment
```
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

---

## ▶️ Running the App

```
python app.py
```

Then open your browser and go to:
```
http://localhost:5000
```

---

## 🖥️ How to Use

1. Open `http://localhost:5000` in your browser
2. Click **Start Scraping**
3. Wait for the results to appear in the table
4. Click **⬇ Download CSV** to save the data
5. Click **📋 Copy JSON** to copy the data to clipboard

---

## 🔍 How It Works

The Starlink account page renders daily data usage as an SVG bar chart. The scraper:

1. Reads the saved `Starlink.html` file
2. Finds the SVG bar chart in the page
3. Extracts each bar's height (which represents GB used per day)
4. Converts pixel height to GB using the chart's y-axis scale
5. Cross-validates the total against the "Total Data Usage" label on the page
6. Maps each bar to a calendar date (April 2026, 30 days)
7. Saves results to `starlink_data_usage.csv`

---

## 📊 CSV Output Format

| Column | Description |
|---|---|
| `day` | Date in YYYY-MM-DD format |
| `data_usage` | Data used that day (e.g. `22.83 GB`) |
| `extra` | Day of week and month label |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web framework and API server |
| `beautifulsoup4` | HTML parsing support |

---

## 🔐 Account Credentials

The scraper uses the following Starlink account (provided by the assignment):

- **Website:** https://www.starlink.com
- **Username:** fundamentalssystem@gmail.com
- **Password:** systemfundamentals2026

---

## 📅 Data Extracted

- **Month:** April 2026
- **Total Usage:** 459 GB
- **Records:** 30 daily entries (April 1–30, 2026)
