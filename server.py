from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

rooms = {}
MAX_PLAYERS = 2

START_POSITIONS = {
    0: "Marker3D1",
    1: "Marker3D2"
}

@app.route("/")
def home():
    return jsonify({"message": "✅ السيرفر يعمل بنجاح على Koyeb!"})

@app.route("/join", methods=["POST"])
def join_game():
    player_id = request.json.get("player_id", str(uuid.uuid4()))

    for room_id, players in rooms.items():
        if len(players) < MAX_PLAYERS:
            players.append(player_id)
            start_position = START_POSITIONS[len(players) - 1]

            return jsonify({
                "room_id": room_id,
                "players": players,
                "status": "full" if len(players) == MAX_PLAYERS else "waiting",
                "start_positions": {players[i]: START_POSITIONS[i] for i in range(len(players))},
                "message": "🚦 السباق بدأ!" if len(players) == MAX_PLAYERS else "👥 في انتظار اللاعب الآخر..."
            })

    new_room_id = str(uuid.uuid4())
    rooms[new_room_id] = [player_id]

    return jsonify({
        "room_id": new_room_id,
        "players": rooms[new_room_id],
        "status": "waiting",
        "start_positions": {player_id: START_POSITIONS[0]},  # تأكد من وجود نقطة البداية دائمًا
        "message": "🆕 تم إنشاء غرفة جديدة!"
    })

@app.route("/finish", methods=["POST"])
def finish_race():
    room_id = request.json.get("room_id")
    if room_id in rooms:
        del rooms[room_id]
        return jsonify({
            "room_id": room_id,
            "status": "deleted",
            "message": "🏁 تم حذف الغرفة بعد انتهاء السباق."
        })
    return jsonify({"error": "الغرفة غير موجودة!"}), 400

@app.route("/rooms", methods=["GET"])
def get_rooms():
    return jsonify({"active_rooms": rooms})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)