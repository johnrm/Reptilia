import os
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


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("   Reptilia Bank")
    print("-------------------")
    print("        ATM")
    print("-------------------\n")
  
    card = input("Insert card or enter card ID to begin\n")
    print("    ATM Options")
    print("-------------------\n")
    print("1> Check Balance")
    print("2> Withdrawal")
    print("3> Lodgement")
    print("4> Print Statement\n")

main()