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
    def __init__(self, name, full_name, login):
        self.name = name
        self.full_name = full_name
        self.login = login


def is_valid_login(login):
    """
    Validation for login
    Checks that user entered login with letters, numbers and uppercase
    """
    return all(c.isalnum() or c.isupper() for c in login) and any(c.isupper() for c in login)


def update_google_sheet(name, full_name, login):
    """
    Updates sheet adding details
    """
    worksheet = SHEET.get_worksheet(0)  #
    # Check if login already exists in the sheet
    login_column = worksheet.col_values(3)  # Assuming login is in the third column (adjust if needed)
    if login in login_column:
        print("Login already exists. Please choose a different login.")
        return

    # Append data to the sheet
    worksheet.append_row([name, full_name, login])
    print(f"Sign-up successful! Welcome, {name} {full_name}")


def main():
    print("Welcome to the German Tax Return Calculator CLI")
    # Get user input for personal details
    name = input("Enter your name: ")
    full_name = input("Enter your full name: ")
    while True:
        print("Enter your login, which must include numbers and uppercase letters.")
        login = input("Enter your login here: ")

        if is_valid_login(login):
            new_user = User(name, full_name, login)
            # Update Google Sheet if login is valid
            update_google_sheet(name, full_name, login)
            break
        else:
            print("Invalid login. Please ensure it includes numbers and uppercase letters.")

if __name__ == "__main__":
    main()
