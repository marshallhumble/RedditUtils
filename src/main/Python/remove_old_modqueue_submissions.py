#! /usr/bin/env python

import praw
import json
import praw.models
from os.path import expanduser

home = expanduser("~")

try:
    with open('../resources/credentials.json') as data_file:
        data = json.load(data_file)
except FileNotFoundError:
    with open(home + '/RedditUtls/src/main/resources/credentials.json') as data_file:
        data = json.load(data_file)

# Reddit Oauth Credentials
REDDIT_APP_KEY = data["script"]["client_id"]
REDDIT_APP_SECRET = data["script"]["client_secret"]
REDDIT_USER_NAME = data["user"]["username"]
REDDIT_USER_PASSWORD = data["user"]["password"]
REDDDIT_USER_AGENT = data["sub"]["user_agent"]

reddit = praw.Reddit(user_agent=REDDDIT_USER_AGENT,
                     client_id=REDDIT_APP_KEY,
                     client_secret=REDDIT_APP_SECRET,
                     username=REDDIT_USER_NAME,
                     password=REDDIT_USER_PASSWORD)

# Place the subreddit you want to look up posts from here
SUBREDDIT_TO_MONITOR = data["sub"]["subreddit"]

modqueue = reddit.request('GET', 'r/' + SUBREDDIT_TO_MONITOR + '/about/reports')

for i in modqueue:
    print(i)
