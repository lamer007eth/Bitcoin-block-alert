import time
import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

TARGET_BLOCK = int(os.getenv("TARGET_BLOCK", 0))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 5))

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FORWARD_CHANNEL_ID = os.getenv("FORWARD_CHANNEL_ID")

last_block = None
last_time = None
last_fee = None


def send_telegram_message(text, chat_id):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"❌ Telegram error: {e}")


def get_latest_block():
    try:
        r = requests.get("https://mempool.space/api/blocks", timeout=5)
        r.raise_for_status()
        return r.json()[0]["height"]
    except Exception as e:
        print(f"❌ Block fetch error: {e}")
        return None


def get_fee():
    global last_fee
    try:
        r = requests.get(
            "https://mempool.space/api/v1/fees/recommended",
            timeout=5
        )
        r.raise_for_status()
        data = r.json()
        fee = data.get("fastestFee")
        if fee:
            last_fee = fee
    except Exception as e:
        print(f"❌ Fee fetch error: {e}")
    return last_fee


def notify():
    now = datetime.datetime.now().strftime("%H:%M:%S")

    msg = (
        f"⚡️⚡️⚡️\n"
        f"🚨 TARGET BLOCK <b>{TARGET_BLOCK}</b> MINED 🚨\n"
        f"🕒 Time: {now}\n"
        f"⚡️⚡️⚡️"
    )

    print(msg)

    send_telegram_message(msg, CHAT_ID)
    send_telegram_message(msg, FORWARD_CHANNEL_ID)


print(f"🟡 Waiting for block {TARGET_BLOCK}...\n")

send_telegram_message(
    f"🟡 Monitoring block <b>{TARGET_BLOCK}</b>...",
    CHAT_ID
)

while True:
    now = datetime.datetime.now()
    block = get_latest_block()

    if block is None:
        time.sleep(CHECK_INTERVAL)
        continue

    if block != last_block:
        time_diff = (
            (now - last_time).total_seconds()
            if last_time else None
        )

        last_time = now
        last_block = block
        fee = get_fee()

        log = (
            f"📦 Block: {block}\n"
            f"⛽ Fee: {fee} sats/vB"
        )

        if time_diff:
            log += f"\n⏱ Interval: {int(time_diff)} sec"

        print(log)
        send_telegram_message(log, CHAT_ID)

        if block >= TARGET_BLOCK:
            notify()
            break

    time.sleep(CHECK_INTERVAL)

print("✅ Target block reached. Bot stopped.")