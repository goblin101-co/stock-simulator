import os
import dataset

# Define the path to the database file
db_path = 'sqlite:///stock_portfolio.db'

# Check if the database file exists
if os.path.exists('stock_portfolio.db'):
    db = dataset.connect(db_path)
    table = db['Stock_Portfolio']
    
    # Check if the table contains any records
    if table.count() > 0:
        print("Welcome back, returning player!")
    else:
        print("Welcome, new player! Setting up your portfolio.")
else:
    # Create a new database and table
    db = dataset.connect(db_path)
    table = db['Stock_Portfolio']
    print("Welcome, new player! Setting up your portfolio.")

def find_user(username):
    """
    Searches for a specific username in the Stock_Portfolio table.

    :param username: The username to search for.
    :return: The record if found, otherwise None.
    """
    record = table.find_one(username=username)
    return record

# Example usage
username_to_search = 'JohnDoe'
user_record = find_user(username_to_search)

if user_record:
    print(f"User found: {user_record}")
else:
    print(f"User {username_to_search} not found.")