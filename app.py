from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime
from get_response import get_rate
from get_response import delete_data
from get_russian import get_rurate

def get_today_date():
    # Function to get today's date in 'YYYY', 'MM', 'DD' format
    today = datetime.now()
    return today.strftime('%Y'), today.strftime('%m'), today.strftime('%d')

year, month, day = get_today_date()
df1, df2 = get_rate(year, month, day)
df3 = get_rurate(year, month, day)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', tables=[df1.to_html(classes='data'), df2.to_html(classes='data'), df3.to_html(classes='data')],
                            titles=[f"{year}-{month}-{day}", 'Main', 'Sub', 'Rus'],
                            input_year=year, input_month=month, input_day=day)

@app.route('/update_dataframes', methods=['POST'])
def update_dataframes():
    new_year = request.form.get('input_year')
    new_month = request.form.get('input_month')
    new_day = request.form.get('input_day')
    df1, df2 = get_rate(new_year, new_month, new_day)
    df3 = get_rurate(new_year, new_month, new_day)
    return render_template('index.html', 
                            tables=[df1.to_html(classes='data'), df2.to_html(classes='data'), df3.to_html(classes='data')],
                            titles=[f"{new_year}-{new_month}-{new_day}", 'Main', 'Sub', 'Rus'],
                            input_year=new_year, input_month=new_month, input_day=new_day)

# Working, but unused
# @app.route('/delete', methods=['POST'])
# def delete_saved():
#     year = request.form.get('input_year')
#     month = request.form.get('input_month')
#     day = request.form.get('input_day')
#     delete_data(year, month, day)

@app.route('/get_main_data/<date>')
def get_main_dataframe(date):
    # Convert the string date to a datetime object, handle exceptions if format is incorrect
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_string = date_obj.strftime('%Y-%m-%d')
        year, month, day = date_string.split('-')

        df1, df2 = get_rate(year, month, day)
        df1.set_index('Currency', inplace=True)
        return jsonify(df1.to_dict())
        # return jsonify(df1.to_dict(orient='index'))

    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD.", 400

@app.route('/get_main_data/<date>/<key>')
def get_main_dataframe_key(date, key):
    # Convert the string date to a datetime object, handle exceptions if format is incorrect
    print(key)
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_string = date_obj.strftime('%Y-%m-%d')
        year, month, day = date_string.split('-')

        df1, df2 = get_rate(year, month, day)
        df1.set_index('Currency', inplace=True)

        # Split the key on "-" and then navigate through the data frame
        key = key.replace("_", " ")
        keys = key.split('-')
        print(keys)
        data = df1
        for k in keys:
            if k.isdigit():
                k = int(k)  # Convert to integer if the key is a digit
            print(data[k])
            data = data[k]  # Navigate through the DataFrame or Series

        return jsonify(data)

    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD.", 400
    except KeyError:
        return "Key not found in the data.", 404
    except IndexError:
        return "Index out of range.", 404

@app.route('/get_sub_data/<date>')
def get_sub_dataframe(date):
    # Convert the string date to a datetime object, handle exceptions if format is incorrect
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_string = date_obj.strftime('%Y-%m-%d')
        year, month, day = date_string.split('-')

        df1, df2 = get_rate(year, month, day)
        df2.set_index('Currency', inplace=True)
        return jsonify(df2.to_dict())
        # return jsonify(df2.to_dict(orient='index'))

    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD.", 400

@app.route('/get_sub_data/<date>/<key>')
def get_sub_dataframe_key(date, key):
    # Convert the string date to a datetime object, handle exceptions if format is incorrect
    print(key)
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_string = date_obj.strftime('%Y-%m-%d')
        year, month, day = date_string.split('-')

        df1, df2 = get_rate(year, month, day)
        df2.set_index('Currency', inplace=True)

        # Split the key on "-" and then navigate through the data frame
        key = key.replace("_", " ")
        keys = key.split('-')
        print(keys)
        data = df2
        for k in keys:
            if k.isdigit():
                k = int(k)  # Convert to integer if the key is a digit
            print(data[k])
            data = data[k]  # Navigate through the DataFrame or Series

        return jsonify(data)

    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD.", 400
    except KeyError:
        return "Key not found in the data.", 404
    except IndexError:
        return "Index out of range.", 404

@app.route('/get_rus_data/<date>')
def get_rus_dataframe(date):
    # Convert the string date to a datetime object, handle exceptions if format is incorrect
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_string = date_obj.strftime('%Y-%m-%d')
        year, month, day = date_string.split('-')

        df3 = get_rurate(year, month, day)
        # Not a regular c. Same for Num code
        df3.set_index('Charcode', inplace=True)
        return jsonify(df3.to_dict())
        # return jsonify(df3.to_dict(orient='index'))

    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD.", 400

@app.route('/get_rus_data/<date>/<key>')
def get_rus_dataframe_key(date, key):
    # Convert the string date to a datetime object, handle exceptions if format is incorrect
    print(key)
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_string = date_obj.strftime('%Y-%m-%d')
        year, month, day = date_string.split('-')

        df3 = get_rurate(year, month, day)
        df3.set_index('Charcode', inplace=True)
        # Change applied

        # Split the key on "-" and then navigate through the data frame
        key = key.replace("_", " ")
        keys = key.split('-')
        print(keys)
        data = df3
        # json_result = data.to_json()
        # print(json_result)
        for k in keys:
            if k.isdigit():
                k = int(k)  # Convert to integer if the key is a digit
            data = data[k]  # Navigate through the DataFrame or Series

        return jsonify(data)

    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD.", 400
    except KeyError:
        return "Key not found in the data.", 404
    except IndexError:
        return "Index out of range.", 404

@app.route('/test')
def test_route():
    return "Test route works"

import stock_page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)