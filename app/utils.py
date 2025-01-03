from passlib.context import CryptContext

#hasing password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

def hash(password:str):
    return pwd_context.hash(password)


#set up a route or path operation that allows you to fetch 
#retrive informaiton about a user based off their ID
#1. part of the authentication process --if JWT tokens are used -- endpoint to let you returve information about your own account
#2. retive yours profile if you want to view it 

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)