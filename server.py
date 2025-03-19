from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# عدد اللاعبين المتصلين
player_count = 0

@app.route("/")
def index():
    return "🚀 WebSocket Server is running!"

@socketio.on("connect")
def on_connect():
    global player_count
    player_count += 1
    print(f"✅ لاعب متصل! العدد الحالي: {player_count}")

    # إرسال عدد اللاعبين إلى جميع المتصلين
    emit("update_count", {"count": player_count}, broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    global player_count
    player_count -= 1
    print(f"❌ لاعب غادر! العدد الحالي: {player_count}")

    # تحديث عدد اللاعبين بعد الخروج
    emit("update_count", {"count": player_count}, broadcast=True)

@socketio.on("join")
def on_join(data):
    player_id = data.get("player_id", "unknown")
    print(f"🎮 لاعب جديد انضم: {player_id}")

    # إرسال الحدث إلى الجميع ليتمكن العميل (Godot) من معالجة الانضمام
    emit("player_joined", {"player_id": player_id}, broadcast=True)

if __name__ == "__main__":
    print("🚀 بدء تشغيل السيرفر على المنفذ 8000 ...")
    socketio.run(app, host="0.0.0.0", port=8000)