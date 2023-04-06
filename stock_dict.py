stocks = {}

def buy_stock(stock_name, shares, price):
    if stock_name in stocks:
        stocks[stock_name]['shares'] += shares
    else:
        stocks[stock_name] = {'shares': shares, 'price': price}
    print(f"Bought {shares} shares of {stock_name} at {price} per share.")

def sell_stock(stock_name, shares, price):
    if stock_name in stocks:
        if stocks[stock_name]['shares'] >= shares:
            stocks[stock_name]['shares'] -= shares
            print(f"Sold {shares} shares of {stock_name} at {price} per share.")
        else:
            print(f"You don't have enough shares of {stock_name} to sell.")
    else:
        print(f"You don't have any shares of {stock_name}.")
def view_stock(stock_name, shares, price):
  if price>0:
    print(f"{stock_name}:{shares} +{price}%")
  else:
    print(f"{stock_name}:{shares} {price}%")