from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Open webpage
url = "http://www.smbs.biz/ExRate/TodayExRate.jsp?StrSch_Year=2024&StrSch_Month=01&StrSch_Day=09"
driver = webdriver.Chrome()
driver.get(url)

# Click the button
wait = WebDriverWait(driver, 10)
close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick='closeMainPopup();']")))
close_button.click()

# Get the source
html_source = driver.page_source

# Find all tables with class name 'table_type7'
tables = driver.find_elements(By.CLASS_NAME, "table_type7")

# List to store the content of each table
tables_content = []

# Iterate over the tables and extract their HTML content
for table in tables:
    tables_content.append(table.get_attribute('outerHTML'))

print(len(tables))

# Close after 0.3 seconds
time.sleep(0.3)
driver.quit()