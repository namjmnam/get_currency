import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_rurate(year, month, day):
    url = f"https://www.cbr.ru/eng/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={day}.{month}.{year}"
    # Send a GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with class 'data'
        table = soup.find('table', {'class': 'data'})

        # Read the table with pandas
        df = pd.read_html(str(table))[0]

        return df
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

df = get_rurate('2024', '01', '20')
print(df)