from flask import Flask, request, jsonify

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def home():
    return "✅ السيرفر يعمل بنجاح!"

# مثال على API لاستقبال طلب من Godot
@app.route("/join_game", methods=["POST"])
def join_game():
    data = request.json  # استقبال البيانات من الطلب
    player_name = data.get("player_name", "لاعب مجهول")  # جلب اسم اللاعب

    response = {
        "message": f"👋 مرحبًا {player_name}, لقد انضممت إلى اللعبة!",
        "status": "success"
    }
    return jsonify(response)  # إرجاع استجابة بصيغة JSON

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
