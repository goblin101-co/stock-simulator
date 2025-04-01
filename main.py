import pygame
import pygame_gui
import random
import sys
import stock_buy
import menu
import player_setup

pygame.init()
pygame.display.set_caption('Stock Simulator Game')
WINDOW_SIZE = (800, 600)
window_surface = pygame.display.set_mode(WINDOW_SIZE)
manager = pygame_gui.UIManager(WINDOW_SIZE)

clock = pygame.time.Clock()

# Global state variables
amount_money = menu.amount_money  # 100000
total_num_of_stock = menu.total_num_of_stock  # 0
days = menu.days  # Will be set by player input
player_name = ""

# Define stock groups (each group shares the same price today)
stock_options = ["APPLE", "GOOGLE", "NVIDIA"]
stock_options2 = ["NINTENDO", "TESLA", "LOGITECH"]
stock_options3 = ["SAMSUNG", "MICROSOFT", "FACEBOOK"]

# Variables for current day stock prices (for buying and selling)
price_group1 = 0
price_group2 = 0
price_group3 = 0
sell_price_group1 = 0
sell_price_group2 = 0
sell_price_group3 = 0

# Also store randomized full list for dropdown menus (all nine stocks)
display_buy_options = []
display_sell_options = []

def update_stock_prices():
    global price_group1, price_group2, price_group3
    global sell_price_group1, sell_price_group2, sell_price_group3
    global display_buy_options, display_sell_options

    # Generate new random prices for the day for each group.
    price_group1 = random.randint(100, 600)
    price_group2 = random.randint(100, 600)
    price_group3 = random.randint(100, 600)
    sell_price_group1 = random.randint(100, 600)
    sell_price_group2 = random.randint(100, 600)
    sell_price_group3 = random.randint(100, 600)

    # Combine all stocks for the dropdown menus.
    combined_options = stock_options + stock_options2 + stock_options3
    display_buy_options = combined_options.copy()
    display_sell_options = combined_options.copy()
    random.shuffle(display_buy_options)
    random.shuffle(display_sell_options)

# ------------------------------
# GameButton Class Definition
# ------------------------------
class GameButton:
    def __init__(self, rect, text, manager, action, attributes=None, container=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action  # e.g., "buy", "sell", "next_day"
        self.attributes = attributes if attributes else {}
        # Create the actual UI button as part of the container (game_panel)
        self.button = pygame_gui.elements.UIButton(relative_rect=self.rect,
                                                    text=self.text,
                                                    manager=manager,
                                                    container=container)
    def update_text(self, new_text):
        self.button.set_text(new_text)
        self.text = new_text

# ------------------------------
# MAIN MENU UI
# ------------------------------
main_menu_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((200, 150), (400, 300)),
                                              manager=manager)

welcome_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 20), (300, 30)),
                                            text="Welcome to the Stock Market",
                                            manager=manager,
                                            container=main_menu_panel)

name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 70), (100, 30)),
                                         text="Name:",
                                         manager=manager,
                                         container=main_menu_panel)
name_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((150, 70), (200, 30)),
                                                 manager=manager,
                                                 container=main_menu_panel)

days_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 120), (100, 30)),
                                         text="Days to play:",
                                         manager=manager,
                                         container=main_menu_panel)
days_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((150, 120), (200, 30)),
                                                 manager=manager,
                                                 container=main_menu_panel)

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 180), (100, 50)),
                                            text="Start Game",
                                            manager=manager,
                                            container=main_menu_panel)

# ------------------------------
# GAME SCREEN UI (initially hidden)
# ------------------------------
game_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (800, 600)),
                                         manager=manager,
                                         visible=0)

info_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (400, 50)),
                                         text="",
                                         manager=manager,
                                         container=game_panel)

# Use a UITextBox for multiline stock display.
stock_label = pygame_gui.elements.UITextBox(html_text="",
                                            relative_rect=pygame.Rect((10, 70), (780, 200)),
                                            manager=manager,
                                            container=game_panel)

# Create game buttons as actual objects with attributes
buy_game_button = GameButton((50, 500, 100, 50), "Buy", manager, action="buy", container=game_panel)
sell_game_button = GameButton((200, 500, 100, 50), "Sell", manager, action="sell", container=game_panel)
next_day_game_button = GameButton((350, 500, 150, 50), "Next Day", manager, action="next_day", container=game_panel)

# Modal windows (created when needed)
buy_modal = None
sell_modal = None

def show_buy_modal():
    global buy_modal
    buy_modal = pygame_gui.elements.UIWindow(rect=pygame.Rect((250, 200), (300, 200)),
                                             manager=manager,
                                             window_display_title="Buy Stock")
    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                text="Stock:",
                                manager=manager,
                                container=buy_modal)
    # Use the full list for the dropdown.
    buy_stock_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=display_buy_options,
                                                            starting_option=display_buy_options[0],
                                                            relative_rect=pygame.Rect((120, 10), (150, 30)),
                                                            manager=manager,
                                                            container=buy_modal)
    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 60), (100, 30)),
                                text="Shares:",
                                manager=manager,
                                container=buy_modal)
    buy_shares_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((120, 60), (150, 30)),
                                                           manager=manager,
                                                           container=buy_modal)
    confirm_buy_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 120), (100, 40)),
                                                      text="Confirm",
                                                      manager=manager,
                                                      container=buy_modal,
                                                      object_id="#confirm_buy_button")
    # Save references for later access.
    buy_modal.user_data = {
        "dropdown": buy_stock_dropdown,
        "shares_entry": buy_shares_entry
    }

