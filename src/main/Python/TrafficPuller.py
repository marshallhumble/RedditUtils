#!/usr/bin/env python

import praw
import json
import pprint

with open('../resources/credentials.json') as data_file:
    data = json.load(data_file)

reddit_app_key = data["script"]["client_id"]
reddit_app_secret = data["script"]["client_secret"]
reddit_user_name = data["user"]["username"]
reddit_user_password = data["user"]["password"]
reddit_user_agent = "mod utils v0.1"
subreddit_name = 'NeutralPolitics'

reddit = praw.Reddit(user_agent=reddit_user_agent,
                     client_id=reddit_app_key,
                     client_secret=reddit_app_secret,
                     username=reddit_user_name,
                     password=reddit_user_password)

traffic_json = reddit.request('GET', 'r/NeutralPolitics/about/traffic/')
pp = pprint.PrettyPrinter(indent=4)

pp.pprint(traffic_json["day"])

