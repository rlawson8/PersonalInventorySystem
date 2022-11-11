"""Application entry point."""
from flask import Flask, render_template, request, url_for, flash
from forms import registration, login
from DB_API import *
from flask_login import LoginManager, login_required, current_user, login_user

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = '_5#y2LF4Q8z*n*xec]/'

@login_manager.user_loader
def load_user(user_id):
    user = load_user_helper(user_id)
    return user

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

        user_object = login(username, password)
        print(user_object)
        if user_object != None:
            login_user(user_object)
            space = get_space(user_object.rootSpace)
            return render_template('design.html', subspaces = space.spaces, itemss = space.items, space_name = space.name)
        else:
            flash('Invalid Credentials please try again.') #this and the line above need to be tested one might work hopefully
            return render_template("login.html")
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
            return redirect(url_for('register.html'))
        elif action == 410:
            flash('Email address already exists')
            return redirect(url_for("register.html"))
        else:
            flash('Thank you for creating your account '+username)
            return render_template("login.html")
    return render_template("register.html")

@app.route('/design')
@login_required
def space_design():



    """
    #test data to test the front end functionality
    subspaces_dict = {"Living Room" : "home",
                      "Kitchen" : "login",
                      "Dining Room" : "createAccount"}
    items_dict = {"Coasters" : "2343",
                  "Fabreeze" : "23234",
                  "Paper Towel" : "2212",
                  "Lip Balm" : "9985"}
    spaceName = "Bobert's Space"
    """
    space = get_space(1)

    return render_template("design.html", subspaces = space.spaces, items = space.items, space_name = space.name)

@app.route('/details')
def detail_page():
    return "This is the item details page."

@app.route('/load')
def loading_page():

    return "This is the loading page."

@app.route('/find')
def query_page():
    return "This is the query page."



"""Things to do.
Add back end for design page. -- Trevor

Interface with the buttons for add space, and delete. -- Reid

Customize login required to not throw internal server error. --Trevor

Finish loading page tasks. 

For nav bar if you click on user icon it has drop down that has options for logout if the current_user.is_authenticated == True or login/registration if current_user.is_authenticated == False

Hydrate
"""

