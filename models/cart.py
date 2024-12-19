# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# Cart model... - cart table -

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship,Session
from storage.setup import BASE

from models.stock import Stock

class Cart(BASE):
    __tablename__:str = "cart"
    CartID:int       = Column(Integer, primary_key=True)
    UserID:int       = Column(Integer, ForeignKey('users.UserID'))
    ItemID:int       = Column(Integer, ForeignKey('stocks.ItemID'))
    Quantity:int     = Column(Integer)
    ItemPrice:float  = Column(Float)

    owner = relationship("User", back_populates="cart")
    item  = relationship("Stock")

    @classmethod
    def add_to_cart(
        cls,
        DB:Session,
        UserID:int,
        ItemID:int,
        Quantity:int,
        Price:float):
        cart_item = DB.query(cls).filter_by(UserID=UserID, ItemID=ItemID).first()
        item = DB.query(Stock).filter_by(ItemID=ItemID).first()

        if not item:
            return f"Item with ID:{ItemID} not found."
        
        if item.ItemQuantity < Quantity:
            return f"Not enough stock for item {item.ItemName}. Available Quantity: {item.ItemQuantity}"

        if cart_item:
            # item exists... so increment it's value...
            cart_item.Quantity += Quantity
            cart_item.ItemPrice += Price
        else:
            # item does not exist... so create an entry for it...
            cart_item = cls(UserID=UserID, ItemID=ItemID, Quantity=Quantity, ItemPrice=Price)
            DB.add(cart_item)
        
        # update the stock quantity...
        item.ItemQuantity -= Quantity
        DB.commit()
        return cart_item
    
    @classmethod
    def delete_from_cart(
        cls,
        DB:Session,
        UserID:int,
        ItemID:int)->str:
        cart_item = DB.query(cls).filter_by(UserID=UserID, ItemID=ItemID).first()
        item      = DB.query(Stock).filter_by(ItemID=ItemID).first()
        if cart_item:
            # the item... does exist, do the necessary 😉
            if item:
                # return the item to stock...
                item.ItemQuantity += cart_item.Quantity

            # then delete the record...
            DB.delete(cart_item)
            DB.commit()
            return f"Item: {ItemID} removed from your cart. User account: {UserID}"
        else:
            return f"Item: {ItemID} not found in cart..."
        
    @classmethod
    def edit_quantity(
        cls,
        DB:Session,
        UserID:int,
        ItemID:int,
        NewQuantity:int)->str:
        cart_item = DB.query(cls).filter_by(UserID=UserID, ItemID=ItemID).first()
        if cart_item:
            price_per_unit = cart_item.ItemPrice / cart_item.Quantity
            cart_item.Quantity = NewQuantity
            cart_item.ItemPrice = price_per_unit * NewQuantity

            DB.commit()
            return f"Quantity for the item {ItemID} updated... thus price updated too: {cart_item.ItemPrice}."
        else:
            return f"Item not found... in cart."
        
    @classmethod
    def check_all(
        cls,
        DB:Session,
        UserID:int)->list:
        # Retrieve all items from the cart...
        cart_items = DB.query(cls).filter_by(UserID=UserID).all()
        return cart_items
    
    @classmethod
    def remove_all(
        cls,
        DB:Session,
        UserID:int, 
        message:str="All items removed from the cart.")->str:
        cart_items = DB.query(cls).filter_by(UserID=UserID).all()

        for cart_item in cart_items:
            DB.delete(cart_item)

        DB.commit()
        return message
        
    @classmethod
    def get_totals(
        cls,
        DB:Session,
        UserID:int)->float:
        cart_items = DB.query(cls).filter_by(UserID=UserID).all()

        total_sum = sum(cart_item.ItemPrice for cart_item in cart_items)
        return total_sum