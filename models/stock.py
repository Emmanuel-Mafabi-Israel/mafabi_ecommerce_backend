# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# Stocks model... - stocks table -

from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship,Session
from storage.setup import BASE

class Stock(BASE):
    __tablename__:str = "stocks"
    ItemID:int       = Column(Integer, primary_key=True)
    ItemName:str     = Column(String, unique=True, nullable=False)
    ItemCategory:str = Column(String, nullable=False)
    ItemQuantity:int = Column(Integer, nullable=False)
    ItemPrice:int    = Column(Float, default=0.0)

    # methods
    @classmethod
    def add_stock(
        cls,
        DB:Session,
        Name:str,
        Category:str,
        Price:float,
        Quantity:int):
        # first check if the item exists inside the database...
        # if it does - add to it's quantity count...
        db_item = DB.query(cls).filter_by(ItemName=Name, ItemCategory=Category).first()

        if db_item:
            db_item.ItemQuantity += Quantity
        else:
            # item does not exist...
            # then create new record...
            db_item = cls(ItemName=Name, ItemCategory=Category, ItemPrice=Price, ItemQuantity=Quantity)
            DB.add(db_item)

        DB.commit()
        return db_item

    @classmethod
    def rem_stock(
        cls,
        DB:Session,
        Name:str):
        item = DB.query(cls).filter_by(ItemName=Name).first()
        if item:
            # checking if the item exists first...
            DB.delete(item)
            DB.commit()
            return f"Removed item: {item.ItemName} from the stocks list."
        else:
            return f"Item... not found."

    @classmethod
    def change_price(
        cls, 
        DB:Session,
        Name:str, 
        NewPrice:int):
        # updating the price of an existing item in the database...
        item = DB.query(cls).filter_by(ItemName=Name).first()
        item.ItemPrice = NewPrice
        DB.commit()

    @classmethod
    def list_all(cls, DB:Session)->list:
        # listing all the items in the database...
        items = DB.query(cls).all()
        return items

    @classmethod
    def find_item(
        cls,
        DB:Session,
        Name:str):
        # find item
        item = DB.query(cls).filter_by(ItemName=Name).first()
        if item:
            return item
        else:
            return f"Item: {Name}, not found."
        
    @classmethod
    def delete_all(
        cls,
        DB:Session):
        # delete all - reset...
        items = DB.query(cls).all()

        for item in items:
            DB.delete(item)

        DB.commit()
        return "Succesfully deleted all items..."