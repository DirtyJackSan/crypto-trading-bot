import requests
import os
import time

from notify.handler import process_callback

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

offset = 0


def poll():
    global offset

    r = requests.get(
        f"{API}/getUpdates",
        params={"timeout": 10, "offset": offset},
        timeout=15
    )

    data = r.json()
    if not data.get("ok"):
        return

    for update in data["result"]:
        offset = update["update_id"] + 1

        # CALLBACK (inline кнопки)
        if "callback_query" in update:
            cb = update["callback_query"]
            process_callback(cb)