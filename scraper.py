import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# For handling <select> elements:
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def scrape_calls_for_service():
    """
    1) Launches Chrome with Selenium
    2) Navigates to https://callsforservice.sdsheriff.gov/
    3) Sets the table's 'Show entries' dropdown to 'All'
    4) Searches for 'Fallbrook' in the search bar
    5) Waits for table rows to appear
    6) Scrapes Date/Time, Event Type, Approx. Location, & Event Number
    7) Saves results to /Users/andrewwhite/Desktop/calls_for_service_data.csv

    NOTE: The table columns discovered are (indexed 0..5):
        0) Date/Time
        1) Event Type
        2) Approx. Location
        3) Community
        4) Service Area
        5) Event Number

    We only need columns #0, #1, #2, and #5 in the final CSV.
    """

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
        # 3. SELECT "ALL" FROM THE "SHOW ENTRIES" DROPDOWN
        # ====================================================================
        # Wait until the <select> element is present on the page:
        wait = WebDriverWait(driver, 20)
        dropdown_locator = (By.CSS_SELECTOR, "select[name='table_length']")
        wait.until(EC.presence_of_element_located(dropdown_locator))

        dropdown_element = driver.find_element(*dropdown_locator)
        select = Select(dropdown_element)
        select.select_by_visible_text("All")  # If the site uses "All" literally

        # Give DataTables a moment to update the table after changing the page length
        time.sleep(2)

        # ====================================================================
        # 4. SEARCH FOR "FALLBROOK"
        # ====================================================================
        search_bar = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_bar.clear()
        search_bar.send_keys('Fallbrook')
        search_bar.send_keys(Keys.ENTER)  # Press ENTER to trigger filter
        time.sleep(2)

        # ====================================================================
        # 5. WAIT FOR TABLE ROWS (OR "NO MATCHING" MESSAGE)
        # ====================================================================
        table_rows_locator = (By.CSS_SELECTOR, '#table tbody tr')
        rows = wait.until(EC.presence_of_all_elements_located(table_rows_locator))

        # If no rows at all, exit
        if not rows:
            print("No table rows found. Exiting.")
            return

        # Check if there's exactly 1 row that says "No matching records found"
        if len(rows) == 1 and "no matching" in rows[0].text.lower():
            print("No matching records found for 'Fallbrook'. Exiting.")
            return

        # ====================================================================
        # 6. PREPARE CSV FILE FOR WRITING
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

            # ===============================================================
            # 7. LOOP THROUGH ROWS AND COLLECT DATA
            # ===============================================================
            for row in rows:
                cells = row.find_elements(By.CSS_SELECTOR, 'td')

                # Expecting 6 columns total; skip if fewer
                if len(cells) < 6:
                    print(f"Skipping row with {len(cells)} cells. Text={row.text}")
                    continue

                # Extract columns 0, 1, 2, and 5
                date_time       = cells[0].text.strip()  # column #0
                event_type      = cells[1].text.strip()  # column #1
                approximate_loc = cells[2].text.strip()  # column #2
                event_number    = cells[5].text.strip()  # column #5

                # Debug print
                print(f"Date/Time: {date_time}, "
                      f"Event Type: {event_type}, "
                      f"Approx. Location: {approximate_loc}, "
                      f"Event Number: {event_number}")

                # Write row to CSV
                writer.writerow([
                    date_time,
                    event_type,
                    approximate_loc,
                    event_number
                ])

        # ====================================================================
        # 8. PRINT SUCCESS MESSAGE
        # ====================================================================
        print(f"\nScraping complete! Data saved to:\n{output_file}")

    finally:
        # ====================================================================
        # 9. QUIT THE DRIVER (ALWAYS)
        # ====================================================================
        driver.quit()

# If run directly, execute the function
if __name__ == "__main__":
    scrape_calls_for_service()
