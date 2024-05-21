"""
Modules to be imported
"""
import os
import time
import getpass
import datetime
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
SHEET = GSPREAD_CLIENT.open('ATM')

# System constants
# Bank name
BANK_NAME = "Reptilia Bank"
# Currency
CURRENCY = "EUR "
# Max failed PIN on card
MAX_PIN_FAIL = 3
# Set display width
DISPLAY_WIDTH = 30
# Bank Account (Account for the ATM machine)
CASH_AC = "9999"
# Bank Account (Account for the ATM machine)
CHEQUE_AC = "9998"
# Withdrawal limit
WITHDRAWAL_LIMIT = 300
# Lodgement limit
LODGEMENT_LIMIT = 1000


def atm_log(action, data):
    """
    Log and Timestamp actions on the ATM
    action - The current machine action
    data - differs depending on machine action
    """
    timestamp = str(datetime.datetime.now())
    data = [timestamp, action, data]
    log = SHEET.worksheet('atm_log')
    log.append_row(data)


def transaction_log(account, transaction_type, amount, medium, new_acc_balance):
    """
    Log the transaction for accounting and statement purposes
    account - the account for which the transaction is being logged
    transaction_type - transaction type
    amount - value of  transaction
    medium - cash or cheque
    new_acc_balance - new account balance based on this transaction
    """
    timestamp = str(datetime.datetime.now())
    data = [timestamp, account, transaction_type, amount, medium, new_acc_balance]
    log = SHEET.worksheet('transactions')
    log.append_row(data)


def statement(account):
    """
    Statement display
    Displays transactions and account balance for the current card/account
    account - the account for which a statement is required
    """
    atm_log("Statement", account)
    screen_header("Statement")
    transactions = SHEET.worksheet("transactions")
    rows = transactions.get_all_values()
    print (" Date".ljust(15," "), CURRENCY.rjust(14," "))
    balance = 0
    for row in rows:
        if row[1] == account:
            date = row[0]
            date = date[8:10] + "-" + date[5:7] + "-" + date[2:4]
            amount = float(row[3])
            balance = float(row[5])
            print (date.ljust(15," "), str("%.2f" % amount).rjust(14," "))
    print('--------' , '--------'.rjust(21," "))
    print('Balance:' , str("%.2f" % balance).rjust(21," "))
    time.sleep(5)


