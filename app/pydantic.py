from pydantic import BaseModel,EmailStr

# creating the pydantic for the usersignup
class create_user(BaseModel):
    email:EmailStr
    password:str


class verifyed_otp(BaseModel):
    email:EmailStr
    otp:str


# create login
class get_user(create_user):
    pass
