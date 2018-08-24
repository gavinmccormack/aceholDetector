
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA() # Sentiment intensity analyser

grim = "I'm going to make an asshole detector"
polarity_stats = sia.polarity_scores(grim)
print(polarity_stats)
torrenz = "insane death retard"
polarity_stats = sia.polarity_scores(torrenz)
print(polarity_stats)  