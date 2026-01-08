import requests
import os
from notify.handler import process_callback

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

offset = 0

def poll():
    global offset
    r = requests.get(f"{API}/getUpdates", params={"offset": offset, "timeout": 30})
    data = r.json()

    for update in data.get("result", []):
        offset = update["update_id"] + 1

        if "callback_query" in update:
            process_callback(update["callback_query"])
