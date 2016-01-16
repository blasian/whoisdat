# whoisdat
a helpful, name-dropping reddit bot

###What it does:
WhoDatBot will troll image posts a given subreddit, and respond to any comment containing "who dat" with who the person is
###Potential user / use case:
Reddit user wanting to identify an athlete in an image
###How it works:
Scan posts from subreddit with PRAW -> Give image to Project Oxford Face API -> Post comment response from Project Oxford using PRAW 
###Issues:
1. Only works with imgur links (some older imgur links will not work)

###Scope limitations:
1. Will only identify MLB players -> Resulting from requirement to populate Project Oxford with every face

###Instructions to run:
1. Configure userName and sub variables at the top of bot.py
2. Train ProjectOxford with people using JSONToAPI.py
3. Run bot.py python file with a Project Oxford Face API key as a command line argument
