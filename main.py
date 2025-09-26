import pygame
import pygame_gui
import random
import sys
import sqlite3
import dataset
import json
import stock_buy
from stock_buy import buy_stock, sell_stock, initialize_player, update_days

# Initialize pygame
pygame.init()
pygame.display.set_caption('Stock Simulator Game')
WINDOW_SIZE = (800, 600)
window_surface = pygame.display.set_mode(WINDOW_SIZE)
manager = pygame_gui.UIManager(WINDOW_SIZE)
clock = pygame.time.Clock()

# Connect to existing database
db = dataset.connect('sqlite:///stock_portfolio.db')
player_table = db['Player']
portfolio_table = db['Stock_Portfolio']

# Global state
player_name = ""
days = 0
amount_money = 100000

# Stock setup
stock_options = ["APPLE", "GOOGLE", "NVIDIA"]
stock_options2 = ["NINTENDO", "TESLA", "LOGITECH"]
stock_options3 = ["SAMSUNG", "MICROSOFT", "FACEBOOK"]
group1_price = group2_price = group3_price = 0
display_buy_options = []

# Game state
game_state = "login"
buy_modal = None
sell_modal = None

# UI Panels
login_panel = pygame_gui.elements.UIPanel(pygame.Rect((200, 150), (400, 300)), manager)
name_input = pygame_gui.elements.UITextEntryLine(pygame.Rect((150, 70), (200, 30)), manager, login_panel)
days_input = pygame_gui.elements.UITextEntryLine(pygame.Rect((150, 120), (200, 30)), manager, login_panel)
login_button = pygame_gui.elements.UIButton(pygame.Rect((150, 180), (100, 50)), "Start Game", manager, login_panel)

# Game panel
game_panel = pygame_gui.elements.UIPanel(pygame.Rect((0, 0), (800, 600)), manager, visible=False)
info_label = pygame_gui.elements.UILabel(pygame.Rect((10, 10), (400, 50)), "", manager, game_panel)
total_stocks_label = pygame_gui.elements.UILabel(pygame.Rect((600, 10), (190, 50)), "Total Stocks: 0", manager, game_panel)
stock_label = pygame_gui.elements.UITextBox("", pygame.Rect((10, 70), (780, 200)), manager, game_panel)

# Buttons
buy_button = pygame_gui.elements.UIButton(pygame.Rect((50, 500), (100, 50)), "Buy", manager, game_panel)
sell_button = pygame_gui.elements.UIButton(pygame.Rect((200, 500), (100, 50)), "Sell", manager, game_panel)
next_day_button = pygame_gui.elements.UIButton(pygame.Rect((350, 500), (150, 50)), "Next Day", manager, game_panel)

# Utility Functions
def update_stock_prices():
    global group1_price, group2_price, group3_price, display_buy_options
    group1_price = random.randint(100, 600)
    group2_price = random.randint(100, 600)
    group3_price = random.randint(100, 600)
    display_buy_options = stock_options + stock_options2 + stock_options3

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

def get_stock_price(stock):
    if stock in stock_options:
        return group1_price
    elif stock in stock_options2:
        return group2_price
    else:
        return group3_price

def update_total_stocks():
    total = sum(stock['shares'] for stock in stock_buy.stocks.values())
    total_stocks_label.set_text(f"Total Stocks: {total}")

def show_buy_modal():
    global buy_modal
    buy_modal = pygame_gui.elements.UIWindow(pygame.Rect((250, 200), (300, 200)), manager, window_display_title="Buy Stock")
    dropdown = pygame_gui.elements.UIDropDownMenu(display_buy_options, display_buy_options[0], pygame.Rect((120, 10), (150, 30)), manager, buy_modal)
    entry = pygame_gui.elements.UITextEntryLine(pygame.Rect((120, 60), (150, 30)), manager, buy_modal)
    confirm = pygame_gui.elements.UIButton(pygame.Rect((100, 120), (100, 40)), "Confirm", manager, buy_modal, object_id="#confirm_buy_button")
    buy_modal.user_data = {"dropdown": dropdown, "entry": entry}

def show_sell_modal():
    global sell_modal
    options = [s for s in stock_buy.stocks if stock_buy.stocks[s]['shares'] > 0]
    if not options:
        info_label.set_text("No stocks to sell.")
        return
    sell_modal = pygame_gui.elements.UIWindow(pygame.Rect((250, 200), (300, 200)), manager, window_display_title="Sell Stock")
    dropdown = pygame_gui.elements.UIDropDownMenu(options, options[0], pygame.Rect((120, 10), (150, 30)), manager, sell_modal)
    entry = pygame_gui.elements.UITextEntryLine(pygame.Rect((120, 60), (150, 30)), manager, sell_modal)
    confirm = pygame_gui.elements.UIButton(pygame.Rect((100, 120), (100, 40)), "Confirm", manager, sell_modal, object_id="#confirm_sell_button")
    sell_modal.user_data = {"dropdown": dropdown, "entry": entry}

# Main loop
while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == login_button:
                player_name = name_input.get_text().strip()
                try:
                    days = int(days_input.get_text().strip())
                except ValueError:
                    days = 10
                if not player_name:
                    continue
                initialize_player(player_name, days)
                login_panel.hide()
                game_panel.show()
                update_stock_prices()
                refresh_stock_display()

            elif event.ui_element == buy_button:
                show_buy_modal()

            elif event.ui_element == sell_button:
                show_sell_modal()

            elif event.ui_element == next_day_button:
                if days > 0:
                    days -= 1
                    update_days(player_name)
                    update_stock_prices()
                    refresh_stock_display()
                else:
                    info_label.set_text("No days left.")

            elif hasattr(event.ui_element, 'get_object_ids'):
                if '#confirm_buy_button' in event.ui_element.get_object_ids():
                    dropdown = buy_modal.user_data["dropdown"]
                    entry = buy_modal.user_data["entry"]
                    stock = dropdown.selected_option
                    try:
                        shares = int(entry.get_text())
                        price = get_stock_price(stock)
                        buy_stock(stock, shares, price)
                        info_label.set_text(f"Bought {shares} shares of {stock}.")
                    except:
                        info_label.set_text("Error during purchase.")
                    buy_modal.kill()
                    update_total_stocks()

                elif '#confirm_sell_button' in event.ui_element.get_object_ids():
                    dropdown = sell_modal.user_data["dropdown"]
                    entry = sell_modal.user_data["entry"]
                    stock = dropdown.selected_option
                    try:
                        shares = int(entry.get_text())
                        if shares <= stock_buy.stocks[stock]['shares']:
                            price = get_stock_price(stock)
                            sell_stock(stock, shares, price)
                            info_label.set_text(f"Sold {shares} shares of {stock}.")
                        else:
                            info_label.set_text("Not enough shares to sell.")
                    except:
                        info_label.set_text("Error during sale.")
                    sell_modal.kill()
                    update_total_stocks()

        manager.process_events(event)
    manager.update(time_delta)

    if game_panel.visible:
        info_label.set_text(f"Player: {player_name} | Money: ${amount_money} | Days left: {days}")
        update_total_stocks()

    window_surface.fill(pygame.Color('#000000'))
    manager.draw_ui(window_surface)
    pygame.display.update()



    # Not even far from being done yet!