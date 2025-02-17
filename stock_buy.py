import dataset

# Connect to the database
db = dataset.connect('sqlite:///stock_portfolio.db')
table = db['Stock_Portfolio']
"""
when buying stocks the programme checks if the stock is already in the database.
If yes then it adds the number of shares to the existing number of shares, and updates the quantity and price.
If no then it creates a new record in the database.
"""
def buy_stock(stock_name, shares, price):
    record = table.find_one(stock_name=stock_name)
    if record:
        record['shares'] += shares
        record['price'] = price
        table.update(record, ['stock_name'])
    else:
        table.insert(dict(stock_name=stock_name, shares=shares, price=price))
    print(f"Bought {shares} shares of {stock_name} at {price} per share.")
"""
when selling stocks the programme checks if the stock is already in the database.
If yes then it subtracts the number of stocks from the existing number of stocks, and updates the quantity and price.
If no then it prints a message saying that the user does not have any shares of that stock.
"""
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