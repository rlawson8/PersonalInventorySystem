#Using the BCrypt Algorith to hash and salt the password
import bcrypt
from DB_API import newUser, user_login, get_user, user
import boto3
import os
from PIL import Image, ImageDraw, ImageFilter


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

def connectToS3():
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id='AKIA2XTPVX4V6IHG55MK',
        aws_secret_access_key='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'
    )
    #for bucket in s3.buckets.all():
    #    print(bucket.name)

    return s3
def uploadPhoto(filename,item_id, user_id):
    filename = "./static/images/tmp/" + filename
    item_id = str(item_id)
    user_id = str(user_id)
    key = user_id + '*' + item_id
    s3 = connectToS3()
    s3.Bucket("tabsbucket").upload_file(Filename=filename, Key=key)
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("File doesn't exist.")
    return 200

def getPhoto(user_id, item_id):
    item_id = str(item_id)
    user_id = str(user_id)
    key = user_id + '*' + item_id
    location = "./static/images/tmp/" + key + ".jpg"

    try:
        s3 = connectToS3()
        #photo = s3.Bucket("tabsbucket").Object(key).get()
        s3.Bucket("tabsbucket").download_file(key, location)
        return 200
    except:
        return 410


def prepImage(path):
    print(path)
    image = Image.open(path)
    #gets image size for reference
    width, height = image.size
    print("Sizes gotten.")
    print(width)
    print(height)
    #crops image into the largest square it can
    if width > height:
        print("Width>Height")
        crop_width = ((width-height) //2)
        image = image.crop((0 + crop_width, 0, width - crop_width, height))
    elif height > width:
        print("Height>Width")
        crop_height = ((height - width) //2)
        #print(crop_height)
        image = image.crop((0, 0 + crop_height, width, height - crop_height))
    else:
        print("Height==Width")

    print("image cropped")
    image = image.resize((350, 350))
    print("image sized")
    image.save(path)

###Test Area###
#code = uploadPhoto("test_subject1*17.png", 17, "test_subject1")

