# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# USER INTERFACES and RELATED FUNCTIONS

import sys
from dependencies.helpers import clear_screen, sanitize_input, transition, user_selection, validate_email, header, separator

from models.user  import User
from models.stock import Stock
from models.cart  import Cart

from sqlalchemy.orm import Session

def register(DB:Session)->None:
    print(f" ---- Register ---- ")
    user_name:str     = sanitize_input("Enter your name: ", 2, 50, "Names should be a string - ranging from 2 to above characters long.")
    while True:
        user_email:str    = sanitize_input("Enter your email: ", 5, 50, "Follow the right email structure please.")
        if validate_email(user_email):
            break
        else:
            print(" Enter a valid email address, follow this structure: your-name@domain.com")
    user_password:str = sanitize_input("Enter your account password: ", 7, 10, "Enter a password ranging from 7 to 10 characters long.")
    # before creating the account... let's check if the account exists first...
    existing_user = DB.query(User).filter(User.UserEmail == user_email).first()
    if not existing_user:
        try:
            hashed_password = User.hash_password(user_password)
            new_user = User.create_account(DB, user_name, user_email, hashed_password, user_password)
            print(f"Account creation succeeded")
            transition(lambda: main_dashboard(DB, new_user), "Loading your panel", 1)
        except Exception as ERROR:
            print(f"an error occured - details: {ERROR}")
            print(f"Share this error with, help@trade-engine.com")
    else:
        # the user exists...
        print("Account found...")
        transition(lambda: login(DB), "Loading login")

def login(DB:Session):
    print(f" ---- Login ---- ")
    print(f" note: login attempts given: 3")
    attempts:int = 0

    while attempts < 3:
        while True:
            user_email:str    = sanitize_input("Enter your email: ", 5, 50, "Names should be a string - ranging from 2 to above characters long.")
            if validate_email(user_email):
                break
            else:
                print(" Enter a valid email address, follow this structure: your-name@domain.com")
        user_password:str = sanitize_input("Enter your account password: ", 7, 10, "Enter a password ranging from 7 to 10 characters long.")
        user = DB.query(User).filter(User.UserEmail == user_email, User.UserPassword == User.hash_password(user_password)).first()
        if user:
            print(f"Welcome back, {user.UserName}")
            transition(lambda: main_dashboard(DB, user), "Login loading", 1)
            return
        else:
            attempts += 1
            if attempts < 3:
                print("---------------------------------------------------------------------------")
                print(f"Invalid email or password. Please try again, login attempts: [{attempts}].")
                print("---------------------------------------------------------------------------")
                # transition(login)
            else:
                selection:str = input("Forgot your Password? (yes/no): ")
                if selection.lower() == "yes" or selection.lower() == "y":
                    print("Initiating Password Recovery")
                    transition(lambda: password_recovery(DB), "Password Recovery Loading")
                    return
                else:
                    print("Proceeding to account Registration...")
                    transition(lambda: register(DB))
                    return

def main_dashboard(DB:Session, user:User)->None:
    from dependencies.interfaces.main_menu import main_menu

    print(f" ---- Welcome, {user.UserName} ---- ")
    print("1) View Cart")
    print("2) Add item to Cart")
    print("3) Remove item from Cart")
    print("4) Checkout")
    print("5) Account Options")
    print("6) Log out")
    print("7) View Stock Items")
    print("8) Clear Screen")

    print("Press any other key above or below selection to exit...")
    selection:int = user_selection()

    if   selection == 1:
        view_cart(DB, user)
    elif selection == 2:
        add_item_to_cart(DB, user)
    elif selection == 3:
        remove_item_from_cart(DB, user)
    elif selection == 4:
        checkout(DB, user)
    elif selection == 5:
        transition(lambda: account_options(DB, user), "Account Options Loading", 1)
    elif selection == 6:
        transition(lambda: main_menu(DB), "Logging out", 1)
    elif selection == 7:
        items = DB.query(Stock).all()
        print(" -------------------------------------------- STOCK -------------------------------------------- ")
        for item in items:
            print(f" ItemID: {item.ItemID} | Name: {item.ItemName} | Category: {item.ItemCategory} | Price: ${item.ItemPrice} | Quantity: {item.ItemQuantity}")
        print(" ----------------------------------------------------------------------------------------------- ")
        transition(lambda: main_dashboard(DB, user))
    elif selection == 8:
        clear_screen()
        main_dashboard(DB, user)
    else:
        print("Goodbye!")
        sys.exit()


def view_cart(DB:Session, user:User):
    h_string:str = header(f"Your Cart: {user.UserName}")
    print(h_string)
    cart_items = Cart.check_all(DB, user.UserID)
    for cart_item in cart_items:
        print(f"ItemID: {cart_item.ItemID} | ItemPrice: ${cart_item.ItemPrice} | ItemQuantity: {cart_item.Quantity}")
    print(separator(h_string))
    transition(lambda: main_dashboard(DB, user))

