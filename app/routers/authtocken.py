from datetime import datetime, timedelta,timezone
from jose import JWTError, jwt
# pip install python-jose

#  expire time of the tocken
ACCESS_TOKEN_EXPIRE_MINUTES = 10
# keys of the tocken should be in env hide it
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

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
       expiretime = datetime.now(timezone.utc) + timedelta(minutes=15)
    # updating the expire time with the encode to create tocken
    to_encode.update({"exp":expiretime})
    # creating the jwt tocken
    encode_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # returning the tocken to the login function
    return encode_jwt

    