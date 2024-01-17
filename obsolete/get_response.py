import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_context, *args, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

# Create an SSL context with specific TLS version and cipher suite
context = ssl.create_default_context()
context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!RC4')
# context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 # Disable older versions
context.check_hostname = False  # Disable hostname checking
context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

#Create a session and mount the adapter
session = requests.Session()
adapter = SSLAdapter(context)
session.mount('https://', adapter)

# URL to access
url = "https://www.smbs.biz/ExRate/TodayExRate.jsp?StrSch_Year=2024&StrSch_Month=01&StrSch_Day=09"

# Send a request to the URL using the session
try:
    response = session.get(url, verify=False)
    # Process the response here
    print(response)

except requests.exceptions.SSLError as e:
    print("SSL Error:", e)
    # Handle the SSL error

# Close the session
session.close()