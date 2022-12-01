#Using the BCrypt Algorith to hash and salt the password
import bcrypt
from DB_API import newUser, user_login, get_user, user
import boto3
import os
from PIL import Image, ImageDraw, ImageFilter
import requests
import json


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
    print("Function: connectToS3")
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id='AKIA2XTPVX4VY6MMG5ZD',
        aws_secret_access_key='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'
    )
    #for bucket in s3.buckets.all():
    #    print(bucket.name)

    return s3
def uploadPhoto(filename,item_id, user_id):
    print("Function: uploadPhoto")
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


def prepImage(photo):
    image = Image.open(photo)
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
    print(photo)
    image = image.convert('RGB')
    image.save(photo)


def productLookup(barcode, cu):
    url = "https://product-lookup-by-upc-or-ean.p.rapidapi.com/code/" + str(barcode)
    headers = {
        "X-RapidAPI-Key": "3dbeec8d00msh776115b9d0450a2p14917cjsn1603398d5c77",
        "X-RapidAPI-Host": "product-lookup-by-upc-or-ean.p.rapidapi.com"
    }


    response = requests.request("GET", url, headers=headers)

    print(response.text)
    file = "./tmp/" + cu + "_search.json"
    f = open(file, "w+")
    f.write(response.text)
    f.close()

    with open(file) as json_file:
        data = json.load(json_file)

    name = data.get('product').get('name')
    description = data.get('product').get('description')
    brand = data.get('product').get('brand')
    image_url = data.get('product').get('imageUrl')
    description = "Brand: " + brand + "\n" + description

    print(name)
    print(description)
    print(image_url)

    #uncomment when you get api access
    os.remove(file)

    returnList = [name, description, image_url]
    return returnList

def submitPhoto(url, user, item):
    try:
        path = "./static/images/tmp/"
        item = str(item)
        user = str(user)
        filename = user + '*' + item + ".jpg"
        file=path + filename
        img = Image.open(requests.get(url, stream=True).raw)
        img.save(file)

        code = uploadPhoto(filename, item, user)
        os.remove(file)
        print(code)
    except:
        pass





###Test Area###
#code = uploadPhoto("test_subject1*17.png", 17, "test_subject1")
#thing = productLookup(9781492053118, "test_subject1")
#print("Name: " + thing[0] + "\nDescription: " + thing[1] + "\nURL: " + thing[2])
#submitPhoto(thing[2], "test_subject1", "1")
