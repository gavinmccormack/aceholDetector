#! usr/bin/env python3
# 
import pandas as pd
import datetime as dt
import requests
import json
import sys
from bs4 import BeautifulSoup
from collections import deque
from config import REDDIT_SECRET, REDDIT_ID

# Access method 1 : defined in config, access method 2 defined as param
#
# So PRAW was a great tool for the reddit API, but they have removed "get post before time" which prohibits searching into the past.
# More traditional webscraping is needed !

# to do
#   Tidy get_most_recent_posts() 
#   Look into profiling to see if there is any way we can speed this up ( without getting blocked ! )
#   Check for errors ( getting blocked, failed requests, etc )

class redditPost:
    """ Object to hold reddit posts. 
        Fullname refers to the ID that refers to this post """
    def __init__(self, fullname=None, title=None, timestamp=None):
        self.fullname = fullname
        self.title = title
        self.timestamp = timestamp

    def to_dict(self):  
        return {
            'fullname' : self.fullname,
            'title' : self.title,
            'timestamp' : self.timestamp
        }

class aceholReddit:
    reddit = "some"
    def __init__(self):
        self.reddit = None
        self.headers = {'User-Agent': 'Mozilla/5.0'} # Mimic a browser visit

    def get_date(self, created):
        return dt.datetime.fromtimestamp(created)

    def create_post_object(self, domain):
        """ Creates a post object from a beautiful soup tag targetting the 'thing' wrapping div of each post """
        title = domain.find('p', class_="title").text
        fullname = domain['data-fullname']
        timestamp = domain['data-timestamp']
        reddit_post = redditPost(title=title,fullname=fullname, timestamp=timestamp)
        return reddit_post

    def get_most_recent_posts(self, subreddit_name, limit=-1):
        """ Get most recent posts in the specified subreddit. Set limit to -1 for all posts """
        # So reddit has removed their "before" param that allows for backdating posts. Hmm.
        TARGET_SUBREDDIT = "The_Donald"
        url = "https://old.reddit.com/r/{0}/new/".format(TARGET_SUBREDDIT)

        # Returns a requests.models.Response object
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        domains = soup.find_all("div", class_="thing")
        post_objects = []
        last_domain_id = None
        for domain in domains:
            print(domain['data-fullname'], domain.text)
            last_domain_id = domain['data-fullname']
            post_objects += [self.create_post_object(domain)]
        post_limit_reached = (len(post_objects) < limit) or limit == -1
        while len(domains) > 24 and post_limit_reached: # If the page is full, then try the next page. If it has exactly 25 items, then 404 and crash this program. Okay dokay.

            # Using the last post ID we can define the next page to look at.
            url = "https://old.reddit.com/r/{0}/new/?count=25&after={1}".format(TARGET_SUBREDDIT, last_domain_id)
            page = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            domains = soup.find_all("div", class_="thing")
            for domain in domains:
                print(domain['data-fullname'], domain.text)
                last_domain_id = domain['data-fullname']
                post_objects += [self.create_post_object(domain)]

            
            post_limit_reached = (len(post_objects) < limit) or limit == -1 # Also abort if we have reached out post limit
        return post_objects

 


def main():
    """ only run if called directly """
    api = aceholReddit()
    try:
        print("Testing reddit API...")
        posts = api.get_most_recent_posts("Python", limit=-1)
        print(len(posts))
        print(posts[0].__dict__)
        df = pd.DataFrame.from_records([post.to_dict() for post in posts]) # Class object to data frame format
        df2 = df[['title', 'fullname',  'timestamp']]
        df2.to_csv('data/reddit_posts.csv', mode='a', encoding='utf-8', index=False) 
    except Exception as e:
        print(e)

    

if __name__ == "__main__": 
    main() # If run directly