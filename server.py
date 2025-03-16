from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

players = {}  # قائمة اللاعبين المتصلين
rooms = {}  # قائمة الغرف المفتوحة
MAX_PLAYERS_PER_ROOM = 6

@app.route('/')
def home():
    return "🚀 سيرفر اللعبة يعمل بنجاح على Koyeb!"

@sock.route('/connect')
def handle_connect(ws):
    player_id = len(players) + 1
    players[player_id] = ws
    print(f"🔗 لاعب متصل: {player_id}")
    assign_player_to_room(player_id)

    while True:
        message = ws.receive()
        if message == "disconnect":
            break

    remove_player_from_room(player_id)
    ws.close()
    print(f"🔴 لاعب خرج: {player_id}")

def assign_player_to_room(player_id):
    for room_id in rooms:
        if len(rooms[room_id]) < MAX_PLAYERS_PER_ROOM:
            rooms[room_id].append(player_id)
            print(f"🎮 اللاعب {player_id} انضم إلى الغرفة {room_id}")
            check_room_status(room_id)
            return

    new_room_id = len(rooms) + 1
    rooms[new_room_id] = [player_id]
    print(f"🆕 غرفة جديدة {new_room_id} تم إنشاؤها")

def remove_player_from_room(player_id):
    for room_id in rooms:
        if player_id in rooms[room_id]:
            rooms[room_id].remove(player_id)
            print(f"🚪 اللاعب {player_id} خرج من الغرفة {room_id}")
            if not rooms[room_id]:
                del rooms[room_id]
                print(f"❌ الغرفة {room_id} تم حذفها")

def check_room_status(room_id):
    if len(rooms[room_id]) == MAX_PLAYERS_PER_ROOM:
        print(f"🏁 الغرفة {room_id} ممتلئة! بدء السباق 🚀")
        start_race(room_id)

def start_race(room_id):
    print(f"🏎️ السباق في الغرفة {room_id} يبدأ الآن!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
