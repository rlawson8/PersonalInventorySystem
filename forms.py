#Using the BCrypt Algorith to hash and salt the password
import bcrypt
from DB_API import newUser, user_login, get_user


#Adding pepper
_pepper = 'Mizzou2022!_IMT'
#Adding salt
_salt = bcrypt.gensalt()


class Safe:
    def __init__(self, salt, hash):
        self.salt = salt
        self.hash = hash
def user_load(userID):
    thisUser = get_user(userID)

    if thisUser != None:
        root = thisUser.get(userID)
        returnUser = user(userID, root)
        return returnUser

    else:
        return None

def hash(password):
    #Adding pepper to password
    password = password + _pepper
    seasoning = _salt
    #Hashing password
    hash = bcrypt.hashpw(password.encode('utf-8'), seasoning)

    #safes everything into the object 'Safe'
    safe = Safe(seasoning, hash)

    #Returns the incrypted password
    return safe

def registration(username, email,  password):
    #Hashing password
    password = hash(password)
    #Storing username, email, and encrypted password and holds answer from database
    action = newUser(username, email, password)
    #Returns the answer from the database
    return action

##########We need to have login return a user object and not just a true or false.
def login(username, password):
    #Hashing password
    #password = hash(password)
    print(password)
    #Checks database if info is correct and stores answer
    action = user_login(username, password)
    #Conditional statements for answer from server since we probably shouldn't
    #say if just the username or password is worng
    if action == 403 or action == 409:
        return None
    else:
        return action


###Test Area###
"""
result = user_load('ilnam')
print(result)

result = hash('asdfg')
print(result)
testPass = 'asdfg' + _pepper
if bcrypt.checkpw(testPass.encode('utf-8'), result):
    print('match')
else:
    print('no dice')

code = login('trevorB', testPass)
print(code)

bdb = hash('abc123')"""
