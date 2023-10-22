"""
Contain function for password encrption and jwt token regarding operations
"""

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from config import settings
from pydantic import ValidationError
from fastapi import HTTPException,status

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRES_IN
ALGORITHM = settings.JWT_ALGORITHM
JWT_SECRET_KEY = settings.JWT_PRIVATE_KEY 

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# password should be save in encrypted form 
def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

# function to validate password
def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(user: dict, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "user_id": user["user_id"]}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_access_token(token:str):
    try:
        token_data = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        
        if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data
"""
        We can store access token and refresh token in database as per business requirements
"""