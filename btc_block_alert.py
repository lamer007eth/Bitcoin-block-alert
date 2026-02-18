import time
import requests
import datetime
import os
from playsound import playsound

TARGET_BLOCK = 904612            # Задай нужный блок
CHECK_INTERVAL = 5               # Интервал проверки в секундах
SOUND_FILE = "alert.mp3"         # Файл со звуком (в той же папке)

last_block = None
last_time = None
last_gas = None

def get_latest_block():
    try:
        response = requests.get("https://mempool.space/api/blocks", timeout=3)
        response.raise_for_status()
        blocks = response.json()
        return blocks[0]['height']
    except Exception as e:
        print(f"❌ Ошибка при получении блока: {e}")
        return None

def get_gas():
    global last_gas
    try:
        gas_resp = requests.get("https://mempool.space/api/v1/fees/recommended", timeout=3)
        gas_resp.raise_for_status()
        gas_data = gas_resp.json()
        gas = gas_data.get("fastestFee")
        if gas is not None:
            last_gas = gas
    except Exception as e:
        print(f"❌ Ошибка при получении газа: {e}")
    return last_gas

def notify():
    print("\n" + "⚡️" * 18)
    print(f"🚨 НАЙДЕН БЛОК {TARGET_BLOCK} В {datetime.datetime.now().strftime('%H:%M:%S')} 🚨")
    print("⚡️" * 18 + "\n")
    try:
        playsound(SOUND_FILE)
    except Exception as e:
        print(f"❌ Не удалось воспроизвести звук: {e}")

print(f"🟡 Ожидаем блок {TARGET_BLOCK}...\n")

while True:
    now = datetime.datetime.now()
    block = get_latest_block()

    if block is None:
        time.sleep(CHECK_INTERVAL)
        continue

    if block != last_block:
        time_diff = (now - last_time).total_seconds() if last_time else None
        last_time = now
        last_block = block
        gas = get_gas()
        
        print(f"[{now.strftime('%H:%M:%S')}] Новый блок: {block}")
        if time_diff:
            print(f"Время между блоками: {int(time_diff)} сек")
        print(f"Газ (fastest): {gas} sats/vB")
        print("─" * 30)

        if block >= TARGET_BLOCK:
            notify()
            break

    time.sleep(CHECK_INTERVAL)
