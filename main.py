# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# main - entry point

import os
import platform
import sys
import time

from storage.setup import get_db, init_db
from models.user   import User
from models.cart   import Cart
from models.stock  import Stock

def main()->None:
    # initialize the database...
    init_db()
    DB = next(get_db())

    def clear_screen():
        if platform.system() == "Windows":
            os.system('cls') # Windows
        else:
            os.system('clear') # Unix Systems...

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

    def sanitize_input(prompt:str, min:int=0, max:int=50)->str:
        while True:
            user_input:str = input(prompt).strip()
            if isinstance(user_input, str) and len(user_input) > min and len(user_input) <= max:
                return user_input
            else:
                print("Invalid input, Enter valid values please.")

    def user_selection()->int:
        while True:
            try:
                selection:int = int(input("Option: "))
                return selection
            except ValueError:
                print("Invalid choice, Please try again.")        

    def main_menu():
        print(" ---- Welcome to: Trade-Engine ---- ")
        print("To proceed, choose an option below: ")
        print("1) Login")
        print("2) Register")
        print("3) Admin")
        print("4) Help")
        print("8) Press this to clear screen in all interfaces...")
        print("Press any other key above or below selection to exit...")

        selection:int = user_selection()
        if   selection == 1:
            transition(login)
        elif selection == 2:
            transition(register)
        elif selection == 3:
            transition(admin_menu)
        elif selection == 4:
            # help menu
            transition(lambda: help_menu(main_menu))
        elif selection == 8:
            clear_screen()
            main_menu()
        else:
            print("Goodbye!")
            sys.exit()

    def main_dashboard(user:User)->None:
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
            view_cart(user)
        elif selection == 2:
            add_item_to_cart(user)
        elif selection == 3:
            remove_item_from_cart(user)
        elif selection == 4:
            checkout(user)
        elif selection == 5:
            transition(lambda: account_options(user), "Account Options Loading", 1)
        elif selection == 6:
            transition(main_menu, "Logging out", 1)
        elif selection == 7:
            items = DB.query(Stock).all()
            print(" -------------------------------------------- STOCK -------------------------------------------- ")
            for item in items:
                print(f" ItemID: {item.ItemID} | Name: {item.ItemName} | Category: {item.ItemCategory} | Price: ${item.ItemPrice} | Quantity: {item.ItemQuantity}")
            print(" ----------------------------------------------------------------------------------------------- ")
            transition(lambda: main_dashboard(user))
        elif selection == 8:
            clear_screen()
            main_dashboard(user)
        else:
            print("Goodbye!")
            sys.exit()

    def register()->None:
        print(f" ---- Register ---- ")
        user_name:str     = sanitize_input("Enter your name: ", 2, 50)
        user_email:str    = sanitize_input("Enter your email: ", 5, 50)
        user_password:str = sanitize_input("Enter your account password: ", 7, 10)

        # before creating the account... let's check if the account exists first...
        existing_user = DB.query(User).filter(User.UserEmail == user_email).first()
        if not existing_user:
            try:
                hashed_password = User.hash_password(user_password)
                new_user = User.create_account(DB, user_name, user_email, hashed_password, user_password)
                print(f"Account creation succeeded")
                transition(lambda: main_dashboard(new_user), "Loading your panel", 1)
            except Exception as ACC_CREATE_FAILED:
                print(f"Failed to create account - error: {ACC_CREATE_FAILED}")
                print(f"Share this error with, help@trade-engine.com")
        else:
            # the user exists...
            print("Account found...")
            transition(login, "Loading login")

    def login():
        print(f" ---- Login ---- ")
        print(f" note: login attempts given: 3")
        attempts:int = 0

        while attempts < 3:
            user_email:str    = sanitize_input("Enter your email: ", 5, 50)
            user_password:str = sanitize_input("Enter your account password: ")

            user = DB.query(User).filter(User.UserEmail == user_email, User.UserPassword == User.hash_password(user_password)).first()
            if user:
                print(f"Welcome back, {user.UserName}")
                transition(lambda: main_dashboard(user), "Login loading", 1)
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
                        transition(password_recovery, "Password Recovery Loading")
                        return
                    else:
                        print("Proceeding to account Registration...")
                        transition(register)
                        return

    def admin_menu():
        print(" ---- Trade-Engine, Admin Menu ---- ")
        print("1) Add Stock")
        print("2) Remove Stock")
        print("3) Change Price")
        print("4) List All Items")
        print("5) Back to Main Menu")
        print("Press any other key above or below selection to exit...")

        selection:int = user_selection()
        if   selection == 1:
            add_stock()
        elif selection == 2:
            remove_stock()
        elif selection == 3:
            change_price()
        elif selection == 4:
            list_all_items()
        elif selection == 5:
            transition(main_menu, "Logging out", 1)
        else:
            print("Goodbye!")
            sys.exit()

    def help_menu(instance:callable):
        print(" --------------- Trade-Engine, Help Menu --------------- ")
        print(" For assistance, please contact support@trade-engine.com")
        print(" ------------------------------------------------------- ")
        print("\n") # put a newline...
        transition(instance)

    def add_stock():
        print(" ---- Trade-Engine, Add Stock ---- ")
        item_name     = sanitize_input("Enter Item Name: ")
        item_category = sanitize_input("Enter Item Category: ")
        while True:
            try:
                item_price    = float(input("Enter Item Price: "))
                break
            except ValueError:
                print(f"Invalid input. Enter a price value - please.")

        while True:
            try:
                item_quantity = int(input("Enter Item Quantity: "))
                break
            except ValueError:
                print(f"Invalid input. Enter a quantity value - please.")

        Stock.add_stock(DB, item_name, item_category, item_price, item_quantity)
        print(f"Stock for {item_name} added.")
        transition(admin_menu)

    def remove_stock(): 
        print(" ---- Remove Stock ---- ") 
        item_name = sanitize_input("Enter item name: ") 
        Stock.rem_stock(DB, item_name) 
        print(f"Stock for {item_name} removed.") 
        transition(admin_menu)
        
    def change_price():
        print(" ---- Price Change ---- ")
        item_name:str = sanitize_input("Enter item name: ")
        while True:
            try:
                new_price    = float(input("Enter Item Price: "))
                break
            except ValueError:
                print(f"Invalid input. Enter a price value - please.")      

        Stock.change_price(DB, item_name, new_price)
        print(f"Price for {item_name} updated.")
        transition(admin_menu)

    def list_all_items():
        print(" ---- All Items ---- ")
        items = Stock.list_all(DB)
        for item in items:
            print(f"ItemName: {item.ItemName} | ItemCategory: {item.ItemCategory} | ItemPrice: {item.ItemPrice} | ItemQuantity: {item.ItemQuantity}")
        transition(admin_menu)

    def view_cart(user:User):
        print(f" ---------------- Your Cart: {user.UserName} ---------------- ")
        cart_items = Cart.check_all(DB, user.UserID)
        for cart_item in cart_items:
            print(f"ItemID: {cart_item.ItemID} | ItemPrice: {cart_item.ItemPrice} | ItemQuantity: {cart_item.Quantity}")
        print(" --------------------------------------------- ")
        transition(lambda: main_dashboard(user))

    def add_item_to_cart(user:User):
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
                print(f"Added {item_quantity} of {new_item.ItemName} to cart.")
        else:
            print("Item not found.")
        transition(lambda: main_dashboard(user))

    def remove_item_from_cart(user:User)->None:
        print(f" ---- Remove Item from Your Cart: {user.UserName} ---- ")
        while True:
            try:
                item_id    = int(input("Enter Item ID: "))
                break
            except ValueError:
                print(f"Invalid input. Enter an item id value - please.")
        Cart.delete_from_cart(DB, user.UserID, item_id)
        print(f"Removed item {item_id} from your cart.")
        transition(lambda: main_dashboard(user))

    def checkout(user:User)->None:
        print(f" ---- Checkout for: {user.UserName} ---- ")
        total = Cart.get_totals(DB, user.UserID)
        print(f"Total amount payable: {total}")

        confirmation:str = sanitize_input("Do you want to proceed with the checkout? (yes/no): ")
        if confirmation.lower() == "yes" or "y":
            Cart.remove_all(DB, user.UserID)
            print("Checkout Complete.")
        else:
            print("Checkout canceled...")

        transition(lambda: main_dashboard(user))

    def account_options(user:User):
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
            transition(lambda: account_options(user))
        elif selection == 2:
            print(" ------------------------------- ")
            print(" Changing your - Account Name...")
            print(f" Old username: {user.UserName}")
            print(" ------------------------------- ")
            new_account_name:str = sanitize_input("New Username: ")
            user.change_username(DB, user.UserID, new_account_name)
            # transition(lambda: main_dashboard(user))
            transition(lambda: account_options(user))
        elif selection == 3:
            print(" ------------------------------- ")
            print(" Changing your - Account Email...")
            print(f" Old email: {user.UserEmail}")
            print(" ------------------------------- ")
            new_account_email:str = sanitize_input("New account email: ")
            user.change_email(DB, user.UserID, new_account_email)
            # transition(lambda: main_dashboard(user))
            transition(lambda: account_options(user))      
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
                        user.change_password(DB, user.UserID, new_account_password)
                        transition(lambda: account_options(user))
                        return
                    else:
                        # passwords do not match...
                        print("Passwords do not match. Please try again.")                
            else:
                print("Incorrect old password.")
                transition(lambda: account_options(user))
        elif selection == 5:
            # viewing your back-up password...
            # ensure no one's wacthing... 🤭🫣
            print(" ------------------------------- ")
            print(f"Your Password: {user.UserPasswordB}")
            print(" ------------------------------- ")
            transition(lambda: account_options(user))
        elif selection == 6:
            # account deletion...
            choice:str = sanitize_input("Continue with account deletion? (yes/no): ")
            if choice.lower() == "yes" or choice.lower() == "y":
                # continue with account deletion request
                user.delete_account(DB, user.UserEmail)
                clear_screen()
                print("Account deletion was a Success...")
                transition(main_menu)
            else:
                print("Account deletion cancelled...")
                transition(lambda: account_options(user))
        elif selection == 7:
            # back to dashboard...
            transition(lambda: main_dashboard(user), "Loading", 1)
        else:
            # goodbye
            print("Goodbye!!!")
            sys.exit()

    def password_recovery():
        print(" ---- Password Recovery ---- ")
        user_email:str = sanitize_input("Enter your account email: ")

        user = DB.query(User).filter(User.UserEmail == user_email).first()
        if user:
            # user is existing...
            print(f"Your password is: {user.UserPasswordB}")
            transition(login, "Login loading")
        else:
            # user is not found...
            print(f"User with email: {user_email} not found...")
            print("Proceeding with registration")
            transition(register, "Register loading")

    # start...
    main_menu()

if __name__ == "__main__":
    main()