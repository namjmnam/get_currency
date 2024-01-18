from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
from datetime import datetime

def is_valid_date(year, month, day):
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
    return df

def get_rate(year, month, day):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    main_file = script_directory+f'/saved_data/{year}-{month}-{day}-main.csv'
    sub_file = script_directory+f'/saved_data/{year}-{month}-{day}-sub.csv'
    if os.path.exists(main_file) and os.path.exists(sub_file):
        df1 = pd.read_csv(main_file)
        df2 = pd.read_csv(sub_file)
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

                # Close it
                driver.quit()
            else:
                return df1, df2
        except:
            pass
        df1.to_csv(main_file, index=False)
        df2.to_csv(sub_file, index=False)
    return df1, df2
