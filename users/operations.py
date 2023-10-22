"""
Contains functions to fetch and insert users data in database
"""


from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas,utils


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email_or_phone(db: Session, email: str,phone:str):
    return db.query(models.User).filter(or_(models.User.email == email,models.User.phone==phone)).first()

def validate_user(db: Session, username: str,password:str):
    user= db.query(models.User).filter(or_(models.User.email == username,models.User.phone==username)).first()
    if not user:
        return False
    is_valid=utils.verify_password(password=password,hashed_pass=user.password)
    if not is_valid:
        return False
    return user

def create_user(db: Session, user: schemas.UserCreate):
    user=dict(user)
    user['password']=utils.get_hashed_password(user["password"])
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def upload_user_dp(db:Session, dp:bytes,user_id: int):
    profile=models.UserProfile(dp=dp,user_id=user_id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile