from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ السيرفر يعمل بنجاح على Koyeb!"

# نقطة نهاية لاختبار الاتصال من Godot
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})

# نقطة نهاية لاستقبال بيانات من اللعبة
@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.json  # استلام البيانات بصيغة JSON
    if not data or "player" not in data or "score" not in data:
        return jsonify({"error": "بيانات غير صالحة"}), 400
    
    player = data["player"]
    score = data["score"]
    
    # يمكنك هنا حفظ البيانات في قاعدة بيانات أو معالجتها بأي شكل تريده
    print(f"تم استلام النتيجة: اللاعب {player} حصل على {score} نقطة.")

    return jsonify({"message": "تم استلام النتيجة بنجاح!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
