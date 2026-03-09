from market import get_live_price, get_company_name

symbol = input("Enter ticker: ").upper()

try:
    company = get_company_name(symbol)
    price = get_live_price(symbol)
    print(f"{company} ({symbol}) = ${price}")
except Exception as e:
    print("Error:", e)