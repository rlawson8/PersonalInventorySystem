import mariadb
import sys
import bcrypt

class user:
    def __init__(self, userID, root_space):
        self.userID = userID
        self.rootSpace = root_space
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    def get_id(self):
        return self.userID

pepper = "Mizzou2022!_IMT"
#connects to the database and passes the cursor to the function needing the connection.
def connectToDB():
    try:
        db = mariadb.connect(
            user="trevor",
            password="Graduation",
            host="127.0.0.1",
            port=3306,
            database="tabs_db",

            # user="root",
            # password="capstone"
            # database="pis_db"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    #ALlows all of the insert statements to automatically be forwarded to the databse
    db.autocommit = True

    #Creates the cursor
    cur = db.cursor()

    #Returns cursor to the function calling for the connection.
    return cur



class Space_Object:
    def __init__(self, name, subspaces, items, id, parent_space):
        self.name = name
        self.spaces = subspaces
        self.items = items
        self.id = id
        self.parent_space = parent_space


#Checks if a username is taken. If it is the function exits with code 409. If not it checks if email is taken. If it is
#the function exits with code 410. If not it goes on to add the user and exits with code 200.
def newUser(username, email, user_password):
    #Calls the connect to DB function to get the curson.
    cur = connectToDB()

    #Get's the new_space_id
    new_space_id = max_space_id(cur)
    print(new_space_id)

    #Checks to see if the username is already taken returns code 409 if it is.
    print(username)
    try:
        cur.execute("SELECT user_id FROM person WHERE user_id =?", (username,))

        for x in cur:
            check=x
            x = check[0]
            if x == username:
                raise Exception('e')
            else:
                continue

    except:
        #Returns 409 if the username is taken.
        return 409

    #Checks if email is already taken returns 410 if it is.
    try:
        cur.execute("SELECT email FROM person WHERE email =?", (email,))
        for x in cur:
            check=x
            x = check[0]
            if x == email:
                raise Exception('e')
            else:
                continue
    except:
        #Returns 410 if the email is taken
        return 410


    #Test print
    #print(prev_id)

    #Test print
    #print(new_space_id)

    #Creates a name for the new user's root space.
    new_space_name = username + "s " + "space"

    #Separate the password.
    password_hash = user_password.hash
    seasoning = user_password.salt

    #Writes the INSERT statements for the space and person.
    cur.execute("INSERT INTO space (space_id, space_name) VALUES (?, ?)", (new_space_id, new_space_name))
    cur.execute("INSERT INTO person (user_id, email, password, root_space_id, seasoning) VALUES (?, ?, ?, ?, ?)", (username, email, password_hash, new_space_id, seasoning))

    #Test print.
    cur.execute("SELECT * FROM person")
    for x in cur:
        print(x)

    #Returns 200 if everything went ok.
    return 200


def load_item(name, group, description, quantity, consumable, image):
    cur = connectToDB()
    new_item_id = max_item_id(cur)

    try:
        cur.execute("SELECT space_id FROM space WHERE space_name =?",(group))
        spaceId = cur.fetchone()
        if spaceId == None:
            raise Exception('e')
        else:
            pass

    except:
        #Returns 409 if the space doesn't exist.
        return 409
    cur.execute("SELECT item_name FROM item WHERE item_name =? AND space_id =?", (name, spaceId))
    check = cur.fetchone()
    if(check == None):
        cur.execute("INSERT INTO item (item_id, item_name, description, quantity, consumable, image_location, space_id) VALUES (?, ?, ?, ?, ?, ?, ?)",(new_item_id, name, description, quantity, consumable, image, spaceId))
    else:
        cur.execute("UPDATE item SET quantity = quantity + 1 WHERE item_name =? AND space_id =?", (name, spaceId))
        
    return 200

#Creates a new primary key for an item.
def max_item_id(cur):
    cur.execute("SELECT MAX(item_id) FROM item;")
    for x in cur:
        # print(x)
        prev_id = x
    prev_id = prev_id[0]
    new_item_id = prev_id + 1
    return new_item_id


#Creates a new primary key for a space. Will be used when creating new users for root spaces and with creating new spaces.
def max_space_id(cur):
    cur.execute("SELECT MAX(space_id) FROM space;")
    for x in cur:
        # print(x)
        prev_id = x
    prev_id = prev_id[0]
    new_space_id = prev_id + 1
    return new_space_id





#Checks a username and password. Returns 409 if username isn't found. 403 if the password is incorrect. And 200 if everything
#goes through. Is used by login function from forms.py.

##########Need it to return a user object.
def user_login(username, password):

    ###connection to database
    cur = connectToDB()

    try:
    ###Queries the DB for user_id, password, and salt.
        cur.execute("SELECT user_id, password, seasoning, root_space_id FROM person WHERE user_id =?", (username,))
        #cur.execute(f"SELECT user_id FROM person WHERE user_id = 'ilnam'")

    ###Puts the results of the query in a list.
        for x in cur:
            person = x

        print(person)
        #user_username = person[0]

    ###Puts the user's stored pasword into a variable user_pass and then encodes it in utf-8
        user_pass = person[1]
        user_pass = user_pass.encode('utf-8')
        print(user_pass)

    ###Put's the user's salt into a variable salt, then encodes it in utf-8
        salt = person[2]
        salt = salt.encode('utf-8')
        print(salt)

    ###Put's the root space into a variable
        root_space = person[3]

    ###Adds the pepper to the provided password, then hashes submitted password with the user's salt
        password = password + pepper
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
        print(hashed_pass)

    ###Test prints
        print('******')
        print(user_pass)
        print(hashed_pass)

    ###Checks to see if the hashed submitted password is equal to the password stored in the DB and returns 200 if so and 403 if not.
        if hashed_pass == user_pass:
            #Returns 200 if password is good
            return user(username, root_space)
        else:
            #Returns 403 if pass is bad.
            return 403

    except:
        #Returns 409 if username can't be found.
        return 409



def addSpace(spaceName, parentSpaceName):
    cur = connectToDB()
    new_space_id = max_space_id(cur)
    print(parentSpaceName)
    try:
        cur.execute("SELECT space_id FROM space WHERE space_id =?",(parentSpaceName,))
        parentSpaceId = cur.fetchone()
        parentSpaceId = parentSpaceId[0]
        if parentSpaceId == None:
            raise Exception('e')
        else:
            pass
    except:
        #Returns 409 if the parent space doesn't exist.
        return 410

    """try:
        cur.execute("SELECT space_id FROM space WHERE space_name =?",(spaceName))
        spaceId = cur.fetchone()
        if parentSpaceId != None:
            raise Exception('e')
        else:
            pass
    except:
        #Returns 409 if the space already exists.
        return 409"""
    
    cur.execute("INSERT INTO space (space_id, space_name, parentspace_id) VALUES (?, ?, ?)",(new_space_id, spaceName, parentSpaceId))
        
    return 200


def get_space(space_identifier):
    print("It's hitting the function.")
    cur = connectToDB()
    cur.execute("SELECT space_name, parentspace_id FROM space WHERE space_id = ?", (space_identifier,))

    print("It's getting to the while loop.")
    for x in cur:
        name = x

    print(name)
    parent_space = name[1]
    name = name[0]
    print(parent_space)
    print(name)

    items = {}
    item_names = []
    item_ids = []

    ###Performs the database call for the items in a space.


    cur.execute("SELECT item_name, item_id FROM item WHERE space_id = ?", (space_identifier,))
    for (item_name, item_id) in cur:
        #print(item_name)
        #print(item_id)
        item_names.append(item_name)
        item_ids.append(item_id)

    ###Convert lists to dictionary with id:name pairs###
    for key in item_ids:
        for value in item_names:
            items[key] = value
            item_names.remove(value)
            break

    ###Test print of the items dict.###
    print(items)


    ###Initialize empty subspace lists and dictionary.###
    subspaces = {}
    subspace_names = []
    subspace_ids = []

    ###Perform the database call for the subspaces.###
    cur.execute("SELECT space_id, space_name FROM space WHERE parentspace_id = ?", (space_identifier,))
    for (space_name, space_id) in cur:
        subspace_names.append(space_name)
        subspace_ids.append(space_id)

    ###Test prints of the lists###
    #print(subspace_names)
    #print(subspace_ids)

    ###Converting lists to dictionary with name:id pairs###
    for key in subspace_ids:
        for value in subspace_names:
            subspaces[key] = value
            subspace_names.remove(value)
            break

    ###Test print of the concatinated dictionary###
    print(subspaces)

    #For later reference dictionary items are items, var name is name, subspaces are subspaces.
    if parent_space == None:
        parent_space = 0
    else:
        parent_space = int(parent_space)
    returnObject = Space_Object(name, subspaces, items, space_identifier, parent_space)

    return returnObject

def get_user(userID):
    cur = connectToDB()
    try:
        cur.execute("SELECT user_id, root_space_id FROM person WHERE user_id =?", (userID,))
        returnDict = {}
        for (user_id, root_space_id) in cur:
            returnDict[user_id] = root_space_id

        if len(returnDict) != 1:
            return None
        else:
            return returnDict

    except:
        #Returns 409 if the username is taken.
        return None


def load_user_helper(user_id):
    cur = connectToDB()
    cur.execute("SELECT root_space_id FROM person WHERE user_id =?", (user_id,))
    try:
        for x in cur:
            rootSpace = x

        rootSpace = rootSpace[0]
        returnObject = user(user_id, rootSpace)
        return returnObject
    except:
        return None

def deleteSpace(space_name):
    try:
        # ADD CODE HERE TO HANDLE MULTI LEVELS OF DELETING SPACES CURRENTLY ONLY WORKS FOR TWO LEVELS
        cur = connectToDB()
        cur.execute("DELETE FROM space WHERE parentspace_id = ?", (space_name,))
        cur.execute("DELETE FROM space WHERE space_id = ?", (space_name,))
    except:
        pass
def deleteItem(item_name):
    try:
        # pass
        cur = connectToDB()
        cur.execute("DELETE FROM item WHERE item_id = ?" (item_name,))
    except:
        pass



#Testing
pace = get_space(13)
print(pace)