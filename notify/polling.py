import requests
import os
import time

from notify.handler import process_callback
from notify.telegram import send, main_menu
from utils.users import is_admin

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

OFFSET = 0


def poll():
    global OFFSET

    try:
        r = requests.get(
            f"{API}/getUpdates",
            params={"timeout": 30, "offset": OFFSET},
            timeout=35
        )
        data = r.json()

        if not data.get("ok"):
            return

        for upd in data["result"]:
            OFFSET = upd["update_id"] + 1

            # 🖱 CALLBACK (нажатие кнопки)
            if "callback_query" in upd:
                cb = upd["callback_query"]
                chat_id = cb["message"]["chat"]["id"]
                data_cb = cb["data"]

                process_callback(data_cb, chat_id)

            # 💬 Обычное сообщение
            elif "message" in upd:
                msg = upd["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")

                if text == "/start":
                    send(
                        "Главное меню",
                        keyboard=main_menu(is_admin(chat_id)),
                        chat_id=chat_id
                    )

    except Exception as e:
        raise e