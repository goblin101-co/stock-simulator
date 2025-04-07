import pygame
import pygame_gui
import random
import sys
import stock_buy
from stock_buy import buy_stock, sell_stock, initialize_player, update_days
import menu
import player_setup

pygame.init()
pygame.display.set_caption('Stock Simulator Game')
WINDOW_SIZE = (800, 600)
window_surface = pygame.display.set_mode(WINDOW_SIZE)
manager = pygame_gui.UIManager(WINDOW_SIZE)

clock = pygame.time.Clock()

# Global state variables
amount_money = menu.amount_money  # e.g. 100000
days = 0  # Will be set by the player
player_name = ""
portfolio = {}  # Dictionary tracking stocks owned; keys are stock names, values are number of shares

# Define stock groups (each group shares the same price today)
stock_options = ["APPLE", "GOOGLE", "NVIDIA"]
stock_options2 = ["NINTENDO", "TESLA", "LOGITECH"]
stock_options3 = ["SAMSUNG", "MICROSOFT", "FACEBOOK"]

# Daily stock prices for each group
group1_price = 0
group2_price = 0
group3_price = 0

# Dropdown for buying (selling will be built from the portfolio)
display_buy_options = []

def update_stock_prices():
    global group1_price, group2_price, group3_price, display_buy_options
    group1_price = random.randint(100, 600)
    group2_price = random.randint(100, 600)
    group3_price = random.randint(100, 600)
    combined = stock_options + stock_options2 + stock_options3
    random.shuffle(combined)
    display_buy_options = combined[:]  # For buying, show all stocks

def refresh_stock_display():
    stock_text = "<b>Today's Stock Prices:</b><br>"
    for stock in stock_options:
        stock_text += f"{stock}: ${group1_price}<br>"
    for stock in stock_options2:
        stock_text += f"{stock}: ${group2_price}<br>"
    for stock in stock_options3:
        stock_text += f"{stock}: ${group3_price}<br>"
    stock_label.html_text = stock_text
    stock_label.rebuild()

def get_stock_price(selected_stock):
    if selected_stock in stock_options:
        return group1_price
    elif selected_stock in stock_options2:
        return group2_price
    else:
        return group3_price

def update_total_stocks_label():
    # Compute total stocks by summing all values in portfolio.
    total = sum(portfolio.values())
    total_stocks_label.set_text(f"Total Stocks: {total}")

class GameButton:
    def __init__(self, rect, text, manager, action, attributes=None, container=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.attributes = attributes if attributes else {}
        self.button = pygame_gui.elements.UIButton(
            relative_rect=self.rect,
            text=self.text,
            manager=manager,
            container=container
        )
    def update_text(self, new_text):
        self.button.set_text(new_text)
        self.text = new_text

# START PANEL (Name and Days Input)
start_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((200, 150), (400, 300)),
    manager=manager
)
start_title = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((50, 20), (300, 30)),
    text="Welcome to the Stock Market",
    manager=manager,
    container=start_panel
)
name_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((50, 70), (100, 30)),
    text="Name:",
    manager=manager,
    container=start_panel
)
name_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((150, 70), (200, 30)),
    manager=manager,
    container=start_panel
)
days_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((50, 120), (100, 30)),
    text="Days to play:",
    manager=manager,
    container=start_panel
)
days_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((150, 120), (200, 30)),
    manager=manager,
    container=start_panel
)
start_game_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((150, 180), (100, 50)),
    text="Start Game",
    manager=manager,
    container=start_panel
)

# GAME PANEL (Main Gameplay Screen)
game_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((0, 0), (800, 600)),
    manager=manager,
    visible=False
)
# Info label on top left
info_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 10), (400, 50)),
    text="",
    manager=manager,
    container=game_panel
)
# Total Stocks label on top right
total_stocks_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((600, 10), (190, 50)),
    text="Total Stocks: 0",
    manager=manager,
    container=game_panel
)
stock_label = pygame_gui.elements.UITextBox(
    html_text="",
    relative_rect=pygame.Rect((10, 70), (780, 200)),
    manager=manager,
    container=game_panel
)
buy_game_button = GameButton((50, 500, 100, 50), "Buy", manager, action="buy", container=game_panel)
sell_game_button = GameButton((200, 500, 100, 50), "Sell", manager, action="sell", container=game_panel)
next_day_button = GameButton((350, 500, 150, 50), "Next Day", manager, action="next_day", container=game_panel)

buy_modal = None
sell_modal = None

def show_buy_modal():
    global buy_modal
    buy_modal = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((250, 200), (300, 200)),
        manager=manager,
        window_display_title="Buy Stock"
    )
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((10, 10), (100, 30)),
        text="Stock:",
        manager=manager,
        container=buy_modal
    )
    buy_stock_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=display_buy_options,
        starting_option=display_buy_options[0],
        relative_rect=pygame.Rect((120, 10), (150, 30)),
        manager=manager,
        container=buy_modal
    )
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((10, 60), (100, 30)),
        text="Shares:",
        manager=manager,
        container=buy_modal
    )
    buy_shares_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((120, 60), (150, 30)),
        manager=manager,
        container=buy_modal
    )
    confirm_buy_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((100, 120), (100, 40)),
        text="Confirm",
        manager=manager,
        container=buy_modal,
        object_id="#confirm_buy_button"
    )
    buy_modal.user_data = {"dropdown": buy_stock_dropdown, "shares_entry": buy_shares_entry}

