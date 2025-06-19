from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(
    app,
    origins=["http://localhost:3000", "https://demo-send-email.onrender.com"],
)  # Cho phép React gọi API


# Email configuration from .env
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
receiver_email = os.getenv("MAIL_DEFAULT_RECEIVER")
mail = Mail(app)

# Cơ sở dữ liệu tạm trong RAM
memory_db = {
    "fruits": [
        {"name": "kiwi"},
        {"name": "apple"},
        {"name": "banana"},
        {"name": "orange"},
        {"name": "grape"},
    ]
}


# Lấy danh sách trái cây
@app.route("/fruits", methods=["GET"])
def get_fruits():
    return jsonify({"fruits": memory_db["fruits"]})


# Thêm trái cây mới
@app.route("/fruits", methods=["POST"])
def add_fruit():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' field"}), 400

    fruit = {"name": data["name"]}
    memory_db["fruits"].append(fruit)

    try:
        msg = Message(
            subject="Thêm trái cây mới",
            recipients=[receiver_email],
            body=f"Đã thêm: {fruit['name']}",
        )
        mail.send(msg)
    except Exception as e:
        return jsonify({"error": f"Lỗi gửi mail: {str(e)}"}), 500

    return jsonify(fruit), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
