#!/opt/homebrew/bin/python3
"""
File Name: scraper.py
Location: /Users/andrewwhite/Desktop/Patrol-Poro/scraper.py
Description: This script opens a Chrome browser using Selenium, navigates to a
'calls for service' website, searches for 'Fallbrook' data, extracts rows from
the results table, and saves them to a CSV file in the same directory.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

def scrape_calls_for_service():
    """
    This function launches Chrome via Selenium, navigates to the provided URL,
    performs a search for 'Fallbrook', waits for the table of calls for service
    to appear, then extracts each row's details and writes them to a CSV file.
    """

    # ========================================================================
    # 1. SETUP THE CHROME DRIVER
    # ========================================================================
    driver = webdriver.Chrome()

    try:
        # ====================================================================
        # 2. NAVIGATE TO THE 'CALLS FOR SERVICE' WEB PAGE
        #    Replace the URL below with the official "calls for service" page.
        # ====================================================================
        driver.get('https://callsforservice.sdsheriff.gov/')  # <-- Replace with actual URL

        # ====================================================================
        # 3. LOCATE THE SEARCH BAR AND ENTER 'FALLBROOK'
        #    Update the CSS selector if the actual site differs.
        # ====================================================================
        search_bar = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_bar.send_keys('Fallbrook')  # Type 'Fallbrook' in the search bar

        # Optionally press "ENTER" if needed, or if the page triggers auto-search, skip this
        # search_bar.send_keys(Keys.ENTER)

        # Give the page time to load search results
        time.sleep(3)

        # ====================================================================
        # 4. WAIT FOR THE TABLE TO LOAD
        #    You can replace the time.sleep with an explicit WebDriverWait
        #    if the table takes varying times to load.
        # ====================================================================
        time.sleep(5)

        # ====================================================================
        # 5. GET THE TABLE ROWS
        #    Update the selector (#table tbody tr) to match the actual HTML.
        # ====================================================================
        rows = driver.find_elements(By.CSS_SELECTOR, '#table tbody tr')

        # ====================================================================
        # 6. PREPARE CSV FILE FOR WRITING
        #    Save the CSV file in the same folder as the script.
        # ====================================================================
        output_file = '/Users/andrewwhite/Desktop/MAC AUTOMATIONS/calls_for_service_data.csv'
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write a header row to describe each column
            writer.writerow([
                "Date/Time", 
                "Call Status", 
                "Event Type", 
                "Location", 
                "Community", 
                "Service Area", 
                "Event Number"
            ])

            # =================================================================
            # 7. LOOP THROUGH EACH ROW, EXTRACT TEXT, AND WRITE TO CSV
            # =================================================================
            for row in rows:
                date_time    = row.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text.strip()
                call_status  = row.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text.strip()
                event_type   = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text.strip()
                location     = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text.strip()
                community    = row.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text.strip()
                service_area = row.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text.strip()
                event_number = row.find_element(By.CSS_SELECTOR, 'td:nth-child(7)').text.strip()

                # Print to console so we can see what's being scraped
                print(f"Date/Time: {date_time}, Call Status: {call_status}, "
                      f"Event Type: {event_type}, Location: {location}, "
                      f"Community: {community}, Service Area: {service_area}, "
                      f"Event Number: {event_number}")

                # Write row data to CSV
                writer.writerow([
                    date_time,
                    call_status,
                    event_type,
                    location,
                    community,
                    service_area,
                    event_number
                ])

        # ====================================================================
        # 8. SUCCESS MESSAGE
        # ====================================================================
        print(f"\nScraping complete! Data saved to:\n{output_file}")

    finally:
        # ====================================================================
        # 9. ALWAYS QUIT THE DRIVER, EVEN IF AN ERROR OCCURS
        # ====================================================================
        driver.quit()

# ========================================================================
# 10. RUN THE SCRIPT
# ========================================================================
if __name__ == "__main__":
    scrape_calls_for_service()
