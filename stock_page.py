from __main__ import app
from flask import request, render_template

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

    # Process your data here
    # ...

    return "Data Received"
