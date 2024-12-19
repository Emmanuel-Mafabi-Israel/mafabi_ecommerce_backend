# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# main - entry point

from storage.setup import get_db, init_db

from dependencies.interfaces.main_menu import main_menu

def main()->None:
    # initialize the database... 
    init_db()
    DB = next(get_db())    
    # start...
    main_menu(DB)

if __name__ == "__main__":
    main()