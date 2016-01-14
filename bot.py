import praw
from projectoxford.Client import Client
from projectoxford.Person import Person
from projectoxford.PersonGroup import PersonGroup
import json
import time

client = Client()
faceClient = client.face('9defe6b7bd8045eea6cccb8e4b8d5ddd')

user_agent = 'User-Agent: windows:Who_is_that:v0.0.1 (by /u/jpatomic96)'
r = praw.Reddit(user_agent)

#r.login()

subreddit = r.get_subreddit('whoisdat')

def constructComment(result):
    if result[0]['candidates'] == []:
        return "I couldn't figure out who this is. Sorry!"
    else:
        return "I'm " + "x%" + " certain that this is " + result[0]['candidates'][0]

posts = subreddit.get_new(limit=1)

for submission in posts:
    # Analyze the face from the url
    url = r.get_submission(submission.permalink).url
    print url
    # Detect face from image
    inputFace = faceClient.detect({'url': (url)})
    faceId = inputFace[0]['faceId']
    result = faceClient.identify('mlb', [faceId])
    # Post a comment with who was identified 
    #submission.add_comment(constructComment(result))