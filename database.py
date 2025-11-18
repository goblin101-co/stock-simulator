stocks = {}
import dataset

# Connect to the database
db = dataset.connect('sqlite:///stock_portfolio.db')
portfolio_table = db['Stock_Portfolio']
player_table = db['Player']  # New table to store player data

"""
When buying stocks, the program checks if the stock is already in the database.
If yes, it adds the number of shares to the existing number of shares and updates the quantity and price.
If no, it creates a new record in the database.
"""
def buy_stock(stock_name, shares, price):
    record = portfolio_table.find_one(stock_name=stock_name)
    if record and stock_name in stocks:
        stocks[stock_name]['shares'] += shares
        record['shares'] += shares
        record['price'] = price
        portfolio_table.update(record, ['stock_name'])
        db.commit()
    else:
        stocks[stock_name] = {'shares': shares, 'price': price}
        portfolio_table.insert(dict(stock_name=stock_name, shares=shares, price=price))
        db.commit()
    print(f"Bought {shares} shares of {stock_name} at {price} per share.")

"""
When selling stocks, the program checks if the stock is already in the database.
If yes, it subtracts the number of shares from the existing quantity and updates the database.
If no, it prints a message saying the user does not own any shares of that stock.
"""
def sell_stock(stock_name, shares, price):
    record = portfolio_table.find_one(stock_name=stock_name)
    if record and stock_name in stocks:
        stocks[stock_name]['shares'] -= shares
        if record['shares'] >= shares:
            record['shares'] -= shares
            portfolio_table.update(record, ['stock_name'])
            print(f"Sold {shares} shares of {stock_name} at {price} per share.")
        else:
            print(f"You don't have enough shares of {stock_name} to sell.")
    else:
        print(f"You don't have any shares of {stock_name}.")

"""
Initialize player data by storing the player's name and the number of days they have in the market.
If the player exists, update their days remaining.
"""
def initialize_player(name, days):
    player = player_table.find_one(name=name)
    if player:
        player['days_remaining'] = days
        player_table.update(player, ['name'])
    else:
        player_table.insert(dict(name=name, days_remaining=days))

"""
Prints the stock name, and number of shares and price.
Changes if negative or positive.
"""
def view_stock(stock_name, shares, price):
    if price>0:
        print(f"{stock_name}:{shares} +{price}%")
    else:
        print(f"{stock_name}:{shares} {price}%")

"""
Decrease the player's remaining days by 1.
If the player does not exist, return None.
"""
def update_days(name):
    player = player_table.find_one(name=name)
    if player:
        player['days_remaining'] -= 1
        player_table.update(player, ['name'])
        return player['days_remaining']
    return None

"""
Adds password to player data in database.
"""