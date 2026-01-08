from notify.telegram import (
    send,
    send_to_all,
    main_menu,
    symbols_menu,
    status_text
)
from utils.state import STATE
from utils.users import is_admin


def process_callback(data, chat_id):
    # 🔙 Назад
    if data == "back":
        send("Главное меню", main_menu(is_admin(chat_id)), chat_id=chat_id)
        return

    # 📊 Статус
    if data == "status":
        send(status_text(), chat_id=chat_id)
        return

    # ⛔️ Ограничения для НЕ админа
    if not is_admin(chat_id):
        send("⛔ У вас нет прав для этого действия", chat_id=chat_id)
        return

    # ▶️ Торговля
    if data == "trade_menu":
        STATE["bot_active"] = not STATE["bot_active"]
        send_to_all(f"▶️ Торговля {'ВКЛ' if STATE['bot_active'] else 'ВЫКЛ'}")
        return

    # 💱 Валюты
    if data == "symbols_menu":
        send("Выбор валют", symbols_menu(), chat_id=chat_id)
        return

    # 🔄 Переключение пары
    if data.startswith("toggle_symbol:"):
        symbol = data.split(":")[1]
        STATE["symbols"][symbol] = not STATE["symbols"].get(symbol, False)
        send("Обновлено", symbols_menu(), chat_id=chat_id)
        return