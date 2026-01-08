import os
import json
import requests
import re
import time

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

# GPT rate limit защита
LAST_CALL_TS = 0
MIN_INTERVAL = 30  # секунд между вызовами

# Кэш анализов (по заголовку)
CACHE = {}


def safe_json_extract(text: str):
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group())
    return None


def analyze_news(item):
    global LAST_CALL_TS

    title = item.get("title")
    if not title:
        return None

    # 1️⃣ Кэш
    if title in CACHE:
        return CACHE[title]

    # 2️⃣ Cooldown
    now = time.time()
    if now - LAST_CALL_TS < MIN_INTERVAL:
        return None

    LAST_CALL_TS = now

    if not OPENAI_KEY:
        print("❌ OPENAI_API_KEY not found")
        return None

    prompt = (
        "You are a professional crypto market analyst.\n"
        "Analyze the news below.\n\n"
        f"Title: {title}\n"
        f"Summary: {item.get('summary', '')}\n\n"
        "Respond ONLY in valid JSON.\n"
        "{"
        '"score":0-100,'
        '"sentiment":"bullish|bearish|neutral",'
        '"impact":"low|medium|high",'
        '"reason":"short explanation"'
        "}"
    )

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)

        if r.status_code == 429:
            print("⏳ GPT rate limit hit, waiting...")
            return None

        if r.status_code != 200:
            print("❌ GPT HTTP:", r.status_code, r.text)
            return None

        data = r.json()
        content = data["choices"][0]["message"]["content"]
        parsed = safe_json_extract(content)

        if parsed:
            CACHE[title] = parsed

        return parsed

    except Exception as e:
        print("❌ GPT exception:", e)
        return None