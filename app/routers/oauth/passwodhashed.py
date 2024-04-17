from passlib.context import CryptContext



# Create an instance of CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_password(password):
    return pwd_context.hash(password)

# Verify the password from user and crosscheck the user enter the password and hashed password
def verifythepasswod(pydantic_password,passwordfromdb):
    return pwd_context.verify(pydantic_password,passwordfromdb)