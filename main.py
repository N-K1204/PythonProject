from flask import Flask, render_template, request, abort
import os
import logging
from datetime import datetime, timezone, timedelta
import json
import requests
from dotenv import load_dotenv

# --------------------
# 設定
# --------------------
load_dotenv()
LINE_CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
JST = timezone(timedelta(hours=9))
LOG_FILE = "logs_local.txt"
USERS_FILE = "users.json"

COLOR_LABELS = {
    "pink": "😄 うれしい",
    "green": "😌 おちつく",
    "yellow": "😮 びっくり",
    "purple": "😕 もやもや",
    "blue": "😢 さみしい",
    "black": "😴 つかれた",
    "red": "😡 イライラ",
    "white": "😁 期間限定"
}

THEME_COLORS = {
    "pink":   {"bg": "#fff0f7", "main": "#ff8bb0"},
    "green":  {"bg": "#f0fff3", "main": "#6ecb63"},
    "yellow": {"bg": "#fffbe0", "main": "#f1c232"},
    "purple": {"bg": "#f9f5ff", "main": "#b49cff"},
    "blue":   {"bg": "#f0f6ff", "main": "#7da6ff"},
    "black":  {"bg": "#f3f3f3", "main": "#8c8c8c"},
    "red":    {"bg": "#fff0f0", "main": "#ff6f6f"},
    "white":  {"bg": "#ffffff", "main": "#cccccc"}
}

FIXED_MESSAGE = "きもち、うけとったよ！ありがとう😊"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --------------------
# ユーザー管理
# --------------------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(users), f, ensure_ascii=False, indent=2)

users = load_users()

# --------------------
# ログ管理
# --------------------
def save_log(color, emotion_label, user_input):
    if not user_input.strip():
        user_input = "-"
    timestamp = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp}\t{color}\t{emotion_label}\t{user_input}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    logger.info(f"Saved log for color: {color}")

def load_logs(filter_color=None, keyword=None, date=None):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in reversed(f.readlines()):
                if not line.strip(): continue
                parts = line.strip().split("\t")
                if len(parts) < 4: continue
                timestamp, color, emotion_label, user_input = parts
                if filter_color and color != filter_color: continue
                if keyword and keyword not in user_input: continue
                if date and not timestamp.startswith(date): continue
                logs.append({
                    "created_at": timestamp,
                    "color": color,
                    "emotion_label": emotion_label,
                    "user_input": user_input
                })
    return logs

# --------------------
# LINE通知
# --------------------
def send_line_notify(user_ids, message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_TOKEN}"
    }
    for user_id in user_ids:
        payload = {
            "to": user_id,
            "messages": [{"type": "text", "text": message}]
        }
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code != 200:
            logger.error(f"LINE通知失敗: {res.text}")

# --------------------
# Flask ルート
# --------------------
@app.route("/")
def index():
    return render_template("index.html", colors=COLOR_LABELS)

# manifest.json を返す
@app.route("/manifest.json")
def manifest():
    return app.send_static_file("manifest.json")

@app.route("/input/<color>", methods=["GET"])
def input_form(color):
    if color not in COLOR_LABELS:
        return "色が無効です", 400
    theme = THEME_COLORS[color]
    return render_template(
        "input.html",
        color=color,
        emotion_label=COLOR_LABELS[color],
        bg_color=theme["bg"],
        main_color=theme["main"]
    )

@app.route("/generate", methods=["POST"])
def generate():
    color = request.form.get("color")
    user_input = request.form.get("user_input", "")
    if color not in COLOR_LABELS:
        return "色が無効です", 400
    emotion_label = COLOR_LABELS[color]
    save_log(color, emotion_label, user_input)

    # LINE通知を送信
    message = f"💌 {emotion_label} が入力されました！\n内容: {user_input if user_input else '-'}"
    send_line_notify(users, message)

    return render_template("result.html", color=color, emotion_label=emotion_label, message=FIXED_MESSAGE)

@app.route("/logs")
def logs():
    filter_color = request.args.get("color")
    date = request.args.get("date")
    keyword = request.args.get("keyword")
    logs_data = load_logs(filter_color=filter_color, keyword=keyword, date=date)
    return render_template(
        "logs.html",
        logs=logs_data,
        colors=COLOR_LABELS,
        filter_color=filter_color,
        filter_date=date,
        keyword=keyword
    )

# --------------------
# Webhook受信用（友だち追加時にユーザーIDを登録）
# --------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    for event in data.get("events", []):
        if event["type"] == "follow":  # 友だち追加時
            user_id = event["source"]["userId"]
            users.add(user_id)
            save_users(users)
            logger.info(f"新しいユーザー登録: {user_id}")
    return "OK"

# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
