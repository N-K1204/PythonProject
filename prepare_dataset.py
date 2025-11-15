# prepare_dataset.py

import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model

# === 設定 ===
img_root = r'\\150.89.226.195\Private\6期生\小畑\img_data'  # 画像フォルダ（YYYYMMDD サブフォルダあり）
csv_root = r'\\150.89.226.195\Private\7期生\西山\Attached_WeatherData'  # A_model_*.csvなど
output_path = r'features_dataset.csv'  # 出力ファイル

# === モデル準備（ResNet50, avg_pool出力） ===
base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
feature_model = Model(inputs=base_model.input, outputs=base_model.output)

def extract_features(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        feat = feature_model.predict(x, verbose=0)
        return feat.flatten()
    except Exception as e:
        print(f"[×] 画像読み込み失敗: {img_path} → {e}")
        return None

# === 処理開始 ===
all_features = []
all_labels = []

csv_files = sorted([f for f in os.listdir(csv_root) if f.endswith('.csv')])

for csv_file in tqdm(csv_files, desc="CSV処理中"):
    csv_path = os.path.join(csv_root, csv_file)
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    # 日付フォルダ名取得
    date_folder = csv_file.split('_')[-1].split('.')[0]
    img_folder = os.path.join(img_root, date_folder)
    if not os.path.exists(img_folder):
        print(f"[×] 対応する画像フォルダが見つかりません: {img_folder}")
        continue

    for _, row in df.iterrows():
        img_file = row['filename']
        img_path = os.path.join(img_folder, img_file)
        feat = extract_features(img_path)
        if feat is None:
            continue

        # 気象特徴（必要なら追加）
        weather_feat = [
            row.get('temperature', np.nan),
            row.get('humidity', np.nan)
        ]

        # ラベル（降水量）
        label = row.get('precipitation', np.nan)

        all_features.append(np.concatenate([feat, weather_feat]))
        all_labels.append(label)

# === 保存 ===
feat_df = pd.DataFrame(all_features)

# ラベル列追加（回帰用と分類用）
feat_df['precipitation'] = all_labels
feat_df['rain_mm'] = feat_df['precipitation']
feat_df['label'] = (feat_df['precipitation'] > 0).astype(int)

feat_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ 完了：{len(feat_df)}件の特徴データを {output_path} に保存しました。")
