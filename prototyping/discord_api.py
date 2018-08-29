import discord
import asyncio
import pprint
import seaborn as sns
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

client = discord.Client()
sns.set(style='darkgrid', context='talk', palette='Dark2')
sia = SIA() # Sentiment intensity analyser

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

async def get_logs_from(channel):
    results = []
    async for m in client.logs_from(channel, limit=100000):
        message = sia.polarity_scores(m.clean_content)
        message['author'] = m.author
        message['message'] = m.clean_content
        message['time'] = m.timestamp  
        results += [message] 
    # Make a CSV
    df = pd.DataFrame.from_records(results)
    df2 = df[['author', 'message', 'time', 'pos', 'neg', 'compound']]
    df2.to_csv('discord_messages.csv', mode='a', encoding='utf-8', index=False)  
    client.close()

@client.event
async def on_ready(): 
    client.edit_profile(username="Robot Wizzard")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    general_channel = client.get_channel("292052706653110272")
    await get_logs_from(general_channel)
    client.close() 
 

 
client.run('MzAzMTAwODMwNzUwNDc0MjQw.Dl9XOQ.t4tpWOXn6jdhIUufI-jAKbKfwfM')   