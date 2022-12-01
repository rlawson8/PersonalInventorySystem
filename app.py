"""Application entry point."""
import flask_login
from flask import Flask, render_template, request, url_for, flash, session
from forms import *
from DB_API import *
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import os
from PIL import Image

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = '_5#y2LF4Q8z*n*xec]/'
app.config['UPLOAD_FOLDER'] = './static/images/tmp/'

@login_manager.user_loader
def load_user(user_id):
    user = load_user_helper(user_id)
    return user

@app.route('/')
def hello_moto():
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
            return render_template('design.html', subspaces = space.spaces, items = space.items, space_name = space.name, space_id = space.id)
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
            return render_template('register.html')
        elif action == 410:
            flash('Email address already exists')
            return render_template("register.html")
        else:
            flash('Thank you for creating your account '+username)
            return render_template("login.html")
    return render_template("register.html")

@app.route('/design', methods=['GET','POST'])
@login_required
def space_design():

    try:
        urlRequest = request.url
        urlRequest = urlRequest.split('?')
        urlRequest = urlRequest[1]
        urlRequest = urlRequest.split('=')
        space_id = urlRequest[1]

        print(space_id)
        space = get_space(space_id)
        return render_template("design.html", subspaces = space.spaces, items = space.items, space_name = space.name, space_id = space.id, parent_space = space.parent_space)
        print(urlRequest)
    except:
        pass

    if '_user_id' in session.keys():
        user = load_user(session['_user_id'])
        space = get_space(user.rootSpace)

    if request.method == 'POST':
        form = request.form['formSelector']

        if 'addspace' in request.form:
            spaceName = request.form['spaceName']
            parentSpaceName = request.form['parentSpaceName']

            action = addSpace(spaceName, parentSpaceName, user.userID)
            space = get_space(parentSpaceName)
            if action == 409:
                flash('Space name already exists')
                return render_template("design.html", subspaces = space.spaces, items = space.items, space_name = space.name, space_id = space.id, parent_space = space.parent_space)
            elif action == 410:
                flash('Parent space does not exist')
                return render_template("design.html", subspaces = space.spaces, items = space.items, space_name = space.name, space_id = space.id, parent_space = space.parent_space)
            else:
                return render_template("design.html", subspaces = space.spaces, items = space.items, space_name = space.name, space_id = space.id, parent_space = space.parent_space)
        elif 'deleteform' in request.form:
            # parentSpaceName = request.form['parentSpaceName']
            # space = get_space(parentSpaceName)
            itemChoice = request.form['choice1']
            subspaceChoice = request.form['choice2']
            parentSpaceName = request.form['parentSpaceName']

            print(itemChoice)
            print(subspaceChoice)

            deleteSpace(subspaceChoice)
            deleteItem(itemChoice)

            user = load_user(session['_user_id'])
            space = get_space(parentSpaceName)

            return render_template("design.html", subspaces=space.spaces, items=space.items, space_name=space.name, space_id=space.id, parent_space=space.parent_space)
        elif 'addItem' in request.form:
            itemName = request.form['itemName']
            parentSpaceID = request.form['parentSpaceID']

            action = quickAddItem(itemName, parentSpaceID, user.userID)
            space = get_space(parentSpaceID)
            print(action)
            if action == 410:
                flash('This item already exists.')
                return render_template("design.html", subspaces=space.spaces, items=space.items, space_name=space.name,
                                       space_id=space.id, parent_space=space.parent_space)
            else:
                return render_template("design.html", subspaces=space.spaces, items=space.items, space_name=space.name,
                                       space_id=space.id, parent_space=space.parent_space)
        else:
            pass



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

    return render_template("design.html", subspaces = space.spaces, items = space.items, space_name = space.name, space_id = space.id, parent_space=space.parent_space)

@app.route('/details')
@login_required
def detail_page():
    try:
        urlRequest = request.url
        urlRequest = urlRequest.split('?')
        urlRequest = urlRequest[1]
        urlRequest = urlRequest.split('=')
        item_id = urlRequest[1]
        print(item_id)
        code = getPhoto(current_user.userID, item_id)
        print(code)
        if code == 200:
            #Makes the path for the photo.
            photoName = str(current_user.userID) + '*' + str(item_id) + '.jpg'
            photo = "./static/images/tmp/" + photoName
            #Preps the image.
            prepImage(photo)
            print('Photo prep complete.')

            item = getItem(item_id)
            space = get_space(item.spaceID)
            print("With Pic")
            return render_template("itemdetails.html", item_name = item.itemName, space_name = space.name, space_id = space.id, item_quantity = item.quantity, item_consumable = item.consumable, item_description = item.description, item_image = photo)
        else:
            item = getItem(item_id)
            space = get_space(item.spaceID)
            return render_template("itemdetails.html", item_name = item.itemName, space_name = space.name, space_id = space.id,item_quantity = item.quantity, item_consumable = item.consumable, item_description = item.description, item_image = None)
    except Exception as e:
        print(e)
    return render_template("itemdetails.html")

