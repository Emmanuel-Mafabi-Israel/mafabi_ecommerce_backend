# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# HELPERS - helper functions

import os
import platform
import sys
import re
import time

# function for clearing the screen...
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls') # Windows
    else:
        os.system('clear') # Unix Systems...

# transitional animation - three loading dots...
def transition(menu:callable, message:str="Loading", clear:int = 0):
    # display loading dots for 3 seconds...
    print(message, end="")
    for _ in range(3):
        time.sleep(1)
        print(".", end="")
        sys.stdout.flush()
    print("\n") # print a newline...
    if clear == 1:
        clear_screen()
    menu() # then call out our function...

# function incorporating both input and input sanitization...
def sanitize_input(
    prompt:str, 
    min:int=0, 
    max:int=50, 
    message:str = "Invalid input, Enter valid values please.")->str:
    while True:
        user_input:str = input(prompt).strip()
        if isinstance(user_input, str) and len(user_input) > min and len(user_input) <= max:
            return user_input
        else:
            print(message)

# function for checking valid email addresses
def validate_email(email:str)->bool:
    regex:str = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # regex pattern
    return re.match(regex, email)

# function for choice selection - quite universal...
def user_selection()->int:
    while True:
        try:
            selection:int = int(input("Option: "))
            return selection
        except ValueError:
            print("Invalid choice, Please try again.")

def header(message:str)->str:
    return f"-------------------------- {message} --------------------------"

def separator(header:str)->None:
    sep = "-" * len(header)
    return sep 