import requests

CRYPTO_PANIC_API = "https://cryptopanic.com/api/v1/posts/"
API_KEY = "377c1425964e645bf4f97717ed7affb380932eef"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


def fetch_cryptopanic():
    params = {
        "auth_token": API_KEY,
        "kind": "news"
    }

    try:
        r = requests.get(
            CRYPTO_PANIC_API,
            params=params,
            headers=HEADERS,
            timeout=20
        )

        if r.status_code != 200:
            print(f"❌ CryptoPanic HTTP {r.status_code}")
            print(r.text[:200])
            return []

        data = r.json()
        return data.get("results", [])

    except Exception as e:
        print("❌ CryptoPanic request error:", e)
        return []


def normalize(item):
    return {
        "title": item.get("title", ""),
        "url": item.get("url", ""),
        "source": "CryptoPanic",
        "published": item.get("published_at"),
        "currencies": [c["code"] for c in item.get("currencies", [])]
    }


def collect():
    raw = fetch_cryptopanic()
    return [normalize(n) for n in raw]
