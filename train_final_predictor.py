# train_final_predictor.py

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import os

# === 設定 ===
MODEL_PATH = "final_predictor_convLSTM.h5"
CSV_PATH = "features_dataset.csv"

# === 入力受け取り ===
img_path = input("🖼️ 入力画像のパスを入力してください（例: ./images/20230920/image001.jpg）: ").strip()
if not os.path.isfile(img_path):
    print(f"❌ 画像ファイルが見つかりません: {img_path}")
    exit()

try:
    temperature = float(input("🌡️ 気温 (℃): "))
    humidity = float(input("💧 相対湿度 (%): "))
except ValueError:
    print("❌ 数値を正しく入力してください。")
    exit()

# === ResNet50 特徴抽出モデル ===
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model

base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
feature_model = Model(inputs=base_model.input, outputs=base_model.output)

def extract_feature(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        feat = feature_model.predict(x, verbose=0)
        return feat.flatten()
    except Exception as e:
        print(f"[×] 特徴抽出失敗: {img_path} → {e}")
        return None

# === 特徴量抽出 ===
img_feat = extract_feature(img_path)
if img_feat is None:
    exit()

# CSVの特徴量に合わせて切り出し（2048次元）
X_feat = img_feat[:2048]

# 天候データを追加（あなたのCSVでは、気温 + 湿度）
X_full = np.concatenate([X_feat, [temperature, humidity]])
X_full = X_full.astype(np.float32).reshape(1, -1)

# === ラベル列の構造チェック（参考用） ===
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    print("✅ CSVから構造を読み込み済み")
    print(f"✔️ 特徴量数: {X_full.shape[1]} 列")
except:
    print("⚠️ CSVファイルの読み込みに失敗しました。")

# === ConvLSTM モデル読み込み ===
if not os.path.exists(MODEL_PATH):
    print(f"❌ モデルファイルが見つかりません: {MODEL_PATH}")
    exit()

model = load_model(MODEL_PATH)
print("✅ モデル読み込み成功")

# ConvLSTM モデルは画像時系列が必要 → (1, T, H, W, C) 形式にする
# 今回は画像1枚 → T=1 としてダミーデータ化
img_sequence = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img_sequence)
x = preprocess_input(x)
x = np.expand_dims(x, axis=0)  # (1, H, W, C)
x = np.expand_dims(x, axis=1)  # (1, 1, H, W, C)

# 天気データ（temperature, humidity）
weather_input = np.array([[temperature, humidity]], dtype=np.float32)

# === 予測（5分〜30分後, 5分刻み） ===
print("\n===== ⏳ 未来予測 (5分〜30分後) =====")
for minutes_ahead in range(5, 31, 5):
    pred_class, pred_reg = model.predict([x, weather_input], verbose=0)

    rain_prob = float(pred_class[0][0])
    pred_mm = float(pred_reg[0][0])

    print(f"\n▶️ {minutes_ahead}分後の予測：")
    print(f"   🌧️ 降水確率（分類）: {rain_prob * 100:.2f} %")
    print(f"   💧 降水量予測（回帰）: {pred_mm:.2f} mm")
    if rain_prob >= 0.5:
        print("   ☔ 雨が降る可能性があります。")
    else:
        print("   ☀ 雨の可能性は低いです。")
