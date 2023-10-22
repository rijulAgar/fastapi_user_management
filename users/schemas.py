"""
Contains schemas of request and response data for users

"""



from pydantic import BaseModel,validator,Field
import re

class UserBase(BaseModel):
    email: str  = Field(max_length=300,pattern='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    full_name:str 
    phone:str  = Field(pattern='^\d{10}$') # we can adjust the regex pattern as needed

    # @validator('email')
    # def matches_regex(cls, v):
    #     regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    #     print(v)
    #     if not re.match(regex, v):
    #         raise ValueError("invalid email")
    #     return v


class UserCreate(UserBase):
    password: str= Field(min_length=8,max_length=20,pattern='.*\W')
    

class User(UserBase):
    user_id: int
    is_active: bool
    class Config:
        from_attributes = True


class UserDetail(User):
    profile_picture:bytes=None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username:str
    password: str


class UserRegistrationSuccess(BaseModel):
    is_active:bool = True
    message:str = "User Register Successfully"


class UserToken(BaseModel):
    token:str


class Token(BaseModel):
    access_token: str
    token_type: str

