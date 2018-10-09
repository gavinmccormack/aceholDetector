import pandas as pd

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pendulum # for times
import pprint
from colorama import Fore, Style, init # Coloured prints

sia = SIA() # Sentiment intensity analyser

init(convert=True) # Colorama init
messages = pd.read_csv('discord_messages.csv') 


results = []
total_negative = 0
total_positive = 0

def create_time_blocks(start_time, end_time):
    """ Returns a list of dict objects, representing time/number_of_blocks sized divisions of the total time """
    # Alright, let's deal with time blocks.
    dt = start_time.diff(end_time)/number_of_blocks
    blocks = []
    for n in range(0,number_of_blocks): 
        if (n > 0): 
            block_start = block_start + dt
        else: 
            block_start = start_time # First iteration block start is equal to the start time
        block_end = block_start + dt
        blocks += [{'ID' : n, 'items' : [] ,'block_start' : block_start, 'block_end' : block_end}]
    return blocks
 
number_of_blocks = 1000
last = len(messages['time']) - 1 # -1 index not working
start_time = pendulum.parse(messages['time'][last])
end_time = pendulum.parse(messages['time'][0])
print(start_time)
print(end_time)
blocks = create_time_blocks(start_time, end_time) 
unique_names = set()

def populate_time_blocks():
    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")
    for n in range(0, len( messages['message'] ) ):
        message = str(messages['message'][n])
        item_time = pendulum.parse(messages['time'][n])  
        #print(item_time)  
        polarity_stats = sia.polarity_scores(message)
        polarity_stats['author'] = messages['author'][n]
        polarity_stats['message'] = message 
        polarity_stats['time'] = item_time
        #print(polarity_stats)
        unique_names.add( messages['author'][n] )
        # Convert compound value to trinary
        for block in blocks: 
            if ( block['block_start'] <= item_time and block['block_end'] >= item_time ): # Does this item fall within the block start/end
                block['items'] += [polarity_stats] # If so, add it to this bucket
    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")
    return blocks 


blocks = populate_time_blocks()

authors_and_negativity = dict.fromkeys(unique_names, 0)
print(unique_names)
cn = 0

# Create a dictionary where the key is the user, and the value is the total of the blocks they were present in when negativity occured
for n in blocks:
    total_negativity_for_this_block = 0
    unique_authors_for_this_block = set()
    for item in n['items']:
        total_negativity_for_this_block += item['neg']
        unique_authors_for_this_block.add(item['author'])
        authors_and_negativity[item['author']] += item['compound']
    

print(authors_and_negativity)

# More convenient to have these in order
authors_and_negativity = [ (v,k) for k,v in authors_and_negativity.items() ]
authors_and_negativity.sort(reverse=True) # natively sort tuples by first element
for v,k in authors_and_negativity:
    print("%s: %d" % (k,v))