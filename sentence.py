# Sentence Object

class Sentence:
    def __init__(self, text):
        self.text = text
        self.sentiment = []
        self.sentimentize()
    
    # calculate sentiment for the sentence
    def sentimentize(self, compare = True):
        from sentiment import get_sentiment
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
        return '%s >>>>> Pol: %.1f (Sub: %.1f)' % (self.text,
                                                   self.polarity,
                                                   self.subjectivity) 