def show_sell_modal():
    global sell_modal
    sell_modal = pygame_gui.elements.UIWindow(rect=pygame.Rect((250, 200), (300, 200)),
                                              manager=manager,
                                              window_display_title="Sell Stock")
    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                text="Stock:",
                                manager=manager,
                                container=sell_modal)
    sell_stock_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=display_sell_options,
                                                             starting_option=display_sell_options[0],
                                                             relative_rect=pygame.Rect((120, 10), (150, 30)),
                                                             manager=manager,
                                                             container=sell_modal)
    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 60), (100, 30)),
                                text="Shares:",
                                manager=manager,
                                container=sell_modal)
    sell_shares_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((120, 60), (150, 30)),
                                                            manager=manager,
                                                            container=sell_modal)
    confirm_sell_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 120), (100, 40)),
                                                       text="Confirm",
                                                       manager=manager,
                                                       container=sell_modal,
                                                       object_id="#confirm_sell_button")
    sell_modal.user_data = {
        "dropdown": sell_stock_dropdown,
        "shares_entry": sell_shares_entry
    }

# Game state flag
game_state = "main_menu"  # possible states: "main_menu", "game"

# ------------------------------
# MAIN LOOP
# ------------------------------
is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Handle dropdown changes (avoid unhandled events causing a crash)
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            print("Dropdown changed to:", event.ui_element.selected_option)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Main Menu actions
            if event.ui_element == start_button:
                player_name = name_entry.get_text()
                try:
                    days = int(days_entry.get_text())
                except ValueError:
                    days = 10  # default if invalid
                menu.days = days
                stock_buy.initialize_player(player_name, days)
                update_stock_prices()  # sets prices for the day
                main_menu_panel.hide()
                game_panel.show()
                game_state = "game"

            # In-game button actions via our GameButton objects
            elif event.ui_element == buy_game_button.button:
                show_buy_modal()
            elif event.ui_element == sell_game_button.button:
                show_sell_modal()
            elif event.ui_element == next_day_game_button.button:
                if days > 0:
                    days -= 1
                    menu.days = days
                    stock_buy.update_days(player_name)
                    update_stock_prices()  # update prices for new day
                    if days <= 0:
                        info_label.set_text("Game Over: No more days left.")
                    else:
                        info_label.set_text(
                            f"Player: {player_name} | Money: ${amount_money} | Days left: {days} | Total Stocks: {total_num_of_stock}"
                        )
                else:
                    info_label.set_text("No days left. You cannot go to the next day.")

            # Modal confirmation actions for buying
            elif "#confirm_buy_button" in event.ui_element.get_object_ids():
                if buy_modal is not None:
                    dropdown = buy_modal.user_data["dropdown"]
                    shares_entry = buy_modal.user_data["shares_entry"]
                    selected_stock = dropdown.selected_option
                    try:
                        shares = int(shares_entry.get_text())
                    except ValueError:
                        shares = 0
                    # Determine the buy price by checking which group the stock belongs to.
                    if selected_stock in stock_options:
                        price = price_group1
                    elif selected_stock in stock_options2:
                        price = price_group2
                    else:
                        price = price_group3
                    cost = price * shares
                    print(f"Attempting to buy {shares} shares of {selected_stock} at ${price} each (Total cost: ${cost}). Funds available: ${amount_money}")
                    if cost <= amount_money and shares > 0:
                        amount_money -= cost
                        stock_buy.buy_stock(selected_stock, shares, price)
                        total_num_of_stock += shares
                    else:
                        info_label.set_text("Insufficient funds or invalid share number.")
                    buy_modal.kill()
                    buy_modal = None

            # Modal confirmation actions for selling
            elif "#confirm_sell_button" in event.ui_element.get_object_ids():
                if sell_modal is not None:
                    dropdown = sell_modal.user_data["dropdown"]
                    shares_entry = sell_modal.user_data["shares_entry"]
                    selected_stock = dropdown.selected_option
                    try:
                        shares = int(shares_entry.get_text())
                    except ValueError:
                        shares = 0
                    if selected_stock in stock_options:
                        price = sell_price_group1
                    elif selected_stock in stock_options2:
                        price = sell_price_group2
                    else:
                        price = sell_price_group3
                    stock_buy.sell_stock(selected_stock, shares, price)
                    amount_money += price * shares
                    total_num_of_stock -= shares
                    sell_modal.kill()
                    sell_modal = None

        manager.process_events(event)

    manager.update(time_delta)

    if game_state == "game":
        info_label.set_text(
            f"Player: {player_name} | Money: ${amount_money} | Days left: {days} | Total Stocks: {total_num_of_stock}"
        )
        # Build a multiline HTML string to display ALL stocks.
        stock_text = "<b>Today's Stock Prices:</b><br>"
        for stock in stock_options:
            stock_text += f"{stock}: Buy ${price_group1}, Sell ${sell_price_group1}<br>"
        for stock in stock_options2:
            stock_text += f"{stock}: Buy ${price_group2}, Sell ${sell_price_group2}<br>"
        for stock in stock_options3:
            stock_text += f"{stock}: Buy ${price_group3}, Sell ${sell_price_group3}<br>"
        stock_label.html_text = stock_text
        stock_label.rebuild()

    window_surface.fill(pygame.Color('#000000'))
    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
sys.exit()
