#!./venv/bin/python3

# Data Cleaning
#   Remove Mentions
#   remove the mention is it is not the candidate. If it is, remove the @

def remove_mentions(tweet):
    import re
    from var import mentions, query
    # starting with @ and following by alphanumeric and underscore
    mention_regex = re.compile('@[a-z|0-9|_]+')
    tweet = tweet.lower()
    words = tweet.split()
    clean_words = []
    for word in words:
        if word.startswith('@'):
            candidate_mentioned = False
            for m in mentions:
                if m.lower() in word:
                    candidate_mentioned = True
                    # replace with extra spaces just in case, we'll strip it later
                    clean_words.append(word.replace(m.lower(),
                                       ' ' + query[m] + ' '))
                    break
            if not candidate_mentioned:
                #word = mention_regex.sub('pnm', word) # Proper Noun Mrntion
                word = mention_regex.sub(' ', word) # replace with a space
                clean_words.append(word)
        else:
            clean_words.append(word)
    return ' '.join(clean_words)

if __name__ == '__main__':
    text = """This mentions has to be swaped with the name: @berniesanders or @BernieSanders
Also these ones with colon: @berNieSanderS: and @eWarren: or at the end of sentencs like this:
@ewarren! or @bernieSanders. or @ewarren? But these have to be changed with PNM: @alire or
@Alire_M or @_anything!"""

    print('Otiginal Text: %s\nRemoved Mentions: %s' % (text, remove_mentions(text)))
