from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Enable browser logging
capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

# Set up Chrome options
chrome_options = Options()
chrome_options.headless = True  # Running in headless mode

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options,
                          desired_capabilities=capabilities)

# URL to access
url = "https://www.example.com"

# Access the website
driver.get(url)

# Wait for the page to load completely
time.sleep(5)

# Retrieve JavaScript logs
logs = driver.get_log("browser")

# Close the browser
driver.quit()

# Print the JavaScript logs
for log in logs:
    print(log)
