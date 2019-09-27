#!./venv/bin/python3

# Web App Core

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    from tweet_downloader import download_tweets
    tweets = download_tweets(query_phrase = 'Bernie Sanders', tweet_count = 2)
    string = ''
    for tweet in tweets:
        string += str(tweet) + '\n'
    return string.replace('\n', '<br/>')

if __name__ == '__main__':
    app.run(debug=True)
