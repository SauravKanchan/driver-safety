import socketio

sio = socketio.Client()
sio.connect('http://localhost:5000')
print("asdf")
sio.emit("test","asdf")
sio.emit(event="asdf",data="asdf")
