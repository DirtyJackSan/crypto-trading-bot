def signal(data):
    if not data:
        return None

    if data["ema_fast"] > data["ema_slow"] and data["trend"] == "UP":
        return "LONG"

    if data["ema_fast"] < data["ema_slow"] and data["trend"] == "DOWN":
        return "SHORT"

    return None
