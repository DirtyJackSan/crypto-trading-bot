def indicators(candles):
    if candles is None:
        return None

    closes = [c[4] for c in candles if c and len(c) > 4]
    if len(closes) < 25:
        return None

    ema_fast = sum(closes[-9:]) / 9
    ema_slow = sum(closes[-21:]) / 21

    trend = "UP" if closes[-1] > closes[-5] else "DOWN"

    return {
        "ema_fast": ema_fast,
        "ema_slow": ema_slow,
        "trend": trend,
        "close": closes[-1]
    }
