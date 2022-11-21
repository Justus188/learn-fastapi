from auth.hash import verify_password_hash
from auth.schemas import Token
from auth.token import create_token, decode_token
from auth.exceptions import CredentialsException, FailedLoginException

from database import get_db
from models import User

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

PATH_AUTH = '/login'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = PATH_AUTH[1:])

def get_user_by_username(username:str, db: Session):
    return db.query(User).filter(User.username == username).first()

def get_user_by_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user = get_user_by_username(decode_token(token), db)
    if not user:
        raise CredentialsException
    return user

router = APIRouter(tags = ['auth'])

@router.post(PATH_AUTH, response_model = Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(request.username, db)
    if not user:
        raise FailedLoginException
    if not verify_password_hash(request.password, user.hashed_password):
        raise FailedLoginException
    return {'access_token': create_token({"sub": user.username}), 'token_type': 'bearer'}