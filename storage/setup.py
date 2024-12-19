# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# main setup file... connection establishment
# and so on...

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

os.makedirs('storage/database', exist_ok=True)
DB_URL        = "sqlite:///storage/database/storage.db"
ENGINE        = create_engine(DB_URL)

LOCAL_SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
BASE          = declarative_base() 

def get_db(): # -> Generator...
    DB = LOCAL_SESSION()
    try:
        yield DB
    finally:
        DB.close()

def init_db()->None:
    # importing the models registering with metadata...
    from models.user  import User
    from models.cart  import Cart
    from models.stock import Stock

    BASE.metadata.create_all(bind=ENGINE)