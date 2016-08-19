#!/usr/bin/env python

import praw

import json
import tweepy
import time
import os
import logging
from os.path import expanduser

with open('../resources/credentials.json') as data_file:
    data = json.load(data_file)

# Place your Twitter API keys here
OAUTH_TOKEN = data["twitter"]["oauth_token"]
OAUTH_TOKEN_SECRET = data["twitter"]["oauth_token_secret"]
CONSUMER_KEY = data["twitter"]["consumer_key"]
CONSUMER_SECRET = data["twitter"]["consumer_secret"]

# Place the subreddit you want to look up posts from here
SUBREDDIT_TO_MONITOR = data["sub"]["subreddit"]

# File System Settings
log_path = data["file_settings"]["log_path"]
POSTED_CACHE = 'posted_posts.txt'
home = expanduser("~")
# filepath = home + '/' + log_path + '/' + 'twitter_bot.log'
filepath = home + '/' + 'twitter_bot.log'
logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', filename=filepath, level=logging.DEBUG)

# Reddit Oauth Credentials
REDDIT_APP_KEY = data["script"]["client_id"]
REDDIT_APP_SECRET = data["script"]["client_secret"]
REDDIT_USER_NAME = data["user"]["username"]
REDDIT_USER_PASSWORD = data["user"]["password"]
REDDDIT_USER_AGENT = data["sub"]["user_agent"]

short_link_prefix = "http://redd.it/"

reddit = praw.Reddit(user_agent=REDDDIT_USER_AGENT,
                     client_id=REDDIT_APP_KEY,
                     client_secret=REDDIT_APP_SECRET,
                     username=REDDIT_USER_NAME,
                     password=REDDIT_USER_PASSWORD)

# Tweepy init
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

twitter = tweepy.API(auth)


def get_new_links():
    print('/' + log_path + '/' + POSTED_CACHE)

    with open('/' + log_path + '/' + POSTED_CACHE, 'rw') as f:
        posted = f.read()

    new_posts = reddit.subreddit(SUBREDDIT_TO_MONITOR).new()
    while new_posts.next():
        rid = next(new_posts).id
        if rid not in posted:
            title = next(new_posts).title[:90] + '... ' + short_link_prefix + rid
            twitter.update_status(title)
            print(len(title))
            f.write(rid)
