import feedparser

FEEDS = {
    "Cointelegraph": "https://cointelegraph.com/rss",
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "BitcoinMagazine": "https://bitcoinmagazine.com/.rss/full/",
    "TheBlock": "https://www.theblock.co/rss",
    "Decrypt": "https://decrypt.co/feed"
}

TRACKED = ["BTC", "ETH", "SOL", "ETF", "FED", "SEC", "BINANCE"]


def collect_rss():
    items = []

    for source, url in FEEDS.items():
        feed = feedparser.parse(url)

        for e in feed.entries[:15]:
            title = e.get("title", "")
            text = (title + " " + e.get("summary", "")).upper()

            coins = [c for c in TRACKED if c in text]
            if not coins:
                continue

            items.append({
                "title": title,
                "summary": e.get("summary", ""),
                "url": e.get("link", ""),
                "source": source,
                "currencies": coins
            })

    return items