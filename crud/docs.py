import uuid
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import validator
from auth.Auth import todo_user
from models.models import Docs


def get_docs(db: Session, _user_id: str):
    response = db.query(Docs).filter(Docs.user_id == _user_id).all()
    if response:
        return response
    else:
        return None


def get_docs_by_id(db: Session, document_id: str, _user_id: str):
    try:
        response = db.query(Docs).filter(Docs.id == document_id, Docs.user_id == _user_id).first()
        return response
    except Exception as err:
        return err


# def create_docs(db: Session, Document: dict):
#     uid = str(uuid.uuid4())
#     Document.update(id=uid)
#     todo = schemas.schemas.TodoAddSchema(**Document)
#     _docs = Docs(**todo.dict())
#     db.add(_docs)
#     db.commit()
#     db.refresh(_docs)
#     return _docs

def create_docs(db: Session, user_id: str, todo_data):
    uid = str(uuid.uuid4())
    todo = Docs(id=uid, title=todo_data.title,
                task=todo_data.task, user_id=user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def remove_docs(db: Session, document_id: str, user_id: str):
    _docs = get_docs_by_id(db=db, document_id=document_id, _user_id=user_id)
    if _docs:
        db.delete(_docs)
        db.commit()
    else:
        return None


def update_docs(db: Session, document_id: str, title: str, task: str, user_id: str):
    _docs = get_docs_by_id(db=db, document_id=document_id, _user_id=user_id)
    if _docs:
        _docs.user_id = user_id
        _docs.title = title
        _docs.task = task
        db.commit()
        db.refresh(_docs)
        return _docs
    else:
        return None
