
"""
Contain models for database tables
"""


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime,LargeBinary
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    profile = relationship("UserProfile", uselist=False, back_populates="user")



class UserProfile(Base):
    __tablename__ = "user_profile"

    profile_id= Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.user_id"))
    dp=Column(LargeBinary)
    user = relationship("User", back_populates="profile")



# class UserTokens(Base):
#     __tablename__ = "user_token"

#     token_id= Column(Integer, primary_key=True, index=True)
#     user_id=Column(Integer, ForeignKey("users.user_id"))
#     expire_at=Column(DateTime)
#     created_at = Column(DateTime)
