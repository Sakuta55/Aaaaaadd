from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # دعم WebSockets

rooms = {}
MAX_PLAYERS = 2

@app.route("/")
def home():
    return jsonify({"message": "✅ السيرفر يعمل بنجاح عبر WebSockets على Koyeb!"})

@socketio.on("join")
def handle_join(data):
    player_id = data.get("player_id", str(uuid.uuid4()))
    
    for room_id, players in rooms.items():
        if len(players) < MAX_PLAYERS:
            players.append(player_id)
            join_room(room_id)
            emit("player_joined", {"room_id": room_id, "players": players}, room=room_id)
            return
    
    new_room_id = str(uuid.uuid4())
    rooms[new_room_id] = [player_id]
    join_room(new_room_id)
    emit("new_room", {"room_id": new_room_id, "players": [player_id]}, room=new_room_id)

@socketio.on("finish")
def handle_finish(data):
    room_id = data.get("room_id")
    if room_id in rooms:
        del rooms[room_id]
        emit("room_deleted", {"room_id": room_id}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000)