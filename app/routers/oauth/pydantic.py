from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import date
from .enum import Gender
# creating the pydantic for the usersignup
class create_user(BaseModel):
    username:str
    email:EmailStr
    password:str
   
   




class verifyed_otp(BaseModel):
    email:EmailStr
    otp:str


# create login





class tockendata(BaseModel):
    token :str



class update_user(BaseModel):
   profile_pic:Optional[str]=None

class signupresponse(BaseModel):
    id:int


class personaldata(BaseModel):
    id:int
    dob:Optional[date]=None
    gender:Optional[Gender]=None
    profile_pic:Optional[str]=None

class facebook(BaseModel):
    email:str
    username:str
    fromwhere:str
