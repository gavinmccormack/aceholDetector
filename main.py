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
        self.result = None
        self.csv_name = "default.csv"
        self.sentiment_lib = None

    def load_csv(self, csv_name):  
        """ Load a CSV into the data """
        self.csv_name = os.path.join("data", csv_name)
        self.data = pd.read_csv(self.csv_name, skip_blank_lines=True)

    def load_json(self, json):
        self.data = json
        self.populate_sentiment_fields()


    def save_csv(self):
        """ Save current data to CSV """ 
        self.data.to_csv(self.csv_name, mode='a', encoding='utf-8', index=False)    
 
    def populate_sentiment_fields(self):
        """ Applies sentiment columns to the data """
        self.sentiment_lib = sentiment(self.data) # Create an instance of the sentiment library, analysis ( or config ) is done here
        self.result = self.sentiment_lib.df

    def print_stats(self):
        self.sentiment_lib.print_stats()
 

def main():
    """ This is a fair simulation of how this package would be used if you weren't interested in the internals """
    # Assuming CSV with author, timestamp, and text is already present
    # Some data sources might have title/body or other features

    ace = aceholDetector() 
    #ace.load_csv('discord_messages.csv')  
    disco_api = aceholDiscord.aceholDiscord() 
    messages = disco_api.get_messages(limit=1000000)
    ace.load_json(messages)  
    ace.print_stats()            
        
     

if __name__ == "__main__": 
    main() # If run directly