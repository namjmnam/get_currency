from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException

# Initialize the WebDriver (Assuming you are using Chrome)
# chrome_options = Options()
# chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--ignore-ssl-errors=yes")
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

# Open the target URL
url = "https://www.smbs.biz/ExRate/TodayExRate.jsp?StrSch_Year=2024&StrSch_Month=01&StrSch_Day=09"
# driver.get("http://www.smbs.biz/ExRate/TodayExRate.jsp")
driver.get(url)

# Wait for the elements to be present on the page
wait = WebDriverWait(driver, 10)

# Find the input field for the date (assuming it is named 'StrSchFull')
# date_input = wait.until(EC.presence_of_element_located((By.NAME, "StrSchFull")))

# Clear the field and enter the desired date
# date_input.clear()
# date_input.send_keys('20240116')

# Execute the JavaScript function to submit the form
# driver.execute_script('doSearch("frm_SearchDate")')

# Add any additional code here, e.g., to verify submission or process results

# Close the driver (optional, depending on your use case)
driver.quit()
