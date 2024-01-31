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

    # Extracting the table with summary '시가총액 정보'
    table = soup.find('table', {'summary': '시가총액 정보'})
    if table is not None:
        # Using StringIO to treat the HTML string as a file-like object
        html_string = str(table)
        df = pd.read_html(StringIO(html_string))[0]
    return df

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
        df['지주시총'] = df['종가'] * shrout * ratio / 100000000

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
        return nm, df[['날짜', '지주시총', '종속시총']]

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
