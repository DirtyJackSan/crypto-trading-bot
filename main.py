import time
import threading
from datetime import datetime, UTC

from market.data import candles
from market.indicators import indicators
from core.strategy import signal

from notify.telegram import (
    send,
    send_to_all,
    main_menu
)
from notify.polling import poll

from utils.state import STATE
from utils.users import all_users, is_admin
from utils.formatter import format_market_update
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
# MARKET LOOP (ЦЕНЫ + СИГНАЛЫ)
# =========================
def market_loop():
    # 🔔 Приветствие всем пользователям с их меню
    for uid in all_users():
        send(
            "🤖 Бот запущен и работает",
            keyboard=main_menu(is_admin(uid)),
            chat_id=uid
        )

    last_market_send = 0

    while True:
        now = time.time()
        print(f"[{datetime.now(UTC)}] 📊 Market tick")

        rows = []

        for symbol, enabled in STATE["symbols"].items():
            if not enabled:
                continue

            try:
                c = candles(symbol, TIMEFRAME)

                if not c or len(c) < 4:
                    print(f"⚠️ {symbol}: недостаточно свечей")
                    continue

                last_price = c[-1][4]
                prev_price = c[-4][4]  # ~15 минут назад

                if not prev_price or prev_price <= 0:
                    continue

                change = ((last_price - prev_price) / prev_price) * 100

                print(
                    f"✔ {symbol}: price={last_price:.4f} "
                    f"change={change:+.2f}%"
                )

                rows.append({
                    "symbol": symbol,
                    "price": last_price,
                    "change": change
                })

                # 📈 Сигналы (пока только уведомление)
                if STATE["bot_active"]:
                    data = indicators(c)
                    sig = signal(data)
                    if sig:
                        send_to_all(
                            f"📈 <b>{sig}</b> {symbol}"
                        )

            except Exception as e:
                print(f"❌ Market error {symbol}:", e)

        # 📤 Общее обновление рынка раз в 15 минут
        if rows and now - last_market_send >= 900:
            msg = format_market_update(rows)
            send_to_all(msg)
            last_market_send = now
            print("📤 Market update отправлен в Telegram")

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

    # держим главный поток живым
    while True:
        time.sleep(10)