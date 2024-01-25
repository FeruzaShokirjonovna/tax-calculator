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
    def __init__(self, name, full_name, tax_class, yearly_income, elterngeld, kindergeld,
                 pension_tax, health_insurance_tax, car_insurance_tax, tax_id, year):
        self.name = name
        self.full_name = full_name
        self.tax_class = tax_class
        self.yearly_income = yearly_income
        self.elterngeld = elterngeld
        self.kindergeld = kindergeld
        self.pension_tax = pension_tax
        self.health_insurance_tax = health_insurance_tax
        self.car_insurance_tax = car_insurance_tax
        self.tax_id = tax_id
        self.year = year

def update_google_sheet(user):
    """
    Updates sheet adding details
    """
    worksheet = SHEET.get_worksheet(0)
    
    # Append data to the sheet
    worksheet.append_row([user.name, user.full_name, user.tax_class, user.yearly_income, user.elterngeld,
                          user.kindergeld, user.pension_tax, user.health_insurance_tax, user.car_insurance_tax, user.tax_id, user.year])

    # Calculate and display refund
    total_tax_calculated = calculate_total_tax(user.yearly_income, user.elterngeld, user.kindergeld,
                                               user.pension_tax, user.health_insurance_tax, user.car_insurance_tax,
                                               user.tax_class)
    overall_paid_tax = get_positive_float_input("Enter the overall tax you paid in this year: \n")  # User input for overall paid tax
    
    refund = float(overall_paid_tax) - float(total_tax_calculated)

    print("\nUser Details:")
    print(f"Name: {user.name}")
    print(f"Full Name: {user.full_name}")
    print(f"Tax Class: {user.tax_class}")
    
    print("\nUser Entries:")
    print(f"Yearly Income: {user.yearly_income}")
    print(f"Elterngeld: {user.elterngeld}")
    print(f"Kindergeld: {user.kindergeld}")
    print(f"Pension Tax: {user.pension_tax}")
    print(f"Health Insurance Tax: {user.health_insurance_tax}")
    print(f"Car Insurance Tax: {user.car_insurance_tax}")
    print(f"Year: {user.year}")
    print(f"Tax ID: {user.tax_id}")
    print("\nCalculated Refund:")
    print(f"Total Tax Calculated: {total_tax_calculated:.2f} Euros")
    print(f"Overall Paid Tax: {overall_paid_tax:.2f} Euros")
    print(f"Refund: {refund:.2f} Euros")

def get_personal_details():
    """
    Get user input for personal details
    """
    while True:
        name = input("\nEnter your name: \n")
        if not name.isalpha():
            print("Invalid input. Please enter a valid name with only alphabetic characters.")
            continue

        full_name = input("Enter your full name: \n")
        if not full_name.replace(" ", "").isalpha():
            print("Invalid input. Please enter a valid full name with only alphabetic characters.")
            continue

        year = 0  # Initialize 'year' variable

        try:
            # Get user input for the tax year
            print("Enter the year you want to calculate Tax Refund.")
            print("You can calculate tax refund for the year between 2020-2023 years")

            year = year_validation("\nEnter the year you want to calculate income tax here: \n")

        except ValueError:
            print("Invalid input. Please enter a valid year.")

        tax_class = get_tax_class()
        income_details = get_income_details()  # Call the function to gather income details

        return name, full_name, tax_class, *income_details, year  # Unpack income details


