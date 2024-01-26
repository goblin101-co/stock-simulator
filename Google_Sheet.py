import gspread
from oauth2client.service_account import ServiceAccountCredentials

def create_or_open_sheet(user_id):
    # Set up credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("File.json", scope)
    gc = gspread.authorize(credentials)

    # Try to open an existing sheet or create a new one
    try:
        sheet = gc.open(f"User_Sheet_{user_id}")
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = gc.create(f"User_Sheet_{user_id}")

    return sheet

if __name__ == "__main__":
    # Get user_id (could be a device username or any unique identifier)
    user_id = input("Enter your user ID: ")

    # Create or open the Google Sheet for the user
    user_sheet = create_or_open_sheet(user_id)

    # Do something with the user's sheet
    worksheet = user_sheet.sheet1
    worksheet.update_acell("A1", "Hello, User's Sheet!")

    print(f"Access the sheet for User {user_id} at: {user_sheet.url}")
