from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

today = datetime.now()

# Initialize the Chrome driver (make sure ChromeDriver is in your PATH)
driver = webdriver.Chrome()

try:
    # Open the webpage
    driver.get("http://www.smbs.biz/ExRate/TodayExRate.jsp")

    # Execute JavaScript function
    # driver.execute_script('doSearch("frm_SearchDate")')

    # Wait for the element to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "StrSch_Year")))

    # Execute JavaScript to change the value of the hidden element
    driver.execute_script("arguments[0].value = arguments[1];", driver.find_element(By.NAME, "StrSch_Year"), "2024")

    # Wait for the table to load
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "table_type7")))

    # Extract the table HTML content
    # table_html = driver.find_element(By.CLASS_NAME, "table_type7").get_attribute('outerHTML')

    # Use BeautifulSoup to parse the table
    # soup = BeautifulSoup(table_html, 'html.parser')

    # search_date = driver.find_element(By.ID, "frm_SearchDate")

    # # Find the input elements by their name attribute and set their values to today's date
    # driver.find_element(By.NAME, "StrSch_Year").send_keys('2024')
    # driver.find_element(By.NAME, "StrSch_Month").send_keys('01')
    # driver.find_element(By.NAME, "StrSch_Day").send_keys('09')

    # # If you need to update the 'StrSchFull' field as well
    # driver.find_element(By.NAME, "StrSchFull").send_keys('2024.01.09')

    # # Find all input elements within this form
    # inputs = search_date.find_elements(By.TAG_NAME, "input")

    # # Iterate through the inputs and print their details
    # for input_elem in inputs:
    #     input_name = input_elem.get_attribute('name')
    #     input_value = input_elem.get_attribute('value')
    #     input_type = input_elem.get_attribute('type')
    #     print(f"Name: {input_name}, Value: {input_value}, Type: {input_type}")

finally:
    # Close the browser
    driver.quit()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

# # Initialize the Chrome driver (make sure ChromeDriver is in your PATH)
# driver = webdriver.Chrome()

# try:
#     # Open the webpage
#     driver.get("http://www.smbs.biz/ExRate/TodayExRate.jsp")

#     # Set date
#     # search_date = driver.find_element(By.ID, "frm_SearchDate")
#     # driver.find_element(By.NAME, "StrSchFull").send_keys('2024.01.09')
#     # driver.execute_script('doSearch("frm_SearchDate")')

#     # Find all input elements within this form
#     # search_date = driver.find_element(By.ID, "frm_SearchDate")
#     # inputs = search_date.find_elements(By.TAG_NAME, "input")

#     # # Iterate through the inputs and print their details
#     # for input_elem in inputs:
#     #     input_name = input_elem.get_attribute('name')
#     #     input_value = input_elem.get_attribute('value')
#     #     input_type = input_elem.get_attribute('type')
#     #     print(f"Name: {input_name}, Value: {input_value}, Type: {input_type}")

# finally:
#     # Close the browser
#     driver.quit()
