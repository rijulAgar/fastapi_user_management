from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Security,Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import ValidationError
from users import operations, models, schemas
from users.database import SessionLocal, engine
from users.utils import create_access_token,decode_access_token

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  Handling error from Field validation in schema
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


# Return User after token validation
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.User:
    token_data=decode_access_token(token)
    user= operations.get_user(db,token_data["user_id"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user


# Login API
@app.post("/login/", response_model=schemas.Token)
def user_login(user: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    try:
        db_user = operations.validate_user(db, user.username,user.password)
        if not db_user:
            raise Exception("Incorrect username or password")
        access_token=create_access_token({"user_id":db_user.user_id})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))


# User Registration API
@app.post("/user/", response_model=schemas.UserRegistrationSuccess)
def create_user(user: schemas.UserCreate= Depends(), dp: UploadFile= File(...), db: Session = Depends(get_db)):
    try:
        db_user = operations.get_user_by_email_or_phone(db, email=user.email,phone=user.phone)
        if db_user:
            raise Exception("Email or phone number already registered")
        
        
        if dp.content_type not in ['image/jpeg','image/png']:
            raise Exception("File should be image")
        if dp.size/1024**2 >2 : #2mb validation
            raise Exception("FIle size should be less then 2MB")
            """
            we can place after user creation so that user create and can login , profile picture can be update later, it depend on requirements
            """

        # new_user=operations.create_user(db=db, user=user)
        # dp_data=operations.upload_user_dp(db=db,dp=dp.file.read(),user_id=new_user.user_id)
        return schemas.UserRegistrationSuccess()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

 
# Get Detail of login user
@app.get("/user/", response_model=schemas.UserDetail)
def get_user(user: Annotated[schemas.User, Security(get_current_user)]):
    return schemas.UserDetail(email=user.email,
                full_name=user.full_name,
                phone=user.phone,
                user_id=user.user_id,
                is_active=user.is_active,
                profile_picture=user.profile.dp.decode(errors='ignore') if user.profile else b''
                )