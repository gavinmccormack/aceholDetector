# !/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
from config import TARGET_CHANNEL, DISCO_TOKEN

from pprint import pprint #debug

# Discord wrapper to pull text from a channel
# Requires a bot setup at https://discordapp.com/
# Use a token and set TARGET_CHANNEL (channel ID) and DISCO_TOKEN(token from discord app) in config.py



# Would love to make this class based, but I have no idea how to work with the client object and decorators inside of a class

class aceholDiscord(object):
    """ Wrapper for retrieving messages from a discord channel """
    def __init__(self):
        pass

    def get_messages_json(self, before_id):
        """ Get the first 100 messages before the message ID """
        request_url = "https://discordapp.com/api/channels/{0}/messages?token={1}&limit=100&before={2}".format(TARGET_CHANNEL, DISCO_TOKEN, before_id)
        response = requests.get(request_url)
        return json.loads(response.content)
    
    def get_messages(self, limit=999999):
        """ Get messages from target discord channel. Defaults to all messages(or 99,9999 of them) """
        messages = self.get_most_recent()
        oldest_id = messages[-1]['id']
        no_of_results_in_batch = len(messages)
        while (no_of_results_in_batch >= 100 and limit > len(messages)): # check rate limits here, this is a 'dumb' way of doing this that misses the last messages and fails in a few other ways.
            new_messages = self.get_messages_json(oldest_id)
            messages += new_messages
            oldest_id = messages[-1]['id']
            no_of_results_in_batch = len(new_messages)
        
        message_data = self.format_data(messages) # Strip out unneeded fields
        return message_data  

    def format_data(self, json):
        data = []
        for item in json: # This is discord specific. Clearing out unneeded data from the json
            data_row = {}
            data_row['message'] = item['content']
            data_row['timestamp'] = item['timestamp']
            data_row['author'] = item['author']['username']
            data += [data_row]

        return data

    def get_most_recent(self):
        """ Most recent 100 messages """
        request_url = "https://discordapp.com/api/channels/{0}/messages?token={1}&limit=100".format(TARGET_CHANNEL, DISCO_TOKEN)
        response = requests.get(request_url)
        return json.loads(response.content)

def main():
    """ Test method only run if called directly """
    api = aceholDiscord()
    try:
        messages = api.get_most_recent()
        print(messages)
        messages = api.get_messages(limit=100)
    except Exception as e:
        print(e)

    

if __name__ == "__main__": 
    main() # If run directly