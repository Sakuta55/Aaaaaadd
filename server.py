from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return "Server is running!"

@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("message", {"data": "Connected to server"})

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)
    emit("message", {"data": f"Joined room {room}"}, room=room)

@socketio.on("leave")
def handle_leave(data):
    room = data["room"]
    leave_room(room)
    emit("message", {"data": f"Left room {room}"}, room=room)

@socketio.on("message")
def handle_message(data):
    room = data["room"]
    message = data["message"]
    emit("message", {"data": message}, room=room)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, allow_unsafe_werkzeug=True)