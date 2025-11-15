# evaluate_final_predictor.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model

# 1. データ読み込み
df = pd.read_csv("features_dataset.csv")

# 特徴量とラベルを分ける
X = df.drop(columns=["label", "rain_mm"]).values
y_class = df["label"].values
y_reg = df["rain_mm"].values

# 訓練・テスト分割（ランダムシードは同じに）
X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
    X, y_class, y_reg, test_size=0.2, random_state=42
)

# 2. モデル読み込み
model = load_model("final_predictor_model.h5")

# 3. 予測
y_pred_class, y_pred_reg = model.predict(X_test)

# 4. 分類評価
print("=== 分類評価 ===")
y_pred_class_label = (y_pred_class > 0.5).astype(int)
print(classification_report(y_class_test, y_pred_class_label))

# 混同行列の表示
cm = confusion_matrix(y_class_test, y_pred_class_label)
plt.figure(figsize=(4, 3))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("混同行列 (分類)")
plt.xlabel("予測")
plt.ylabel("実際")
plt.tight_layout()
plt.show()

# 5. 回帰評価
print("=== 回帰評価 ===")
mae = mean_absolute_error(y_reg_test, y_pred_reg)
mse = mean_squared_error(y_reg_test, y_pred_reg)
print(f"MAE（平均絶対誤差）: {mae:.3f}")
print(f"MSE（平均二乗誤差）: {mse:.3f}")

# 散布図（実際 vs 予測）
plt.figure(figsize=(5, 5))
plt.scatter(y_reg_test, y_pred_reg, alpha=0.5)
plt.plot([0, max(y_reg_test)], [0, max(y_reg_test)], 'r--')
plt.xlabel("実際の降水量 (mm)")
plt.ylabel("予測された降水量 (mm)")
plt.title("実際 vs 予測（回帰）")
plt.grid(True)
plt.tight_layout()
plt.show()
