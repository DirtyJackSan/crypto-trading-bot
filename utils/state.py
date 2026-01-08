import time

START_TIME = time.time()

STATE = {
    "bot_active": True,
    "mode": "SPOT",              # SPOT / FUTURES
    "symbols": {
        "BTC-USDT": True,
        "ETH-USDT": True,
        "SOL-USDT": True
    },
    "leverage": 15,
    "strategy": "AGGRESSIVE",
    "news_enabled": False,
    "twitter_enabled": False
}
