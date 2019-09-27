#!/usr/bin/python3

# Data Cleaning
#   Expand Contractions 
#   Expand the contratciton in english: i'm -> i am
#   Refer to contractions.py for a complete list.
#   TODO: At the current stage it picks the most probable contraction, example, I'd -> I would
#         and not "I had"

def expand_contractions(tweet):
    import re
    from contractions import contractions
    tweet = tweet.lower()
    #convert U+2019 to U+0027 (apostrophe)
    tweet = tweet.replace(u"\u2019", u"\u0027")
    contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))
    def replace(match):
        # expand the contraction with the most possible alternative : [0]
        return contractions[match.group(0)][0]
    return contractions_re.sub(replace, tweet)
    
if __name__ == '__main__':
    text = """i'm fine!"""
    print('Original Text: %s\nUncontracted Text: %s' % (text, expand_contractions(text)))
