from market.data import candles


CONFIRM_SYMBOLS = {
    "BTC": "BTC-USDT",
    "ETH": "ETH-USDT"
}

PRICE_THRESHOLD = {
    "BTC": 0.2,   # %
    "ETH": 0.3
}

VOLUME_MULTIPLIER = 1.5


def confirm_market(symbol: str, sentiment: str):
    """
    Проверяет реакцию рынка на новость за 3–5 минут
    """
    try:
        pair = CONFIRM_SYMBOLS.get(symbol)
        if not pair:
            return None

        c = candles(pair, "1m")
        if not c or len(c) < 6:
            return None

        # последние 5 минут
        last = c[-1]
        prev = c[-6]

        price_now = last[4]
        price_then = prev[4]

        if price_then <= 0:
            return None

        change = ((price_now - price_then) / price_then) * 100

        # направление
        if sentiment == "bullish" and change <= 0:
            return None
        if sentiment == "bearish" and change >= 0:
            return None

        # порог
        if abs(change) < PRICE_THRESHOLD[symbol]:
            return None

        # объём
        volumes = [x[5] for x in c[-10:-1]]
        avg_volume = sum(volumes) / len(volumes)
        last_volume = last[5]

        if last_volume < avg_volume * VOLUME_MULTIPLIER:
            return None

        return {
            "pair": pair,
            "change": round(change, 3),
            "volume_ratio": round(last_volume / avg_volume, 2)
        }

    except Exception as e:
        print("❌ Confirmation error:", e)
        return None