import requests
import json
from datetime import datetime

print("🤖 ربات هوش طلایی - GitHub Actions")
print("=" * 50)

def get_wallex_prices():
    """گرفتن قیمت از Wallex"""
    try:
        url = "https://api.wallex.ir/v1/markets"
        response = requests.get(url, timeout=15)
        data = response.json()
        result = {}
        symbols = data.get("result", {}).get("symbols", {})
        
        if "USDTTMN" in symbols:
            price = symbols["USDTTMN"].get("stats", {}).get("lastPrice", 0)
            if price:
                result["usdt"] = int(float(price))
        if "BTCTMN" in symbols:
            price = symbols["BTCTMN"].get("stats", {}).get("lastPrice", 0)
            if price:
                result["btc_irr"] = int(float(price))
        if "ETHTMN" in symbols:
            price = symbols["ETHTMN"].get("stats", {}).get("lastPrice", 0)
            if price:
                result["eth_irr"] = int(float(price))
        return result
    except Exception as e:
        print(f"خطا در Wallex: {e}")
        return None

def get_crypto_and_gold():
    """قیمت جهانی ارز دیجیتال و طلا"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,pax-gold",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return {
            "btc": data.get("bitcoin", {}).get("usd", 0),
            "eth": data.get("ethereum", {}).get("usd", 0),
            "ounce": data.get("pax-gold", {}).get("usd", 4000),
        }
    except Exception as e:
        print(f"خطا در کریپتو: {e}")
        return None

def update_prices():
    print(f"\n{datetime.now().strftime('%H:%M:%S')} - در حال بروزرسانی...")
    
    prices = {
        "coin": 920000000, "half_coin": 470000000, "quarter_coin": 250000000,
        "gold18": 187000000, "melted_gold": 811000000, "ounce": 4039,
        "usd": 193000, "eur": 218000, "usdt": 193000,
        "btc": 64000, "eth": 3000,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    crypto = get_crypto_and_gold()
    if crypto:
        prices["btc"] = crypto["btc"]
        prices["eth"] = crypto["eth"]
        prices["ounce"] = crypto["ounce"]
        print(f"BTC: ${crypto['btc']:,}")
        print(f"انس: ${crypto['ounce']:,}")
    
    wallex = get_wallex_prices()
    if wallex and "usdt" in wallex:
        prices["usdt"] = wallex["usdt"]
        prices["usd"] = wallex["usdt"]
        prices["eur"] = int(wallex["usdt"] * 1.13)
        print(f"دلار: {wallex['usdt']:,} تومان")
    
    if prices["usd"] > 50000 and prices["ounce"] > 1000:
        gold_24_per_gram = (prices["ounce"] * prices["usd"]) / 31.1035
        prices["gold18"] = int(gold_24_per_gram * 0.75)
        prices["melted_gold"] = int(gold_24_per_gram * 0.7047 * 4.608)
        
        coin_intrinsic = gold_24_per_gram * 0.900 * 8.133
        prices["coin"] = int(coin_intrinsic * 1.08)
        prices["half_coin"] = int(coin_intrinsic / 2 * 1.10)
        prices["quarter_coin"] = int(coin_intrinsic / 4 * 1.15)
        
        print(f"سکه: {prices['coin']:,} تومان")
    
    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)
    
    print("prices.json ذخیره شد")
    return prices

try:
    update_prices()
    print("\nموفقیت‌آمیز اجرا شد!")
except Exception as e:
    print(f"خطا: {e}")
    exit(1)
