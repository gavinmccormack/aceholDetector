# /usr/bin/python
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pendulum

class sentiment(object):
    def __init__(self, data):
        self.sia = SIA()
        self.data = data
        self.unreadable_data = [] # List of unreadable indexes
        self.total_negative = 0
        self.total_positive = 0
        self.total_compound = 0
        print("Running aceholSentiment")
        self.validate_data()
        #self.add_sentiment_fields()

    def dframe(self):
        """ Return the data frame """
        return self.data

    def add_sentiment_fields(self):
        """ Process the data and add sentiment columns to the data """
        for n in range(0, len( self.data['message'] ) ):
            text = str(self.data['message'][n])
            print(self.data['time'][n])
            item_time = pendulum.parse(self.data['time'][n])
            # SIA will create an object with pos, neg, and compound stats. Additional fields are added and the data is updated
            sentiment_stats = self.sia.polarity_scores(text)
            sentiment_stats['author'] = self.data['author'][n] # Not ideal for title/body/more layered data to have these defined here
            sentiment_stats['message'] = text
            sentiment_stats['time'] = item_time 
    
    def validate_data(self):
        """ Run through CSV and remove invalid data points """
        for n in range(0, len( self.data['message'] ) ):
            try:
                pendulum.parse(self.data['time'][n])
                print("Did 'time' work?", self.data['time'][n])
            except:
                print("Warning: Incorrect time at row ", n)
                self.data.drop(n)
                self.unreadable_data += [n]
        print(self.unreadable_data)