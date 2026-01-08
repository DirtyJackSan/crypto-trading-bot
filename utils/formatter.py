from datetime import datetime, UTC

def format_market_update(rows):
    text = "📊 <b>Обзор рынка (выбранные пары)</b>\n"
    text += "━━━━━━━━━━━━\n"

    for r in rows:
        arrow = "🟢" if r["change"] >= 0 else "🔴"
        text += (
            f"💱 <b>{r['symbol']}</b>\n"
            f"Цена: <b>{r['price']:,.2f}</b>\n"
            f"15м: {arrow} <b>{r['change']:+.2f}%</b>\n\n"
        )

    text += "━━━━━━━━━━━━\n"
    text += f"🕒 {datetime.now(UTC).strftime('%H:%M UTC')}"
    return text
