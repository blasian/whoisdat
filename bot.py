import praw
from projectoxford.Client import Client
from projectoxford.Person import Person
from projectoxford.PersonGroup import PersonGroup
import json
import time
import sys
import re

##### userName and subreddit must be configured in order for the bot to run

# This is the user running the bot
userName = 'jpatomic96'

# Define subreddit to troll
sub = 'whoisdat'

#####


# Define user agent
user_agent = 'User-Agent: windows:WhoDat:v0.0.1 (by /u/' + userName + ')'
# Create initial praw object
r = praw.Reddit(user_agent)
subreddit = r.get_subreddit('whoisdat')
# Configure Project Oxford API
client = Client()
faceClient = client.face(sys.argv[1]) # The API key is retrieved from the first command line argument
# This will hold all submissions that have been dealt with
submissions = []

def getAppropriateComment(result): # JSON -> JSON
    ''' Returns the appropriate comment to post given a result from Project Oxford'''
    # Name, debut date, draft date, position
    print "response \n\n"
    print result
    if result[0]['candidates'] == []:
        comment = "I couldn't figure out who this is. Sorry!"
        return comment
    else:
        conf = result[0]['candidates'][0]['confidence']
        person = faceClient.person.get('mlb', result[0]['candidates'][0]['personId'])
        identitySentence = "**WhoDatBot:**\nI'm " + str(conf * 100) + "% certain that this is " + person['name'] + "."
      #  playerDescriptionSentence = person['name'] + " was drafted to "  + data['team'] + "in " + data['draft_year'] + " as a " + data['position'] +  "."
        botInfoSentence = "I'm a bot who will identify players when you call me! Click [here](https://github.com/blasian/whoisdat) to see my code!"
        return (identitySentence + "\n\n\n" + botInfoSentence + "\n\n")

def fixImgurUrl(url): # String -> String
    ''' Fixes imgur urls so that they point directly to the image rather than the post'''
    # If the url already points to an image, don't fix it
    if re.search("\.jpg|png|bmp|gif", url):
        return url
    # Else fix it so that it points to in image
    return url.replace('://', '://i.') + ".jpg"
    
def makeComment(requestComment, commentToPost):
    ''' Responds to the comment requesting WhoDatBot with commentToPost'''
    ### LOG
    print "makeComment"
    
    # Reply to the post
    requestComment.reply(commentToPost)

def getResponseFromPost(post): # Submission -> Praw Object -> JSON
    ### LOG
    print "getResponseFromPost " + post.short_link
    
    # Get the appropriate url
    url = r.get_submission(post.permalink).url
    # Fix imgur links
    fixed_url = fixImgurUrl(url)
    # Detect face from image
    inputFace = faceClient.detect({'url': (fixed_url)})
    faceId = inputFace[0]['faceId']
    result = faceClient.identify('mlb', [faceId])
    # Return detected person json
    return result

def hasReplied(comment): # Comment -> Bool
    # Iterate through comment's replies
    for reply in comment.replies:
        print reply
        # If reply's author is userName (the signed in user), then we don't need to reply
        if userName == reply.author.name:
            return True
    # If no post by the running user has been found, then we haven't replied
    return False

def respondToComments(subreddit): # Some praw object -> Some other praw object -> ()
    ''' This function will respond to comments where the bot is called to identify a post'''
    ### LOG
    print "respondToComments"
    
    # Get new posts from subreddit
    posts = subreddit.get_new(limit=10)
    # For each remaining post 
    for post in posts:
        # Only deal with posts that haven't been dealt with
        if post not in submissions and isImgur(post):
            # For each comment in remaining posts
            for comment in post.comments:
                # If comment contain's "who dat" and has not already been replied to
                if "who dat" in comment.body and not hasReplied(comment):
                    # Identify person
                    response = getResponseFromPost(post)
                    print response
                    # Respond to comment with response
                    makeComment(comment, getAppropriateComment(response))
                    # Add submission to higher scoped submissions list
                    submissions.append(post)
                
                
            
def isImgur(post): # Some praw object -> Submission -> Bool
    ''' This function will return whether the inputted post links to imgur'''
    # If permalink is from imgur
    return ("imgur" in r.get_submission(post.permalink).url)
        
 
def runBot(): # ()
    ''' Runs WhoDatBot'''
    ### LOG
    print "runBot"
    
    # Login to reddit
    r.login()
    
    # This is the main loop
    while True:
        respondToComments(subreddit)
        print "Done responding"
        # Runs every minute
        time.sleep(60)
        
runBot()