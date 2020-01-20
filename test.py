# !/usr/bin/python
# -*- coding: utf-8 -*-

# Integration style test scenarios

import aceholSentiment
import aceholDiscord

dummy_messages = {}

def main():
    """ This is a fair simulation of how this package would be used if you weren't interested in the internals """
    import nltk
    nltk.download('vader_lexicon')
    ace = aceholSentiment.aceholSentiment(dummy_messages) 
    #ace.save_to_csv()  
    ace.print_stats()      


    
    # If we were pulling from discord 
    #disco_api = aceholDiscord.aceholDiscord()  
    #all_messages = disco_api.get_server_messages()
    #messages = disco_api.get_messages(limit=1000)
    #ace.load_json(messages)
          


if __name__ == "__main__":  
    main() # If run directly 