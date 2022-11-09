import mariadb
import sys

#connects to the database and passes the cursor to the function needing the connection.
def connectToDB():
    try:
        db = mariadb.connect(
            user="trevor",
            password="Graduation",
            host="127.0.0.1",
            port=3306,
            database="PIS_DB"

            #user="root",
            #password="root",
            #database="pis_db"
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






#Checks if a username is taken. If it is the function exits with code 409. If not it checks if email is taken. If it is
#the function exits with code 410. If not it goes on to add the user and exits with code 200.
def newUser(username, email, password):
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
    new_space_name = username + "'s " + "space"

    #Writes the INSERT statements for the space and person.
    cur.execute("INSERT INTO space (space_id, space_name) VALUES (?, ?)", (new_space_id, new_space_name))
    cur.execute("INSERT INTO person (user_id, email, password, root_space_id) VALUES (?, ?, ?, ?)", (username, email, password, new_space_id))

    #Test print.
    cur.execute("SELECT * FROM person")
    for x in cur:
        print(x)

    #Returns 200 if everything went ok.
    return 200







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
#goes through.
def user_login(username, password):
    cur = connectToDB()

    try:
        cur.execute("SELECT user_id, password FROM person WHERE user_id =?", (username,))
        #cur.execute(f"SELECT user_id FROM person WHERE user_id = 'ilnam'")

        for x in cur:
            person = x
        #user_username = person[0]
        user_pass = person[1]

        #prints user and pass
        #print(user_username)
        #print(user_pass)

        #Verifies user submitted correct password.
        if user_pass != password:
            #Returns 403 is password is incorrect
            return 403
        else:
            #Returns 200 if pass is good.
            return 200

    except:
        #Returns 409 if username can't be found.
        return 409






code = newUser('serverTest', 'test@robtert.com', 'bubbadubbas')
print(code)
code = user_login('bobby', 'wiejfoiwjf')
print(code)

