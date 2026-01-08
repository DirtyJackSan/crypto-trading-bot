import time
import threading
from datetime import datetime, UTC

from market.data import candles
from market.indicators import indicators
from core.strategy import signal

from notify.telegram import (
    send,
    send_to_all,
    main_menu,
    edit
)
from notify.polling import poll

from utils.state import STATE
from utils.users import all_users, is_admin
from utils.dashboard import DASHBOARD
from config.settings import TIMEFRAME, LOOP_SLEEP

from news.engine import news_loop


# =========================
# TELEGRAM LOOP (INLINE МЕНЮ)
# =========================
def telegram_loop():
    print("🤖 Telegram loop started")
    while True:
        try:
            poll()
        except Exception as e:
            print("❌ Telegram polling error:", e)
        time.sleep(1)


# =========================
# FORMAT DASHBOARD
# =========================
def format_dashboard(rows):
    lines = ["📊 <b>Market Dashboard</b>\n"]

    for r in rows:
        change = r["change"]
        arrow = "🟢" if change > 0 else "🔴" if change < 0 else "⚪️"

        lines.append(
            f"{arrow} <b>{r['symbol']}</b>: "
            f"{r['price']:.4f} ({change:+.2f}%)"
        )

    ts = datetime.now(UTC).strftime("%H:%M:%S UTC")
    lines.append(f"\n⏱ Updated: {ts}")

    return "\n".join(lines)


# =========================
# MARKET LOOP (DASHBOARD + SIGNALS)
# =========================
def market_loop():
    # 🔔 Приветствие всем пользователям
    for uid in all_users():
        send(
            "🤖 Бот запущен и работает",
            keyboard=main_menu(is_admin(uid)),
            chat_id=uid
        )

    while True:
        print(f"[{datetime.now(UTC)}] 📊 Market tick")

        rows = []

        for symbol, enabled in STATE["symbols"].items():
            if not enabled:
                continue

            try:
                c = candles(symbol, TIMEFRAME)

                if not c or len(c) < 4:
                    continue

                last_price = c[-1][4]
                prev_price = c[-4][4]  # ~15 минут

                if not prev_price or prev_price <= 0:
                    continue

                change = ((last_price - prev_price) / prev_price) * 100

                rows.append({
                    "symbol": symbol,
                    "price": last_price,
                    "change": change
                })

                # 📈 СИГНАЛЫ (ТОЛЬКО УВЕДОМЛЕНИЯ)
                if STATE["bot_active"]:
                    data = indicators(c)
                    sig = signal(data)
                    if sig:
                        send_to_all(
                            f"📈 <b>{sig}</b> {symbol}"
                        )

            except Exception as e:
                print(f"❌ Market error {symbol}:", e)

        # 📊 DASHBOARD (ОДНО СООБЩЕНИЕ)
        if rows:
            text = format_dashboard(rows)

            admin_id = next(iter(all_users()))

            if DASHBOARD["message_id"] is None:
                msg = send(
                    text,
                    chat_id=admin_id,
                    keyboard=main_menu(is_admin(admin_id)),
                    return_message_id=True
                )
                DASHBOARD["message_id"] = msg["message_id"]
            else:
                edit(
                    text,
                    message_id=DASHBOARD["message_id"],
                    chat_id=admin_id
                )

        time.sleep(LOOP_SLEEP)


# =========================
# START ALL THREADS
# =========================
if __name__ == "__main__":
    t1 = threading.Thread(target=telegram_loop, daemon=True)
    t2 = threading.Thread(target=market_loop, daemon=True)
    t3 = threading.Thread(target=news_loop, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    print("🚀 Все потоки запущены")

    while True:
        time.sleep(10)