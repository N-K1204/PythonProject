from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
import os
import logging
import psycopg2
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
client = None
if api_key:
    client = OpenAI(api_key=api_key)
    logger.info("OpenAI client initialized successfully")
else:
    logger.warning("OPENAI_API_KEY not found in environment variables")

COLOR_LABELS = {
    "red": "怒ってる時・イライラしてる時",
    "blue": "寂しい時・しょんぼりしてる時",
    "yellow": "落ち着かない時・びっくりした時",
    "green": "落ち着いてる時・ホッとしてる時",
    "pink": "嬉しい時・楽しい時",
    "purple": "モヤモヤしてる時・よく分からない気持ちの時",
    "black": "疲れてる時・何も考えたくない時"
}

def get_db_connection():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    return conn

def generate_ai_message(color_label, user_input):
    if not client:
        logger.warning("Attempted to generate message without API key")
        return "OpenAI APIキーが設定されていません。アプリを使用するには、OPENAI_API_KEYを設定してください。"
    
    prompt = f"""
あなたは子どもの気持ちに寄り添う優しいカウンセラーです。
決して否定せず、その子の気持ちを受け止めて安心させる言葉だけを返してください。

【気持ちの色】: {color_label}
【子どもが書いたこと】: {user_input}

この子の気持ちにそっと寄り添う優しいメッセージを、50文字程度で1つ作ってください。
短く、温かく、受け止める言葉をお願いします。
"""
    try:
        logger.info(f"Generating AI message for emotion: {color_label}, input: {user_input[:50]}...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Failed to generate AI message: {str(e)}")
        return "ごめんなさい、今メッセージを作れませんでした。もう一度試してみてください。"

def save_log(color, emotion_label, user_input, ai_message):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO emotion_logs (color, emotion_label, user_input, ai_message) VALUES (%s, %s, %s, %s)",
            (color, emotion_label, user_input, ai_message)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Saved log for color: {color}")
    except Exception as e:
        logger.error(f"Failed to save log: {str(e)}")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", colors=COLOR_LABELS)

@app.route("/input/<color>", methods=["GET"])
def input_form(color):
    if color not in COLOR_LABELS:
        return "色が無効です", 400
    return render_template("input.html", color=color, emotion_label=COLOR_LABELS[color])

@app.route("/generate", methods=["POST"])
def generate():
    color = request.form.get("color")
    user_input = request.form.get("user_input", "")
    
    if color not in COLOR_LABELS:
        return "色が無効です", 400
    
    if not user_input.strip():
        user_input = "（何も書かなかった）"
    
    emotion_label = COLOR_LABELS[color]
    ai_message = generate_ai_message(emotion_label, user_input)
    
    save_log(color, emotion_label, user_input, ai_message)
    
    return render_template("result.html", color=color, emotion_label=emotion_label, message=ai_message)

@app.route("/logs", methods=["GET"])
def logs():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT color, emotion_label, user_input, ai_message, created_at FROM emotion_logs ORDER BY created_at DESC LIMIT 50")
        logs = cur.fetchall()
        cur.close()
        conn.close()
        
        logs_data = []
        for log in logs:
            logs_data.append({
                "color": log[0],
                "emotion_label": log[1],
                "user_input": log[2],
                "ai_message": log[3],
                "created_at": log[4].strftime("%Y年%m月%d日 %H:%M")
            })
        
        return render_template("logs.html", logs=logs_data, colors=COLOR_LABELS)
    except Exception as e:
        logger.error(f"Failed to fetch logs: {str(e)}")
        return "ログの取得に失敗しました", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