@app.route('/load', methods=['GET','POST'])
@login_required
def loading_page():
    if request.method == "POST":
        name = request.form['itemName']
        space = request.form['groupName']
        quantity = request.form['quantity']
        if 'consumable' in request.form:
            consumable = request.form['consumable']
        else:
            consumable = 0
        if 'description' in request.form:
            description = request.form['description']
        pic = request.files['uploadfile']
        pic = pic.filename
        if pic != '':
            print("It sees a pic")
            picture = request.files['uploadfile']

            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture.filename))
            filename = picture.filename
            print("picture saved")
            code = addItem(name, description, quantity, consumable, space, current_user.userID, None)
            id = get_itemID(name, current_user.userID)
            print("item added")
            print(code)
            if code == 409:
                flash("Space name does not exist")
                cu = current_user.userID
                spaces = get_all_spaces(cu)
                return render_template("loaditems.html", spaces = spaces)
            else:
                code == uploadPhoto(filename, id, current_user.userID)
                flash("Success!")
                cu = current_user.userID
                spaces = get_all_spaces(cu)
                return render_template("loaditems.html", spaces = spaces)
        else:
            code = addItem(name, description, quantity, consumable, space, current_user.userID, None)
            if code == 409:
                flash("Space name does not exist")
                cu = current_user.userID
                spaces = get_all_spaces(cu)
                return render_template("loaditems.html", spaces = spaces)
            else:
                flash("Success!")
                cu = current_user.userID
                spaces = get_all_spaces(cu)
                return render_template("loaditems.html", spaces = spaces)
    else:


    #Get data for drop down.
        cu = current_user.userID
        spaces = get_all_spaces(cu)
        return render_template("loaditems.html", spaces = spaces)

@app.route('/itemSearch', methods=["POST", "GET"])
def findResults():
    if request.method == "POST" :
        search_word = request.form['search']
        print(search_word)
        results = appFunctionSearch(current_user.userID, search_word)

        spaces = results[0]
        items = results[1]

        print(spaces)
        print("Items")
        print(items)
        return render_template("finditems.html", search_word=search_word, spaces=spaces, items=items)
    return render_template("finditems.html")

@app.route('/response')
@login_required
def query_page():
    if request.method == "POST" :
        search_word = request.form['search']
        print(search_word)
        results = appFunctionSearch(search_word)

        return render_template(response.html, search_word=search_word, results=results)
    return render_template("response.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("HomePage.html")

@app.route('/scannerLoad', methods=["GET", "POST"])
@login_required
def scannerLoad():
    if request.method == "POST" :
        barcode = request.form['barcode']
        location = request.form['location']
        space_id = location.split('?')
        space_id = space_id[1]
        space_id = space_id.split('=')
        space_id = space_id[1]

        print("Location: " + location + " Barcode: " + barcode + " Space: " + space_id)
        item = productLookup(barcode, current_user.userID)

        name = item[0]
        description = item[1]
        photoURL = item[2]
        quantity = get_quantity(name, current_user.userID)

        #have to stop now, but see if you can get it to increment the quantity.
        code = addItem(name, description, quantity + 1, None, space_id, current_user.userID, barcode)
        item_id = get_itemID(name, current_user.userID)
        submitPhoto(photoURL, current_user.userID, item_id)
        if code == 409:
            flash("Space name does not exist")
            cu = current_user.userID
            spaces = get_all_spaces(cu)
            return render_template("loaditems.html", spaces=spaces)
        else:
            flash("Success!")
            cu = current_user.userID
            spaces = get_all_spaces(cu)
            return render_template("loaditems.html", spaces=spaces)


        flash("Success!")
        return render_template("scannerLoad.html")

    return render_template("scannerLoad.html")

@app.route('/qr', methods=["GET"])
def qrPage():
    urlRequest = request.url
    urlRequest = urlRequest.split('?')
    urlRequest = urlRequest[1]
    urlRequest = urlRequest.split('=')
    space_id = urlRequest[1]
    return render_template("qr.html", space_id=space_id)

@app.errorhandler(500)
def pageNotFound(error):
    flash('Please login or create an account first')
    return render_template("login.html")

