import os
import time
import getpass
import gspread
import datetime
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('atm_creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ATM')

#System constants
#Bank name
BANK_NAME = "Reptilia Bank"
#Currency
CURRENCY = "EUR"
#Max failed PIN on card
MAX_PIN_FAIL = 3
#Set display width
DISPLAY_WIDTH = 30
#Bank Account (Account for the ATM machine)
BANK_AC = "9999"
#Transaction limit
TRANSACTION_LIMIT = 300

def atm_log(action, amount):
    time='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    data=[time,action,amount]
    print("Updating log...\n")
    log = SHEET.worksheet('atm_log')
    log.append_row(data)
    print("Log updated successfully\n")

def validate_number(numbers,length):
    """
    Check 'numbers' is numeric, correct length, reporting if incorrect
    """
    try:
        [int(number) for number in numbers]
        if len(numbers) != length:
            raise Exception
        return True
    except ValueError:
        print("Non-numeric entry!")
        return False
    except Exception:
        print(f"{len(numbers)} digits entered, {length} expected!")
        return False

def return_card():
    """
    Return card to user
    """
    screen_header("ATM")
    print("    Please take your card")
    print("      Have a nice day!")
    time.sleep(3)

def pin_fail(card):
    """
    Do this when PIN is entered incorrectly
    """
    input('PIN fail')
  
def get_card_detail(card):
    """
    Get details for the inserted Card
    Tell calling function if card is valid/invalid
    """
    cardsheet = SHEET.worksheet("cards")
    cardlist = cardsheet.col_values(1)
    try:
        rownum = cardlist.index(card) + 1
    except ValueError:
        return "invalid", 0, 0, 0
    row = cardsheet.row_values(rownum)
    pin_no = row[1]
    pin_count = row[2]
    account = row[3]
    return "valid", pin_no, pin_count, account

def get_account_detail(account):
    """
    Get and return account details
    """
    accountsheet = SHEET.worksheet("accounts")
    accountlist = accountsheet.col_values(1)
    try:
        rownum = accountlist.index(account) + 1
    except ValueError:
        return "invalid", 0
    row = accountsheet.row_values(rownum)
    time.sleep(3)
    balance = row[4]
    return "valid", balance 

def put_card_detail(card,pin_no,pin_count):
    """
    Update details for the inserted Card
    (pin_no and pin_count only)
    """
    cardsheet = SHEET.worksheet("cards")
    cardlist = cardsheet.col_values(1)
    try:
        rownum = cardlist.index(card) + 1
    except ValueError:
        return
    row = cardsheet.row_values(rownum)
    cardsheet.update([[pin_no, pin_count]], f'B{rownum}:C{rownum}')
    
def card_input():
    """
    Input Card and PIN from user
    Call validation and check for PIN count
    """
    card = input("Insert card (or enter card ID): ")
    if validate_number(card, 4):
        return card
    else:
        return False

def pin_input(pin_no):
    """
    Get pin from user
    """
    user_pin=getpass.getpass('Enter PIN (4 digits): ')
    if validate_number(user_pin, 4):
        if (user_pin != pin_no):
            return False
        else:
            return True
    else:
        return False
   
def screen_header(function):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANK_NAME.center(DISPLAY_WIDTH))
    print ("-" * DISPLAY_WIDTH)
    print(function.center(DISPLAY_WIDTH))
    print ("-" * DISPLAY_WIDTH)
    print()    

def menu(account):
    """
    Menu of user options 
    """
    while True:
        screen_header("ATM Options")
        print("1> Check Balance")
        print("2> Withdraw cash")
        print("3> Lodgement")
        print("4> Print Statement")
        print("5> Change PIN")
        print("0 or <Enter> Cancel\n")

        #Menu selection
        choice=input("Select: ")

        if choice=="1":
            #Account Balance
            screen_header("Account balance")
            verify, balance = get_account_detail(account)
            print(f'Current balance: {CURRENCY}{balance}'.center(DISPLAY_WIDTH))
            time.sleep(3)

        elif choice=="2":
            #Cash Withdrawal
            screen_header("Withdraw cash")
            verify, bank_bal = get_account_detail(BANK_AC)
            verify, acc_balance = get_account_detail(account)
            print(f"Transaction limit {CURRENCY}{TRANSACTION_LIMIT}")
            withdrawal = input("Withdrawal amount? ")
            #validate(amount)
            print(f'Current balance: {CURRENCY}{acc_balance}')
            bank_bal = int(bank_bal)
            acc_balance = int(acc_balance)
            withdrawal = int(withdrawal)
            new_balance=acc_balance-withdrawal
            print(f'New balance    : {CURRENCY}'+ str(new_balance))         
            time.sleep(3)

        elif choice=="3":
            print("\nLodgement unimplemented")
            time.sleep(1)

        elif choice=="4":
            print("\nPrint Statement unimplemented")
            time.sleep(1)

        elif choice=="5":
            print("\nChange PIN unimplemented")
            time.sleep(1)

        elif (choice=="0" or choice==""):
            print("\nCancel")
            time.sleep(1)
            break

def test_splash():
    screen_header("ATM simulator")
    print('For testing purposes...')
    print()    
    print('Sample card: 2234')
    print('Sample PIN: 3234')
    print()    
    input("Press <Enter> to continue")    


def main():
    """
    Main routine
    """
    while True:
        atm_log('Start', 0)
        screen_header("ATM")

        card = card_input()
        verify, pin_no, pin_count, account = get_card_detail(card)      

        #Notify user of invalid card and quit loop
        if verify == "invalid":
            print("Invalid card - please contact Bank")
            return_card()
            continue

        #Notify user of card and PIN issues
        if (int(pin_count) == MAX_PIN_FAIL):
            print("Card error - please contact Bank")
            time.sleep(3)
            continue
        elif (int(pin_count) > 0):
            print(f"{MAX_PIN_FAIL - int(pin_count)} PIN attempt{'s' if (MAX_PIN_FAIL - int(pin_count) > 1) else ''} left")

        #Increment fail count if incorrect PIN, reset if PIN is correct, then continue to Menu
        while True:
            pin = pin_input(pin_no)
            if not pin:
                #If PIN is incorrect
                pin_count = str(int(pin_count) + 1)
                put_card_detail(card, pin_no, pin_count)
                if pin_count == 3:
                    #Card retained
                    print("Card retained - please contact Bank")
                    time.sleep(3)
                    break
                pin_fail(card)
                break
            else:
                #If PIN is correct, reset fail count on card
                put_card_detail(card, pin_no, 0)
                menu(account)
                return_card()
                break

#test_splash()
main()