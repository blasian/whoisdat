''' This program should do two things:
1. Add all of the people from the db.json into Project Oxford's API
2. Train the mlb person group 
'''
from projectoxford.Client import Client
from projectoxford.Person import Person
from projectoxford.PersonGroup import PersonGroup
import json
import time

client = Client()
faceClient = client.face('9defe6b7bd8045eea6cccb8e4b8d5ddd')
personClient = Person('9defe6b7bd8045eea6cccb8e4b8d5ddd') 


def getJSONfromDB(path): # readDB :: String -> JSON
    ''' Gets the JSON from the file at the inputted path and returns it as a string'''
    json_data=open(path).read()

    with open(path) as data_file:    
        data = json.load(data_file)
        
    return data
    #pprint.PrettyPrinter(indent=4).pprint(data)
    

def addPerson(name, url, personGroup): # addPerson :: String -> String -> String -> ()
    ''' Creates a person based in an inputted name and image url before adding it to the inputted personGroup in Project Oxford's API'''
    # Detect face from image
    result = faceClient.detect({'url': url})
    print result
    faceId = result[0]['faceId']
    # Create person
    faceClient.person.createOrUpdate(personGroup, [faceId], name)
    
def addPeople(people, groupName): # addPeople :: JSON -> String -> ()
    ''' Adds all of the inputted people into the inputted group '''
    # Iterate through the person Dictionary
    for person in people:
        # Add this specific person to personGroup
        addPerson(person['name'], person['image_url'], groupName)
        # Log addition of person
        print (person['name'] + ' was added to the ' + groupName + ' personGroup')
        # Wait 3 seconds in between each person to avoid throttling
        time.sleep(3)

def main():
    # Add people to person group
    group = 'mlb'
    #faceClient.personGroup.create(group, group)   
    #addPeople(getJSONfromDB('db.json'), group)
    print faceClient.person.list(group)
    # Train person group
    #faceClient.personGroup.trainAndPollForCompletion(group)

main()