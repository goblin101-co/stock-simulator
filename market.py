import finnhub

API_KEY = "d6ng57hr01qodk5vlne0d6ng57hr01qodk5vlneg"

client = finnhub.Client(api_key=API_KEY)


def get_live_price(symbol: str) -> float:
    symbol = symbol.upper().strip()
    quote = client.quote(symbol)
    price = quote.get("c")

    if price is None or price == 0:
        raise ValueError(f"Could not get valid price for {symbol}")

    return float(price)


def get_company_name(symbol: str) -> str:
    symbol = symbol.upper().strip()
    profile = client.company_profile2(symbol=symbol)
    return profile.get("name", symbol)