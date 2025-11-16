from flask import Flask, render_template, request
import os
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

COLOR_LABELS = {
    "pink": "😄 うれしい！",
    "green": "😌 おちつく",
    "yellow": "😮 びっくり！",
    "purple": "😕 もやもや",
    "blue": "😢 さみしい...",
    "black": "😴 つかれた...",
    "red": "😡 イライラ"
}

LOG_FILE = "logs_local.txt"

FIXED_MESSAGE = "きもち、うけとったよ！ありがとう😊"


def message(color_label, user_input):
    return FIXED_MESSAGE


def save_log(color, emotion_label, user_input):
    # 空欄なら「-」にする
    if not user_input.strip():
        user_input = "-"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ai_message は保存しない
    line = f"{timestamp}\t{color}\t{emotion_label}\t{user_input}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
        logger.info(f"Saved log for color: {color}")
    except Exception as e:
        logger.error(f"Failed to save log: {e}")


def load_logs(filter_color=None, keyword=None, date=None):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in reversed(f.readlines()):  # 最新順
                if not line.strip():
                    continue  # 空行スキップ
                parts = line.strip().split("\t")
                if len(parts) < 4:
                    continue  # 形式がおかしい行はスキップ
                timestamp = parts[0]
                color = parts[1]
                emotion_label = parts[2]
                user_input = parts[3] if parts[3] else "-"
                # ai_message はもう使わないので読み飛ばす
                if filter_color and color != filter_color:
                    continue
                if keyword and keyword not in user_input:
                    continue
                if date and not timestamp.startswith(date):
                    continue
                logs.append({
                    "created_at": timestamp,
                    "color": color,
                    "emotion_label": emotion_label,
                    "user_input": user_input
                })
    return logs

@app.route("/")
def index():
    return render_template("index.html", colors=COLOR_LABELS)


THEME_COLORS = {
    "pink":   {"bg": "#fff0f7", "main": "#ff8bb0"},
    "green":  {"bg": "#f0fff3", "main": "#6ecb63"},
    "yellow": {"bg": "#fffbe0", "main": "#f1c232"},
    "purple": {"bg": "#f9f5ff", "main": "#b49cff"},
    "blue":   {"bg": "#f0f6ff", "main": "#7da6ff"},
    "black":  {"bg": "#f3f3f3", "main": "#8c8c8c"},
    "red":    {"bg": "#fff0f0", "main": "#ff6f6f"},
}

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
    ai_message = message(emotion_label, user_input)

    # ai_message を保存しない仕様に変更
    save_log(color, emotion_label, user_input)

    return render_template("result.html", color=color, emotion_label=emotion_label, message=ai_message)


@app.route("/logs")
def logs():
    filter_color = request.args.get("color")
    keyword = request.args.get("keyword")
    date = request.args.get("date")

    logs_data = load_logs(filter_color=filter_color, keyword=keyword, date=date)

    return render_template(
        "logs.html",
        logs=logs_data,
        colors=COLOR_LABELS,
        filter_color=filter_color,
        keyword=keyword,
        date=date
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
