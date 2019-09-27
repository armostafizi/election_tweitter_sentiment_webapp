#!/usr/bin/python3


# Tweet downloader
#     This downloads tweets to test clearning and sentiment analysis with
#     tweeter rest api. This is for testing if the cleaning and sentiment
#     analysis is working as expected.

def download_tweets(query_phrase, tweet_count):
    import api_keys
    import tweepy
    from datetime import datetime
    from tweet import Tweet
    # authorization
    auth = tweepy.AppAuthHandler(api_keys.API_KEY, api_keys.API_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                           # wait until the limit is replenished
                           wait_on_rate_limit_notify=True) 
                           # reply with a message if the limit is reached

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
            
        ts = datetime.strptime(status._json['created_at'],
                               '%a %b %d %H:%M:%S +0000 %Y')
        tweets.append(Tweet(full_text, ts))
    return tweets


if __name__ == '__main__':
    import sys
    tweet_count = int(sys.argv[1])
    tweets = download_tweets(query_phrase = 'Bernie Sanders', tweet_count = tweet_count)
    for tweet in tweets:
        tweet.disp()
