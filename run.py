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

data = accounts.get_all_values()
print(data)
x = input("<Enter> to begin\n")

def validate_card():
    card = input("Insert card or enter card ID to begin: ")
    password=getpass.getpass('PIN (4 digits): ')
    #print(password)
#    a=input ("Press <Enter>")
    return True
    
def menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("        Reptilia Bank")
        print("-----------------------------")
        print("         ATM Options")
        print("-----------------------------")
        print("1> Check Balance")
        print("2> Withdraw cash")
        print("3> Lodgement")
        print("4> Print Statement\n")
        choice=input("Select: ")


def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("        Reptilia Bank")
        print("-----------------------------")
        print("             ATM")
        print("-----------------------------\n")
        if validate_card():
            menu()

main()