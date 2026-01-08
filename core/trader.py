import requests
import os

BASE_URL = "https://www.okx.com"

def place_order(symbol, side, amount):
    # ПОКА ЗАГЛУШКА (без реальных ордеров)
    # Здесь позже будет реальный POST запрос
    print(f"💰 ORDER MOCK: {side} {symbol} amount={amount}")
    return True
