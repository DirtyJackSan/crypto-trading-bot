def recommended(atr):
    if atr < 0.3: return 30
    if atr < 0.6: return 20
    if atr < 1: return 12
    return 5
