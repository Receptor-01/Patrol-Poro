
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

def scrape_calls_for_service():
    """
    This function:
      1) Launches Chrome with Selenium
      2) Goes to 'https://callsforservice.sdsheriff.gov/'
      3) Searches for 'Fallbrook'
      4) Waits for results
      5) Scrapes Date/Time, Event Type, Approx. Location, & Event Number
      6) Writes everything to a CSV file
    """

    # ========================================================================
    # 1. SETUP THE CHROME DRIVER
    #    Make sure you have ChromeDriver installed (same version as Chrome).
    # ========================================================================
    driver = webdriver.Chrome()

    try:
        # ====================================================================
        # 2. NAVIGATE TO THE 'CALLS FOR SERVICE' WEB PAGE
        # ====================================================================
        driver.get('https://callsforservice.sdsheriff.gov/')

        # ====================================================================
        # 3. LOCATE THE SEARCH BAR AND ENTER 'FALLBROOK'
        #    If the page auto-updates upon typing, we don't need to press ENTER.
        # ====================================================================
        search_bar = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_bar.send_keys('Fallbrook')  # Type 'Fallbrook'

        # If the site requires hitting ENTER to filter, uncomment below:
        # search_bar.send_keys(Keys.ENTER)

        # ====================================================================
        # 4. WAIT FOR THE TABLE TO LOAD
        #    You can replace these sleeps with WebDriverWait if needed.
        # ====================================================================
        time.sleep(3)  # Allow time for search to update
        time.sleep(5)  # Additional time for table data to load

        # ====================================================================
        # 5. GET THE TABLE ROWS
        #    The table with id="table" should populate with <tr> elements.
        # ====================================================================
        rows = driver.find_elements(By.CSS_SELECTOR, '#table tbody tr')

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

            # =============================================================
            # 7. LOOP THROUGH EACH ROW, EXTRACT TEXT, WRITE TO CSV
            #    The 7 columns in the table are:
            #      1) Date Time
            #      2) Call Status
            #      3) Event Type
            #      4) Approximate Location
            #      5) Community
            #      6) Service Area
            #      7) Event Number
            #    We only need columns #1, #3, #4, #7
            # =============================================================
            for row in rows:
                # Get each relevant <td>
                date_time          = row.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text.strip()
                event_type         = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text.strip()
                approximate_loc    = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text.strip()
                event_number       = row.find_element(By.CSS_SELECTOR, 'td:nth-child(7)').text.strip()

                # Print to console
                print(f"Date/Time: {date_time}, "
                      f"Event Type: {event_type}, "
                      f"Approx. Location: {approximate_loc}, "
                      f"Event Number: {event_number}")

                # Write to CSV file
                writer.writerow([
                    date_time,
                    event_type,
                    approximate_loc,
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
