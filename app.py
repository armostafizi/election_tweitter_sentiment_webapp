#!./venv/bin/python3


# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, " +\
                                            "must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 10
        super(RandomThread, self).__init__()

    def monitor_sentimentsDB(self):
        import sqlalchemy as db
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import func
        from sqlalchemy_declarative import Base, Sentiment_ent
        print("Monitoritng Sentiments DB")
        engine = db.create_engine("sqlite:///election.sqlite")
        metadata = db.MetaData(engine)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        last_id = None
        while not thread_stop_event.isSet():
            obj = session.query(Sentiment_ent).order_by(Sentiment_ent.Id.desc()).first()
            print(str(obj))
            if last_id != obj.Id:
                print('sending data ...')
                socketio.emit('newdata', {'txt': str(obj)}, namespace='/test')
            last_id = obj.Id
            sleep(self.delay)

    def run(self):
        self.monitor_sentimentsDB()


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@app.route('/downloader')
def test_downloader():
    from tweet_downloader import download_tweets
    tweets = download_tweets(query_phrase = 'Bernie Sanders', tweet_count = 2)
    string = ''
    for tweet in tweets:
        string += str(tweet) + '\n'
    return string.replace('\n', '<br/>')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
    


