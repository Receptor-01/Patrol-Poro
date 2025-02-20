
# Patrol Poro

![alt text](PATROL-PORO-COVER-IMAGE.jpg)

**Patrol Poro** is a web scraping project that collects real-time police call data from a police radio dispatcher website. The data is scraped and stored for analysis or reporting.


## Features
✅ **Automated Data Scraping** – No manual copying needed.  
✅ **Filters by City** – Only relevant incidents are extracted.  
✅ **Saves to CSV** – Structured output for easy analysis.  
✅ **Runs in Headless Mode (Optional)** – Can be modified to run without opening a browser.  



## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Receptor-01/Patrol-Poro.git


## 1. Clone or Download the Repository

   ```bash
git clone https://github.com/YOUR-USERNAME/calls-for-service-scraper.git
cd calls-for-service-scraper
   ```

## 2. Run the Script

   ```bash
python scrape_calls.py
   ```

## 3. Wait for the Script to Complete
The script will:

- Open a Chromium browser
- Load the Calls for Service page
- Select "All" entries
- Search for "City" (be sure to specify in script)
- Scrape available data
- Save it to a CSV file on your desktop

