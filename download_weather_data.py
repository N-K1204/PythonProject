# download_weather_data.py

import requests
from bs4 import BeautifulSoup
import os
import csv
from datetime import datetime, timedelta

# === 開始日 ===
start_date = datetime(2025, 7, 15)
today = datetime.now()
yesterday = today - timedelta(days=1)

# === 保存先フォルダ ===
save_dir = r"\\150.89.226.195\Private\7期生\西山\weather_data"
os.makedirs(save_dir, exist_ok=True)

# === 枚方の気象庁コード ===
pref_no = "62"
block_no = "1065"

# === 処理開始 ===
current_date = start_date
while current_date <= yesterday:
    target_date_str = current_date.strftime("%Y%m%d")
    year, month, day = current_date.strftime("%Y"), current_date.strftime("%m"), current_date.strftime("%d")
    url = f"https://www.data.jma.go.jp/stats/etrn/view/10min_a1.php?prec_no={pref_no}&block_no={block_no}&year={year}&month={month}&day={day}&view="

    csv_path = os.path.join(save_dir, f"{target_date_str}.csv")
    if os.path.exists(csv_path):
        current_date += timedelta(days=1)
        continue

    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="data2_s")

        if table:
            rows = table.find_all("tr")
            with open(csv_path, "w", newline="", encoding="cp932", errors="replace") as f:
                writer = csv.writer(f)
                writer.writerow(["時分", "降水量 (mm)", "気温 (℃)", "相対湿度 (%)", "平均風速 (m/s)", "平均風向"])
                
                for row in rows[2:]:  # ヘッダーの次から
                    cells = row.find_all("td")
                    if len(cells) < 6:
                        continue

                    time_str = cells[0].get_text(strip=True)
                    try:
                        hour = int(time_str.split(":")[0])
                        if hour < 6 or hour > 21:
                            continue  # 6:00〜21:59 のみ
                    except:
                        continue
                    
                    data = [cell.get_text(strip=True) for cell in cells[:6]]
                    writer.writerow(data)

            print(f"✅ {target_date_str}.csv を保存しました。")
        else:
            print(f"❌ {target_date_str} のデータが見つかりませんでした。")

    except Exception as e:
        print(f"⚠️ {target_date_str} エラー: {e}")

    current_date += timedelta(days=1)
