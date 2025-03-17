from flask import Flask, request, jsonify
import uuid  # لإنشاء معرفات فريدة للغرف

app = Flask(__name__)

# قائمة لتخزين الغرف
rooms = {}

# قائمة لتخزين مواقع اللاعبين في كل غرفة
player_positions = {}

# عدد اللاعبين في كل غرفة (تم التعديل ليكون 2 فقط)
MAX_PLAYERS = 2  

# مواقع البداية الثابتة للسيارات (مثال لمكانين فقط)
START_POSITIONS = [
    {"x": 0, "y": 0, "rotation": 0},  # الموقع الأول
    {"x": 5, "y": 0, "rotation": 0}   # الموقع الثاني
]

@app.route("/")
def home():
    return jsonify({"message": "✅ السيرفر يعمل بنجاح على Koyeb!"})

@app.route("/join", methods=["POST"])
def join_game():
    """يبحث عن غرفة متاحة أو ينشئ غرفة جديدة وينضم إليها اللاعب"""
    player_id = request.json.get("player_id", str(uuid.uuid4()))

    # البحث عن غرفة غير ممتلئة
    for room_id, players in rooms.items():
        if len(players) < MAX_PLAYERS:
            players.append(player_id)
            # إذا اكتملت الغرفة، يبدأ السباق
            if len(players) == MAX_PLAYERS:
                # توزيع اللاعبين على مواقع البداية
                player_positions[room_id] = {
                    players[0]: START_POSITIONS[0],
                    players[1]: START_POSITIONS[1]
                }
                return jsonify({
                    "room_id": room_id,
                    "players": players,
                    "positions": player_positions[room_id],
                    "status": "full",
                    "message": "🚦 السباق بدأ!"
                })
            return jsonify({"room_id": room_id, "players": players, "status": "waiting", "message": "👥 في انتظار لاعب آخر..."})

    # إذا لم تكن هناك غرفة متاحة، يتم إنشاء غرفة جديدة
    new_room_id = str(uuid.uuid4())
    rooms[new_room_id] = [player_id]
    
    return jsonify({"room_id": new_room_id, "players": rooms[new_room_id], "status": "waiting", "message": "🆕 تم إنشاء غرفة جديدة!"})

@app.route("/update_position", methods=["POST"])
def update_position():
    """تحديث موقع اللاعب وإرساله لباقي اللاعبين"""
    data = request.json
    room_id = data.get("room_id")
    player_id = data.get("player_id")
    position = data.get("position")  # مثال: {"x": 100, "y": 200, "rotation": 45}

    if room_id not in rooms or player_id not in rooms[room_id]:
        return jsonify({"error": "الغرفة غير موجودة أو اللاعب غير موجود!"}), 400

    # حفظ موقع اللاعب
    if room_id not in player_positions:
        player_positions[room_id] = {}

    player_positions[room_id][player_id] = position

    return jsonify({"message": "تم تحديث موقع اللاعب!"})

@app.route("/get_positions", methods=["GET"])
def get_positions():
    """إرسال مواقع جميع اللاعبين في الغرفة"""
    room_id = request.args.get("room_id")

    if room_id not in player_positions:
        return jsonify({"error": "الغرفة غير موجودة أو لا تحتوي على لاعبين!"}), 400

    return jsonify({"positions": player_positions[room_id]})

@app.route("/finish", methods=["POST"])
def finish_race():
    """عند انتهاء السباق، يتم حذف الغرفة"""
    room_id = request.json.get("room_id")
    if room_id in rooms:
        del rooms[room_id]  # حذف الغرفة
        if room_id in player_positions:
            del player_positions[room_id]  # حذف بيانات اللاعبين
        return jsonify({"room_id": room_id, "status": "deleted", "message": "🏁 تم حذف الغرفة بعد انتهاء السباق."})
    
    return jsonify({"error": "الغرفة غير موجودة!"}), 400

@app.route("/rooms", methods=["GET"])
def get_rooms():
    """إرجاع قائمة الغرف النشطة واللاعبين فيها"""
    return jsonify({"active_rooms": rooms})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)