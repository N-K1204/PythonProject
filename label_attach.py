# label_attach.py

import os
import pandas as pd
from datetime import datetime, timedelta

def get_image_timestamp(filename):
    base = os.path.splitext(filename)[0]
    return datetime.strptime(base, '%Y%m%d%H%M')

def label_images(image_folder, weather_csv, mode='A', save_dir=None):
    try:
        df_weather = pd.read_csv(weather_csv, encoding='cp932')
    except Exception as e:
        print(f"[×] CSV読込エラー: {weather_csv} -> {e}")
        return

    date_str = os.path.basename(weather_csv)[:8]
    try:
        df_weather['timestamp'] = pd.to_datetime(
            df_weather['時分'].apply(lambda t: date_str + ' ' + t),
            format='%Y%m%d %H:%M'
        )
    except Exception as e:
        print(f"[×] '時分'列の変換失敗: {weather_csv} -> {e}")
        return

    try:
        image_files = sorted([
            f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png'))
        ])
        df_images = pd.DataFrame({
            'filename': image_files,
            'img_time': [get_image_timestamp(f) for f in image_files]
        })
    except Exception as e:
        print(f"[×] 画像フォルダ読込失敗: {image_folder} -> {e}")
        return

    labeled = []
    for _, w in df_weather.iterrows():
        wt = w['timestamp']
        if mode == 'A':
            start, end = wt, wt + timedelta(minutes=9)
        elif mode == 'B':
            start, end = wt - timedelta(minutes=5), wt + timedelta(minutes=4)
        else:
            raise ValueError("mode must be 'A' or 'B'")

        subset = df_images[(df_images['img_time'] >= start) & (df_images['img_time'] <= end)]

        for _, img in subset.iterrows():
            labeled.append({
                'filename': img['filename'],
                'img_time': img['img_time'].strftime('%Y-%m-%d %H:%M'),
                'label_time': wt.strftime('%Y-%m-%d %H:%M'),
                'temperature': w.get('気温 (℃)', None),
                'humidity': w.get('相対湿度 (%)', None),
                'pressure': None  # 気圧があれば追加可能
            })

    if not labeled:
        print(f"[△] {date_str} - mode {mode}：ラベル付け対象なし")
        return

    os.makedirs(save_dir, exist_ok=True)
    output_path = os.path.join(save_dir, f"{mode}_model_{date_str}.csv")
    pd.DataFrame(labeled).to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"[✔] {date_str} - mode {mode}: {len(labeled)}件 → {output_path}")


if __name__ == '__main__':
    # パス設定
    img_root = r'\\150.89.226.195\Private\6期生\小畑\img_data'
    weather_root = r'\\150.89.226.195\Private\7期生\西山\weather_data'
    output_root = r'\\150.89.226.195\Private\7期生\西山\Attached_WeatherData'

    os.makedirs(output_root, exist_ok=True)

    for folder_name in sorted(os.listdir(img_root)):
        if not folder_name.isdigit() or len(folder_name) != 8:
            continue

        image_folder = os.path.join(img_root, folder_name)
        weather_csv = os.path.join(weather_root, f"{folder_name}.csv")

        if not os.path.exists(image_folder):
            print(f"[×] 画像フォルダなし: {image_folder}")
            continue
        if not os.path.exists(weather_csv):
            print(f"[×] 天気CSVなし: {weather_csv}")
            continue

        # Aモードの出力CSVが存在するか？
        a_output_csv = os.path.join(output_root, f"A_model_{folder_name}.csv")
        if os.path.exists(a_output_csv):
            print(f"[→] {folder_name} - mode A: 既に存在、スキップ")
        else:
            label_images(image_folder, weather_csv, mode='A', save_dir=output_root)

        # Bモードの出力CSVが存在するか？
        b_output_csv = os.path.join(output_root, f"B_model_{folder_name}.csv")
        if os.path.exists(b_output_csv):
            print(f"[→] {folder_name} - mode B: 既に存在、スキップ")
        else:
            label_images(image_folder, weather_csv, mode='B', save_dir=output_root)
