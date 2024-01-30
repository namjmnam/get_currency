import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import os
from datetime import datetime
script_directory = os.path.dirname(os.path.abspath(__file__))

def is_valid_date(year, month, day):
    # Check if month and day are exactly two characters long
    if len(month) != 2 or len(day) != 2:
        return False

    try:
        input_date = datetime(int(year), int(month), int(day))
        current_date = datetime.now()
        return input_date <= current_date
    except ValueError:
        # This occurs if the date is invalid (like April 31st)
        return False

def get_rurate(year, month, day):
    rus_file = script_directory+f'/saved_data/{year}-{month}-{day}-rus.csv'
    df = pd.DataFrame()
    if os.path.exists(rus_file):
        df = pd.read_csv(rus_file)
        print("Russian file already exists")

    elif is_valid_date(year, month, day):
        url = f"https://www.cbr.ru/eng/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={day}.{month}.{year}"
        # Send a GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            server_day = soup.find('button', {'class': 'datepicker-filter_button'})
            print(server_day)
            # print(server_day[:2])

            # Find the table with class 'data'
            table = soup.find('table', {'class': 'data'})

            if 'table' in locals():
                table_html = str(table)
                df = pd.read_html(io.StringIO(table_html))[0]
                df.columns = ['Numcode', 'Charcode', 'Unit', 'Currency', 'Rate']
                # print(df)
                # print(len(df))
                # Issue is that when the date is in the future, the russian central bank will retrieve past.
                # Depending on timezone, this can be a problem.
                # Thus, if the date here and the date on the website are different, it should not accept the dataframe
                # <button class="datepicker-filter_button" type="button">31.01.2024</button>
                # The class="datepicker-filter_button" should be same as the date
                # This fix is not implemented yet
                if not os.path.exists(script_directory+f'/saved_data/'):
                    os.makedirs(script_directory+f'/saved_data/')
                df.to_csv(rus_file, index=False)
            else:
                print("The table data is not available. Please provide the HTML content or the table data for processing.")
            df.columns = ['Numcode', 'Charcode', 'Unit', 'Currency', 'Rate']
            return df
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    else:
        return df
    df.columns = ['Numcode', 'Charcode', 'Unit', 'Currency', 'Rate']
    return df