def get_tax_class():
    """
    Get user input, for which tax class the user in
    """
    while True:
        try:
            print("\nIn the German income tax system, there are six tax classes, known as 'Steuerklasse'. ")
            print("Each tax class is associated with specific circumstances and may affect the overall tax liability.")
            print("Here is a brief overview:")
            print("\n1.Single individuals and those who are divorced or widowed.")
            print("2.Single parents (personally raising at least one child and eligible for child benefits(Kindergeld)).")
            print("3.Married individuals whose spouse is in Tax Class 5.")
            print("4.Married individuals where both partners earn income.")
            print("5.Married individuals whose spouse is in Tax Class 3.")
            print("6.Applies when an individual has more than one job simultaneously.")
            tax_class = int(input("\nEnter your tax class (1-6): \n"))
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
        yearly_income = get_positive_float_input("Enter your yearly income: \n")
        print("If you have children, enter total Elterngeld and Kindergeld.")
        print("\nElterngeld is a financial benefit provided by the German government to support parents during the time they take off work to care for their newborn or adopted child. ")
        print("Kindergeld is intended to support families in covering the basic needs of their children, such as food, clothing, and education.")
        print("\nIf you do not get these, please enter 0 for each.")
        elterngeld = get_positive_float_input("Enter your Elterngeld: \n")
        kindergeld = get_positive_float_input("Enter your Kindergeld: \n")
        pension_tax = get_positive_float_input("Enter taxes for pension: \n")
        health_insurance_tax = get_positive_float_input("Enter taxes for health insurance: \n")
        print("If you pay for car insurance, enter. If not enter 0.")
        car_insurance_tax = get_positive_float_input("Enter taxes for car insurance: \n")
        
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return 0, 0, 0, 0, 0, 0  # Return default values in case of an error

    return (
        float(yearly_income),
        float(elterngeld),
        float(kindergeld),
        float(pension_tax),
        float(health_insurance_tax),
        float(car_insurance_tax)
    )
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
    total_income -= float(pension_tax) + float(health_insurance_tax) + float(car_insurance_tax)
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

def calculate_tax_refund(overall_paid_tax, tax_class, yearly_income, elterngeld, kindergeld,
                         pension_tax, health_insurance_tax, car_insurance_tax):
    """
    Calculate tax refund, getting income details
    Display provided data and calculated data
    """
    income_details = (yearly_income, elterngeld, kindergeld, pension_tax, health_insurance_tax, car_insurance_tax)
    total_tax_calculated = calculate_total_tax(*income_details, tax_class)  
    refund = overall_paid_tax - total_tax_calculated
    print("\nCalulating Tax Refund...")
    print("\nUser Entries:")
    print(f"Tax Class: {tax_class}")
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
    print("\nThank you for using Wunder eTax!")

def get_tax_id():
    """
    Get user input for tax ID with validation
    """
    print("\nThe tax identification number , abbreviated tax ID, helps tax offices identify and manage taxpayers.")# User input for tax ID
    tax_id = input("Enter your tax ID: \n")
    while True:
        if tax_id.isnumeric() and int(tax_id) > 0 and len(tax_id) == 11:  # Assuming a tax ID is a numeric value with a specific length
            return tax_id
        else:
            print("Invalid tax ID. Please enter a numeric positive tax ID with a length of 11 digits.")

def main():
    print("Welcome to the Wunder eTax Return ")
    print("Answer our easy-to-understand question-answer process, or have your tax done by an independent tax advisor.")
    print("We are willing to assist you in estimating potential tax refunds quickly and accurately avoiding complicated tax jargon.")
    print("Your data is always transmitted in encrypted form to our servers and via ELSTER to the tax office.")

    print("\nChoose an option:")
    print("1. Calculate Tax Refund.")
    print("2. Get Help from an independent tax advisor, who will prepare and submit your tax return to tax office for you.")

    choice = input("\nEnter your choice (1 or 2): ")
    if choice == "1":
        overall_paid_tax = get_positive_float_input(f"Enter the overall tax you paid in this year: \n")  # User input for overall paid tax
        tax_class = get_tax_class()
        yearly_income, elterngeld, kindergeld, pension_tax, health_insurance_tax, car_insurance_tax = get_income_details()
        calculate_tax_refund(overall_paid_tax, tax_class, yearly_income, elterngeld, kindergeld,
                             pension_tax, health_insurance_tax, car_insurance_tax)
    elif choice == "2":
        user = get_personal_details()
        update_google_sheet(User(*user, get_tax_id()))   # send data to google sheets for admin
        print("\nYour data is successfully sent to our server!")
        
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
