import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# WebDriverWait imports:
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_calls_for_service():
 
    # ========================================================================
    # 1. SETUP THE CHROME DRIVER
    # ========================================================================
    driver = webdriver.Chrome()  # Ensure chromedriver is installed and in PATH

    try:
        # ====================================================================
        # 2. NAVIGATE TO THE 'CALLS FOR SERVICE' PAGE
        # ====================================================================
        driver.get('https://callsforservice.sdsheriff.gov/')

        # ====================================================================
        # 3. LOCATE THE SEARCH BAR AND ENTER 'TARGET SEARCH CITY'
        # ====================================================================
        search_bar = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_bar.send_keys('Fallbrook')
        # If needed: search_bar.send_keys(Keys.ENTER)

        # ====================================================================
        # 4. WAIT FOR THE TABLE TO LOAD AT LEAST ONE ROW (EXPLICIT WAIT)
        # ====================================================================
        wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds
        table_rows_locator = (By.CSS_SELECTOR, '#table tbody tr')

        # Wait until at least 1 row appears in the table's <tbody>
        rows = wait.until(EC.presence_of_all_elements_located(table_rows_locator))

        # If no rows are found, handle it gracefully
        if not rows:
            print("No rows found for 'Fallbrook' at this time.")
            return

        # ====================================================================
        # 5. PREPARE THE CSV FILE FOR WRITING
        # ====================================================================
        output_file = '/Users/andrewwhite/Desktop/calls_for_service_data.csv'
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write headers for the 4 columns we care about
            writer.writerow([
                "Date/Time",
                "Event Type",
                "Approximate Location",
                "Event Number"
            ])

            # =============================================================
            # 6. LOOP THROUGH EACH ROW, EXTRACT TEXT, AND WRITE TO CSV
            #
            #    The table columns (1..6) are:
            #       #1) Date/Time
            #       #2) Event Type
            #       #3) Approx. Location
            #       #4) Community
            #       #5) Service Area
            #       #6) Event Number
            #
            #    We only need columns #1, #2, #3, and #6.
            # =============================================================
            for row in rows:
                cells = row.find_elements(By.CSS_SELECTOR, 'td')

                # Ensure we have at least 6 columns
                if len(cells) < 6:
                    print(f"Skipping a row with only {len(cells)} cells.")
                    continue

                # Extract the columns we care about
                date_time       = cells[0].text.strip()  # Date/Time (#1)
                event_type      = cells[1].text.strip()  # Event Type (#2)
                approximate_loc = cells[2].text.strip()  # Approx. Location (#3)
                event_number    = cells[5].text.strip()  # Event Number (#6)

                # Print to console for debugging
                print(f"Date/Time: {date_time}, "
                      f"Event Type: {event_type}, "
                      f"Approx. Location: {approximate_loc}, "
                      f"Event Number: {event_number}")

                # Write to CSV
                writer.writerow([
                    date_time,
                    event_type,
                    approximate_loc,
                    event_number
                ])

        # ====================================================================
        # 7. PRINT SUCCESS MESSAGE
        # ====================================================================
        print(f"\nScraping complete! Data saved to:\n{output_file}")

    finally:
        # ====================================================================
        # 8. ALWAYS QUIT THE DRIVER, EVEN IF AN ERROR OCCURS
        # ====================================================================
        driver.quit()

# ========================================================================
# 9. RUN THE SCRIPT IF CALLED DIRECTLY
# ========================================================================
if __name__ == "__main__":
    scrape_calls_for_service()
s