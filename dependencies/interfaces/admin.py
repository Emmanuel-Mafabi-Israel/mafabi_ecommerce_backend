# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# ADMIN INTERFACES and RELATED FUNCTIONS

import sys
from dependencies.helpers import clear_screen, sanitize_input, transition, user_selection

from models.stock import Stock

from sqlalchemy.orm import Session

def admin_menu(DB:Session):
    from dependencies.interfaces.main_menu import main_menu
    print(" ---- Trade-Engine, Admin Menu ---- ")
    print("1) Add Stock")
    print("2) Remove Stock")
    print("3) Change Price")
    print("4) List All Items")
    print("5) Back to Main Menu")
    print("8) To clear the screen")
    print("Press any other key above or below selection to exit...")

    selection:int = user_selection()
    if   selection == 1:
        add_stock(DB)
    elif selection == 2:
        remove_stock(DB)
    elif selection == 3:
        change_price(DB)
    elif selection == 4:
        list_all_items(DB)
    elif selection == 5:
        transition(lambda: main_menu(DB), "Logging out", 1)
    elif selection == 8:
        clear_screen()
        admin_menu(DB)
    else:
        print("Goodbye!")
        sys.exit()

def add_stock(DB:Session):
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
    transition(lambda: admin_menu(DB))

def remove_stock(DB:Session): 
    print(" ---- Remove Stock ---- ") 
    item_name = sanitize_input("Enter item name: ") 
    Stock.rem_stock(DB, item_name) 
    print(f"Stock for {item_name} removed.") 
    transition(lambda: admin_menu(DB))

def change_price(DB:Session):
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
    transition(lambda: admin_menu(DB))

def list_all_items(DB:Session):
    print(" ---- All Items ---- ")
    items = Stock.list_all(DB)
    for item in items:
        print(f"ItemName: {item.ItemName} | ItemCategory: {item.ItemCategory} | ItemPrice: {item.ItemPrice} | ItemQuantity: {item.ItemQuantity}")
    transition(lambda: admin_menu(DB))

def help_menu(instance:callable):
    print(" --------------- Trade-Engine, Help Menu ---------------- ")
    print(" For assistance, please contact: support@trade-engine.com")
    print(" -------------------------------------------------------- ")
    print("\n") # put a newline...
    transition(instance)