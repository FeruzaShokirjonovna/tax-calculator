Wunder eTax is a tax refund calculator app serves as a convenient and secure solution for individuals seeking a hassle-free way to estimate their tax refunds without the burden of intricate tax language. The combination of user-friendly design, straightforward questions, and robust security measures ensures that users can confidently and easily navigate the tax estimation process.

[View live website here](https://tax-refund-calculator-6ba07d15fa62.herokuapp.com/)

# Table of Content

* [**Project**](<#project>)
    * [Site Users Goal](<#site-users-goal>)
    * [User Stories](<#user-stories>)
    * [Site Owners Goal](<#site-owners-goal>)

* [**User Experience (UX)**](<#user-experience-ux>)
    * [Site Structure](<#site-structure>)
    * [Flow chart](<#flow-chart>)
    * [Data Model](<#data-model>)
    * [Design Choices](<#design-choices>)

* [**Features**](<#features>)

* [**Features Left To Implement**](<#features-left-to-implement>)

* [**Technologies Used**](<#technologies-used>)
    * [Languages](<#languages>)
    * [Frameworks, Librarys & Software](<#frameworks-libraries--software>)
    * [Python Packages](<#python-packages>)

* [**Testing**](<#testing>)
  * [Code Validation](<#code-validation>)
  * [Additional Testing](<#additional-testing>)
  * [Known Bugs](<#known-bugs>)
* [Deployment](<#deployment>)
* [Credits](<#credits>)
* [Acknowledgements](<#acknowledgements>)

# **Project**

## Site Users Goal

## Site Owners Goal

[Back to top](<#table-of-content>)

# **User Experience (UX)**

For this project I didn't make a wireframe in [Balsamiq](https://balsamiq.com/) as in the earlier projects. The reason is the 'Wunder eTax' application will have a command line interface which means that there will not be room for that many creative design choices. Instead I decided to create a logic [Flow Chart](<#flow-chart>) to get a broad understanding of the application flow.

## Flow chart
The flow chart for this application was made with the online service [Lucid App](https://lucid.app/). I tried to keep in on a quite general level but with enough details to get a good understanding of how everything in the application is connected. The flow chart made it more easy when going into the coding phase.

<details><summary><b>Flow Chart</b></summary>

![Flow Chart]()
</details><br/>

[Back to top](<#table-of-content>)

## Site Structure

The 'Wunder eTax' is a terminal based application that is being presented in a one page website. When the application starts the user will be presented with a short welcome message and a menu with 2 options. The menu consists of the following choices: *Calculate Tax Refund*, *Get Help from an independent tax advisor*. Read more about the choices in the [Features](<#features>) section.

In the top of the page there is also a 'Run Program' button that the user can use to reload the application if needed.

## Data Model
To store all data in the application I made a choice to use [Google Sheets](https://www.google.co.uk/sheets/about/). All data in the application provided by the user is being sent and retrieved from the Google Sheet.

* Name of workbook: *tax-calculator*
* Name of worksheet: *sheet*

<details><summary><b>Google Sheet</b></summary>

![Google Sheet]()
</details><br/>

The worksheet holds 11 columns with information such as: *name*, *full name*, *tax class*, *yearly income*, *kindergeld(Childcare benefits)*, *elterngeld(parental benefits)*, *pension tax*, *health insurace tax*, *car insurace tax* that is being controlled from the application via Python.

[Back to top](<#table-of-content>)

## Design Choices

* ### Color Scheme
'Wunder eTax' is a terminal based application which means that there aren't that many visual design choices. I have used black and white colors.

 ### Typography
No specific typography is being used in the application. The font is just the standard font that is being used in the terminal.

[Back to top](<#table-of-content>)

# **Features**
When the application starts it calls the *main function* which   *prints the welcome message*. As stated in the [Site Structure](<#site-structure>) area the application consists of 2 different areas (functions) : *Calculate Tax Refund*, *Get Help from an independent tax advisor*. The features are being explained more in detail in the [Existing Features](<#existing-features>) area below.

## **Existing Features**

### Main Menu
The Main Menu is quite straight forward and consists of 2 choices. See each choice being explained below.

<details><summary><b>Main Menu</b></summary>

![Main Menu](assets/images/welcome_message.png)
</details><br/>

### Calculate Tax Refund (Option 1)
Users can choose the option to calculate their tax refund independently. The process involves providing information about income and taxes paid. The calculator considers various factors such as yearly income, Elterngeld, Kindergeld, pension tax, health insurance tax, and car insurance tax to estimate the potential tax refund. Users are prompted with easy-to-understand questions to gather the necessary details.

<details><summary><b>Yearly Tax input</b></summary>

![Yearly Tax input](assets/images/yearly_tax_input.png)
</details><br/>

<details><summary><b>Tax Class input</b></summary>

Before asking to enter tax class, users are informed the 6 types of tax classes and noticed the importance of selecting the tax class as it may affect the overall tax liability.

![Tax Class input](assets/images/tax_class_input.png)
</details><br/>
<details><summary><b>Invalid tax class message</b></summary>

![Invalid tax class message](assets/images/invalid_tax_class_alert_message.png)
</details><br/>

<details><summary><b>Yearly Income input</b></summary>

![Yearly Income input](assets/images/yearly_income_input.png)
</details><br/>

<details><summary><b>Elterngeld(parental financial benefits) and Kindergeld(childcare financial benefits) input</b></summary>

Before the user is asked to input, the app gives detailed information.

![Elterngeld(parental financial benefits) and Kindergeld(childcare financial benefits) input](assets/images/parental_and_childcare_financial_benefits_input.png)
</details><br/>

<details><summary><b>Tax for pension input</b></summary>

![Tax for pension input](assets/images/pension_tax_input.png)
</details><br/>
<details><summary><b>Tax for health insurance input</b></summary>

![Tax for health insurance input](assets/images/health_insurance_input.png)
</details><br/>
<details><summary><b>Tax for car insurance input</b></summary>

![Tax for car insurance input](assets/images/car_insurance_input.png)
</details><br/>
<details><summary><b>Tax return calculation display</b></summary>

![Tax return calculation display](assets/images/tax_return_calculation_display.png)
</details><br/>


# Technologies Used

## Languages

* [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) - Provides the functionality for the application.

## Frameworks, Libraries & Software

* [Google Sheets](https://www.google.co.uk/sheets/about/) - Used to host the application data.
* [Github](https://github.com/) - Used to host and edit the website.
* [Gitpod](https://www.gitpod.io) - Used to push changes to the GitHub repository.
* [Heroku](https://en.wikipedia.org/wiki/Heroku) - A cloud platform that the application is deployed to.
* [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/) - Used to test performance of site.
* [Responsive Design Checker](https://www.responsivedesignchecker.com/) - Used for responsiveness check.
* [Wave Web Accessibility Evaluation Tool](https://wave.webaim.org/) - Used to validate the sites accessibility.

## Python Packages
* [GSpread](https://pypi.org/project/gspread/) - A Python API for Google Sheets that makes it possible to transfer data between the application and the Google Sheet.

[Back to top](<#table-of-content>)
[Back to top](<#table-of-content>)
[Back to top](<#table-of-content>)