# !/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import sys
from config import TARGET_CHANNEL, DISCO_TOKEN, TARGET_SERVER

from pprint import pprint #debug

# Discord wrapper to pull text from a channel
# Requires a bot setup at https://discordapp.com/
# Use a token and set TARGET_CHANNEL (channel ID) and DISCO_TOKEN(token from discord app) in config.py

class aceholDiscord(object):
    """ Wrapper for retrieving messages from a discord channel """
    def __init__(self):
        pass

    def send_request(self, url):
        """ Sends a request to discord servers. Authentication is taken care of here so a ?Token= parameter is not necessary """
        response = requests.get(url, headers={"Authorization": "Bot " + DISCO_TOKEN})
        if response.status_code != 200:
            print(response.status_code)
            print("Request URL: " , request_url)
            print("There has been an error with the discord request; please check the access token and target channel is correct")
            sys.exit()
        return response

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
        request_url = "https://discordapp.com/api/channels/{0}/messages?limit=100".format(TARGET_CHANNEL)
        response = self.send_request(request_url)
        return json.loads(response.content)

    def get_channel_list(self, server_id = TARGET_SERVER):
        """ Returns a list of channel IDs within a server """
        request_url = "https://discordapp.com/api/guilds/{0}/channels".format(TARGET_SERVER)
        response = self.send_request(request_url)
        response_json = json.loads(response.content)
        channel_ids = [x['id'] for x in response_json]
        return channel_ids

    def get_messages_json(self, before_id, channel_id):
        """ Get the first 100 messages before the message ID """
        request_url = "https://discordapp.com/api/channels/{0}/messages?token={1}&limit=100&before={2}".format(channel_id, DISCO_TOKEN, before_id)
        response = self.send_request(request_url)
        return json.loads(response.content)
    
    def get_messages(self, limit=999999, channel_id=TARGET_CHANNEL):
        """ Get messages from target discord channel. Defaults to all messages(or 99,9999 of them) """
        messages = self.get_most_recent()
        oldest_id = messages[-1]['id']
        no_of_results_in_batch = len(messages)
        while (no_of_results_in_batch >= 100 and limit > len(messages)): # check rate limits here, this is a 'dumb' way of doing this that misses the last messages and fails in a few other ways.
            new_messages = self.get_messages_json(oldest_id, channel_id)
            messages += new_messages
            oldest_id = messages[-1]['id']
            no_of_results_in_batch = len(new_messages)
        message_data = self.format_data(messages) # Strip out unneeded fields
        return message_data  

    def get_server_messages(self, limit=999999):
        """ Get all messages in all channels of a server """
        channels = self.get_channel_list()
        messages = []
        for channel_id in channels:
            messages += self.get_messages(channel_id=channel_id)
        return messages        

def main():
    """ only run if called directly """
    api = aceholDiscord()
    try:
        messages = api.get_most_recent()
        print(messages)
        api.get_channel_list()
        messages = api.get_messages(limit=100)
    except Exception as e:
        print(e)

    

if __name__ == "__main__": 
    main() # If run directly