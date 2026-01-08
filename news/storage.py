import time

SEEN = {}
TTL = 60 * 60  # 1 час


def is_new(uid):
    now = time.time()

    if uid in SEEN and now - SEEN[uid] < TTL:
        return False

    SEEN[uid] = now

    # чистка старых
    for k in list(SEEN.keys()):
        if now - SEEN[k] > TTL:
            del SEEN[k]

    return True
