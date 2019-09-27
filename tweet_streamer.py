#!/usr/bin/python3

# Tweet Streamer 
#    This function streams tweets give a list of query phrases.

def stream_tweets(query_phrases, tweet_count, verbose = False):
    import sys
    import tweepy
    import api_keys
    from tweepy import OAuthHandler, API, Stream
    from stream import StreamListener
    
    auth = OAuthHandler(api_keys.API_KEY, api_keys.API_SECRET)
    auth.set_access_token(api_keys.ACS_TOKEN, api_keys.ACS_SECRET)
    api = API(auth, wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)

    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)

    streamListener = StreamListener(max_count = tweet_count, verbose = verbose)
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    
    try:
        stream.filter(track = query_phrases, languages=['en'])
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        print('Done.')
        stream.disconnect()


if __name__ == '__main__':
    import sys
    tweet_count = int(sys.argv[1])
    query_phrases = ['Bernie Sanders', '@BernieSanders']
    stream_tweets(query_phrases = query_phrases,
                  tweet_count = tweet_count,
                  verbose = sys.argv[2].lower() == 'v')
