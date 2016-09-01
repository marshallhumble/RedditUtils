#!/usr/bin/env python

import praw

import json
import tweepy
import logging
from os.path import expanduser

home = expanduser("~")

try:
    with open('../resources/credentials.json') as data_file:
        data = json.load(data_file)
except FileNotFoundError:
    with open(home + '/RedditUtils/src/main/resources/credentials.json') as data_file:
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
POSTED_CACHE = './posted_posts.txt'
filepath = home + '/' + log_path + '/' + 'twitter_bot.log'

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
    new_posts = reddit.subreddit(SUBREDDIT_TO_MONITOR).new()
    while new_posts.next():
        rid = next(new_posts).id
        if not already_tweeted(rid):
            with open(POSTED_CACHE, 'a') as f:
                f.write(rid + '\n')

            title = next(new_posts).title[:90] + '... ' + short_link_prefix + rid
            print(title)
            try:
                twitter.update_status(title)
                append_post_id(rid)
            except tweepy.TweepError:
                continue


def already_tweeted(post_id):
    ''' Checks if the reddit Twitter bot has already tweeted a post. '''
    found = False
    with open(POSTED_CACHE, 'r') as in_file:
        for line in in_file:
            if post_id in line:
                found = True
                break
    return found


def append_post_id(post_id):
    with open(POSTED_CACHE, 'a') as in_file:
        in_file.write(post_id + '\n')

if __name__ == "__main__":
    get_new_links()
