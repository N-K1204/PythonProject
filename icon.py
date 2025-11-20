from PIL import Image
import os

# 元画像のパス（JPGでもOK）
input_image = "icon.jpg"  # ここをJPGに変更

# 保存先フォルダ
output_folder = "statics/icons"
os.makedirs(output_folder, exist_ok=True)

# 画像を開く
img = Image.open(input_image)

# 192x192 のアイコン
img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
img_192.save(os.path.join(output_folder, "icon-192.png"))

# 512x512 のアイコン
img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
img_512.save(os.path.join(output_folder, "icon-512.png"))

print("PWA用アイコン生成完了！")
