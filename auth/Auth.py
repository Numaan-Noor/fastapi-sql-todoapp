import uuid
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, HTTPBasic
from rest_framework.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from typing import Union
from fastapi import status, HTTPException, Depends, Request
from jose import JWTError
import jwt
from database.database import SessionLocal
from models.models import User
from schemas.Auth_Schemas import UserInDB, pwd_context, TokenData, SignUpSchema

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30000


def token_response(token: str):
    return {
        "access_token": token
    }


security = HTTPBasic()


def get_db():
    db = SessionLocal()
    return db


def get_password_hash(password: str):
    password = pwd_context.hash(password)
    return password


def create_user(db: Session, signUp: UserInDB):
    uid = str(uuid.uuid4())
    password = get_password_hash(password=signUp.password)
    _signup = User(id=uid, username=signUp.username, email=signUp.email, password=password)
    db.add(_signup)
    db.commit()
    db.refresh(_signup)
    return _signup


def verify_password(password: str, hashed_password):
    response = pwd_context.verify(password, hashed_password)
    return response


def get_user(username: str, signup_data: SignUpSchema, db: Session = Depends(get_db)):
    if username in db:
        user = db.query(User).filter(User.username == signup_data.username).first()
        return User(**user.username)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_username(
        signup_data: SignUpSchema,
        db: Session = Depends(get_db)
):
    # TODO: Check credentials in database else throw an error
    user = db.query(User).filter(User.username == signup_data.username).first()
    if not user or not verify_password(signup_data.password, user.password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    response = {"user_name": user.username, "password": user.password, "id": user.id}
    return response


async def get_current_active_user(current_user: User = Depends(get_current_username)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def todo_user(token: str):
    try:
        d_token = jwt.decode(
            jwt=token,
            key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
            algorithms="HS256"
        )
        user = d_token.get("sub")
        return user
    except Exception as err:
        print({"err": err})
        return None


def verify_jwt(token: str) -> bool:
    try:
        payload = todo_user(token)
        if not payload:
            return False
        return True
    except Exception as err:
        print({"error": err})


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


def get_user_credentials(
        creds: dict = Depends(JWTBearer())
):
    response = todo_user(str(creds))
    return response
