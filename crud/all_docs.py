import uuid
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, HTTPBasic
from rest_framework.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from typing import Union
from fastapi import status, HTTPException, Depends, Request
from jose import JWTError
import uuid
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import schemas.schemas
from auth.Auth import todo_user
from models.models import Docs


def get_all_docs(db: Session):
    response = db.query(Docs).all()
    return response

# def create_docs(db: Session, Document: dict):
#     uid = str(uuid.uuid4())
#     Document.update(id=uid)
#     todo = schemas.schemas.TodoAddSchema(**Document)
#     _docs = Docs(**todo.dict())
#     db.add(_docs)
#     db.commit()
#     db.refresh(_docs)
#     return _docs

