from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def process_table_text(table_text):
    # Remove all unnecessary strings
    table_text = table_text.replace(" (US$)", "")
    table_text = table_text.replace("통화명 환율(원) 전일대비 Cross Rate\n", "")
    processed_rows = []

    for line in table_text.split('\n'):
        words = line.split()

        if len(words) >= 3:
            third_column = words[-1]
            second_column = words[-3]
            first_column = " ".join(words[:-3])
            processed_rows.append([first_column, second_column, third_column])

    df = pd.DataFrame(processed_rows, columns=['통화명', '환율(원)', 'Cross Rate(US$)'])
    return df

def process_first_table_text(table_text):
    # Remove all unnecessary strings
    table_text = table_text.replace("통화명 환율(원) 전일대비\n", "")
    processed_rows = []

    for line in table_text.split('\n'):
        words = line.split()

        if len(words) >= 3:
            second_column = words[-2]
            first_column = " ".join(words[:-2])
            processed_rows.append([first_column, second_column])

    df = pd.DataFrame(processed_rows, columns=['통화명', '환율(원)'])
    return df

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

# print(tables[1].get_attribute('outerHTML'))
first_table_text = tables[0].text
table_text = tables[1].text
df = process_first_table_text(first_table_text)
# df = process_table_text(table_text)
print(df.to_string(index=False))

# Close after 0.3 seconds
time.sleep(0.3)
driver.quit()

