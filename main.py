from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
client = None
if api_key:
    client = OpenAI(api_key=api_key)

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
        return "OpenAI APIキーが設定されていません。アプリを使用するには、OPENAI_API_KEYを設定してください。"
    
    prompt = f"""
あなたは子どもの気持ちに寄り添う優しいカウンセラーです。
決して否定せず、その子の気持ちを受け止めて安心させる言葉だけを返してください。

【気持ちの色】:
{color_label}

この気持ちにそっと寄り添うメッセージを、80文字程度で1つ作ってください。
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

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
