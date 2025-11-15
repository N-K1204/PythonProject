import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model

# === 1. 学習済みモデルの読み込み ===
model = load_model("final_predictor_model.h5")

# === 2. ResNet50モデルで画像特徴抽出 ===
base_model = ResNet50(weights="imagenet", include_top=False, pooling="avg")
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
        print(f"[×] 画像読み込み失敗: {e}")
        return None

# === 3. 入力データ（画像と気象） ===

# 🔻 編集して入力してください 🔻
image_path = "new_sample.jpg"        # 新しい画像ファイル
temperature = 28.5                   # 気温（例：28.5度）
humidity = 75.0                      # 湿度（例：75%）

# === 4. 特徴ベクトルを組み立てる ===
img_feat = extract_features(image_path)
if img_feat is None:
    exit()

weather_feat = [temperature, humidity]
input_data = np.concatenate([img_feat, weather_feat])
input_data = input_data.reshape(1, -1)  # (1, feature_dim)

# === 5. 予測 ===
y_pred_class, y_pred_reg = model.predict(input_data)
predicted_label = int(y_pred_class[0][0] > 0.5)
predicted_rain_mm = float(y_pred_reg[0][0])

# === 6. 結果表示 ===
print("===== 予測結果 =====")
print(f"降水の有無（分類）: {'あり' if predicted_label == 1 else 'なし'}")
print(f"降水量の予測値（mm）: {predicted_rain_mm:.2f} mm")
