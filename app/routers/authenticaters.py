from fastapi import APIRouter,Depends,HTTPException,status
from  ..database import engine,getdb
from sqlalchemy.orm import Session
from .. import passwodhashed,email,pydantic,models
from . import authtocken
from cachetools import TTLCache
from datetime import datetime, timedelta


router=APIRouter()

#_____________________________________________Signu of the user_____________________________________
# TTLCache with a 1-minute expiration time
cache = TTLCache(maxsize=1000, ttl=60)

# function of signup 
@router.post('/signup')
async def signup(user:pydantic.create_user,db:Session=Depends(getdb)):
    try:
        # check the email is exist or not
        existing_user = db.query(models.User).filter(models.User.email==user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Email already exists")
        # checking the passwod is length is 6
        if len(user.password)<6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Password length must be at least 6 characters ")
        # CHECKING THE PASSWORD HAVE UPPERCASE MORE THAN ONE TIME
        if sum(1 for i in user.password if i.isupper())<2:
         
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="password should need atleast More than one Uppercase")
        # creating the hashpassword
        userpassword=passwodhashed.create_password(user.password)
        # sending the otp to mail for verification of user
        send_mail=email.createotpforuser(user.email)
        emailname=user.email
       
        # if there is otp returing from the send_email it will go with this condition else it will return the else case
        if 'otp' in send_mail:
            #  store the userame,password also otp in cache and also expire time of 1 min
             cache[(emailname)] = ({"otp": send_mail['otp'], "password": userpassword}, datetime.now() + timedelta(minutes=10))
             return {"message":"successfully send the otp to the mail"}
        else:
            return send_mail

        
    except Exception as e:
        
        raise HTTPException(status_code=400, detail=f"Duplicate entry. Error: {str(e)}")
    


# function after successfully send the otp and verifiying the otp and commiting to the database
@router.post("/verify-otp")
async def verify_otp(otp_user:pydantic.verifyed_otp,db:Session=Depends(getdb)):
    try:
        key = (otp_user.email)
        stored_data = cache.get(key)
        if stored_data:
                # retrive the data from cache and cache will be clear or expire with in 10 min
                otp = stored_data[0]["otp"]
                password=stored_data[0]["password"]
                email=otp_user.email
                # checking the otp in cache and mail to user is matching
                if otp !=otp_user.otp:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Otp your enter is not match")
                #  after the checking we can add to the database 
                users=models.User(email=email,hashed_password=password,is_active=True,role="user")
                db.add(users)
                db.commit()
                # giving the response to the user when it successfull
                return {"message":"succesfully register your account"}
                
                
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="otp your return is expired please resignup")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"error is founded {e}")



#_____________________________________________Login_____________________________________
@router.post("/login")
def login(users:pydantic.get_user,db:Session=Depends(getdb)):
    try:
        # checking the user with this email is exist or not
        existing_user=db.query(models.User).filter(models.User.email==users.email).first()
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this email not found")
        # checking the user with this email is active 
        if existing_user.is_active == False:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"user with this email{users.email} is not active contact the admin")
        # checking the password that user enter is maching to the db hashed password
        if not passwodhashed.verifythepasswod(users.password,existing_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
        # if the user is exixit and the user is not admin it enter into this condition
        if existing_user.role =="user":
            # create the tocken for the user
            jwt_tocken=authtocken.create_tocken({"data":existing_user.id})
            
            if not jwt_tocken:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed to login")
            return jwt_tocken
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"error {e}")


    
      




   