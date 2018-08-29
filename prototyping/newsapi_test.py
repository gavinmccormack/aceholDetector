
# /usr/bin/python

import newsapi
from newsapi import newsapi_client 
from pprint import pprint

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pendulum # for times
from colorama import Fore, Style, init # Coloured prints

import nltk
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.tokenize import word_tokenize, RegexpTokenizer

import discord
import asyncio
# Gone wild with the imports here

sns.set(style='darkgrid', context='talk', palette='Dark2')

init(convert=True) # Colorama init

# Newsapi Params
page_size = 100
sources = 'al-jazeera-english,ary-news,associated-press,axios,bild,breitbart-news,bloomberg,business-insider-uk,bbc-news'
query = ""
less_prints = True
from_parameter='2017-12-01'
to='2018-12-12'

#Timeline
number_of_blocks = 10

#nltk
tokenizer = RegexpTokenizer(r'\w+')
stop_words = stopwords.words('english')

# Inits because of function wraps
df = None

# Less crap in console
def quiet_print(*input):
    """ This is the filter for only simple output """
    if (less_prints != True):
        print(input)

# Initialise
sia = SIA() # Sentiment intensity analyser
newsapi = newsapi_client.NewsApiClient(api_key='eac6fe3e10d44f23b04a0e3fc472b6d8')

def get_articles():
    return newsapi.get_everything(
                                            q=query, 
                                            sources=sources, 
                                            language='en', 
                                            page_size=page_size,
                                            from_param='2017-12-01',
                                            to='2018-12-12',
                                            sort_by='publishedAt'
                                        )

## New draft. Will need to write a looping function to call the API, and progressively work backwards in 100 unit blocks to recover some number of articles
def get_articles_in_range(publishedAfter, publishedBefore):
    all_articles = []
    first_request = newsapi.get_everything(
        q=query, 
        sources=sources, 
        language='en', 
        page_size=page_size,
        from_param=publishedAfter,
        to=publishedBefore,
        sort_by='publishedAt'
    )
    articles = first_request['articles']
    all_articles.extend( articles )
    earliest_article = min(articles, key=lambda article: article['publishedAt'])['publishedAt']
    # shoehorn in some limited iterations
    n = 0
    while ( earliest_article > publishedAfter and articles ): # Articles is an empty dict and should return false. A more typical way to do this would be check for rate limiting 429 / x-RateLimit-Limit
        request = newsapi.get_everything(
            q=query, 
            sources=sources, 
            language='en', 
            page_size=page_size,
            from_param=publishedAfter,
            to=publishedBefore,
            sort_by='publishedAt'
        )
        all_articles.extend( request['articles'] )
        print("These are the values the request has run with... ")
        print("Published Before : ", publishedBefore)
        print("Published After : ", publishedAfter)
        publishedBefore = min(articles, key=lambda article: article['publishedAt'])['publishedAt']

        n += 1
        if (n > 1): # Stop this spamming the newsapi while we're testing by stopping at 3 requests
            break
    
    return all_articles

def test_get_range():
    all_articles = get_articles_in_range(from_parameter,to)
    for n in range(0, len(all_articles)):
        pass
        print(all_articles[n]['title'], "Article number " , n)


def test_article_loop():
    global df
    # Test loop for checking total negativity/polarity via the newsapi
    # Also attaching a bit of graphing to this
    # Absolutely positively a dumb function
    # Articles
    articles = get_articles()['articles']
    articles = sorted(articles, key=lambda article: article['publishedAt'])

    # A time block is a sub division of the total time
    # The source is ordered already, so could just grab first and last if required
    minimum_time = min(articles, key=lambda article: article['publishedAt'])['publishedAt']
    maximum_time = max(articles, key=lambda article: article['publishedAt'])['publishedAt']

    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")
    print("First article published on : " , minimum_time )
    print("Last article published on : " , maximum_time)

    # Is the news, by and large, positive or negative
    total_negative = 0
    total_positive = 0
    results = []
    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")
    print("Showing news statistics for the word '", query , "'")
    for article in articles:
        polarity_stats = sia.polarity_scores(article['title'])
        quiet_print(article['title'], ", Pol score: ", polarity_stats)
        polarity_stats['title'] = article['title']
        total_negative += polarity_stats['neg'] 
        total_positive += polarity_stats['pos']
        results += [polarity_stats]

    print("Total Negativity: ", total_negative)
    print("Total positivity: ", total_positive)

    # Make a CSV
    df = pd.DataFrame.from_records(results)
    print(df.head())

    # Convert compound value to trinary
    df['label'] = 0
    df.loc[df['compound'] > 0.1, 'label'] = 1 # the comparison value here is used to define the bounds of "neutral" in the bar chart
    df.loc[df['compound'] < -0.1, 'label'] = -1 

    df2 = df[['title', 'compound','label']]
    df2.to_csv('news_headlines.csv', mode='a', encoding='utf-8', index=False)

def create_sentiment_bar_chart():
    # Make a bar chart
    fig, ax = plt.subplots(figsize=(8, 8))
    counts = df.label.value_counts(normalize=True) * 100
    sns.barplot(x=counts.index, y=counts, ax=ax)
    ax.set_xticklabels(['Positive', 'Neutral', 'Negative'])
    ax.set_ylabel("Percentage")
    plt.show()



#test_article_loop()
#create_sentiment_bar_chart()

# Take start time, add dt, check if publish date falls in range

def create_time_blocks(start_time, end_time):
    """ Returns a list of dict objects, representing time/number_of_blocks sized divisions of the total time """
    # Alright, let's deal with time blocks.
    start_time = pendulum.parse(minimum_time)
    end_time = pendulum.parse(maximum_time)
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

#blocks = populate_time_blocks(start_time, end_time) 

def populate_time_blocks():
    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")
    for article in articles:
        item_time = pendulum.parse(article['publishedAt']) 
        for block in blocks: 
            if ( block['block_start'] >= item_time and item_time <= block['block_end']): # Does this item fall within the block start/end
                block['items'] += [article] # If so, add it to this bucket
    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")
    pprint(blocks) 

# Most common words for positive and negative headlines

def process_text(titles):
    tokens = []
    for line in titles:
        toks = tokenizer.tokenize(line)
        toks = [t.lower() for t in toks if t.lower() not in stop_words]
        tokens.extend(toks)
    return tokens

def plot_positive_frequency():
    global df
    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}",)
    print("Most common words in positive headlines, and frequency", "\n")
    pos_lines = list(df[df.label == 1].title) # Positive Headlines
    pos_tokens = process_text(pos_lines)
    pos_freq = nltk.FreqDist(pos_tokens)
    pprint(pos_freq.most_common(20))

    # Chart the frequencies
    #Positive
    y_val = [x[1] for x in pos_freq.most_common()]
    fig = plt.figure(figsize=(10,5))
    plt.plot(y_val)
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Word Frequency Distribution (Positive)")
    plt.show()
    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")



def plot_negative_frequency():
    global df
    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")
    print("Most common words in negative headlines, and frequency", "\n")
    pos_lines = list(df[df.label == -1].title) # Negative Headlines
    pos_tokens = process_text(pos_lines)
    pos_freq = nltk.FreqDist(pos_tokens)
    pprint(pos_freq.most_common(20))

    #Chart the frequencies
    y_val = [x[1] for x in pos_freq.most_common()]
    fig = plt.figure(figsize=(10,5))
    plt.plot(y_val)
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Word Frequency Distribution (Negative)")
    plt.show()

    print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")


#plot_positive_frequency()
#plot_negative_frequency()

## Discord commencement

