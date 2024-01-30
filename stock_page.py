from app import app

@app.route('/new_page')
def new_page():
    return "This is a new page"