#Using the BCrypt Algorith to hash and salt the password
import bcrypt

#Adding pepper
_pepper = 'Mizzou2022!_IMT'
#Adding salt
_salt = bcrypt.gensalt()
#Number placeholde
x = 0
#Login attemps
login_error = 0

#Temporary values for testing
_tempUser = "error"
_tempPass = "error"
_tempSerial = 0

def hash(password):
    #Adding pepper to password
    password = password + _pepper
    #Hashing password
    safe = bcrypt.hashpw(password.encode('utf-8'), _salt)

    return safe

def registration(username, email,  password):
    #Hashing password
    hash(password)
    #Storing username
    _tempUser = username
    #Storing encrypted password
    _tempPass = safe
    #Storing serial number
    x = x + 1
    _tempSerial = str(x).zfill(4)
    #Storing systematic name
    _tempsystematicName = username[:len(username)//2] + 'Space'

def login(username, password):
    #temporary for testing
    _tempPass = 'Admin'
    _tempPass = _tempPass + _pepper
    temp = bcrypt.hashpw(_tempPass.encode('utf-8'), _salt)
    #Hashing password
    hash(password)
    #Comparing inputs to database
    if username == 'Admin':
        if safe == temp:
            login_error = 0
            return True
    login_error = login_error + 1
    return False