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


    def save_to_csv(self):
        """ Save current data to CSV """    
        df = pd.DataFrame.from_records(self.result)
        df2 = df[['message', 'author',  'timestamp']]
        df2.to_csv('data/messages.csv', mode='a', encoding='utf-8', index=False) 
 
    def populate_sentiment_fields(self):
        """ Applies sentiment columns to the data """
        self.sentiment_lib = sentiment(self.data) # Create an instance of the sentiment library, analysis ( or config ) is done here
        self.result = self.sentiment_lib.df

    def print_stats(self):
        self.sentiment_lib.print_stats()
 
