#Using the BCrypt Algorith to hash and salt the password
import bcrypt
from DB_API import newUser, user_login

#Adding pepper
_pepper = 'Mizzou2022!_IMT'
#Adding salt
_salt = bcrypt.gensalt()

def hash(password):
    #Adding pepper to password
    password = password + _pepper
    #Hashing password
    safe = bcrypt.hashpw(password.encode('utf-8'), _salt)
    #Returns the incrypted password
    return safe

def registration(username, email,  password):
    #Hashing password
    hash(password)
    #Storing username, email, and encrypted password and holds answer from database
    action = newUser(username, email, password)
    #Returns the answer from the database
    return action

def login(username, password):
    #Hashing password
    hash(password)
    #Checks database if info is correct and stores answer
    action = user_login(username, password)
    #Conditional statements for answer from server since we probably shouldn't
    #say if just the username or password is worng
    if action == 403 or action == 409:
        return False
    else:
        return True
