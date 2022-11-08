from fastapi import APIRouter, Depends, HTTPException
from rest_framework import status
from sqlalchemy.orm import Session
from schemas.Auth_Schemas import UserInDB, Token
from schemas.schemas import Response
from database.database import SessionLocal
from auth.Auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_username
from datetime import timedelta
from auth import Auth
from fastapi.security import HTTPBasic

router = APIRouter()
security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
async def create(request: UserInDB, db: Session = Depends(get_db)):
    _signup = Auth.create_user(db, request)
    return Response(status_code=200, message="Created").dict(exclude_none=True)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: HTTPBasic = Depends(get_current_username)
):
    if not form_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}, )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


