import os
import re
from flask import Flask, request
import requests

app = Flask(__name__)

# Store seen links in memory (use DB for persistence)
seen_links = set()

BOT_TOKEN = os.environ.get("8466271055:AAFJHcvJ3WR2oAI7g1Xky2760qLgM68WXMM")  # set in Vercel env
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.route("/api/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    urls = re.findall(r'(https?://\S+)', text)
    if urls:
        for url in urls:
            if url in seen_links:
                send_message(chat_id, f"重复粉 ❌❌\n{url}")
            else:
                seen_links.add(url)
                send_message(chat_id, f"正常粉 ✅✅\n{url}")

    return "ok"
