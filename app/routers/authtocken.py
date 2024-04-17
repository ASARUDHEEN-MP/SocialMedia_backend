from datetime import datetime, timedelta,timezone
from jose import JWTError, jwt

from .oauth import models, pydantic
from .. import database
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
# pip install python-jose

#  expire time of the tocken
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# keys of the tocken should be in env hide it
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


# it's used for handling authentication using OAuth 2.0 with the password grant type.( verify the credentials)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# create function to have the expire time of the tocken
def expire_time():
  create_expire_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  if create_expire_time:
    expire = datetime.now(timezone.utc) + create_expire_time
    return expire

# create a funtion to create the tocken
def create_tocken(data:dict):
    # take a copy of the data and encode it
    to_encode=data.copy()
    # calling the expire function
    expiretime=expire_time()
    if not expiretime:
       expiretime = datetime.now(timezone.utc) + timedelta(minutes=60)
    # updating the expire time with the encode to create tocken
    to_encode.update({"exp":expiretime})
    # creating the jwt tocken
    encode_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # returning the tocken to the login function
    return encode_jwt


# function to verify the token which come from the current_user function
def verify_token(token:str,credtional_expetion):
  try:
      payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
      id : str = payload.get("user_id")
      if id is None:
         raise credtional_expetion
      tocken_data=id

      return tocken_data
      
     


  except  JWTError:
     raise HTTPException(
        status_code=401,
        detail="Token is expired or invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )
  
  

   




# GET THE CURRENT USER WHEN THEY LOGIN CHECKING WITH TOCKEN AND CHECKING THE USER WITH USER_ID
def current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.getdb)):
   
  #  This header is typically used in authentication challenges to indicate that the client needs to provide a Bearer token to access the requested resource.
   credtional_expetion=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
   verifytoken=verify_token(token,credtional_expetion)
   users=db.query(models.User).filter(models.User.id==verifytoken).first()
   

   return users
   
   
   

# here we can decode the tocken and check the user_is 
def validate_the_user(db:Session,token:str=Depends(oauth2_scheme),):
   try:
      payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
      user_id=payload.get("user_id")
      expire:datetime=payload.get("exp")
      expire_datetime = datetime.fromtimestamp(expire)

      if expire_datetime < datetime.now():
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired. Please try with a new one.",
         )
      users_data=db.query(models.User).filter(models.User.id==user_id).first()
      
      return users_data
      
      

   except JWTError:
      raise HTTPException(
        status_code=401,
        detail="Token is expired or invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )