
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
# Gone wild with the imports here

sns.set(style='darkgrid', context='talk', palette='Dark2')

init(convert=True) # Colorama init

# Newsapi Params
page_size = 100
sources = 'al-jazeera-english,ary-news,associated-press,axios,bild,breitbart-news,bloomberg,business-insider-uk,bbc-news'
query = ""
less_prints = True
from_parameter='2017-12-01'
to='2017-12-12'

#Timeline
number_of_blocks = 10

#nltk
tokenizer = RegexpTokenizer(r'\w+')
stop_words = stopwords.words('english')

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
                                            from_parameter='2017-12-01',
                                            to='2017-12-12',
                                            sort_by='PublishedAt'
                                        )

def list_general_information():
    # Articles
    articles = top_headlines['articles']
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

def test_article_loop():
    # Test loop for checking total negativity/polarity via the newsapi
    # Also attaching a bit of graphing to this
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





# Take start time, add dt, check if publish date falls in range

def populate_time_blocks(start_time, end_time):
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
            block_start = start_time # First iteration
        block_end = block_start + dt
        blocks += [{'ID' : n, 'items' : [] ,'block_start' : block_start, 'block_end' : block_end}]
    return blocks

#blocks = populate_time_blocks(start_time, end_time) 

print(f"{Fore.RED}-------------------------------------{Style.RESET_ALL}")
for article in articles:
    item_time = pendulum.parse(article['publishedAt'])
    for block in blocks: 
        if ( block['block_start'] >= item_time and item_time <= block['block_end']):
            block['items'] += [article]
            # Add to block
 

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



