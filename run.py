import os
import time
import getpass
import gspread
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

#Max allowed Pin failures
MAX_PIN_FAIL = 3

accounts = SHEET.worksheet('accounts')

#data = accounts.get_all_values()
#print(data)
#x = input("<Enter> to begin\n")

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

def pin_check(card):
    x=1

def pin_fail(card):
    input('PIN fail')

def pin_reset(card):
    input('PIN reset')
    

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
    print(cardlist)
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
    user_pin=getpass.getpass('Enter PIN (4 digits): ')
    if validate_number(user_pin, 4):
        if (user_pin != pin_no):
            return False
        else:
            return True
    else:
        return False

def validate_card_1():
    try_count = 0
    while (try_count <3):
        card = input("Insert card (or type card ID): ")
        valid = validate_number(card,'Card ID')
        try_count += 1
        print()
        print(valid)
        print(try_count)

    stock = SHEET.worksheet("cards").get_all_values()
    stock_row = stock[-1]
    pin=getpass.getpass('PIN (4 digits): ')
    validate_number(pin,'PIN')
    return False
    
def menu(card):
    """
    Menu of user options 
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("        Reptilia Bank")
        print("-----------------------------")
        print("         ATM Options")
        print("-----------------------------")
        print(f"          Card {card}")
        print()    
        print("1> Check Balance")
        print("2> Withdraw cash")
        print("3> Lodgement")
        print("4> Print Statement")
        print("0 or <Enter> Cancel\n")

        #Menu selection
        choice=input("Select: ")
        if choice=="1":
            print("\nCheck Balance")
        elif choice=="2":
            print("\nWithdraw cash")
        elif choice=="3":
            print("\nLodgement")
        elif choice=="4":
            print("\nPrint Statement")
        elif choice=="0":
            print("\nCancel")
            input("Enter")
            break
        elif choice !="":
            print("\nInvalid Choice Try again")
        input("Enter")

def test_splash():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("        Reptilia Bank")
    print("-----------------------------")
    print('        ATM simulator')
    print("-----------------------------")
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
        os.system('cls' if os.name == 'nt' else 'clear')
        print("        Reptilia Bank")
        print("-----------------------------")
        print("             ATM")
        print("-----------------------------\n")

        card = card_input()
        verify, pin_no, pin_count, account = get_card_detail(card)
#        put_card_detail(card,pin_no, pin_count)

        #Notify user of invalid card and quit loop
        if verify == "invalid":
            print("Invalid card - please contact Bank")
            time.sleep(3)
            continue

        #Notify user of card and PIN issues
        if (int(pin_count) == MAX_PIN_FAIL):
            print("Card retained - please contact Bank")
            time.sleep(3)
            continue
        elif (int(pin_count) > 0):
            print(f"{MAX_PIN_FAIL - int(pin_count)} PIN attempt{'s' if (MAX_PIN_FAIL - int(pin_count) > 1) else ''} left")

        #Increment fail count if incorrect PIN, reset if PIN is correct, then continue to Menu
        while True:
            pin = pin_input(pin_no)
            if not pin:
                pin_count = str(int(pin_count) + 1)
                put_card_detail(card, pin_no, pin_count)
                pin_fail(card)
                break
            else:
                pin_reset(card)
                menu(account)
                break
       
#test_splash()
main()