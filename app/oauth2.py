from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import * 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#secret_key, algorithm,  experiation time

expiration_time = 30 #mins

def create_access_token(data:dict, user_id:int ):
    to_encode = data.copy()
    to_encode["user_id"] = user_id
    expire = datetime.utcnow() + timedelta(minutes=expiration_time)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
#ensure that all the data passed in the token is actally there
def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
#call verify access 
def get_current_user (token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    return user_id

    return verify_access_token(token, credentials_exception)