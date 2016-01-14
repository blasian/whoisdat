import time
import praw

user_agent = 'User-Agent: windows:Who_is_that:v0.0.1 (by /u/jpatomic96)'
r = praw.Reddit(user_agent)

subreddit = r.get_subreddit('whoisdat')

posts = subreddit.get_hot(limit=10)

for submission in posts:
    print r.get_submission(submission.permalink).url