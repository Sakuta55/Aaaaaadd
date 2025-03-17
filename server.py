from flask import Flask, request, jsonify
import uuid  # لإنشاء معرفات فريدة للغرف

app = Flask(__name__)

# قائمة تخزين الغرف
rooms = {}

# الحد الأقصى للاعبين في الغرفة (تم تغييره إلى 2)
MAX_PLAYERS = 2

# نقاط البداية لكل لاعب
START_POSITIONS = {
    0: "Marker3D1",  
    1: "Marker3D2"
}

@app.route("/")
def home():
    return jsonify({"message": "✅ السيرفر يعمل بنجاح على Koyeb!"})

@app.route("/join", methods=["POST"])
def join_game():
    """يبحث عن غرفة متاحة أو ينشئ غرفة جديدة وينضم إليها اللاعب"""
    player_id = request.json.get("player_id", str(uuid.uuid4()))  # إنشاء player_id إذا لم يكن موجودًا
    
    # البحث عن غرفة غير ممتلئة
    for room_id, players in rooms.items():
        if len(players) < MAX_PLAYERS:
            players.append(player_id)
            start_position = START_POSITIONS[len(players) - 1]  # تحديد نقطة البداية
            
            # إذا اكتملت الغرفة، يبدأ السباق
            if len(players) == MAX_PLAYERS:
                return jsonify({
                    "room_id": room_id,
                    "players": players,
                    "status": "full",
                    "start_positions": {players[i]: START_POSITIONS[i] for i in range(len(players))},
                    "message": "🚦 السباق بدأ!"
                })
            
            return jsonify({
                "room_id": room_id,
                "players": players,
                "status": "waiting",
                "start_position": start_position,
                "message": "👥 في انتظار اللاعب الآخر..."
            })
    
    # إذا لم تكن هناك غرفة متاحة، يتم إنشاء غرفة جديدة
    new_room_id = str(uuid.uuid4())
    rooms[new_room_id] = [player_id]
    
    return jsonify({
        "room_id": new_room_id,
        "players": rooms[new_room_id],
        "status": "waiting",
        "start_position": "Marker3D1",
        "message": "🆕 تم إنشاء غرفة جديدة!"
    })

@app.route("/finish", methods=["POST"])
def finish_race():
    """عند انتهاء السباق، يتم حذف الغرفة"""
    room_id = request.json.get("room_id")
    if room_id in rooms:
        del rooms[room_id]  # حذف الغرفة
        return jsonify({
            "room_id": room_id,
            "status": "deleted",
            "message": "🏁 تم حذف الغرفة بعد انتهاء السباق."
        })
    
    return jsonify({"error": "الغرفة غير موجودة!"}), 400

@app.route("/rooms", methods=["GET"])
def get_rooms():
    """إرجاع قائمة الغرف النشطة واللاعبين فيها"""
    return jsonify({"active_rooms": rooms})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)