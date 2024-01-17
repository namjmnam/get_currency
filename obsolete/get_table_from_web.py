import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_context, *args, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

# Create an SSL context with a specific TLS version and cipher suite
context = ssl.create_default_context()
context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!RC4')
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable TLSv1 and TLSv1.1

# Create a session and mount the adapter
session = requests.Session()
adapter = SSLAdapter(context)
session.mount('https://', adapter)

# URL to access
url = "https://www.smbs.biz/ExRate/TodayExRate.jsp?StrSch_Year=2024&StrSch_Month=01&StrSch_Day=09"

# Send a request to the URL
response = requests.get(url)

print(response)

# # Check if the request was successful
# if response.status_code == 200:
#     print(response)
#     # # Parse the HTML content
#     # soup = BeautifulSoup(response.content, 'html.parser')
    
#     # # Find the table in the HTML
#     # table = soup.find('table')
    
#     # # Check if a table was found
#     # if table:
#     #     # Convert the HTML table to a pandas DataFrame
#     #     df = pd.read_html(str(table))[0]
#     #     print(df)
#     # else:
#     #     print("No table found on the page.")
# else:
#     print("Failed to access the page. Status code:", response.status_code)
