from fastapi import APIRouter,Depends,HTTPException,status
from . import email, passwodhashed
from .models import User
from  ...database import engine,getdb
from sqlalchemy.orm import Session
from . import pydantic
from .. import authtocken
from cachetools import TTLCache
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


router=APIRouter()

#_____________________________________________Signu of the user_____________________________________
# TTLCache with a 1-minute expiration time
cache = TTLCache(maxsize=1000, ttl=60)

# function of signup 
@router.post('/signup')
async def signup(user:pydantic.create_user,db:Session=Depends(getdb)):
    try:
        # check the user is already exisit
        
        # check the user is already exisit
        
        existing_user = db.query(User).filter(User.username == user.username).first()
        
        if existing_user:
            print("yes")
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Uername is taken")
          # check the email is exist or not
        existing_email = db.query(User).filter(User.email==user.email).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Email already exists")
        # checking the passwod is length is 6
        if len(user.password)<6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Password length must be at least 6 characters ")
        # CHECKING THE PASSWORD HAVE UPPERCASE MORE THAN ONE TIME
        if sum(1 for i in user.password if i.isupper())<2:
         
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="password should need atleast More than one Uppercase")
        # creating the hashpassword
        print("hello")
        userpassword=passwodhashed.create_password(user.password)
        # sending the otp to mail for verification of user
        print("ll")
        send_mail=email.createotpforuser(user.email)
        emailname=user.email
        print("email")
       
        # if there is otp returing from the send_email it will go with this condition else it will return the else case
        if 'otp' in send_mail:
            
            #  store the userame,password also otp in cache and also expire time of 1 min
             cache[(emailname)] = ({"otp": send_mail['otp'], "password": userpassword,"username":user.username}, datetime.now() + timedelta(minutes=10))
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
                username=stored_data[0]["username"]
                email=otp_user.email
                # checking the otp in cache and mail to user is matching
                if otp !=otp_user.otp:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Otp your enter is not match")
                #  after the checking we can add to the database 
                users=User(username=username,email=email,hashed_password=password,is_active=True,role="user")
                db.add(users)
                db.commit()
                # giving the response to the user when it successfull
                return {"message":"succesfully register your account"}
                
                
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="otp your return is expired please resignup")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"error is founded {e}")



#_____________________________________________Login_____________________________________
@router.post("/login",status_code=status.HTTP_202_ACCEPTED)
def login(users:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(getdb)):
    # OAUTHPASSWORDREQUESTFORM has imbuild form of password and username
    try:
        # checking the user with this email is exist or not
        print("hello")
        existing_user = db.query(User).filter(User.username == users.username).first()
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this USERNAME not found")
        # checking the user with this email is active 
        if existing_user.is_active == False:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"user with this email{users.email} is not active contact the admin")
        # checking the password that user enter is maching to the db hashed password
        if not passwodhashed.verifythepasswod(users.password,existing_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
        # if the user is exixit and the user is not admin it enter into this condition
        if existing_user.role =="user":
            # create the tocken for the user
            jwt_tocken=authtocken.create_tocken(data={"user_id":existing_user.id})
            
            if not jwt_tocken:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="failed to login")
            return {
                "tocken":jwt_tocken,
                "tockentype":"bearer"
            }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"error {e}")
    


#  profile of the user check the tocken and take the user_id from user
@router.get("/profile")
async def current_profile(db:Session=Depends(getdb),currentuser: str = Depends(authtocken.current_user)):
    
    
    
    
    return 12123

@router.get("/test")
async def current_profile(token : str  ,db:Session=Depends(getdb)):
    print("kndsa")
    users =  authtocken.validate_the_user(db,token)
    if  not users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="not authenticated")
    return users

def update_user(db:Session,userupdat:pydantic.update_user,users:User):
    users.profile_pic=userupdat.profile_pic or users.profile_pic
    db.commit()
    return "success"




@router.put("/update")
async def updateprofile(token:str,userupdat:pydantic.update_user,db:Session=Depends(getdb)):
    users =  authtocken.validate_the_user(db,token)
    print(userupdat,"hiiii hlo boys")
    db_data=update_user(db,userupdat,users)
    return db_data

    
      



