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
    STATE = {
    "bot_active": False,

    "mode": "NORMAL",  # NORMAL / HIGH_RISK

    "symbols": {
        "XAUUSD": True,
        "EURUSD": True,
    },

    "risk": {
        "leverage": 100,
        "risk_per_trade": 0.5,   # %
        "max_trades_day": 6,
        "daily_loss_limit": 2.0  # %
    },

    "order": {
        "lot_mode": "AUTO",      # AUTO / MANUAL
        "manual_lot": 0.01,
        "rr": 2.0
    }
}
