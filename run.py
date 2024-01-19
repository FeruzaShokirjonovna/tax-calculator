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
    def __init__(self, name, full_name, login, year, tax_class, yearly_income, elterngeld, kindergeld,
                 pension_tax, health_insurance_tax, car_insurance_tax):
        self.name = name
        self.full_name = full_name
        self.login = login
        self.year = year
        self.tax_class = tax_class
        self.yearly_income = yearly_income
        self.elterngeld = elterngeld
        self.kindergeld = kindergeld
        self.pension_tax = pension_tax
        self.health_insurance_tax = health_insurance_tax
        self.car_insurance_tax = car_insurance_tax


def is_valid_login(login):
    """
    Validation for login
    Checks that user entered login with letters, numbers and uppercase
    """
    return all(c.isalnum() or c.isupper() for c in login) and any(c.isupper() for c in login)


def update_google_sheet(name, full_name, login, year, tax_class, yearly_income, elterngeld, kindergeld,
                         pension_tax, health_insurance_tax, car_insurance_tax):
    """
    Updates sheet adding details
    """
    worksheet = SHEET.get_worksheet(0)  #
    # Check if login already exists in the sheet
    login_column = worksheet.col_values(3)  # Assuming login is in the third column
    if login in login_column:
        print("Login already exists. Please choose a different login.")
        return

    # Append data to the sheet
    worksheet.append_row([name, full_name, login, year, tax_class, yearly_income, elterngeld, kindergeld,
                          pension_tax, health_insurance_tax, car_insurance_tax])
    #Calculate and display refund
    total_tax_calculated = calculate_total_tax(yearly_income, elterngeld, kindergeld,
                                               pension_tax, health_insurance_tax, car_insurance_tax, tax_class)
    overall_paid_tax = float(input("Enter the overall paid tax: "))  # User input for overall paid tax
    refund = overall_paid_tax - total_tax_calculated
    print(f"Your calculated refund is: {refund:.2f} Euros")



def get_personal_details():
    """
    Get user input for personal details
    """
    print("Welcome to the German Tax Return Calculator CLI")
    name = input("Enter your name: ")
    full_name = input("Enter your full name: ")
    while True:
        print("Enter your login, which must include numbers and uppercase letters.")
        login = input("Enter your login here: ")

        if is_valid_login(login):
            new_user = User(name, full_name, login)
            print(f"Sign-up successful! Welcome, {name} {full_name}")
            break
        else:
            print("Invalid login. Please ensure it includes numbers and uppercase letters.")

    while True:
        try:
            # Get user input for the tax year
            print("Enter the year you want to calculate Tax Refund")
            print("For example: 2022")
            year = int(input("Enter the tax year here: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid year.")

    tax_class = get_tax_class()
    income_details = get_income_details()  # Call the function to gather income details

    return name, full_name, login, year, tax_class, *income_details  # Unpack income details


def get_tax_class():
    """
    Get user input, for which tax class the user in
    """
    while True:
        try:
            tax_class = int(input("Enter your tax class (1-6): "))
            if 1 <= tax_class <= 6:
                return tax_class
            else:
                print("Invalid tax class. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_income_details():
    """
    Get user input for income types
    Income for the year, taxes he payed
    """
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
        return 0, 0, 0, 0, 0, 0  # Return default values in case of an error

    return yearly_income, elterngeld, kindergeld, pension_tax, health_insurance_tax, car_insurance_tax

def calculate_income_tax(yearly_income, elterngeld, kindergeld, pension_tax, health_insurance_tax, car_insurance_tax,
                         tax_class):
    """
    Calculate yearly income
    """
    # fictional tax rates
    tax_rates = {
        1: 0.1,
        2: 0.15,
        3: 0.25,
        4: 0.35,
        5: 0.45,
        6: 0.5
    }
    # Calculate total income considering Elterngeld and Kindergeld
    total_income = yearly_income + elterngeld + kindergeld
    # specific taxes like pension, health insurance, car insurance
    total_income -= pension_tax + health_insurance_tax + car_insurance_tax
    tax_rate = tax_rates.get(tax_class, 0.1)
    tax = total_income * tax_rate
    return tax


def calculate_total_tax(yearly_income, elterngeld, kindergeld, pension_tax, health_insurance_tax, car_insurance_tax,
                        tax_class):
    """
    Calculate total tax
    """
    income_tax = calculate_income_tax(yearly_income, elterngeld, kindergeld,
                                      pension_tax, health_insurance_tax, car_insurance_tax, tax_class)
    return income_tax


def main():
    name, full_name, login, year, tax_class, yearly_income, elterngeld, kindergeld, \
    pension_tax, health_insurance_tax, car_insurance_tax = get_personal_details()

    update_google_sheet(name, full_name, login, year, tax_class, yearly_income, elterngeld, kindergeld,
                         pension_tax, health_insurance_tax, car_insurance_tax)



if __name__ == "__main__":
    main()
