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


def update_google_sheet(name, full_name, login, yearly_income,elterngeld, kindergeld,
                          pension_tax, health_insurance_tax, car_insurance_tax, tax_class):
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
    worksheet.append_row([name, full_name, login, year, get_tax_class, yearly_income, Elterngeld, Kindergeld, pension_tax, health_insurance_tax, car_insurance_tax])
    print(f"Sign-up successful! Welcome, {name} {full_name}")

def get_personal_details():
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
            update_google_sheet(name, full_name, login, get_tax_class)
            break
        else:
            print("Invalid login. Please ensure it includes numbers and uppercase letters.")
     #Get user input for the tax year
    try:
        print("Enter the year you want to calculate Tax Refund")
        print("For example: 2022")
        year = int(input("Enter the tax year here: "))
    except ValueError:
        print("Invalid input. Please enter a valid year.")
        return
    
def get_tax_class():
    while True:
        try:
            tax_class = int(input("Enter your tax class (1-6): "))
            if 1 <= tax_class <= 6:
                return tax_class
            else:
                print("Invalid tax class. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def calculate_income_tax():
    """
    Calculate yearly income
    """
    #fictional tax rates
    tax_rates = {
        1: 0.1,
        2: 0.15,
        3: 0.25,
        4: 0.35,
        5: 0.45,
        6: 0.5
    }
    #Calculate total income considering Elterngeld and Kindergeld
    total_income = yearly_income + elterngeld + kindergeld
    #Deduct specific taxes like pension, health insurance, car insurance
    total_income -= pension_tax + health_insurance_tax + car_insurance_tax
    tax_rate = tax_rates.get(tax_class, 0.1)
    tax = total_income * tax_rate
    return tax

def calculate_solidarity_surcharge(income_tax):
    """
    Calculate the solidarity surcharge out of total income
    """

def calculate_total_tax():
    """
    Calculate total tax
    """
    income_tax = calculate_income_tax()
    total_tax = calculate_income_tax
    return total_tax


def main():
    get_personal_details()
    get_tax_class()
    try:
        yearly_income = float(input("Enter your total income: "))
        print("If you have children under years old, enter total Elterngeld and Kindergeld.")
        print("If you do not get these, please enter 0 for each.)")
        elterngeld = float(input("Enter your Elterngeld: "))
        kindergeld = float(input("Enter your Kindergeld: "))
        pension_tax = float(input("Enter taxes for pension: "))
        health_insurance_tax = float(input("Enter taxes for health insurance: "))
        print("If you pay for car insurance, enter. If not enter 0.")
        car_insurance_tax = float(input("Enter taxes for car insurance: "))

    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return

    #Calculate taxes
    total_tax = calculate_total_tax()


if __name__ == "__main__":
    main()
