#!/usr/bin/env python
# coding: utf-8

# # Democratic Candidates
# This notebook analyzes the sentiment of the tweets posted for democratic candidates. There are a few ideas that i need to consider. For instance,
# 
# 1. The number of positive and negative tweets posted for each candidate
# 2. The proportion of positivity and negativity
# 3. How these change over time and possibly after each debate or major event
# 4. Is there any relationship between the tweets sentiments and the pols?
# 5. The location of the sentiments, broken down to the states, possibly focusing on the swing states.
# 6. We can expand the analysis beyond the tweets and to the *users/voters*.
# 7. Make a word cloud for the tweets about each candidate?

# ## Tweeter Data
# I start with pulling some data from the major candidates from twitter, Elizabeth Warren, Bernine Sanders, and Joe Biden. For this, I used *tweepy*.

# In[126]:


# fetch api keys from api_keys.py

from api_keys import *

query = {'@BernieSanders': 'Bernie Sanders',     # Bernie
         '@ewarren':       'Elizabeth Warren',   # Elizabeth
         '@KamalaHarris':  'Kamala Harris',      # Kamala
         '@PeteButtigieg': 'Pete Buttigieg',     # Pete
         '@JoeBiden':      'Joe Biden',          # Joe Biden
         }

query = dict((k.lower(), v.lower()) for k,v in query.items())

# make everything lowercase for consitency
mentions = list(query.keys())
names = list(query.values())


# # Data Cleaning
# 
# Things that are need to be taken care of in data cleaning.
# 
# * Remove links (https, etc.).
# * Remove pnctuations except dots and commas. So later we break them down accordingly. Or maybe *tokenize* does that automatically? Need to check!
# * Remove special characters
# * Remove numbers?

# In[4]:


# clean the tweet
import re
import string
from textblob import TextBlob
import preprocessor as pp
#nltk.download('stopwords')
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from contractions import contractions

# only remove URL, reserved words, emojies, and smilies. Preserve hashtags and mentions
pp.set_options(pp.OPT.URL, pp.OPT.RESERVED, pp.OPT.EMOJI, pp.OPT.SMILEY)
# save stop words to be removed
stop_words = set(stopwords.words('english'))
# nltk tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# For the contractions
contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))

# remove mentions if not a candidate
def remove_mentions(tweet, mentions):
    words = tweet.split()
    clean_words = []
    for w in words:
        if w.startswith('@'):
            candidate_mentioned = False
            for m in mentions:
                if m in w:
                    candidate_mentioned = True
                    clean_words.append(w.replace(m, query[m].lower()))
                    break
            if not candidate_mentioned:
                clean_words.append(w[1:]) # remove @
        else:
            clean_words.append(w)
    return ' '.join(clean_words)

# expand hashtags
def fix_hashtags(tweet):
    # first replace underscore with space
    tweet = tweet.replace('_', ' ')
    words = tweet.split()
    clean_words = []
    for w in words:
        if w.startswith('#'):
            w = ' '.join([a for a in re.split('([A-Z][a-z]+)', w[1:]) if a])
        clean_words.append(w)
    return ' '.join(clean_words)

def expand_contractions(tweet):
    def replace(match):
        # expand the contraction with the most possible alternative : [0]
        return contractions[match.group(0)][0]
    return contractions_re.sub(replace, tweet)
    
def clean_tweet(tweet):
    # remove URL, Reserved words (RT, FAV, etc.), Emojies, Smilies, and Numbers.
    # preserve mentions and hastags for now
    tweet = pp.clean(tweet)
    # fix hashtags
    tweet = fix_hashtags(tweet)
    # make the tweet lowercase
    tweet = tweet.lower()
    # now remove mentions that are not the candidates
    tweet = remove_mentions(tweet, mentions)
    # conver U+2019 to U+0027 (apostrophe)
    tweet = tweet.replace(u"\u2019", u"\u0027")
    # expand the contractions
    tweet = expand_contractions(tweet)
    # remove 's
    tweet = tweet.replace("'s",'')
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
    # break into sentences
    # tb = TextBlob(tweet)
    sentences = []
    for sent in tokenizer.tokenize(tweet):
#    for sent in tb.sentences: # for this punkt package of nltk has to be downloaded once
#                              # with the following code:
#                              # import nltk
#                              # nltk.download('punkt')
        sent = str(sent)
        # remove ponctuations
        sent = sent.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
        # consolidate white spaces
        sent = ' '.join(sent.split())
        if len(sent) > 4: # if the sentence is larger than 4 chars
            sentences.append(sent)
    return sentences


# # Sentiment Analysis
# Each tweet might comprise multiple sentences. Therefore each tweet must be broken down to different sentences with *tokenize* functionality of *TextBlob*. The final sentiment can be a function of the sentiment of different sentences, perhaps the average (?).

# In[130]:


from textblob import TextBlob

