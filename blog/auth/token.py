from datetime import datetime, timedelta
from jose import JWTError, jwt

from auth.exceptions import CredentialsException

SECRET_KEY = "d4d525285238445cf916a4914a642bef9907fe967da2ead78ee07e245ae770ce"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict, expires_delta: timedelta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    # Claims: https://pyjwt.readthedocs.io/en/latest/usage.html#encoding-decoding-tokens-with-hs256
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        username: str = payload.get('sub')
        # get other information from payload here
        if username is None:
            raise CredentialsException
        return username
    except JWTError:
        raise CredentialsException