from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from datetime import datetime
from get_response import get_rate

def get_today_date():
    # Function to get today's date in 'YYYY', 'MM', 'DD' format
    today = datetime.now()
    return today.strftime('%Y'), today.strftime('%m'), today.strftime('%d')

year, month, day = get_today_date()
df1, df2 = get_rate(year, month, day)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', tables=[df1.to_html(classes='data'), df2.to_html(classes='data')],
                            titles=[f"{year}-{month}-{day}", 'Main', 'Sub'])

@app.route('/update_dataframes', methods=['POST'])
def update_dataframes():
    # new_year, new_month, new_day = '2024', '01', '09'
    new_year = request.form.get('input_year')
    new_month = request.form.get('input_month')
    new_day = request.form.get('input_day')
    df1, df2 = get_rate(new_year, new_month, new_day) # Generate new dataframes
    return render_template('index.html', 
                            tables=[df1.to_html(classes='data'), df2.to_html(classes='data')],
                            titles=[f"{new_year}-{new_month}-{new_day}", 'Main', 'Sub'])

if __name__ == '__main__':
    app.run(debug=True)
