from urllib import parse
from ast import literal_eval
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime
from io import StringIO
import os
script_directory = os.path.dirname(os.path.abspath(__file__))

def get_data(code, start_time, end_time, time_from='day') :
    get_param = {
    	'symbol':code,
	    'requestType':1,
	    'startTime':start_time,
	    'endTime':end_time,
	    'timeframe':time_from
    }
    get_param = parse.urlencode(get_param)
    url="https://api.finance.naver.com/siseJson.naver?%s"%(get_param)
    response = requests.get(url)
    print(url)
    return literal_eval(response.text.strip())

def polling_api(code='064850'):
    test_url = f"https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{code}"

    response = requests.get(test_url)
    data = response.json()
    trimmed_data = data['result']['areas'][0]['datas'][0]
    current_price = trimmed_data['nv']
    eps = trimmed_data['eps']
    bps = trimmed_data['bps']
    nm = trimmed_data['nm']
    print('price:', current_price)
    print('EPS:', eps)
    print('BPS:', bps)
    print('종목:', nm)
    return nm

def get_start_end_dates():
    class DateSelection:
        def __init__(self):
            self.start_date = None
            self.end_date = None

    def print_dates():
        start_date_str = start_cal.get_date()
        end_date_str = end_cal.get_date()
        start_date = datetime.datetime.strptime(start_date_str, '%m/%d/%y')
        end_date = datetime.datetime.strptime(end_date_str, '%m/%d/%y')
        date_selection.start_date = start_date.strftime('%Y%m%d')
        date_selection.end_date = end_date.strftime('%Y%m%d')
        root.destroy()

    date_selection = DateSelection()

    # Create the main window
    root = tk.Tk()
    root.title("Date Range Picker")

    # Calculate default dates
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)

    # Create the start date calendar
    start_cal = Calendar(root, selectmode='day', year=one_year_ago.year, month=one_year_ago.month, day=one_year_ago.day)
    start_cal.grid(row=0, column=0, padx=10, pady=10)

    # Create the end date calendar
    end_cal = Calendar(root, selectmode='day', year=today.year, month=today.month, day=today.day)
    end_cal.grid(row=0, column=1, padx=10, pady=10)

    # Create a submit button
    submit_button = tk.Button(root, text="Submit", command=print_dates)
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Run the application
    root.mainloop()

    return date_selection.start_date, date_selection.end_date

def get_codes(code="001940", ratio="100"):
    def add_input_box():
        frame = tk.Frame(root)
        frame.pack(pady=2, before=add_button_frame)

        new_entry = tk.Entry(frame, width=20)
        new_entry.pack(side='left', padx=2)

        # Percentage entry and dropdown
        percentage_frame = tk.Frame(frame)
        percentage_frame.pack(side='left', padx=2)

        new_percentage = tk.Entry(percentage_frame, width=5)
        new_percentage.pack(side='left')

        percentage_options = [f"{i}%" for i in range(0, 101, 10)]
        percentage_dropdown = ttk.Combobox(percentage_frame, values=percentage_options, width=3)
        percentage_dropdown.pack(side='left')
        percentage_dropdown.bind("<<ComboboxSelected>>", lambda event, box=new_percentage: update_percentage(event, box))

        input_frames.append((new_entry, new_percentage, percentage_dropdown))

    def update_percentage(event, entry_box):
        entry_box.delete(0, tk.END)
        entry_box.insert(0, event.widget.get().strip('%'))

    def submit():
        nonlocal primary_input, additional_inputs

        # Fetch primary data
        primary_input = [input_frames[0][0].get(), input_frames[0][1].get()]

        # Fetch additional data
        additional_inputs = [[entry.get(), percentage.get()] for entry, percentage, _ in input_frames[1:]]

        # Close the window
        root.destroy()

    # Initialize primary_input and additional_inputs
    primary_input = [None, None]
    additional_inputs = []

    # Main window
    root = tk.Tk()
    root.title("Input Boxes")

    # List to hold all entry frames
    input_frames = []

    # Label for the first input box
    primary_label = tk.Label(root, text="Primary Code")
    primary_label.pack()

    # Create first input box with percentage
    frame = tk.Frame(root)
    frame.pack(pady=2)

    entry = tk.Entry(frame, width=20)
    entry.pack(side='left', padx=2)
    entry.insert(0, code)  # Default value

    # Percentage entry and dropdown for first input
    percentage_frame = tk.Frame(frame)
    percentage_frame.pack(side='left', padx=2)

    percentage = tk.Entry(percentage_frame, width=5)
    percentage.pack(side='left')
    percentage.insert(0, ratio)  # Default value

    percentage_options = [f"{i}%" for i in range(0, 101, 10)]
    percentage_dropdown = ttk.Combobox(percentage_frame, values=percentage_options, width=3)
    percentage_dropdown.pack(side='left')
    percentage_dropdown.bind("<<ComboboxSelected>>", lambda event, box=percentage: update_percentage(event, box))

    input_frames.append((entry, percentage, percentage_dropdown))

    # Label for the second input box
    additional_label = tk.Label(root, text="Additional Codes")
    additional_label.pack()

    # '+' Button and 'Submit' button frame
    add_button_frame = tk.Frame(root)
    add_button_frame.pack(pady=5)

    # '+' Button to add more input boxes
    add_button = tk.Button(add_button_frame, text='+', command=add_input_box)
    add_button.pack(side='left', padx=5)

    # Submit button
    submit_button = tk.Button(add_button_frame, text="Submit", command=submit)
    submit_button.pack(side='left', padx=5)

    # Run the application
    root.mainloop()

    # Return values after window is closed
    return primary_input, additional_inputs

