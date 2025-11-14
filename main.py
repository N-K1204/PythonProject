from flask import Flask, render_template, request
from openai import OpenAI
import os
import logging

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

def generate_ai_message(color_label):
    if not client:
        logger.warning("Attempted to generate message without API key")
        return "OpenAI APIキーが設定されていません。アプリを使用するには、OPENAI_API_KEYを設定してください。"
    
    prompt = f"""
あなたは子どもの気持ちに寄り添う優しいカウンセラーです。
決して否定せず、その子の気持ちを受け止めて安心させる言葉だけを返してください。

【気持ちの色】:
{color_label}

この気持ちにそっと寄り添うメッセージを、80文字程度で1つ作ってください。
"""
    try:
        logger.info(f"Generating AI message for emotion: {color_label}")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Failed to generate AI message: {str(e)}")
        return "ごめんなさい、今メッセージを作れませんでした。もう一度試してみてください。"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", colors=COLOR_LABELS)

@app.route("/select/<color>", methods=["GET"])
def select(color):
    if color not in COLOR_LABELS:
        return "色が無効です", 400
    message = generate_ai_message(COLOR_LABELS[color])
    return render_template("result.html", color=color, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