def screen_header(function):
    """
    Displays the screen header for all screens
    function - the text to be highlighted
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANK_NAME.center(DISPLAY_WIDTH))
    print ("-" * DISPLAY_WIDTH)
    print(function.center(DISPLAY_WIDTH))
    print ("-" * DISPLAY_WIDTH)
    print()


def validate_number(numbers, length):
    """
    Validate 'numbers' based on fed parameters
    numbers - the number to be validated
    length - length/number of digits
    Returns True or False
    """
    try:
        int(numbers)
        if len(numbers) != length:
            raise Exception
        return True
    except ValueError:
        print("Non-numeric entry!")
        return False
    except Exception:
        print(f"{len(numbers)} digits entered, {length} expected!")
        return False


def card_input():
    """
    Input Card and PIN from user
    Return validated card no. or False
    """
    card = input("Insert card (or enter card ID): ")
    if validate_number(card, 4):
        return card


def get_card_detail(card):
    """
    Get details and validate inserted Card
    card - card number to be checked
    Returns row or False
    """
    cardsheet = SHEET.worksheet("cards")
    cardlist = cardsheet.col_values(1)
    try:
        rownum = cardlist.index(card) + 1
    except ValueError:
        return False
    row = cardsheet.row_values(rownum)
    return row


def input_pin(pin_no):
    """
    Get pin from user
    pin_no - PIN to be validate
    Returns True or False
    """
    user_pin = getpass.getpass('Enter PIN (4 digits): ')
    if validate_number(user_pin, 4):
        if user_pin == pin_no:
            return True
    else:
        return False


def put_card_detail(card, pin_no, pin_count):
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
    cardsheet.update([[pin_no, pin_count]], f'B{rownum}:C{rownum}')


def change_pin(card):
    """
    Function to change PIN on individual card.
    card - Card number is passed in.
    """
    atm_log("change_pin", card)
    screen_header("Change PIN")
    new_pin = getpass.getpass('   Enter new PIN (4 digits): ')
    if validate_number(new_pin, 4):
        valid_pin = getpass.getpass('Re-Enter new PIN (4 digits): ')
        if validate_number(valid_pin, 4) and (new_pin == valid_pin):
            put_card_detail(card, new_pin, 0)
            atm_log("pin_update", card)
            print('\n  PIN updated!')
            print('  Do NOT forget new PIN!')
            time.sleep(3)
        else:
            atm_log("pin_mismatch", card)
            print('PIN mismatch!')
            time.sleep(3)
    else:
        atm_log("pin_error", card)
        print('PIN error!')
        time.sleep(3)


def return_card():
    """
    Return card to user at end of session
    """
    screen_header("ATM")
    print("    Please take your card")
    print("      Have a nice day!")
    time.sleep(3)


def get_account_detail(account):
    """
    Get and return account detail
    account - the account to be retrieved
    """
    accountsheet = SHEET.worksheet("accounts")
    accountlist = accountsheet.col_values(1)
    try:
        rownum = accountlist.index(account) + 1
    except ValueError:
        return False
    row = accountsheet.row_values(rownum)
    balance = row[4]
    return float(balance)


def put_account_detail(account, balance, timestamp):
    """
    Update account balance to gsheet
    account - account to be updated
    balance - new balance
    timestamp - timestamp for the update
    """
    accountsheet = SHEET.worksheet("accounts")
    accountlist = accountsheet.col_values(1)
    try:
        rownum = accountlist.index(account) + 1
    except ValueError:
        return
    accountsheet.update([[balance, timestamp]], f'E{rownum}:F{rownum}')


def withdraw(account):
    """
    Withdrawal transaction takes place here
    account - account to remove cash from
    """
    atm_log("withdraw", account)

    # Find what funds are available to transact
    cash_balance = get_account_detail(CASH_AC) # Amount in ATM
    acc_balance = get_account_detail(account) # Amount in account

    while True:
        # Notify if inadequate balance
        screen_header("Withdrawal")
        print(f'Available funds: {CURRENCY}{"%.2f" % acc_balance}')
        if  acc_balance <= 0:
            print('Inadequate funds')
            time.sleep(3)
            break

        # Notify trx limit
        print(f'Transaction limit: {CURRENCY}{"%.2f" % WITHDRAWAL_LIMIT}')

        # Input and validate transaction amount
        try:
            print(f'Whole amount, multiples of {CURRENCY}10 only')
            value = float(input("Withdrawal amount: ")) # Requested amount
            if (divmod(value,10)[1] != 0) or not int(value):
                print('Multiples of 10 only')
                time.sleep(3)
                break
        except ValueError:
            print("Non-numeric, decimal or Null entry!")
            time.sleep(3)
            break

        if value > WITHDRAWAL_LIMIT:
            print('Exceeds transcation limit') # Withdrawal Limit exceeded
            time.sleep(3)
            break
        if (acc_balance - value) <= 0:
            print('Exceeds available funds') # Insufficient funds in account
            time.sleep(3)
            break
        if (cash_balance - value) <= 0:
            print('ATM out of funds') # Insufficient cash in ATM
            time.sleep(3)
            break
        time.sleep(3)

        # Calculate new balances
        value = -1 * value # Flip the sign to allow withdrawal reduce account balance
        new_cash_balance = cash_balance + value
        new_acc_balance = acc_balance + value

        # Log the transaction to ATM log and transaction log
        atm_log('Withdrawal', value)
        timestamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
        put_account_detail(account, new_acc_balance, timestamp)
        put_account_detail(CASH_AC, new_cash_balance, timestamp)
        print (f'New balance    : {CURRENCY}{"%.2f" % new_acc_balance}')
        transaction_log(account, "withdrawal", value, "cash",new_acc_balance)
        time.sleep(3)
        break


def lodge(account):
    """
    Lodgements take place here
    account - account having funds added
    """
    atm_log("lodge", account)
    screen_header("Lodgement")

    # Find what funds are available to transact
    cheque_balance = get_account_detail(CHEQUE_AC) # Amount in ATM Cheque account
    acc_balance = get_account_detail(account) # Amount in user account

    # Notify trx limit
    print(f'Account Balance: {CURRENCY}{"%.2f" % acc_balance}')
    print(f'Lodgement limit: {CURRENCY}{"%.2f" % LODGEMENT_LIMIT}')

    # Input and validate transaction amount
    try:
        value = float(input("Lodgement amount: ")) # Lodgement amount
    except ValueError:
        print("Non-numeric entry!")
        time.sleep(3)
        return False

    if value > LODGEMENT_LIMIT:
        print('Exceeds lodgement limit') # Lodgement Limit exceeded
        time.sleep(3)
        return False
    if value == 0:
        return False

    # Calculate new balances
    new_cheque_balance = cheque_balance + value
    new_acc_balance = acc_balance + value

    # Log the transaction
    atm_log('Lodgement', value)
    timestamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    put_account_detail(account, new_acc_balance, timestamp)
    put_account_detail(CHEQUE_AC, new_cheque_balance, timestamp)
    print(f'New balance: {CURRENCY}{"%.2f" % new_acc_balance}')
    transaction_log(account, "lodgement", value, "cheque", new_acc_balance)
    time.sleep(3)


def menu(card, account):
    """
    Menu of user options
    card - current users card
    account - current users account
    """
    while True:
        screen_header("ATM Options")
        print("1> Check Balance")
        print("2> Withdraw cash")
        print("3> Lodgement")
        print("4> Print Statement")
        print("5> Change PIN")
        print("-" * 18)
        print("0> Cancel\n")

        # Menu selection
        choice = input("Select: ")

        if choice == "1":
            # Account Balance
            atm_log('menu_balance', account)
            screen_header("Account balance")
            balance = get_account_detail(account)
            print(f'Current balance: {CURRENCY}{"%.2f" % balance}'.center(DISPLAY_WIDTH))
            time.sleep(3)

        elif choice == "2":
            # Withdraw Cash
            atm_log('menu_withdraw', account)
            withdraw(account)

        elif choice == "3":
            # Lodge Cheque
            atm_log('menu_lodge', account)
            lodge(account)

        elif choice == "4":
            # Display statement
            atm_log('menu_statement', account)
            statement(account)

        elif choice == "5":
            # Change card PIN
            atm_log('menu_change_pin', account)
            change_pin(card)

        elif (choice == "0" or choice == ""):
            # Exit the menu
            atm_log('menu_exit', account)
            break


def main():
    """
    Main routine
    """
    while True:
        atm_log('start_attract', 0)
        screen_header("ATM")

        # Get and validate card
        card = card_input()
        atm_log('card_in', card)
        row = get_card_detail(card)
        if row:
            pin_no = row[1]
            pin_count = row[2]
            account = row[3]

        # Notify user of invalid card and quit if invalid
        if not row:
            print("Invalid card - please contact Bank")
            atm_log('card_return', card)
            return_card()
            continue

        # Notify user of card and PIN issues
        if int(pin_count) == MAX_PIN_FAIL:
            print("Card error - please contact Bank")
            atm_log('card_error_max_pin', card)
            time.sleep(3)
            continue
        if int(pin_count) > 0:
            atm_log('card_warning_pin_count', card)
            print(f"{MAX_PIN_FAIL - int(pin_count)} PIN attempts left")

        # Increment fail count if incorrect PIN, reset if PIN is correct, then continue to Menu
        while True:
            pin = input_pin(pin_no)
            if not pin:
                # If PIN is incorrect
                pin_count = int(pin_count) + 1
                print(f"Incorrect PIN {MAX_PIN_FAIL - int(pin_count)} attempts left")
                put_card_detail(card, pin_no, pin_count)
                if pin_count == 3:
                    # Card retained
                    print("Card retained - please contact Bank")
                    atm_log('card_retained', card)
                    time.sleep(3)
                    break
                atm_log('card_pin_fail', card)
                break

            # If PIN is correct, reset fail count on card
            atm_log('card_pin_reset', card)
            put_card_detail(card, pin_no, 0)
            menu(card, account)
            return_card()
            break

atm_log('code_start', 0) # Log program startup
main()
