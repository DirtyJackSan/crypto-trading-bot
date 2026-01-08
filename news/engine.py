import time
from news.collector import collect
from news.filter import classify
from news.storage import is_new
from news.notifier import send_news


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
