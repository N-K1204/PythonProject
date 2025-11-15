# train_model_convLSTM.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# === データ読み込み ===
df = pd.read_csv("features_dataset.csv", encoding="utf-8-sig")

# 欠損値除去
df = df.dropna(subset=["temperature", "humidity", "precipitation", "label"])

# === 特徴量とラベル ===
X = df.iloc[:, :2050].values.astype(np.float32)  # 2048 + 2 の特徴量
y_class = df["label"].values.astype(np.float32)  # 分類用
y_reg = df["precipitation"].values.astype(np.float32)  # 回帰用

# === 特徴量を時系列として扱う（ダミーでT=1）===
# ConvLSTMの入力: (samples, timesteps, height, width, channels)
# ここでは画像1枚（flatten済み）を (1, 32, 64, 1) のように reshape
# 例：2050 = 32×64 に reshape（要調整）

T, H, W, C = 1, 32, 64, 1
X_seq = X.reshape((-1, T, H, W, C))

# === 気象データだけ抽出（気温＋湿度）===
weather_feat = X[:, -2:]  # 最後の2列

# === データ分割 ===
X_img_train, X_img_val, weather_train, weather_val, y_class_train, y_class_val, y_reg_train, y_reg_val = train_test_split(
    X_seq, weather_feat, y_class, y_reg, test_size=0.2, random_state=42
)

# === モデル定義 ===

# 画像部分
img_input = Input(shape=(T, H, W, C), name="img_input")
x = layers.ConvLSTM2D(filters=32, kernel_size=(3,3), padding="same", return_sequences=False, activation='relu')(img_input)
x = layers.GlobalAveragePooling2D()(x)

# 気象情報（別入力）
weather_input = Input(shape=(2,), name="weather_input")

# 結合
combined = layers.concatenate([x, weather_input])
dense = layers.Dense(64, activation='relu')(combined)
dense = layers.Dense(32, activation='relu')(dense)

# 出力（分類 + 回帰）
output_class = layers.Dense(1, activation='sigmoid', name="class_output")(dense)
output_reg = layers.Dense(1, activation='linear', name="reg_output")(dense)

model = models.Model(inputs=[img_input, weather_input], outputs=[output_class, output_reg])
model.compile(
    optimizer=Adam(1e-4),
    loss={'class_output': 'binary_crossentropy', 'reg_output': 'mse'},
    metrics={'class_output': 'accuracy', 'reg_output': 'mae'}
)

model.summary()

# === 学習 ===
callbacks = [EarlyStopping(patience=5, restore_best_weights=True)]

history = model.fit(
    [X_img_train, weather_train],
    {'class_output': y_class_train, 'reg_output': y_reg_train},
    validation_data=([X_img_val, weather_val], {'class_output': y_class_val, 'reg_output': y_reg_val}),
    epochs=50,
    batch_size=32,
    callbacks=callbacks
)

# === モデル保存 ===
model.save("final_predictor_convLSTM.h5")
print("✅ モデルを保存しました → final_predictor_convLSTM.h5")
