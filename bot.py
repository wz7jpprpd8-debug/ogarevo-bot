import requests
from flask import Flask, request

BOT_TOKEN = "8505704573:AAH0ifNiICpePSMVnc0IvUUHiN91aYUcgew"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

source_chat_id = None
target_chat_id = None


@app.route("/", methods=["POST"])
def webhook():
    global source_chat_id, target_chat_id

    update = request.json
    message = update.get("message")
    if not message:
        return "ok"

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/source":
        source_chat_id = chat_id
        requests.post(
            f"{API}/sendMessage",
            json={"chat_id": chat_id, "text": "Источник сохранён"}
        )

    elif text == "/target":
        target_chat_id = chat_id
        requests.post(
            f"{API}/sendMessage",
            json={"chat_id": chat_id, "text": "Приёмник сохранён"}
        )

    elif source_chat_id and target_chat_id and chat_id == source_chat_id:
        if message.get("from", {}).get("is_bot"):
            return "ok"

        requests.post(
            f"{API}/copyMessage",
            json={
                "chat_id": target_chat_id,
                "from_chat_id": source_chat_id,
                "message_id": message["message_id"]
            }
        )

    return "ok"