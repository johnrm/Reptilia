# Repilia ATM 
## Index
* [Live site](#live-site)
* [Reptilia ATM](#reptilia-atm)
* [Program Features](#program-features)
* [Flowchart](#flowchart)
* [Functional Testing](#functional-testing)
* [Bugs](#bugs)
* [Technologies used and Deployment](#technologies-used-and-deployment)
* [Credits and APIs](#credits-and-apis)


## Live Site
https://reptilia-05304502b20b.herokuapp.com/  


Google Sheets...
https://docs.google.com/spreadsheets/d/1pJF4NkcCANY2xROzc-1MtM-QDEhFqRVP0ZvNSLMGAZI/edit#gid=1194371383

([Back to top](#index))  


## Reptilia ATM
Reptilia ATM is and ATM simulator.  
It provides a set of features typical on a highstreet bank ATM...  
1. Check Balance  
2. Withdraw Cash  
3. Lodge Cheque  
4. Print Statement  
5. Change PIN  
  
([Back to top](#index))  


## Program features
### Attract screen
![alt Screenshot of Attract screen](readme_images/Attract.jpg)

This is typical of any ATM, machine is waiting for a card.  
This is a simulator and we do not have cards, so the attract screen waits for a valid card number to be entered.  
Once this is entered, the card is authenticated with PIN.  
Validation is in place checking that the input card number and PIN are numeric and the correct length.  

The machine has 2 internal counters or accounts.  
The first is the Cash account which keeps check of the cash remaingin in the machine. If this runs out then the machine can no longer dispense cash.  
The second account if for Cheque Lodgements. This account keeps track of any funds entered and adds this to the users account balance.  


### Machine Parameters
The machine has a number of parameters by way of constants which are set on program.
# Bank name
BANK_NAME = "Reptilia Bank"
# Currency
CURRENCY = "EUR"
# Max failed PIN on card
MAX_PIN_FAIL = 3
# Set display width
DISPLAY_WIDTH = 30
# Bank Account (Account for the ATM machine)
CASH_AC = "9999"
# Bank Account (Account for the ATM machine)
CHEQUE_AC = "9998"
# Transaction limit
TRANSACTION_LIMIT = 300


### Menu/Navigation
![alt Screenshot of Menu](readme_images/Menu.jpg)

The Menu sits at the core of the program.
From here the user selects the function that they want to use.


### Balance
![alt Screenshot of Balance](readme_images/Balance.jpg)

The user can view their balance on thie screen.
The Balance is displayed for a few seconds, then returns to the Menu.


### Withdraw Cash
![alt Screenshot of Withdraw](readme_images/Withdraw.jpg)

The user can 'withdraw cash' here.  
Validation checks that the users account has enough funds.  
The ATM is also checked to se that it has cash enough to fulfil the transaction.  
A transaction limit is set in the code by way of a constant.  


### Lodge Cheque
![alt Screenshot of Lodge](readme_images/Lodge.jpg)

The user can 'lodge cheques' here.  
Validation checks only that the value is below a transaction limit then adds this amount ot the users account, and to the machine cheque account.  
The transaction limit is set in the code by way of a constant  


### Print Statement
![alt Screenshot of Statement](readme_images/Statement.jpg)

The user can 'Print a statement' here.  
This displays a list of transactions for the account and shows the balance on the account.  
The balance stays on screen for a few seconds, then rolls back back to the menu.  


### Change PIN
![alt Screenshot of Change PIN](readme_images/Change_PIN.jpg)

The user can change the PIN on their card here.  
The entered PIN is requested and verified by requesting a second time, which is checxked agaonst the first PIN entered.  
  
([Back to top](#index))  


## Flowchart
The flowchart details the core function of the program.  
![Flowchart of program](readme_images/atm_flowchart.jpg)  
  
([Back to top](#index))  


## Functional Testing

Testing was performed to ensure all featurs on the respective pages work as designed. This was done by seelecting the appropriate option.

| Menu Option        |  
| ------------------ |  
| 1. Balance         |  
| 2. Withdraw Cash   |  
| 3. Lodge Cheque    |  
| 4. Print Statement |  
| 5. Change PIN      |  
| 0. Exit            |  


### Card and PIN testing
Steps to test:
1. Open application in Heroku site at head of this document.
2. Key in valid card number and PIN

Expected:  
If card is non numeric, error is flagged and control comes back to input.  
If card is not 4 digits, error is flagged and control comes back to input.  
If card number is invalid, error is flagged and control comes back to input.  
  
If PIN is non-numeric, error is flagged and control comes back to input.  
If PIN is not 4 digits, error is flagged and control comes back to input.  
If PIN failed count is 3, user is notified to contact bank.  
If PIN fail reaches 3, user is notified that card is retained.  
If PIN fails but lower than 3, user is notified of remaining atempts.  
If PIN is successful, pin fail count is reset to 0, and transaction progresses.  

Actual:  
All behaviour is as expected  


### Balance  
1. Select Balance opton in Menu.  
2. Balance is displayed on screen for a number of seconds.  
3. Control returns to Menu  

Expected:  
Balance is displayed for a few seconds.  

Actual:  
All behaviour is as expected  


### Withdraw cash  

Actual:  
All behaviour is as expected  


### Lodge Cheque  

Actual:  
All behaviour is as expected  


### Test devices  
Program was also tested on...  
- Google Pixel 4  
- Dell Latitude Laptop  

Actual:  
All behaviour is as expected  


## Bugs  
Most bugs were from syntax errors along the way, and from trial/error as I learned the language on he way.  
Generally, once I found how a coding feature worked and tested, I figured out how to implement it.  
  
Not a bug, but there are delays with read/writ from Google sheets.  
This introduces small delays at times but is outside our control.

Typeahead is possible into keyboard buffer, but not advised. It is best to wait for the outcome of any input.  

([Back to top](#index))


## Technologies used and Deployment  
Site code sits in this Github repository.  
The development IDE used is Gitpod.  
Code commits are pushed to Github as the code develops with brief relevant comments.  
Deployment is on Heroku using standard Heroku deployment processes.  
  
([Back to top](#index))  


## Credits and APIs  
os - This is used to clear the display when repainting the screen.  
time - Used for sleep feature to pause display for a period.  
getpass - This is used to hide PIN inputs.  
gspread - Enables manipulation of Google Sheets to store all transactional data.  
datetime - To generate timestamps on transactions and activities.  
google.oauth2.service_account - To import Google credentials for access to gspread(Google Sheets)  
  
([Back to top](#index))  