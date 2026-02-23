import telebot
import requests
from telebot import types

TOKEN = "8248511756:AAF5c5niQGQwgr6O0nY7GpQwqc_wr02OtWk"
bot = telebot.TeleBot(TOKEN)

# ---------- ارزهای محبوب و گسترده ----------
coin_map = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "BNB": "binancecoin",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "LTC": "litecoin",
    "LINK": "chainlink",
    "MATIC": "matic-network",
    "DOT": "polkadot",
    "UNI": "uniswap",
    "AVAX": "avalanche-2",
    "SHIB": "shiba-inu",
    "ATOM": "cosmos",
    "ALGO": "algorand",
    "TRX": "tron",
    "XLM": "stellar",
    "FTM": "fantom",
    "NEAR": "near",
    "FIL": "filecoin",
    "AAVE": "aave",
    "GRT": "the-graph",
    "SAND": "the-sandbox",
    "MANA": "decentraland",
    "ICP": "internet-computer",
    "EGLD": "elrond-erd-2",
    "CRO": "crypto-com-chain",
    "KSM": "kusama",
    "QNT": "quant-network",
    "KAVA": "kava",
    "VET": "vechain",
    "XTZ": "tezos",
    "EOS": "eos",
    "ZEC": "zcash",
    "DASH": "dash",
    "COMP": "compound-governance-token",
    "AVAX": "avalanche-2",
    "LDO": "lido-dao",
    "BAT": "basic-attention-token"
}

def calculate_rsi(prices, period=14):
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

# ---------- منوی اصلی ----------
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📊 تحلیل BTC", "📊 تحلیل ETH", "📊 تحلیل SOL")
    markup.row("📊 تحلیل XRP", "📊 تحلیل BNB", "📊 تحلیل ADA")
    markup.row("📊 تحلیل DOGE", "📊 تحلیل LTC", "⭐️ ارزهای محبوب")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 *دستیار ترید حرفه‌ای*\n\n"
        "ارز موردنظر رو از منو انتخاب کن 👇",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def analyze(message):
    text = message.text.upper().replace("📊 تحلیل ", "")
    if text == "⭐️ ارزهای محبوب":
        bot.send_message(
            message.chat.id,
            "⭐️ ارزهای پیشنهادی امروز:\n" +
            "\n".join(coin_map.keys())
        )
        return
    if text not in coin_map:
        bot.send_message(message.chat.id, "❌ ارز نامعتبره")
        return

    coin_id = coin_map[text]
    try:
        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        price = requests.get(price_url, timeout=10).json()[coin_id]["usd"]

        chart_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=1"
        prices = [p[1] for p in requests.get(chart_url, timeout=10).json()["prices"]]

        ma_short = sum(prices[-5:]) / 5
        ma_long = sum(prices[-20:]) / 20
        rsi = calculate_rsi(prices)

        trend = "📈 صعودی" if ma_short > ma_long else "📉 نزولی"

        if rsi < 30:
            rsi_state = "🟢 اشباع فروش"
        elif rsi > 70:
            rsi_state = "🔴 اشباع خرید"
        else:
            rsi_state = "🟡 متعادل"

        if ma_short > ma_long and rsi < 70:
            decision = "✅ *پیشنهاد: احتمال خرید*"
        elif ma_short < ma_long and rsi > 30:
            decision = "❌ *پیشنهاد: احتمال فروش*"
        else:
            decision = "⏳ *پیشنهاد: صبر*"

        msg = (
            f"📊 *تحلیل {text}*\n\n"
            f"💰 قیمت: {price}$\n"
            f"{trend}\n"
            f"RSI: {rsi} ({rsi_state})\n\n"
            f"{decision}"
        )

        bot.send_message(
            message.chat.id,
            msg,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ خطا:\n{e}")

bot.polling()