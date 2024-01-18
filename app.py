from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Sample DataFrames
df1 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

df2 = pd.DataFrame({
    'X': ['A', 'B', 'C'],
    'Y': ['D', 'E', 'F']
})

@app.route('/')
def index():
    return render_template('index.html', tables=[df1.to_html(classes='data'), df2.to_html(classes='data')],
                           titles=['na', 'DataFrame 1', 'DataFrame 2'])

@app.route('/execute_function', methods=['POST'])
def execute_function():
    # Example Function
    print("Button Pressed")
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
