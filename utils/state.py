STATE = {
    # включена ли торговля
    "bot_active": False,

    # режим риска
    "mode": "NORMAL",  # NORMAL / HIGH_RISK

    # торговые инструменты
    "symbols": {
        "XAUUSD": True,
        "EURUSD": True,
    },

    # риск-менеджмент
    "risk": {
        "risk_per_trade": 0.5,   # % от депозита
        "max_trades_day": 6,
        "daily_loss_limit": 2.0  # % в день
    },

    # параметры ордера
    "order": {
        "lot_mode": "AUTO",      # AUTO / MANUAL
        "manual_lot": 0.01,
        "rr": 2.0
    }
}