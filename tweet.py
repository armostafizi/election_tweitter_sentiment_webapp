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
    
    def disp(self):
        print('********************')
        print(self.text)
        print('====================')
        for sentence in self.sentences:
            print(sentence)
            print('--------------------')
        print('Compount Sentiment:', self.sentiment)
        print('********************')