# This needs more work to be more accurate. Some ideas:
#    1. Don't remove emoticons and use vader
#    2. clean stopwrds and everything else, and use outofthebox texblob
#    3. Read papers on political sentiment analysis with twitter
def get_sentiment(text, mode = 'textblob'):
    if mode == 'textblob':
        testimonial = TextBlob(text)
        return {'pol': testimonial.sentiment.polarity,
                'subj': testimonial.sentiment.subjectivity}
    elif mode == 'nltk':
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        sid = SentimentIntensityAnalyzer()
        return sid.polarity_scores(text)
    elif mode == 'api':    
        import requests   
        # api-endpoint 
        URL = "http://text-processing.com/api/sentiment/"
        params = {'text':text}
        r = requests.post(url = URL, data = params)
        data = r.json()
        return(data['probability'])
    elif mode == 'vader':
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(text)


# # Tweet and Sentence Objects
# Let's makes some classes and methods for tweets and sentences that cleans and gets the sentiment of the tweets.

# In[194]:


# sentence object
import numpy as np

class Sentence:
    def __init__(self, text):
        self.text = text
        self.sentiment = []
        self.sentimentize()
    
    # calculate sentiment for the sentence
    def sentimentize(self, compare = True):
        if compare:
            self.sentiment = dict()
            for mode in ['nltk', 'vader', 'textblob', 'api']:
                self.sentiment[mode] = get_sentiment(self.text, mode)
        else:
            self.sentiment = {'textblob': get_sentiment(self.text, mode = 'textblob')}
            
    def __str__(self):
        import json
        sentiment_str = ''
        for s in self.sentiment:
            sentiment_str += s + ': ' + json.dumps(self.sentiment[s]) + '\n'
        return '%s >>>>> \n%s' % (self.text, sentiment_str)
    
    def __repr__(self):
        return '%s >>>>> Pol: %.1f (Sub: %.1f)' % (self.text, self.polarity, self.subjectivity)
        
# tweet object
class Tweet:
    def __init__(self, text, time):
        self.time = time
        self.text = text
        self.sentiment = None
        self.sentencize()
        
    # clean tweet and break down sentences
    def sentencize(self):
        self.sentences = [Sentence(t) for t in clean_tweet(self.text)]
        # tweet snetiment is the avergae sentiment of all sentences. TODO: Might not be correct!
        self.sentiment = (np.mean([s.sentiment['textblob']['pol'] for s in self.sentences]),
                                  [s.sentiment['textblob']['pol'] for s in self.sentences])
    
    def disp(self):
        print('********************')
        print(self.text)
        print('====================')
        for sentence in self.sentences:
            print(sentence)
            print('--------------------')
        print('Compount Sentiment:', self.sentiment)
        print('********************')
    


# # Tweet downloader
# This downloads tweets to test clearning and sentiment analyis.

# In[214]:


# REST API
import tweepy
import sys

def get_sample_tweets(query_phrase, tweet_count):
    # authorization
    auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,           # wait until the limit is replenished
                           wait_on_rate_limit_notify=True)    # reply with a message if the limit is reached

    # check if not authorized
    if (not api):
        print ("Can't Authenticate")
        return

    tweets = []
    for status in tweepy.Cursor(api.search, q = query_phrase,
                                        tweet_mode = 'extended',
                                        lang = 'en').items(tweet_count):
        try:
            full_text = status._json['retweeted_status']['full_text']
        except:
            full_text = status._json['full_text']
            
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(status._json['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        tweets.append(Tweet(full_text, ts))
    return tweets


# # Test
# Now let's download some tweets and test the *cleaning* and *sentiment analysis*

# In[197]:


tweets = get_sample_tweets(query_phrase = 'bernie sanders', tweet_count = 1)

for tweet in tweets:
    tweet.disp()


# # Streaming
# 
# Now let's stream the tweets in real time and process them.

# In[248]:


## STREAMING

import tweepy
import json
from datetime import datetime
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
auth = OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACS_TOKEN, ACS_SECRET)
api = API(auth, wait_on_rate_limit=True,
                wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
# Continue with rest of code

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, max_count = 5, verbose = False):
        from datetime import datetime
        self.count = 0
        self.verbose = verbose
        self.max_count = max_count
        self.last_window = datetime.utcnow()
        self.window_count = 0
        self.window_sentiment = []
        
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
        #strftime('%Y-%m-%d %H:%M:%S',
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
        data = json.loads(data)
        text = self.get_text(data)
        timestamp = self.get_time(data)
        tweet = Tweet(text, timestamp)
        #print((tweet.time - self.last_window).total_seconds(), tweet.sentiment)
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


# In[225]:


# TEST
max_count = 1      
myStreamListener = MyStreamListener(max_count = max_count, verbose = True)
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

try:
    myStream.filter(track = mentions + names, languages=['en'])
except KeyboardInterrupt:
    print("Stopped.")
finally:
    print('Done.')
    myStream.disconnect()


# # Steam and plot
# Try streaming and plotting the results on the go for **Bernie Sanders** only!

# In[250]:


max_count = 1000
myStreamListener = MyStreamListener(max_count = max_count)
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

try:
    myStream.filter(track = ['Donald Trump', '@realdonaldtrump'], languages=['en'])
except KeyboardInterrupt:
    print("Stopped.")
finally:
    print('Done.')
    myStream.disconnect()

