import os
import json
import requests

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"


def analyze_news(item):
    prompt = f"""
You are a crypto market analyst.

News:
Title: {item['title']}
Summary: {item['summary']}

Answer in JSON:
{{
  "score": 0-100,
  "sentiment": "bullish | bearish | neutral",
  "impact": "low | medium | high",
  "reason": "short explanation"
}}
"""

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    r = requests.post(API_URL, headers=headers, json=payload, timeout=20)
    data = r.json()

    try:
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception:
        return None