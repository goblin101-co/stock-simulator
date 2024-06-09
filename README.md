# stock-simulator

# There are a lot of changes being made at the moment, but this project will hopefully be done very soon.
# For more information on this project, view the [Wiki](https://github.com/goblin101-co/stock-simulator/wiki) page. Or read and download a paper that I wrote on this project here <--still being writen.

1. **Stock Buying:**
   - Decide to buy stocks; you're shown 3 randomly generated stocks with prices.
   - Each stock is created from 6 lists - 3 with company names and 3 with price ranges.
   - Choose a stock, enter the quantity, and it's added to a dictionary with a function called `buy_stock`.

2. **Stock Selling:**
   - View your portfolio with a function called `view_stock` that displays stock name, quantity, and changing price per share.
   - Select the stock to sell using a function called `sell_stock`, which deducts the sold quantity, removes it from the dictionary, and adds the profit to your account.

3. **Game Progression:**
   - The game progresses daily, with the day count decreasing.
   - A loop continues until the specified number of days is reached, or the players networth reaches zero.

4. **Smooth Output:**
   - To enhance output display, a function called `display_letter_by_letter` is used for smoother text presentation.

5. **End of Day Cleanup:**
   - After each day, the screen is cleared using the function `clear_screen` to maintain a tidy interface.
6. **Music feature:**
   - Whilst playing the game there is music playing through the use of the function `play_music`.
7. **Google Sheet:**
   - Using the `credentials.json` file, the python code has access to the Google Sheets API and can edit the given google sheet.
