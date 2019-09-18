import eventlet
import socketio
import threading
import serial

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)




def print_cube(num):
    """
    function to print cube of given num
    """
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

    # print("Cube: {}".format(num * num * num))


def print_square(num):
    """
    function to print square of given num
    """
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
    # print("Square: {}".format(num * num))


if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))

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