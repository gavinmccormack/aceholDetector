# !/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pendulum
from config import NUMBER_OF_BLOCKS

class sentiment(object):
    def __init__(self, data):
        """ In need of cleaning up """
        self.sia = SIA()
        self.data = data # Raw JSON Data
        self.df = None # Dataframe
        self.total_negative = 0
        self.total_positive = 0
        self.total_compound = 0  
        self.unique_names = set()
        self.posts_per_user = {}
        self.leader_board = {}
        
        self.add_sentiment_fields()
        self.blocks = self.create_time_blocks() 
        self.populate_time_blocks()
        self.create_leaderboard()

    def set_overall_stats(self, stats_obj):
        """ Update the total running stats for messages found using this instance of the sentiment object. """
        self.total_compound +=  stats_obj['compound']
        self.total_positive +=  stats_obj['pos']
        self.total_negative +=  stats_obj['neg']
        if ( stats_obj['author'] not in self.posts_per_user):
            self.posts_per_user[stats_obj['author']] = 1
        self.posts_per_user[stats_obj['author']] += 1

    def add_sentiment_fields(self):
        """ Process the data and add sentiment columns to the data """
        results = []
        for data_row in self.data:
            text = str(data_row['message'])
            sentiment_stats = self.sia.polarity_scores(text) # SIA will create an object with pos, neg, and compound stats.
            sentiment_stats['author'] = data_row['author'] # Not ideal for different data types/sets. Not very flexible.
            sentiment_stats['message'] = text
            sentiment_stats['timestamp'] = pendulum.parse(data_row['timestamp'])
            self.set_overall_stats(sentiment_stats) # Tally up totals and similar
            results += [sentiment_stats]
        self.df = results

    def create_leaderboard(self):
        """ Calculates the total negativity for a block of time, and then assigns blame to anyone in the vicinity. This blame is then tallied up. """
        self.leaderboard = dict.fromkeys(self.unique_names, 0)
        # Create a dictionary where the key is the user, and the value is the total of the blocks they were present in when negativity occured
        for n in self.blocks:
            total_negativity_for_this_block = 0
            unique_authors_for_this_block = set()
            for item in n['items']: 
                total_negativity_for_this_block += item['compound']
                unique_authors_for_this_block.add(item['author'])
            for author in unique_authors_for_this_block:
                self.leaderboard[item['author']] += total_negativity_for_this_block / self.posts_per_user[item['author']]
        self.order_leaderboard()

    def order_leaderboard(self):
        self.leaderboard = [ (v,k) for k,v in self.leaderboard.items() ]
        self.leaderboard.sort(reverse=True) # natively sort tuples by first element

    def create_time_blocks(self):
        """ Returns a list of dict objects, representing time/number_of_blocks sized divisions of the total time """
        start_time = self.df[-1]['timestamp']
        end_time = self.df[0]['timestamp']
        dt = start_time.diff(end_time)/NUMBER_OF_BLOCKS
        blocks = []
        for n in range(0,NUMBER_OF_BLOCKS): 
            if (n > 0): 
                block_start = block_start + dt
            else: 
                block_start = start_time # First iteration block start is equal to the start time
            block_end = block_start + dt
            blocks += [{'ID' : n, 'items' : [] ,'block_start' : block_start, 'block_end' : block_end}]
        return blocks

    def populate_time_blocks(self):
        """ Add messages into the block of time that contains them. Optimisation potential here, particularly with large numbers of blocks """
        for item in self.df:
            self.unique_names.add( item['author'] )
            for block in self.blocks: 
                if ( block['block_start'] <= item['timestamp'] and block['block_end'] >= item['timestamp'] ): # Does this item fall within the block start/end
                    block['items'] += [item] # If so, add it to this bucket

    def count_words(self, word):
        no_of_words = 0
        for data_row in self.data:
            print(data_row['message'])
            if data_row['message'].find(word) != -1:
                no_of_words += 1
        return no_of_words

    def print_stats(self):
        """ Text based output of any stats """
        print("\nFinal results: \n") 
        print("Number of entries : ", len(self.data))
        print("Total Positivity : ", self.total_positive)
        print("Total Negativity : ", self.total_negative)
        print("Overall compound : ", self.total_compound)
        print("\n--------------")
        print("Unique users: \n", self.unique_names)
        print("\n--------------")
        print("LEADERBOARD \n")
        for name, score in self.leaderboard:
            print(name, " : ", score)
        print("\n--------------")
        print(" Posts per user \n")
        for name, number_of_posts in sorted(((value, key) for (key,value) in self.posts_per_user.items() ), reverse=True): # clean me up !
            print(name, " : ", number_of_posts)