import time
import os

# Function to clear the output screen
def clear_screen():
    os.system('clear')  # For Windows, replace 'clear' with 'cls'

# Function to display text letter by letter
def display_letter_by_letter(text):
    displayed_text = ''
    for letter in text:
        displayed_text += letter
        print(displayed_text, end='', flush=True)
        time.sleep(0.05)  # Adjust this delay (in seconds) to control the speed
    print()
    return displayed_text

# Example usage
clear_screen()  # Clear the screen

# Get user input
user_input = input("Enter text: ")

clear_screen()  # Clear the screen

# Display user input letter by letter
final_display = display_letter_by_letter(user_input)