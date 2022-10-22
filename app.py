"""Application entry point."""
from flask import Flask, render_template, request


app = Flask(__name__)

if __name__ == '__main__':
    app.run()

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("index.html", home=True)

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    #check for POST submition of form
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

    return render_template("login.html")

@app.route('/createAccount')
def create_account():
    return "This is the account creation page. "

@app.route('/design')
def space_design():
    return render_template("design.html")

@app.route('/details')
def detail_page():
    return "This is the item details page."

@app.route('/load')
def loading_page():
    return "This is the loading page."

@app.route('/find')
def query_page():
    return "This is the query page."

