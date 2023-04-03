
import pymongo
import pywhatkit
import datetime
import time
import requests

# Connect to the MongoDB instance
client = pymongo.MongoClient('mongodb://localhost:27017/')

# Create a database and a collection
db = client['mydatabase']
collection = db['mycollection']

# Define the URL of the API
url = 'http://localhost:1337/api/automation-datas'

collection.create_index("attributes.Patient_ID", unique=True)

# function to insert data into MongoDB
def insert_data(data):
    for item in data:
        # check if the record exists
        if not collection.find_one({"attributes.Patient_ID": item['attributes']['Patient_ID']}):
            # insert the record into MongoDB
            collection.insert_one(item)

while True:
    # make an API request
    response = requests.get(url)

    # convert response to JSON
    data = response.json()['data']

    # insert data into MongoDB
    insert_data(data)
    # Check if it's 8 am
    now = datetime.datetime.now()
    print(now.hour)
    if now.hour == 15:
        # Get the data from the MongoDB collection where status_flag is True
        data1 = collection.find({'attributes.status_flag': True})
        print(data1)
        for d in data1:
            print(d)
            # Send a message to WhatsApp

            mobile_number = d['attributes']['Patient_Mobile_Number']
            message = d['attributes']['Message']
            print("done2").3
            pywhatkit.sendwhatmsg_instantly(mobile_number, message,5,True,2)
            print(d)
            # Set status_flag to False
            collection.update_one({'_id': d['_id']}, {'$set': {'attributes.status_flag': False}})

    # Wait for 1 hour before checking again
    time.sleep(5)

