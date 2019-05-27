from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random City Generator Thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 3
        super(RandomThread, self).__init__()

    def randomCityGenerator(self):
        print("Making random numbers")
        city_list = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia', 'chennai', 'hyderabad', 'tornoto',
                     'waterfall', 'bangalore', 'pune']
        while not thread_stop_event.isSet():
            city = random.choice(city_list)
            print(city)
            socketio.emit('newnumber', {'number': city}, namespace='/test')
            sleep(self.delay)

    def run(self):
        self.randomCityGenerator()


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index1.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')

    #Start the random city generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)