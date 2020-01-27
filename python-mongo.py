from pymongo import MongoClient
import random
import string
import bcrypt
from datetime import datetime, timedelta, date

# Step 1: Connect the mongodb server. Please change the connection string to yours while testing
client = MongoClient("mongodb://localhost:27017/")

#Step 2: Create a new database called emlab
db = client.emLab

#Step 3: Create some sample data for the initial database
# User name
# email adress
# password
first_names = ["Ben", "Nathan", "Andrew","Blake","Jack","James","Lily","Lucy","Jessica","Emma"]
last_names = ["Smith","Hall","Johnson","Jones","Brown","Davis","Miller","Whilson","Moore","Taylor"]
emails = ["@yahoo.com","@gmail.com","@qq.com","@illinois.edu","@outlook.com"]
#for random password generation
lettersAndDigits = string.ascii_letters + string.digits

# Step 4, create a collection called acccount to store initial user data
# and insert the random generated sample data into it.
salt = bcrypt.gensalt()
for i in range(200):
    # generate random user names, email adresses and passwords from sample pool
    first_name = first_names[random.randint(0, (len(first_names)-1))]
    last_name = last_names[random.randint(0, (len(last_names)-1))]
    user_name = first_name + " " + last_name + " " + str(random.randint(1,500))
    email = first_name + last_name + str(random.randint(1,500)) + emails[random.randint(0, (len(emails)-1))]
    password = ''.join(random.choice(lettersAndDigits) for i in range(8))

    # check if the user name already exists, if so, print warning
    if db.account.count_documents({"user_name":user_name}, limit = 1):
        print('User name {0} already exits'.format(user_name))
        continue

    # check if the email already exists, if so, print warning
    if db.account.count_documents({"email":email}, limit = 1):
        print('Email {0} is already registered'.format(email))
        continue

    # password is hashed for security
    user_sample = {
        "user_name": user_name,
        "email":email,
        "password":bcrypt.hashpw(password.encode('utf8'), salt)
    }

    #create and insert the data into collection account
    result = db.account.insert_one(user_sample)

    # print the result of inserted data for testing
    print('Created {0} of 200 as {1}'.format(i+1,result.inserted_id))

print('finished importing intial data into the database')

# Begin to expand the intial databse with subscription data

# Step 5, expand the database field by addding a new array arrtibute for subscription
# First expand the data model of account by adding new field subscription
db.account.update_many({},{ "$set":{"subscription":[]} })
print('finished adding new field into the database')

# Step 6, create a new collection of subscription, generate sample data and create reference
# between the two collections

# the date when subscription starts
start_point = datetime(2020,1,1)
#number of data in collection account
num = db.account.count_documents({})

# simulate the process when a user begin to subscribe
for i in range(500):

    # randomly get a user
    order = random.randint(0,num-1)
    random_user = db.account.find({}).limit(1).skip(order)

    #randomly generate the data when user begin to subscribe
    start_date = start_point + timedelta(days=random.randint(1,25))

    #take a year as each subscription period
    expire_date = start_date + timedelta(days=365)

    sub_sample = {
        "start_date":start_date,
        "expire_date":expire_date,
    }
    # create a new collection called subscription in database and store data in it
    sub_result = db.subscription.insert_one(sub_sample)

    # create reference between the two collection by inserting the subscription id
    # into the subscription field of the account collection
    db.account.update_one({"_id":random_user[0]["_id"]},{ "$push":{"subscription":sub_result.inserted_id} })
    print('User {0} begins to subscribe'.format(random_user[0]["user_name"]))

<<<<<<< HEAD
# Step 7, simulate a scenario when a we want to check if a user is just a visitor or prime member
=======
# Step 7, simulate a scenario when we want to check if a user is just a visitor or prime member
>>>>>>> 75569b605f09a5db005ab918a4fa975181550088
for i in range(200):

    # randomly get a user
    order = random.randint(0,num-1)
    random_user = db.account.find({}).limit(1).skip(order)

    # get the user name
    random_user_name = random_user[0]["user_name"]

    # get the subscription data
    sub_ids = random_user[0]["subscription"]

    #check if the expire date passed and print result
    flag = True
    for j in sub_ids:
        sub_data = db.subscription.find_one({"_id":j})
        if sub_data["expire_date"] > datetime.today():
            flag = False
            print("User {0} is a prime member".format(random_user_name))
            break
    if flag:
        print("User {0} is a visitor".format(random_user_name))

print("databse expanding finished")
