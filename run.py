import os
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

accounts = SHEET.worksheet('accounts')

#data = accounts.get_all_values()
#print(data)
#x = input("<Enter> to begin\n")

def validate_number(numbers,type):
    try:
        numbers.isnumeric()
#        if len(str(numbers)) != 4:  
#                f"{type} should be 4 digita, you provided {len(str(num))}"
    except:
        print("Please try again.\n")
        return True

    return False


def validate_card():
    card = input("Insert card (or type card ID): ")
    pin=getpass.getpass('PIN (4 digits): ')
    return True
    

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
    
def menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("        Reptilia Bank")
        print("-----------------------------")
        print("         ATM Options")
        print("-----------------------------")

        print("1> Check Balance")
        print("2> Withdraw cash")
        print("3> Lodgement")
        print("4> Print Statement")
        print("0 or <Enter> Cancel\n")

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
            print("\n Cancel") 
        elif choice !="":
            print("\n Not Valid Choice Try again")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Welcome to ATM simulator!')
    print('For testing purposes...')
    print('Sample a/c: 2234')
    print('Sample PIN: 3234')
    input("Press <Enter> to continue")    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("        Reptilia Bank")
        print("-----------------------------")
        print("             ATM")
        print("-----------------------------\n")
        if validate_card():
            input("Card Valid - Press <Enter>")
            menu()
        input("Session end")
#        if validate_card():
#            menu()
#        else:
#            print("fail")
#            x=input('press <enter>')

main()