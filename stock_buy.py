import dataset

# Connect to the database
db = dataset.connect('sqlite:///stock_portfolio.db')
table = db['Stock_Portfolio']

def buy_stock(stock_name, shares, price):
    record = table.find_one(stock_name=stock_name)
    if record:
        record['shares'] += shares
        record['price'] = price
        table.update(record, ['stock_name'])
    else:
        table.insert(dict(stock_name=stock_name, shares=shares, price=price))
    print(f"Bought {shares} shares of {stock_name} at {price} per share.")

def sell_stock(stock_name, shares, price):
    record = table.find_one(stock_name=stock_name)
    if record:
        if record['shares'] >= shares:
            record['shares'] -= shares
            table.update(record, ['stock_name'])
            print(f"Sold {shares} shares of {stock_name} at {price} per share.")
        else:
            print(f"You don't have enough shares of {stock_name} to sell.")
    else:
        print(f"You don't have any shares of {stock_name}.")

def view_stock(stock_name):
    record = table.find_one(stock_name=stock_name)
    if record:
        shares = record['shares']
        price = record['price']
        if price > 0:
            print(f"{stock_name}: {shares} shares, +{price}%")
        else:
            print(f"{stock_name}: {shares} shares, {price}%")
    else:
        print(f"No record found for {stock_name}.")

# Creates Database within file
# Adds stocks to the database instead of the dictionary through functions