import eventlet
import socketio
import threading
import serial
from flask import Flask, render_template


sio = socketio.Server()
app = Flask(__name__)

app = socketio.Middleware(sio, app)


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)




def server():
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


def read_data():
    ser = serial.Serial()
    ser.port = '/dev/ttyUSB1'
    ser.open()
    data = ""

    while True:
        d = ser.read().decode("utf-8")
        if d != "\n":
            data += d
        else:
            print(data)
            data = ""
            sio.emit("test",data)

if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=server)
    t2 = threading.Thread(target=read_data)

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    # both threads completely executed
    print("Done!")