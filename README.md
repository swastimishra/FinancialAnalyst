# Financial Analyst Copilot

A modern, web-based financial analysis dashboard that lets you:
- Upload Excel financial data
- Automatically detect anomalies
- Generate and customize forecasts
- Download reports as PDF or Excel
- Enjoy a beautiful, responsive UI

---

## Features
- **Excel Upload:** Upload your balance sheets or financial data in `.xlsx` format.
- **Anomaly Detection:** Instantly flags irregularities in your data.
- **Forecasting:** Generate forecasts for any number of weeks.
- **Downloadable Reports:** Export results as PDF or Excel.
- **Modern Dashboard UI:** Responsive, aesthetic, and easy to use.

---

## Requirements
- Python 3.8+
- pip

### Python Packages
- Flask
- Flask-Session
- pandas
- openpyxl
- APScheduler
- pdfkit (optional, for PDF export)

---

## Installation
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd project2
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install Flask-Session
   ```
3. **(Optional) For PDF export:**
   - Install [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) and ensure it's in your PATH.
   - Install pdfkit:
     ```bash
     pip install pdfkit
     ```

---

## Usage
1. **Start the app:**
   ```bash
   python app.py
   ```
2. **Open your browser:**
   Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
3. **Upload your Excel file** and explore the dashboard!

---
