from projectoxford.Client import Client
from projectoxford.PersonGroup import PersonGroup
import json
import pprint
import time

client = Client()
faceClient = client.face('9defe6b7bd8045eea6cccb8e4b8d5ddd')

def getJSONfromDB(path): # readDB :: String -> JSON
    json_data=open(path).read()

    with open(path) as data_file:    
        data = json.load(data_file)
    
    return data
    #pprint.PrettyPrinter(indent=4).pprint(data)
    

def addPerson(name, url, personGroup): # addPerson :: String -> String -> String -> ()
    # Detect face from image
    result = faceClient.detect({'url': url})
    faceId = result[0]['faceId']
    # Create person
    faceClient.person.createOrUpdate(personGroup, [faceId], name)
    # Train person group
    faceClient.personGroup.trainAndPollForCompletion(personGroup)

def addPeople(people, groupName): # addPeople :: JSON -> String -> ()
    # Iterate through the person Dictionary
    for person in people:
        # Add this specific person to personGroup
        addPerson(person['name'], person['url'], groupName)
        # Log addition of person
        print (person['name'] + ' was added to the ' + groupName + ' personGroup')
        # Wait 3 seconds in between each person to avoid throttling
        time.sleep(3)

#print faceClient.person.list('example-person-group')
addPeople(getJSONfromDB('db.json'), 'example-person-group')
