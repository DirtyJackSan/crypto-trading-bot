import os
import json
import requests
import re

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"


def safe_json_extract(text: str):
    """
    Извлекает JSON даже если GPT добавил лишний текст
    """
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group())
    return None


def analyze_news(item):
    if not OPENAI_KEY:
        print("❌ OPENAI_API_KEY not found")
        return None

    prompt = (
        "You are a professional crypto market analyst.\n"
        "Analyze the news below.\n\n"
        f"Title: {item['title']}\n"
        f"Summary: {item['summary']}\n\n"
        "Respond ONLY in valid JSON.\n"
        "JSON schema:\n"
        "{\n"
        '  "score": number from 0 to 100,\n'
        '  "sentiment": "bullish" | "bearish" | "neutral",\n'
        '  "impact": "low" | "medium" | "high",\n'
        '  "reason": "short explanation"\n'
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
        if r.status_code != 200:
            print("❌ GPT HTTP:", r.status_code, r.text)
            return None

        data = r.json()
        content = data["choices"][0]["message"]["content"]

        return safe_json_extract(content)

    except Exception as e:
        print("❌ GPT exception:", e)
        return None