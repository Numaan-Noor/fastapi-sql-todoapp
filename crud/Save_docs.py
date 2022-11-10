import uuid
from sqlalchemy.orm import Session
from models.models import Docs, Personal


def check_by_id(db: Session, document_id: str, _user_id: str):
    try:
        response = db.query(Personal).filter(Personal.docs_id == document_id, Personal.user_id == _user_id).first()
        return response
    except Exception as err:
        return err


def save_docs(db: Session, user_id: str, id: str):
    uid = str(uuid.uuid4())
    _docs = check_by_id(db=db, document_id=id, _user_id=user_id)
    if not _docs:
        todo = Personal(id=uid, docs_id=id, user_id=user_id)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    else:
        return None


def get_saved_docs(db: Session, _user_id: str):
    response = db.query(Docs).filter(Personal.user_id == _user_id, Docs.id == Personal.docs_id).all()
    if response:
        return response
    else:
        return None
