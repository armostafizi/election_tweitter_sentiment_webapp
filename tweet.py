# Tweet object

class Tweet:
    def __init__(self, text, time):
        self.time = time
        self.text = text
        self.sentiment = None
        self.sentencize()
        
    # clean tweet and break down sentences
    def sentencize(self):
        from sentence import Sentence
        from clean_tweet import clean_tweet
        import numpy as np
        self.sentences = [Sentence(t) for t in clean_tweet(self.text)]
        # tweet snetiment is the avergae sentiment of all sentences.
        # TODO: Might not be correct!
        self.sentiment = (np.mean([s.sentiment['textblob']['pol'] for s in self.sentences]),
                                  [s.sentiment['textblob']['pol'] for s in self.sentences])
    
    def __str__(self):
        tweet_str = """********************
%s
====================\n""" % (self.text)
        for sentence in self.sentences:
            tweet_str += str(sentence) + '\n' + '--------------------\n'
        tweet_str += 'Compount Sentiment: ' + str(self.sentiment) + '\n********************'
        return tweet_str

    def __repr__(self):
        return self.__str__()
