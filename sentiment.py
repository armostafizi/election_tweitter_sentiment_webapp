#!./venv/bin/python3

# Sentiment Analysis
#    Returns the sentiment of a text with different methods
#    Each tweet might comprise multiple sentences. Therefore each tweet must be
#    broken down to different sentences with *tokenize* functionality of *TextBlob*.
#    The final sentiment can be a function of the sentiment of different sentences,
#    perhaps the average (? )

# This needs more work to be more accurate. Some TODO ideas:
#    1. Don't remove emoticons and use vader
#    2. clean stopwrds and everything else, and use outofthebox texblob
#    3. Read papers on political sentiment analysis with twitter.

def get_sentiment(text, mode = 'textblob'):
    if mode == 'textblob':
        from textblob import TextBlob
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

if __name__ == '__main__':
    text = 'This is good!'
    print(text)
    print(get_sentiment(text, mode = 'textblob'))
    print(get_sentiment(text, mode = 'api'))
    print(get_sentiment(text, mode = 'nltk'))
    print(get_sentiment(text, mode = 'vader'))
