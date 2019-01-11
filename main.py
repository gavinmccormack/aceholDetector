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
        self.data = pd.DataFrame.from_records(self.result)
        self.populate_sentiment_fields()


    def save_to_csv(self):
        """ Save current data to CSV """    
        df = pd.DataFrame.from_records(self.result)
        df2 = df[['author', 'message', 'timestamp']]
        df2.to_csv('data/messages.csv', mode='a', encoding='utf-8', index=False) 
 
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

    # This is the main testing point for this.
    # Ideally this should be a two liner ( or a line for each type of stat returned if it was more granular )
    import nltk
    nltk.download('vader_lexicon')

    ace = aceholDetector() 
    disco_api = aceholDiscord.aceholDiscord()  
    
    all_messages = disco_api.get_server_messages()
    
    print(all_messages)
    messages = disco_api.get_messages(limit=1000)
    ace.load_json(all_messages)

    ace.save_to_csv()  
    ace.print_stats()                


if __name__ == "__main__":  
    main() # If run directly 