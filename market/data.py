import requests

BASE_URL = "https://www.okx.com"

TF_MAP = {
    "1m": "1m",
    "3m": "3m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1H"
}

def candles(symbol, tf):
    try:
        url = f"{BASE_URL}/api/v5/market/candles"
        params = {
            "instId": symbol,
            "bar": TF_MAP.get(tf, "5m"),
            "limit": "100"
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if "data" not in data or not data["data"]:
            return None

        raw = data["data"]

        # OKX возвращает от новых к старым → разворачиваем
        raw.reverse()

        candles = []
        for c in raw:
            candles.append([
                int(c[0]),        # timestamp
                float(c[1]),      # open
                float(c[2]),      # high
                float(c[3]),      # low
                float(c[4]),      # close
                float(c[5])       # volume
            ])

        return candles

    except Exception as e:
        print("❌ candles error:", e)
        return None
