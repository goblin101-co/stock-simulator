import time
import os

# Function to clear the output screen
def clear_screen():
    os.system('clear')  # For Windows, replace 'clear' with 'cls'

# Function to display text letter by letter
def display_letter_by_letter(text):
    for letter in text:
        print(letter, end='', flush=True)
        time.sleep(0.05)  # Adjust this delay (in seconds) to control the speed
    print()

# Example usage
# clear_screen()  # Clear the screen
# text_to_display = "Starting program..."
# display_letter_by_letter(text_to_display)
