import time
import threading
from datetime import datetime, UTC

from market.data import candles
from market.indicators import indicators
from core.strategy import signal

from notify.telegram import send, main_menu
from notify.polling import poll

from utils.state import STATE
from utils.formatter import format_market_update
from config.settings import TIMEFRAME, LOOP_SLEEP

from news.engine import news_loop


# =========================
# TELEGRAM LOOP (МЕНЮ)
# =========================
def telegram_loop():
    print("🤖 Telegram loop started")
    while True:
        try:
            poll()
        except Exception as e:
            print("❌ Telegram error:", e)
        time.sleep(1)


# =========================
# MARKET LOOP (ЦЕНЫ)
# =========================
def market_loop():
    send("🤖 Бот запущен (Termux, OKX)", main_menu())

    last_send = 0  # время последней отправки market update

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

                last = c[-1][4]
                prev = c[-4][4]  # ~15 минут назад

                if not prev or prev <= 0:
                    print(f"⚠️ {symbol}: некорректная цена")
                    continue

                change = ((last - prev) / prev) * 100

                print(f"✔ {symbol}: price={last:.4f} change={change:+.2f}%")

                rows.append({
                    "symbol": symbol,
                    "price": last,
                    "change": change
                })

                # 🔔 сигналы (ПОКА только уведомление)
                if STATE["bot_active"]:
                    data = indicators(c)
                    sig = signal(data)
                    if sig:
                        send(f"📈 <b>{sig}</b> {symbol}")

            except Exception as e:
                print(f"❌ Market error {symbol}:", e)

        # 🔔 ОДНО общее сообщение раз в 15 минут
        if rows and now - last_send >= 900:
            msg = format_market_update(rows)
            send(msg)
            last_send = now
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
