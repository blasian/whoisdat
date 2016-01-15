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

r.login()

subreddit = r.get_subreddit('whoisdat')
submissions = []

def constructComment(result):
    comment = ""
    if result[0]['candidates'] == []:
        comment = "I couldn't figure out who this is. Sorry!"
    else:
        conf = result[0]['candidates'][0]['confidence']
        person = faceClient.person.get('mlb', result[0]['candidates'][0]['personId'])
        comment = "I'm " + str(conf * 100) + "% certain that this is " + person['name']
    print comment
    return comment

while True:
    posts = subreddit.get_new(limit=10)
    for submission in posts:
        if submission not in submissions:
            # Analyze the face from the url
            url = r.get_submission(submission.permalink).url
            url = url.replace('://', '://i.') + ".jpg"
            print url
            # Detect face from image
            inputFace = faceClient.detect({'url': (url)})
            faceId = inputFace[0]['faceId']
            result = faceClient.identify('mlb', [faceId])
            # Post a comment with who was identified 
            submission.add_comment(constructComment(result))
            submissions.append(submission)