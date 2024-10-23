from datetime import datetime, timedelta
import pdb

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from passlib.context import CryptContext
import jwcrypto
from config import config_environment
from config.exceptions import AuthError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
env = config_environment.get_environment_variables()



def create_access_token(subject: dict, expires_delta: timedelta = None):
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(payload, env.SECRET_KEY, algorithm=ALGORITHM)
    expiration_datetime = expire.strftime(env.DATETIME_FORMAT)
    return encoded_jwt, expiration_datetime, expire


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, env.SECRET_KEY, algorithms=ALGORITHM)
        return decoded_token if decoded_token["exp"] >= int(round(datetime.now().timestamp())) else None
    except Exception as e:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise AuthError(detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid