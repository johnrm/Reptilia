import os
import time
import getpass
import gspread
import datetime
from google.oauth2.service_account import Credentials
from colorama import Fore, Back, Style

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ATM')

# System constants
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


def atm_log(action, amount):
    time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    data = [time,action,amount]
    log = SHEET.worksheet('atm_log')
    log.append_row(data)


def validate_number(numbers,length):
    """
    Check 'numbers' is numeric, correct length, reporting if incorrect
    """
    try:
        numbers.isnumeric()
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
    input(Fore.BLACK + Back.WHITE +'PIN fail')
    print(Style.RESET_ALL)
  

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


def get_account_detail(account):
    """
    Get and return account detail
    """
    accountsheet = SHEET.worksheet("accounts")
    accountlist = accountsheet.col_values(1)
    try:
        rownum = accountlist.index(account) + 1
    except ValueError:
        return "invalid", 0
    row = accountsheet.row_values(rownum)
    balance = row[4]
    return "valid", balance 


def put_account_detail(account, balance, time):
    """
    Update account balance
    """
    accountsheet = SHEET.worksheet("accounts")
    accountlist = accountsheet.col_values(1)
    try:
        rownum = accountlist.index(account) + 1
    except ValueError:
        return
    row = accountsheet.row_values(rownum)
    accountsheet.update([[balance, time]], f'E{rownum}:F{rownum}')
    

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
    user_pin = getpass.getpass('Enter PIN (4 digits): ')
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


def withdrawal(account):
    """
    Withdrawal transaction takes place here
    """
    atm_log("Withdrawal", account)
    screen_header("Withdrawal")
    
    # Find what funds are available to transact
    verify, cash_balance = get_account_detail(CASH_AC)
    cash_balance = int(cash_balance) # Amount in ATM
    verify, acc_balance = get_account_detail(account)
    acc_balance = int(acc_balance) # Amount in account

    # Notify if inadequate balance
    print(f'Available funds : {CURRENCY}{acc_balance}')
    if  (acc_balance <= 0):
        print('Inadequate funds, balance: ' + CURRENCY + str(acc_balance))
        time.sleep(3)
        return False

    # Notify trx limit
    print(f"Transaction limit {CURRENCY}{TRANSACTION_LIMIT}")

    # Input and validate transaction amount
    try:
        print(f'Whole amount, multiples of {CURRENCY}10 only')
        value = int(input("Transaction amount? ")) # Requested amount
        if (divmod(value,10)[1] != 0) :
            print('Multiples of 10 only')
            time.sleep(3)
            return False
    except ValueError:
        print("Non-numeric entry!")
        return False

    if (value > TRANSACTION_LIMIT):
        print('Exceeds transcation limit') # Transaction Limit exceeded
        time.sleep(3)
    elif  ((acc_balance - value) <= 0):
        print('Exceeds available funds') # Inadequate funds in account
        time.sleep(3)
    elif ((cash_balance - value) <= 0):
        print('ATM out of funds') # Inadaquete cash in ATM
        time.sleep(3)

    # Validate amounts
    new_cash_balance = cash_balance - value
    new_acc_balance = acc_balance - value
    print(f'New balance    : {CURRENCY}' + str(new_acc_balance))
    atm_log('Withdrawal', value)
    time_stamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    put_account_detail(account, new_acc_balance, time_stamp)
    put_account_detail(CASH_AC, new_cash_balance, time_stamp)


def menu(account):
    """
    Menu of user options 
    """
    while True:
        screen_header("ATM Options")
        print("1> Check Balance")
        print("2> Withdraw cash")
        print("3> Lodgement")
        print("4> !!new lodgement!!")
        print("5> Print Statement")
        print("6> Change PIN")
        print("-" * 18)
        print("0> Cancel\n")

        # Menu selection
        choice = input("Select: ")

        if choice == "1":
            # Account Balance
            atm_log('balance', account)
            screen_header("Account balance")
            verify, balance = get_account_detail(account)
            print(f'Current balance: {CURRENCY}{balance}'.center(DISPLAY_WIDTH))
            time.sleep(3)

        elif choice == "2":
            withdrawal(account)


        elif choice == "3":
            # Lodgement
            atm_log('lodgement', account)
            screen_header("Lodge Cheque")
            verify, cheque_balance = get_account_detail(CHEQUE_AC)
            verify, acc_balance = get_account_detail(account)
            print(f"Lodgement limit {CURRENCY}{TRANSACTION_LIMIT}")
            print(f'Current balance: {CURRENCY}{acc_balance}')
            lodgement = int(input("Lodgement amount? "))
            cheque_balance = int(cheque_balance)
            acc_balance = int(acc_balance)
            # Validate amounts
            new_cheque_balance = cheque_balance + lodgement
            new_acc_balance = acc_balance + lodgement
            print(f'New balance    : {CURRENCY}' + str(new_acc_balance))         
            atm_log('lodgement', lodgement)
            time_stamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            put_account_detail(account, new_acc_balance, time_stamp)
            put_account_detail(CHEQUE_AC, new_cheque_balance, time_stamp)

        elif choice == "4":
            atm_log('!!new lodgement!!', account)

        elif choice == "5":
            atm_log('statement', account)
            print("\nPrint Statement unimplemented")
            time.sleep(1)

        elif choice == "6":
            atm_log('pin_change', account)
            print("\nChange PIN unimplemented")
            time.sleep(1)

        elif (choice == "0" or choice == ""):
            atm_log('exit', account)
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
        atm_log('start_attract', 0)
        screen_header("ATM")

        card = card_input()
        atm_log('card_in', card)
        verify, pin_no, pin_count, account = get_card_detail(card)      

        # Notify user of invalid card and quit loop
        if verify == "invalid":
            print("Invalid card - please contact Bank")
            atm_log('card_return', card)
            return_card()
            continue

        # Notify user of card and PIN issues
        if (int(pin_count) == MAX_PIN_FAIL):
            print("Card error - please contact Bank")
            atm_log('card_error_max_pin', card)
            time.sleep(3)
            continue
        elif (int(pin_count) > 0):
            atm_log('card_warning_pin_count', card)
            print(f"{MAX_PIN_FAIL - int(pin_count)} PIN attempt{'s' if (MAX_PIN_FAIL - int(pin_count) > 1) else ''} left")

        # Increment fail count if incorrect PIN, reset if PIN is correct, then continue to Menu
        while True:
            pin = pin_input(pin_no)
            if not pin:
                # If PIN is incorrect
                pin_count = int(pin_count) + 1
                put_card_detail(card, pin_no, pin_count)
                if pin_count == 3:
                    # Card retained
                    print("Card retained - please contact Bank")
                    atm_log('card_retained', card)
                    time.sleep(3)
                    break
                atm_log('card_pin_fail', card)
                pin_fail(card)
                break
            else:
                # If PIN is correct, reset fail count on card
                atm_log('card_pin_reset', card)
                put_card_detail(card, pin_no, 0)
                menu(account)
                return_card()
                break

atm_log('code_start', 0)
# test_splash()
#main()
menu('1234')
#withdrawal ('1234')