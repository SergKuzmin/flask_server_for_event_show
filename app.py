import typing
from threading import Lock

import pandas as pd
from flask import Flask
from flask import Response
from flask import render_template
from flask import request
from flask_socketio import SocketIO

from utils.event import Event

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

cache: typing.Optional[pd.DataFrame] = None
change = False


def background_thread():
    global change, cache
    while True:
        socketio.sleep(1)
        data_to_emit = {
            'last_15_events':
                cache[::-1][:15].to_html(),
            'total_peoples_in_bus':
                cache['num_in'].sum() - cache['num_out'].sum(),
            'length_of_table':
                len(cache)
        }
        if change and len(cache) != 0:
            socketio.emit('table', data_to_emit)
            change = False


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route("/add_event", methods=['POST'])
def add_row():
    global cache, change
    request_data = request.form.to_dict()
    row_to_add = Event.serializer(request_data)
    cache = cache.append(row_to_add, ignore_index=True) \
        if cache is not None else pd.DataFrame(cache)
    change = True
    return Response(status=200)


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


if __name__ == '__main__':
    app.run()
