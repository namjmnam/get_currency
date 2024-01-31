from __main__ import app
from flask import request, render_template
from fetch_stock import codes_to_plt

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/submit', methods=['POST'])
def submit():
    start_date = request.form.get('startDate')
    end_date = request.form.get('endDate')
    primary_code = request.form.get('primaryCode')
    primary_value = request.form.get('primaryValue')
    additional_codes = request.form.getlist('additionalCode[]')
    additional_values = request.form.getlist('additionalValue[]')

    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")
    primary = [primary_code, primary_value]
    additional = [[a, b] for a, b in zip(additional_codes, additional_values)]
    print(start_date)
    print(end_date)
    print(primary)
    print(additional)

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

    # Works, but not working
    nm, df = codes_to_plt(primary, additional, start_date, end_date)
    data_json = df.to_json(orient='split')
    # print(data_json)
    return render_template('graph.html', data=data_json)
