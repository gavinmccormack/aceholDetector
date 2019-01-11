#! usr/bin/env python3
# 
import pandas as pd
import datetime as dt
import requests
import praw
import json
import sys
from config import REDDIT_SECRET, REDDIT_ID

# Access method 1 : defined in config, access method 2 defined as param
#
#
# http://blog.thehumangeo.com/2014/09/23/supercharging-your-reddit-api-access/ should check out this if it is being a bit slow

class aceholReddit:
    def __init__(self):
        self.reddit = None
        self.start_connection()
        for submission in self.reddit.subreddit('learnpython').hot(limit=10):
            print(submission.title)

    def get_date(self, created):
        return dt.datetime.fromtimestamp(created)

    def start_connection(self):
        self.reddit = praw.Reddit(client_id=REDDIT_ID,
                     client_secret=REDDIT_SECRET,
                     user_agent='Sentiment Tools v 0.3')

    def get_all_posts(self):
        pass


        


def main():
    """ only run if called directly """
    api = aceholReddit()
    try:
        print("Testing reddit API...")
    except Exception as e:
        print(e)

    

if __name__ == "__main__": 
    main() # If run directly