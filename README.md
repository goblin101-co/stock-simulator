# stock-simulator

# This project is currently being refurbished, but the changes will be completed soon!
https://replit.com/@RonSaks29/stonk-sim?v=1 <--- link to the game on Replit if you want to try it out yourself.

1. **Game Setup:**
   - Enter the number of days you want to play and your username.

2. **Stock Buying:**
   - Decide to buy stocks; you're shown 3 randomly generated stocks with prices.
   - Each stock is created from 6 lists - 3 with company names and 3 with price ranges.
   - Choose a stock, enter the quantity, and it's added to a dictionary with a function called `buy_stock`.

3. **Stock Selling:**
   - View your portfolio with a function called `view_stock` that displays stock name, quantity, and changing price per share.
   - Select the stock to sell using a function called `sell_stock`, which deducts the sold quantity, removes it from the dictionary, and adds the profit to your account.

4. **Game Progression:**
   - The game progresses daily, with the day count decreasing.
   - A loop continues until the specified number of days is reached.
   - After each day, the screen is cleared for a cleaner display using the function `clear_screen`.

5. **Smooth Output:**
   - To enhance output display, a function called `display_letter_by_letter` is used for smoother text presentation.

6. **End of Day Cleanup:**
   - After each day, the screen is cleared using the function `clear_screen` to maintain a tidy interface.
