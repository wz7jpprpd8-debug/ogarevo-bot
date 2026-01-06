import os
import json
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

CONFIG_FILE = "config.json"

# значения по умолчанию
source_chat_id = None
target_chat_id = None


def load_config():
    global source_chat_id, target_chat_id
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            source_chat_id = data.get("source_chat_id")
            target_chat_id = data.get("target_chat_id")


def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(
            {
                "source_chat_id": source_chat_id,
                "target_chat_id": target_chat_id,
            },
            f
        )


# загружаем конфиг при старте
load_config()


@app.route("/", methods=["POST"])
def webhook():
    global source_chat_id, target_chat_id

    update = request.json
    if not update:
        return "ok"

    message = update.get("message")
    if not message:
        return "ok"

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/source":
        source_chat_id = chat_id
        save_config()
        requests.post(
            f"{API}/sendMessage",
            json={"chat_id": chat_id, "text": "✅ Источник сохранён"}
        )

    elif text == "/target":
        target_chat_id = chat_id
        save_config()
        requests.post(
            f"{API}/sendMessage",
            json={"chat_id": chat_id, "text": "✅ Приёмник сохранён"}
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
