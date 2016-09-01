#!/usr/bin/env python

import praw
import json
from time import gmtime, strftime
from os.path import expanduser

home = expanduser("~")

try:
    with open('../resources/credentials.json') as data_file:
        data = json.load(data_file)
except FileNotFoundError:
    with open(home + '/RedditUtils/src/main/resources/credentials.json') as data_file:
        data = json.load(data_file)

reddit_app_key = data["script"]["client_id"]
reddit_app_secret = data["script"]["client_secret"]
reddit_user_name = data["user"]["username"]
reddit_user_password = data["user"]["password"]
reddit_user_agent = "mod utils v0.1"
subreddit_name = data["sub"]["subreddit"]
current_date = strftime("%Y-%m-%d", gmtime())
save_path = data["file_settings"]["save_location"]

reddit = praw.Reddit(user_agent=reddit_user_agent,
                     client_id=reddit_app_key,
                     client_secret=reddit_app_secret,
                     username=reddit_user_name,
                     password=reddit_user_password)

traffic_json = reddit.request('GET', 'r/' + subreddit_name + '/about/traffic/')

if traffic_json is not None:
    with open(home + '/' + save_path + '/' + current_date + '.json', 'w') as outfile:
        json.dump(traffic_json, outfile)
