# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# MAIN MENU INTERFACES and RELATED FUNCTIONS

import sys
from dependencies.helpers import clear_screen, transition, user_selection, validate_email
from dependencies.interfaces.admin import admin_menu, help_menu

from sqlalchemy.orm import Session

def main_menu(DB:Session):
    from dependencies.interfaces.user import login, register

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
        transition(lambda: login(DB))
    elif selection == 2:
        transition(lambda: register(DB))
    elif selection == 3:
        transition(lambda: admin_menu(DB))
    elif selection == 4:
        # help menu
        transition(lambda: help_menu(lambda: main_menu(DB)))
    elif selection == 8:
        clear_screen()
        main_menu(DB)
    else:
        print("Goodbye!")
        sys.exit()