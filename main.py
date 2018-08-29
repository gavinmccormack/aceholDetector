# !/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from aceholSentiment import sentiment
import os
import aceholDiscord

class aceholDetector(object):
    """ Main object for interacting with the sentiment tools """
    def __init__(self):
        self.data = None
        self.csv_name = "default.csv"

    def load_csv(self, csv_name):  
        """ Load a CSV into the data """
        self.csv_name = os.path.join("data", csv_name)
        self.data = pd.read_csv(self.csv_name, skip_blank_lines=True)

    def load_json(self, json):
        self.data = json

    def save_csv(self):
        """ Save current data to CSV """
        self.data.to_csv(self.csv_name, mode='a', encoding='utf-8', index=False)    
 
    def populate_sentiment_fields(self):
        """ Applies sentiment columns to the data """
        sentiment_library = sentiment(self.data) # Create an instance of the sentiment library, analysis ( or config ) is done here
        self.data = sentiment_library.dframe() 


def main():
    """ This is a fair simulation of how this package would be used if you weren't interested in the internals """
    # Assuming CSV with author, timestamp, and text is already present
    # Some data sources might have title/body or other features
 
    ace = aceholDetector()
    #ace.load_csv('discord_messages.csv')  
    #ace.populate_sentiment_fields()
    disco_api = aceholDiscord.aceholDiscord()
    messages = disco_api.get_all_messages()
    ace.load_json(messages)
 


if __name__ == "__main__": 
    main() # If run directly