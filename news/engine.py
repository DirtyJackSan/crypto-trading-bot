import time
from news.collector import collect
from news.filter import classify
from news.storage import is_new
from news.notifier import send_news
from market.confirmation import confirm_market

for sym in item["currencies"]:
    if sym not in ("BTC", "ETH"):
        continue

    confirm = confirm_market(sym, analysis["sentiment"])
    if not confirm:
        continue

    msg = (
        f"✅ <b>NEWS CONFIRMED</b>\n\n"
        f"🪙 {confirm['pair']}\n"
        f"📰 {item['title']}\n\n"
        f"📊 GPT Score: {analysis['score']}\n"
        f"📈 Price change (5m): {confirm['change']}%\n"
        f"📊 Volume spike: x{confirm['volume_ratio']}\n\n"
        f"⚠️ Ready for entry"
    )

    send_to_all(msg)


def news_loop():
    print("📰 News engine started")

    while True:
        try:
            news = collect()

            for n in news:
                item = classify(n)
                if not item:
                    continue

                uid = item["title"]
                if not is_new(uid):
                    continue

                send_news(item)

        except Exception as e:
            print("❌ News engine error:", e)

        time.sleep(180)  # каждые 3 минуты
