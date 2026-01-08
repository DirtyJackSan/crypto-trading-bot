KEYWORDS = {
    "bullish": [
        "approve", "approval", "launch", "partnership", "adoption",
        "etf", "listing", "integration", "investment", "buy"
    ],
    "bearish": [
        "hack", "exploit", "lawsuit", "ban", "delay",
        "delisting", "sell", "dump", "crash", "liquidation"
    ]
}

TRACKED_COINS = ["BTC", "ETH", "SOL"]


def classify(news):
    text = news["title"].lower()

    score = 0
    sentiment = "neutral"

    for w in KEYWORDS["bullish"]:
        if w in text:
            score += 1

    for w in KEYWORDS["bearish"]:
        if w in text:
            score -= 1

    if score > 0:
        sentiment = "bullish"
    elif score < 0:
        sentiment = "bearish"

    coins = [c for c in news["currencies"] if c in TRACKED_COINS]

    if not coins:
        return None

    return {
        "title": news["title"],
        "url": news["url"],
        "source": news["source"],
        "coins": coins,
        "sentiment": sentiment
    }
