from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
import config

SECRET_KEY = config.SECRET_KEY

ALGORITHM = config.ALGORITHM
bearer_scheme = HTTPBearer()


def decode_bearer_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


def encode_bearer_token(email: str) -> dict:
    try:
        now = datetime.utcnow()
        access_token_expires = now + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {"email": email, "exp": access_token_expires}
        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
