"""
News Engine

Отвечает за:
- сбор новостей (RSS)
- GPT-анализ значимости
- подтверждение рынком (market confirmation)
- отправку сигналов в Telegram

ТОЛЬКО аналитика, БЕЗ торговли.
"""

import time

from news.rss import collect_rss
from news.gpt import analyze_news
from market.confirmation import confirm_market
from notify.telegram import send_to_all


# Запоминаем уже обработанные новости (по заголовку)
SEEN_TITLES = set()

# Минимальный GPT score для анализа
MIN_GPT_SCORE = 70


def news_loop():
    print("📰 News engine started")

    while True:
        try:
            # 1️⃣ Собираем новости
            news_items = collect_rss()

            for item in news_items:
                title = item.get("title")
                if not title:
                    continue

                # антидубль
                if title in SEEN_TITLES:
                    continue

                # помечаем как просмотренную
                SEEN_TITLES.add(title)

                # 2️⃣ GPT-анализ
                analysis = analyze_news(item)
                if not analysis:
                    continue

                score = analysis.get("score", 0)
                sentiment = analysis.get("sentiment", "neutral")
                impact = analysis.get("impact", "low")

                # фильтр по силе
                if score < MIN_GPT_SCORE:
                    continue

                # 3️⃣ Проверка рынка (только BTC / ETH)
                for sym in item.get("currencies", []):
                    if sym not in ("BTC", "ETH"):
                        continue

                    confirmation = confirm_market(sym, sentiment)
                    if not confirmation:
                        continue

                    # 4️⃣ Отправка подтверждённого сигнала
                    msg = (
                        f"✅ <b>NEWS CONFIRMED</b>\n\n"
                        f"🪙 {confirmation['pair']}\n"
                        f"📰 {title}\n\n"
                        f"📊 GPT Score: {score}\n"
                        f"📈 Price change (5m): {confirmation['price_change_5m']}%\n"
                        f"📊 Volume spike: x{confirmation['volume_ratio']}\n"
                        f"🧠 Sentiment: {sentiment}\n\n"
                        f"⚠️ Ready for entry\n\n"
                        f"🔗 {item.get('url', '')}"
                    )

                    send_to_all(msg)

        except Exception as e:
            print("❌ News engine error:", e)

        # Проверяем новости каждые 5 минут
        time.sleep(300)