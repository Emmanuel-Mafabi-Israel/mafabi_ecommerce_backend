# GLORY BE TO GOD,
# ECOMMERCE BACKEND SYSTEM,
# BY ISRAEL MAFABI EMMANUEL
# Users model... - users table -

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship,Session
from storage.setup import BASE

import hashlib

# the users table
class User(BASE):
    __tablename__:str = "users"
    UserID:int        = Column(Integer, primary_key=True)
    UserName:str      = Column(String, unique=False, nullable=False)
    UserEmail:str     = Column(String, unique=True, nullable=False)
    UserPassword:str  = Column(String, unique=False, nullable=False)
    UserPasswordB:str = Column(String, unique=False, nullable=False)

    cart = relationship("Cart", back_populates="owner")

    # methods
    @classmethod
    def create_account(
        cls, 
        DB:Session,
        Name:str,
        Email:str,
        hashPassword:str,
        passwordBackup):
        db_user = cls(UserName=Name, UserEmail=Email, UserPassword=hashPassword, UserPasswordB=passwordBackup)
        DB.add(db_user)
        DB.commit()
        DB.refresh(db_user)

        return db_user
    
    @classmethod
    def delete_account(
        cls, 
        DB:Session,
        Email:str)->None:
        user = DB.query(cls).filter_by(UserEmail=Email).first()
        DB.delete(user)
        DB.commit()

    @classmethod
    def hash_password(cls, password:str)->str:
        # encode the text
        pass_key:bytes = password.encode('utf-8')
        sha256         = hashlib.sha256() # creating the hash object...
        sha256.update(pass_key) # update the sha256 object with the encoded text...

        return sha256.hexdigest() # return now the hashed text...

    @classmethod
    def change_username(
        cls,
        DB:Session,
        UserID:int,
        NewUserName:str):
        user = DB.query(cls).filter_by(UserID=UserID).first()

        if user:
            # user exists...
            oldUserName = user.UserName
            user.UserName = NewUserName
            DB.commit()
            return f"Succesfully changed your Name from: {oldUserName} to: {user.UserName}"
        else:
            # the user does not exist
            return f"User with the name: {user.UserName} not found."
        
    @classmethod
    def change_email(
        cls,
        DB:Session,
        UserID:int,
        NewUserEmail:str):
        # before any changes... let's check if the email also
        # is existing...
        existing_user = DB.query(cls).filter_by(UserEmail=NewUserEmail).first()
        if existing_user:
            return f"Email address [{NewUserEmail}] is already taken. Please choose another email."

        user = DB.query(cls).filter_by(UserID=UserID).first()
        if user:
            # user exists...
            oldUserEmail = user.UserEmail
            user.UserEmail = NewUserEmail
            DB.commit()
            return f"Succesfully changed your email address from: {oldUserEmail} to: {user.UserEmail}"
        else:
            # the user does not exist
            return f"User with the email: {user.UserEmail} not found."
        
    @classmethod
    def change_password(
        cls,
        DB:Session,
        UserID:int,
        NewUserPassword:str):
        user = DB.query(cls).filter_by(UserID=UserID).first()
        if user:
            # user exists...
            user.UserPassword = cls.hash_password(NewUserPassword)
            user.UserPasswordB = NewUserPassword
            DB.commit()
            return f"Succesfully changed your account password."
        else:
            # the user does not exist
            return f"User with the email: {user.UserEmail} not found."