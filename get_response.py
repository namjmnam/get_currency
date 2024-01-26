from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
from datetime import datetime, timedelta
script_directory = os.path.dirname(os.path.abspath(__file__))

def extract_between_parentheses(s):
    start = s.find('(') + 1
    end = s.find(')', start)
    return s[start:end] if start > 0 and end > start else s

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
    df.columns = ['Currency', 'KRW']
    return df

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
    df.columns = ['Currency', 'KRW', 'USD']
    return df

def delete_data(year, month, day):
    main_file = script_directory+f'/saved_data/{year}-{month}-{day}-main.csv'
    sub_file = script_directory+f'/saved_data/{year}-{month}-{day}-sub.csv'
    if os.path.exists(main_file):
        os.remove(main_file)
        print("File deleted.")
    else:
        print("File does not exist and cannot be deleted.")
    if os.path.exists(sub_file):
        os.remove(sub_file)
        print("File deleted.")
    else:
        print("File does not exist and cannot be deleted.")

def get_rate(year, month, day):
    main_file = script_directory+f'/saved_data/{year}-{month}-{day}-main.csv'
    sub_file = script_directory+f'/saved_data/{year}-{month}-{day}-sub.csv'
    if os.path.exists(main_file) and os.path.exists(sub_file):
        df1 = pd.read_csv(main_file)
        df2 = pd.read_csv(sub_file)
        df1.columns = ['Currency', 'KRW']
        df2.columns = ['Currency', 'KRW', 'USD']
        print("Files already exist")
    else:
        df1 = pd.DataFrame(columns=['통화명', '환율(원)'])
        df2 = pd.DataFrame(columns=['통화명', '환율(원)', 'Cross Rate(US$)'])
        try:
            if is_valid_date(year, month, day):
                # Open webpage
                url = f"http://www.smbs.biz/ExRate/TodayExRate.jsp?StrSch_Year={year}&StrSch_Month={month}&StrSch_Day={day}"
                chrome_options = Options()
                chrome_options.add_argument("--headless")  # Headless mode
                driver = webdriver.Chrome(options=chrome_options)
                driver.get(url)

                # Find all tables with class name 'table_type7'
                tables = driver.find_elements(By.CLASS_NAME, "table_type7")

                # List to store the content of each table
                tables_content = []

                # Iterate over the tables and extract their HTML content
                for table in tables:
                    tables_content.append(table.get_attribute('outerHTML'))

                # Get text
                first_table_text = tables[0].text
                table_text = tables[1].text

                # Make dataframes and print
                df1 = process_first_table_text(first_table_text)
                df2 = process_table_text(table_text)
                # print(df1.to_string(index=False))
                # print(df2.to_string(index=False))
                df1.columns = ['Currency', 'KRW']
                df2.columns = ['Currency', 'KRW', 'USD']
                df1['Currency'] = df1['Currency'].apply(extract_between_parentheses)
                df2['Currency'] = df2['Currency'].apply(extract_between_parentheses)

                # Close it
                driver.quit()
            else:
                df1.columns = ['Currency', 'KRW']
                df2.columns = ['Currency', 'KRW', 'USD']
                df1['Currency'] = df1['Currency'].apply(extract_between_parentheses)
                df2['Currency'] = df2['Currency'].apply(extract_between_parentheses)
                return df1, df2
        except:
            pass
        df1.to_csv(main_file, index=False)
        df2.to_csv(sub_file, index=False)

    # Move back to the last date of publishement
    if len(df1) == 0:
        year = int(year)
        month = int(month)
        day = int(day)

        # Creating a datetime object
        original_date = datetime(year, month, day)

        # Subtracting one day
        new_date = original_date - timedelta(days=1)

        # Convert the new date back to strings
        new_year = str(new_date.year)
        new_month = f"{new_date.month:02d}" # Formats the month as a zero-padded string
        new_day = f"{new_date.day:02d}" # Formats the day as a zero-padded string

        # print(new_year, new_month, new_day)
        return get_rate(new_year, new_month, new_day)
    df1.columns = ['Currency', 'KRW']
    df2.columns = ['Currency', 'KRW', 'USD']
    df1['Currency'] = df1['Currency'].apply(extract_between_parentheses)
    df2['Currency'] = df2['Currency'].apply(extract_between_parentheses)
    return df1, df2