def add_item_to_cart(DB:Session, user:User):
    print(f" ---- Add to Your Cart: {user.UserName} ---- ")
    while True:
        try:
            item_id    = int(input("Enter Item ID: "))
            break
        except ValueError:
            print(f"Invalid input. Enter an item id value - please.")
    while True:
        try:
            item_quantity = int(input("Enter Item Quantity: "))
            break
        except ValueError:
            print(f"Invalid input. Enter a quantity value - please.")    
    new_item = DB.query(Stock).filter_by(ItemID=item_id).first()
    if new_item:
        result = Cart.add_to_cart(DB, user.UserID, item_id, item_quantity, new_item.ItemPrice * item_quantity)
        if isinstance(result, str):
            # this is an error message...
            print(result)
        else:
            print(f"Added {item_quantity} items of {new_item.ItemName} to cart.")
    else:
        print("Item not found.")
    transition(lambda: main_dashboard(DB, user))

def remove_item_from_cart(DB:Session, user:User)->None:
    print(f" ---- Remove Item from Your Cart: {user.UserName} ---- ")
    while True:
        try:
            item_id    = int(input("Enter Item ID: "))
            break
        except ValueError:
            print(f"Invalid input. Enter an item id value - please.")
    result = Cart.delete_from_cart(DB, user.UserID, item_id)
    print(result)
    transition(lambda: main_dashboard(DB, user))

def checkout(DB:Session, user:User)->None:
    print(f" ---- Checkout for: {user.UserName} ---- ")
    total = Cart.get_totals(DB, user.UserID)
    print(f"Total amount payable: ${total}")
    confirmation:str = sanitize_input("Do you want to proceed with the checkout? (yes/no): ")
    if confirmation.lower() in ["yes", "y"]:
        result = Cart.remove_all(DB, user.UserID, "Checkout Complete.")
        print(result)
    else:
        print("Checkout canceled...")
    transition(lambda: main_dashboard(DB, user))

def account_options(DB:Session, user:User):
    from dependencies.interfaces.main_menu import main_menu

    print(f" ---- Account Options ---- ")
    print("1) View account details")
    print("2) Change account Name")
    print("3) Change account email")
    print("4) Change your Password")
    print("5) View your Back-up password")
    print("-------- DANGER ZONE --------")
    print("6) Delete Account")
    print("-------- DANGER ZONE --------")
    print("7) Back to Dashboard")
    print("Press any other key above or below selection to exit...")
    selection:int = user_selection()
    if   selection == 1:
        print(" ------------------------------- ")
        print(f"Your Username: {user.UserName}")
        print(f"Your email   : {user.UserEmail}")
        print(f"Your acc ID  : {user.UserID}")
        print(" ------------------------------- ")
        transition(lambda: account_options(DB, user))
    elif selection == 2:
        print(" ------------------------------- ")
        print(" Changing your - Account Name...")
        print(f" Old username: {user.UserName}")
        print(" ------------------------------- ")
        new_account_name:str = sanitize_input("New Username: ")
        result = user.change_username(DB, user.UserID, new_account_name)
        # transition(lambda: main_dashboard(user))
        print(result)
        transition(lambda: account_options(DB, user))
    elif selection == 3:
        print(" ------------------------------- ")
        print(" Changing your - Account Email...")
        print(f" Old email: {user.UserEmail}")
        print(" ------------------------------- ")
        new_account_email:str = sanitize_input("New account email: ")
        result = user.change_email(DB, user.UserID, new_account_email)
        print(result)
        transition(lambda: account_options(DB, user))      
    elif selection == 4:
        print(" ------------------------------- ")
        print(" Changing your - Account Password...")
        print(f" Old email: {user.UserEmail}")
        print(" ------------------------------- ")
        # but first we need to verify things first...
        old_password:str = sanitize_input("Old account password: ")
        if old_password == user.UserPasswordB:
            # the user is legit...
            while True:
                new_account_password:str = sanitize_input("New password: ")
                password_confirm:str     = sanitize_input("Confirm new password: ")
                if new_account_password.lower() == password_confirm.lower():
                    # passwords match...
                    result = user.change_password(DB, user.UserID, new_account_password)
                    print(result)
                    transition(lambda: account_options(DB, user))
                    return
                else:
                    # passwords do not match...
                    print("Passwords do not match. Please try again.")                
        else:
            print("Incorrect old password.")
            transition(lambda: account_options(DB, user))
    elif selection == 5:
        # viewing your back-up password...
        # ensure no one's wacthing... 🤭🫣
        print(" ------------------------------- ")
        print(f"Your Password: {user.UserPasswordB}")
        print(" ------------------------------- ")
        transition(lambda: account_options(DB, user))
    elif selection == 6:
        # account deletion...
        choice:str = sanitize_input("Continue with account deletion? (yes/no): ")
        if choice.lower() in ["yes", "y"]:
            # continue with account deletion request
            user.delete_account(DB, user.UserEmail)
            clear_screen()
            print("Account deletion was a Success...")
            transition(lambda: main_menu(DB))
        else:
            print("Account deletion cancelled...")
            transition(lambda: account_options(DB, user))
    elif selection == 7:
        # back to dashboard...
        transition(lambda: main_dashboard(DB, user), "Loading", 1)
    else:
        # goodbye
        print("Goodbye!!!")
        sys.exit()

def password_recovery(DB:Session):
    print(" ---- Password Recovery ---- ")
    user_email:str = sanitize_input("Enter your account email: ")
    user = DB.query(User).filter(User.UserEmail == user_email).first()
    if user:
        # user is existing...
        print(f"Your password is: {user.UserPasswordB}")
        transition(lambda: login(DB), "Login loading")
    else:
        # user is not found...
        print(f"User with email: {user_email} not found...")
        print("Proceeding with registration")
        transition(lambda: register(DB), "Register loading")