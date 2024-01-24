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
    def __init__(self, name, full_name, year, tax_class, yearly_income, elterngeld, kindergeld,
                 pension_tax, health_insurance_tax, car_insurance_tax):
        self.name = name
        self.full_name = full_name
        self.year = year
        self.tax_class = tax_class
        self.yearly_income = yearly_income
        self.elterngeld = elterngeld
        self.kindergeld = kindergeld
        self.pension_tax = pension_tax
        self.health_insurance_tax = health_insurance_tax
        self.car_insurance_tax = car_insurance_tax



def update_google_sheet(name, full_name, year, tax_class, yearly_income, elterngeld, kindergeld,
                         pension_tax, health_insurance_tax, car_insurance_tax):
    """
    Updates sheet adding details
    """
    worksheet = SHEET.get_worksheet(0)  #
    # Check if login already exists in the sheet
    
    # Append data to the sheet
    worksheet.append_row([name, full_name, year, tax_class, yearly_income, elterngeld, kindergeld,
                          pension_tax, health_insurance_tax, car_insurance_tax])
    #Calculate and display refund
    total_tax_calculated = calculate_total_tax(yearly_income, elterngeld, kindergeld,
                                               pension_tax, health_insurance_tax, car_insurance_tax, tax_class)
    
    refund = overall_paid_tax - total_tax_calculated
    
    print("\nUser Details:")
    print(f"Name: {name}")
    print(f"Full Name: {full_name}")
    print(f"Year: {year}")
    print(f"Tax Class: {tax_class}")
    print("\nUser Entries:")
    print(f"Yearly Income: {yearly_income}")
    print(f"Elterngeld: {elterngeld}")
    print(f"Kindergeld: {kindergeld}")
    print(f"Pension Tax: {pension_tax}")
    print(f"Health Insurance Tax: {health_insurance_tax}")
    print(f"Car Insurance Tax: {car_insurance_tax}")
    print("\nCalculated Refund:")
    print(f"Total Tax Calculated: {total_tax_calculated:.2f} Euros")
    print(f"Overall Paid Tax: {overall_paid_tax:.2f} Euros")
    print(f"Refund: {refund:.2f} Euros")


def get_personal_details():
    """
    Get user input for personal details
    """
    name = input("Enter your name: \n")
    full_name = input("Enter your full name: \n")
    year = 0  # Initialize 'year' variable
    
    try:
        # Get user input for the tax year
        print("Enter the year you want to calculate Tax Refund. For example: 2022")
        print("You can calculate tax refund for the year between 2020-2023 years")
            
        year = year_validation("Enter the year you want to calculate income tax here: \n")
            
    except ValueError:
        print("Invalid input. Please enter a valid year.")

    tax_class = get_tax_class()
    income_details = get_income_details()  # Call the function to gather income details

    return name, full_name, year, tax_class, *income_details  # Unpack income details


def get_tax_class():
    """
    Get user input, for which tax class the user in
    """
    while True:
        try:
            tax_class = int(input("Enter your tax class (1-6): \n"))
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
        yearly_income = get_positive_float_input("Enter your total income: \n")
        print("If you have children under years old, enter total Elterngeld and Kindergeld.")
        print("If you do not get these, please enter 0 for each.)")
        elterngeld = get_positive_float_input("Enter your Elterngeld: \n")
        kindergeld = get_positive_float_input("Enter your Kindergeld: \n")
        pension_tax = get_positive_float_input("Enter taxes for pension: \n")
        health_insurance_tax = get_positive_float_input("Enter taxes for health insurance: \n")
        print("If you pay for car insurance, enter. If not enter 0.")
        car_insurance_tax = get_positive_float_input("Enter taxes for car insurance: \n")
        overall_paid_tax = float(input("Enter the overall tax you paid in {year} year: \n"))  # User input for overall paid tax
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return 0, 0, 0, 0, 0, 0  # Return default values in case of an error

    return yearly_income, elterngeld, kindergeld, pension_tax, health_insurance_tax, car_insurance_tax

def get_positive_float_input(prompt):
    """
    Check input if it is positive and numeric
    If not display alert message
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a positive value.")
                continue
            return value
        except ValueError:
            print("Please enter a valid numeric value.")

def year_validation(prompt):
    """
    Check year input if it is not below 2020 and not above 2023 and numeric
    If not display an alert message
    """
    while True:
        try:
            value = int(input(prompt))
            if 2020 <= value <= 2023:
                return value
            else:
                print(f"The year you provided is {value}. Please enter a year between 2020 and 2023.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")


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
    print("Welcome to the German Tax Return Calculator")
    print("Answer our easy-to-understand question-answer process, or have your tax done by an independent tax advisor")
    print("This digital tool is designed to assist individuals in estimating potential tax refunds quickly and accurately avoiding complicated tax jargon")
    print("Your data is always transmitted in encrypted form to our servers and via ELSTER to the tax office.")

    print("Choose an option:")
    print("1. Calculate Tax Refund")
    print("2. Get Help from an independent tax advisor, who will prepare and submit your tax return for you")

    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        name, full_name, year, tax_class, yearly_income, elterngeld, kindergeld, \
        pension_tax, health_insurance_tax, car_insurance_tax = get_personal_details()

    elif choice == "2":
        name, full_name, year, tax_class, yearly_income, elterngeld, kindergeld, \
        pension_tax, health_insurance_tax, car_insurance_tax = get_personal_details()

        update_google_sheet(name, full_name, year, tax_class, yearly_income, elterngeld, kindergeld,
                         pension_tax, health_insurance_tax, car_insurance_tax)
    else:
        print("Invalid choice. Please enter 1 or 2.")
    
    update_google_sheet(name, full_name, year, tax_class, yearly_income, elterngeld, kindergeld,
                         pension_tax, health_insurance_tax, car_insurance_tax)

if __name__ == "__main__":
    main()
