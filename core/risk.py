from config.settings import DEPOSIT, DAILY_STOP_PERCENT
daily_loss = 0
def can_trade():
    return daily_loss < DEPOSIT * DAILY_STOP_PERCENT / 100