def codes_to_plt(primary_code, additional_codes, start_date, end_date):
    code = primary_code[0]
    ratio = float(primary_code[1])/100
    rows = get_data(code, start_date, end_date)
    if len(rows)!=1:
        df = pd.DataFrame(rows)
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])

        # Set the font to a known Korean-supporting font
        # https://noonnu.cc/font_page/34
        korean_font_path = script_directory + '/NotoSansKR-Regular.ttf'
        korean_font = fm.FontProperties(fname=korean_font_path)

        plt.rcParams['font.family'] = korean_font.get_name()

        # Converting '날짜' to datetime for better plotting
        df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d')
        
        shrout = int(fetch_financial_data(code).iloc[2, 1])
        df['종가'] = df['종가'] * shrout * ratio / 100000000

        # Create 종속회사 시총
        df['종속시총'] = 0

        for pair in additional_codes:
            print(pair)
            sub_code = pair[0]
            sub_ratio = float(pair[1])/100
            sub_rows = get_data(sub_code, start_date, end_date)
            if len(sub_rows)!=1:
                sub_df = pd.DataFrame(sub_rows)
                sub_df.columns = sub_df.iloc[0]
                sub_df = sub_df.drop(sub_df.index[0])
                sub_shrout = int(fetch_financial_data(sub_code).iloc[2, 1])
                sub_df['종가'] = sub_df['종가'] * sub_shrout * sub_ratio / 100000000
                df['종속시총'] = df['종속시총'] + sub_df['종가']

        nm = polling_api(code)
        # Plotting the graph
        plt.figure(figsize=(10, 6))
        plt.plot(df['날짜'], df['종가'], color='blue', linestyle='-', marker='', label='지주시총')
        plt.plot(df['날짜'], df['종속시총'], color='gray', linestyle='-', marker='', label='종속시총')
        plt.title(f'{nm} 지주-종속 시총 비교', fontproperties=korean_font)
        plt.xlabel('날짜', fontproperties=korean_font)
        plt.ylabel('시계열 시가총액(억원)', fontproperties=korean_font)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        # Show the plot
        plt.show()

def fetch_financial_data(code="001940"):
    df = pd.DataFrame()
    url = f"https://finance.naver.com/item/main.nhn?code={code}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Fetching the web page
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to retrieve data"

    # Parsing the web page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Getting the content of class 'aside_invest_info'
    # invest_info = soup.find(class_='aside_invest_info')
    # if invest_info is not None:
    #     print("Invest Info:\n", invest_info.text.strip())

    # Extracting the table with summary '시가총액 정보'
    table = soup.find('table', {'summary': '시가총액 정보'})
    # if table is not None:
    #     # Converting the table to pandas dataframe
    #     df = pd.read_html(str(table))[0]
    #     print("Table Data:\n", df)
    if table is not None:
        # Using StringIO to treat the HTML string as a file-like object
        html_string = str(table)
        df = pd.read_html(StringIO(html_string))[0]
        # Accessing the value of the 3rd row and 2nd column
        # value = df.iloc[2, 1]
        # print("Value at 3rd row, 2nd column:", value)
    return df

# 예시
# 삼성전자 005930
# 에프앤가이드 064850

# 지주/종속
# 키스코홀딩스 001940
# 한국철강 104700 51.81
# 환영철강공업 83.50 - K-OTC 현재 미지원

# 아세아 002030
# 아세아시멘트 183190 53.94
# 아세아제지 002310 47.19

# start_date, end_date = get_start_end_dates()
start_date, end_date = "20171230", "20240126"
primary_code, additional_codes = get_codes("002030")
print(primary_code)
print(additional_codes)
input()
codes_to_plt(primary_code, additional_codes, start_date, end_date)

# Issue
# K-OTC 주가 가져오는 알고리즘 필요