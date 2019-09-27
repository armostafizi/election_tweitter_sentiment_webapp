#!/usr/bin/python3

# # Data Cleaning
# 
# Things that are need to be taken care of in data cleaning:
# 
# * Remove links (https, etc.).
# * Remove pnctuations except dots and commas. So later we break them down accordingly.
#   Or maybe *tokenize* does that automatically? Need to check!
# * Remove special characters
# * Remove numbers?
# * remove mentions if not a candidate
#   TODO: try not removing the smilies and emojies and use VADER
#         for sentiment analysis

def clean_tweet(tweet):
    import re
    import string
    import preprocessor as pp
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    
    from expand_hashtags import expand_hashtags
    from remove_mentions import remove_mentions
    from expand_contractions import expand_contractions

    # only remove URL, reserved words, emojies, and smilies.
    # Preserve hashtags and mentions
    pp.set_options(pp.OPT.URL, pp.OPT.RESERVED, pp.OPT.EMOJI, pp.OPT.SMILEY)
    # nltk tokenizer
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    # remove URL, Reserved words (RT, FAV, etc.), Emojies, Smilies, and Numbers.
    # preserve mentions and hastags for now
    tweet = pp.clean(tweet)
    # fix hashtags
    tweet = expand_hashtags(tweet)
    # now remove mentions that are not the candidates
    tweet = remove_mentions(tweet)
    # expand the contractions
    tweet = expand_contractions(tweet)
    # remove 's
    tweet = tweet.replace("'s",'')
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
    
    # TODO: try removing the stop words
    # save stop words to be removed
    # stop_words = set(stopwords.words('english'))
   
    sentences = []
    for sent in tokenizer.tokenize(tweet):
        sent = str(sent)
        # remove ponctuations
        sent = sent.translate(str.maketrans(string.punctuation,
                                            ' '*len(string.punctuation)))
        # consolidate white spaces
        sent = ' '.join(sent.split())
        if len(sent) > 4: # if the sentence is larger than 4 chars
            sentences.append(sent)
    return sentences

if __name__ == '__main__':
    # TODO: write a test for this.
    text = """RT This is a test: @berniesanders: what's up y'all?
How's @alire doing back there? Alire's hands are in the air!
Check out www.alire.me. :)) :-( #beGood!"""

    print('Original Text: %s\nCleaned Text: %s' % (text, clean_tweet(text)))