def show_sell_modal():
    global sell_modal
    # Only allow selling if the portfolio is not empty.
    if not portfolio:
        info_label.set_text("No stocks in portfolio to sell.")
        return
    sell_modal = pygame_gui.elements.UIWindow(
        rect=pygame.Rect((250, 200), (300, 200)),
        manager=manager,
        window_display_title="Sell Stock"
    )
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((10, 10), (100, 30)),
        text="Stock:",
        manager=manager,
        container=sell_modal
    )
    # Build dropdown options from portfolio keys only.
    sell_stock_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=list(portfolio.keys()),
        starting_option=list(portfolio.keys())[0],
        relative_rect=pygame.Rect((120, 10), (150, 30)),
        manager=manager,
        container=sell_modal
    )
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((10, 60), (100, 30)),
        text="Shares:",
        manager=manager,
        container=sell_modal
    )
    sell_shares_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((120, 60), (150, 30)),
        manager=manager,
        container=sell_modal
    )
    confirm_sell_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((100, 120), (100, 40)),
        text="Confirm",
        manager=manager,
        container=sell_modal,
        object_id="#confirm_sell_button"
    )
    sell_modal.user_data = {"dropdown": sell_stock_dropdown, "shares_entry": sell_shares_entry}

is_running = True
game_state = "menu"  # Start in menu

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # START PANEL ACTIONS
            if event.ui_element == start_game_button:
                player_name = name_entry.get_text().strip()
                try:
                    days = int(days_entry.get_text())
                except ValueError:
                    days = 10
                if player_name == "" or days <= 0:
                    info_label.set_text("Please enter a valid name and number of days.")
                else:
                    initialize_player(player_name, days)
                    update_stock_prices()
                    refresh_stock_display()
                    start_panel.hide()
                    game_panel.show()
                    game_state = "game"

            # IN-GAME ACTIONS
            elif event.ui_element == buy_game_button.button:
                show_buy_modal()
            elif event.ui_element == sell_game_button.button:
                show_sell_modal()
            elif event.ui_element == next_day_button.button:
                if days > 0:
                    days -= 1
                    menu.days = days
                    update_days(player_name)
                    update_stock_prices()
                    refresh_stock_display()
                    if days <= 0:
                        info_label.set_text("Game Over: No more days left.")
                        pygame.time.delay(2000)
                        is_running = False
                    else:
                        info_label.set_text(f"Player: {player_name} | Money: ${amount_money} | Days left: {days}")
                else:
                    info_label.set_text("No days left. Cannot advance.")

            # BUY MODAL CONFIRMATION
            elif hasattr(event.ui_element, "get_object_ids"):
                object_ids = event.ui_element.get_object_ids()
                if "#confirm_buy_button" in object_ids:
                    if buy_modal is not None:
                        dropdown = buy_modal.user_data["dropdown"]
                        shares_entry = buy_modal.user_data["shares_entry"]
                        selected_stock = dropdown.selected_option
                        try:
                            shares = int(shares_entry.get_text())
                        except ValueError:
                            shares = 0
                        price = get_stock_price(selected_stock)
                        cost = price * shares
                        if cost <= amount_money and shares > 0:
                            print(f"Buying: {selected_stock}, Shares: {shares}, Price: {price}, Money: {amount_money}")
                            try:
                                buy_stock(selected_stock, shares, price)
                                amount_money -= cost
                                # Update portfolio: add shares
                                portfolio[selected_stock] = portfolio.get(selected_stock, 0) + shares
                                info_label.set_text(f"Bought {shares} of {selected_stock} at ${price} each.")
                            except Exception as e:
                                print(f"Error in buy_stock: {e}")
                                info_label.set_text("Error: Could not complete purchase.")
                        else:
                            info_label.set_text("Insufficient funds or invalid share number.")
                        buy_modal.kill()
                        buy_modal = None
                        update_total_stocks_label()

                elif "#confirm_sell_button" in object_ids:
                    if sell_modal is not None:
                        dropdown = sell_modal.user_data["dropdown"]
                        shares_entry = sell_modal.user_data["shares_entry"]
                        selected_stock = dropdown.selected_option
                        try:
                            shares = int(shares_entry.get_text())
                        except ValueError:
                            shares = 0
                        # Verify sufficient shares exist in portfolio
                        if selected_stock not in portfolio or portfolio[selected_stock] < shares or shares <= 0:
                            info_label.set_text("Insufficient shares to sell.")
                        else:
                            price = get_stock_price(selected_stock)
                            print(f"Selling: {selected_stock}, Shares: {shares}, Price: {price}")
                            try:
                                sell_stock(selected_stock, shares, price)
                                amount_money += price * shares
                                portfolio[selected_stock] -= shares
                                if portfolio[selected_stock] <= 0:
                                    del portfolio[selected_stock]
                                info_label.set_text(f"Sold {shares} of {selected_stock} at ${price} each.")
                            except Exception as e:
                                print(f"Error in sell_stock: {e}")
                                info_label.set_text("Error: Could not complete sale.")
                        sell_modal.kill()
                        sell_modal = None
                        update_total_stocks_label()

        manager.process_events(event)
    manager.update(time_delta)

    if game_state == "game":
        info_label.set_text(f"Player: {player_name} | Money: ${amount_money} | Days left: {days}")
        update_total_stocks_label()

    window_surface.fill(pygame.Color('#000000'))
    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
sys.exit()
