# usr/bin/python
import requests
import json

from config import TARGET_CHANNEL, DISCO_TOKEN
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
    
    def get_all_messages(self):
        messages = self.get_most_recent()
        oldest_id = messages[-1]['id']
        no_of_results = len(messages)
        while (no_of_results >= 100): # check rate limits here, this is a 'dumb' way of doing this that misses the last messages and fails in a few other ways.
            messages += self.get_messages_json(oldest_id)
            oldest_id = messages[-1]['id']
            no_of_results = len(messages)
        return messages    

    def get_most_recent(self):
        """ Most recent 100 messages """
        request_url = "https://discordapp.com/api/channels/{0}/messages?token={1}&limit=100".format(TARGET_CHANNEL, DISCO_TOKEN)
        response = requests.get(request_url)
        return json.loads(response.content)

def main():
    """ Test method only run if called directly """
    api = aceholDiscord()
    messages = api.get_all_messages()
    print(len(messages))

if __name__ == "__main__": 
    main() # If run directly