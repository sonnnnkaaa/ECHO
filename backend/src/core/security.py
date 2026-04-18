from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta, datetime
from .config import settings


pwd_context = CryptContext(schemes=settings.PASS_SCHEMES)

def verify_password(typed_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(typed_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires: timedelta) -> str:
    to_encode = data.copy()
    if expires:
        expire = datetime.timezone.utc.now() + expires
    else:
        expire = datetime.timezone.utc.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.timezone.utc.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None