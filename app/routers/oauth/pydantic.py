from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import date
from .enum import Gender
# creating the pydantic for the usersignup
class create_user(BaseModel):
    username:str
    email:EmailStr
    password:str
    dob:Optional[date]=None
    gender:Optional[Gender]=None
    profile_pic:Optional[str]=None
   




class verifyed_otp(BaseModel):
    email:EmailStr
    otp:str


# create login





class tockendata(BaseModel):
    token :str



class update_user(BaseModel):
   profile_pic:Optional[str]=None