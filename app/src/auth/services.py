from sqlalchemy import exc
from typing import Optional, Dict
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword

from src.config import get_settings
from src.auth.models import UserInDB
from src.database import Session, Users

settings = get_settings()

redirect_exception = HTTPException(
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    detail="Token Expired",
    headers={"Location": "/"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authorized",
    headers={"WWW-Authenticate": "Bearer"},
)


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl=tokenUrl, scopes=scopes))
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        try:
            authorization: str = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(authorization)
            if not authorization or scheme.lower() != "bearer":
                raise credentials_exception
            payload = jwt.decode(param, settings.SECRET_KEY, algorithms=[settings.JWT_ALGO])
            username: str = payload.get("sub", None)
            if username is None:
                raise credentials_exception
        except ExpiredSignatureError:
            raise redirect_exception
        except JWTError:
            raise credentials_exception
        return param


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str) -> UserInDB | bool:
    with Session.begin() as session:
        user_row: Users = session.query(Users).filter_by(username=username).first()
        if not user_row:
            return False
        return UserInDB(username=user_row.username, hashed_password=user_row.hashed_password, role=user_row.role)


def authenticate_user(username: str, password: str):
    user: UserInDB = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGO)


def verify_token(authorization: str):
    if not authorization:
        return False

    scheme, param = get_authorization_scheme_param(authorization)
    if scheme.lower() != "bearer":
        return False

    try:
        payload = jwt.decode(param, settings.SECRET_KEY, algorithms=[settings.JWT_ALGO])
        username: str = payload.get("sub", None)
        if not username:
            return False
        return True
    except ExpiredSignatureError:
        return False
    except JWTError:
        return False


def add_user(user: UserInDB):
    try:
        with Session.begin() as session:
            session.add(Users(username=user.username, hashed_password=user.hashed_password, role=user.role))
    except exc.IntegrityError as e:
        ...
