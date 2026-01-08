from notify.telegram import send


def send_news(item):
    emoji = {
        "bullish": "🟢",
        "bearish": "🔴",
        "neutral": "⚪"
    }.get(item["sentiment"], "⚪")

    text = (
        f"📰 <b>NEWS ALERT</b>\n"
        f"━━━━━━━━━━━━\n"
        f"{emoji} <b>{item['sentiment'].upper()}</b>\n\n"
        f"💱 Монеты: {', '.join(item['coins'])}\n"
        f"📌 {item['title']}\n\n"
        f"🔗 <a href='{item['url']}'>Источник</a>"
    )

    send(text)
