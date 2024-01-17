# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('tax-calculator')

class User:
    def __init__(self, name, full_name, username):
        self.name = name
        self.full_name = full_name
        self.username = username


def update_google_sheet(name, full_name, login):
    """
    Get user name, full name
    """
    worksheet = spreadsheet.sheet1

    # Append data to the sheet
    worksheet.append_row([name, full_name, login])

def main():
    print("Welcome to the German Tax Return Calculator CLI")

    # Get user input for personal details
    name = input("Enter your name: ")
    full_name = input("Enter your full name: ")
    login = input("Enter your login: ")

if __name__ == "__main__":
    main()
