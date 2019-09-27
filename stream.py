## Tweet Streaming Object

import tweepy
#override tweepy.StreamListener to add logic to on_status
class StreamListener(tweepy.StreamListener):
    def __init__(self, max_count, query_phrases, table, connection, verbose):
        from datetime import datetime
        self.count = 0
        self.verbose = verbose
        self.max_count = max_count
        self.last_window = datetime.utcnow()
        self.window_count = 0
        self.window_sentiment = []
        self.table = table
        self.connection = connection
        self.query_phrases = query_phrases
        
    @staticmethod
    def get_text(tweet):
        try:
            if 'retweeted_status' in tweet:
                try:
                    text = tweet['retweeted_status']['extended_tweet']['full_text']
                except:
                    text = tweet['retweeted_status']['text']
            else:
                try:
                    text = tweet['extended_tweet']['full_text']
                except:
                    text = tweet['text']
            return text
        except:
            return
        
    @staticmethod
    def get_time(tweet):
        from datetime import datetime
        return datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')

    def update_agg_sents(self, tweet):
        from datetime import datetime
        import numpy as np

        diff = (tweet.time - self.last_window).total_seconds()
        if diff < 30:
            self.window_count += 1
            self.window_sentiment.append(tweet.sentiment[0])
        else:
            print('Start Time:', self.last_window)
            print('Count:', self.window_count)
            print('Avg Sentiment:', np.mean(self.window_sentiment))
            print('*************')
                        # TODO: For now - change later
            query = self.table.insert().values({'Time' : self.last_window,
                                                'Candidate' : self.query_phrases[0],
                                                'Count' : self.window_count,
                                                'Sentiment' : np.mean(self.window_sentiment)}) 
            ResultProxy = self.connection.execute(query)
            
            self.last_window = datetime.utcnow()
            self.window_count = 0
            self.window_sentiment = []

    def disp(self, data, tweet):
        if self.verbose:
            print('*************')
            print(self.count)
            print('*************')
            print(data['text'])
            print('~~~~~~~~~~~~~')
            tweet.disp()

        
    def on_data(self, data):
        import json
        from tweet import Tweet
        data = json.loads(data)
        text = self.get_text(data)
        timestamp = self.get_time(data)
        tweet = Tweet(text, timestamp)
        # if verbose, print the breakdown
        self.disp(data, tweet)
        self.update_agg_sents(tweet)
        
        self.count += 1
        # finish if the greated than count threshold
        if self.count > self.max_count:
            return False

        return True

    def on_error(self, status):
        print('ERR!!')
        print(status)
        if status == 420:
            return False
        
    def on_status(self, status):
        print(status.text)
