"""Application entry point."""
from crypt import methods
from django.shortcuts import redirect
from flask import Flask, render_template, request, url_for, flash
from forms import registration, login


app = Flask(__name__)

if __name__ == "__main__":
	app.run(host='0.0.0.0')

@app.route('/')
def hello_world():
    return render_template("HomePage.html")

@app.route('/home')
def home():
    return render_template("HomePage.html")

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    #check for POST submition of form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login(username, password):
            return redirect(url_for('app.home'))
        else:
            flash('Invalid Credentials please try again.') #this and the line above need to be tested one might work hopefully
            return redirect(url_for('app.login'))
    return render_template("login.html")

@app.route('/createAccount', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
		username = request.form['username']
        password = request.form['password']
        email = request.form['email']
		action = registration(username, email,  password)
        #check here to see if the email and username has already been used by performing a query
        #if the above query is true flash the below message and direct back to the signup page using:
        #return redirect(url_for('app.createAccount'))
        #flash('Email address already exists')
        #create a new user with the form data and hash the password so the plaintext version isn't saved this is where we canc all the method in forms.py
        #add the new user to the database
		if action == 409:
			flash('Username already exists')
			return render_template("register.html")
		elif action == 410:
			flash('Email address already exists')
			return render_template("register.html")
		else:
			flash('Thank you for creating your account '+username)
			return render_template("HomePage.html")
    return render_template("register.html")

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
