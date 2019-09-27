#!/usr/bin/python3

# Data Cleaning:
#   Expand hashtags
#      Don't remove them! Break them apart if the words are separated by "_" or
#      are capitalization, and remove th "#".
#      TODO: Break if alphabet changes to numbers or vice versa.

def expand_hashtags(tweet):
    import re
    # first replace underscore with space
    words = tweet.split()
    clean_words = []
    for word in words:
        if word.startswith('#'): # if hashtag
            # break up with "_" and remove the "#"
            hashtag_words = word[1:].split("_")
            for hashtag_word in hashtag_words:
                # break up and put together again with space if hashtag was capitalized
                hashtag_word = ' '.join([a for a in re.split('([A-Z][a-z]+)',
                                                             hashtag_word) if a])
                clean_words.append(hashtag_word)
        else:
            clean_words.append(word)
    return ' '.join(clean_words)

if __name__ == '__main__':
    text = """remove this #hashTag or #this or #ThisOne,
or maybe #this_one! or why not #this_oneHashTag!? #ThisIsAHashtag!"""
    print('Original Text: %s\nCleaned Hashtags: %s' % (text, expand_hashtags(text)))
