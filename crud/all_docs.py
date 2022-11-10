import uuid
from sqlalchemy.orm import Session
from models.models import Docs, Personal


def get_all_docs(db: Session):
    response = db.query(Docs).all()
    return response


def get_docs_by_id(db: Session, document_id: str, _user_id: str):
    try:
        response = db.query(Docs).filter(Docs.id == document_id, Docs.user_id == _user_id).first()
        return response
    except Exception as err:
        return err


def bookmark_docs(db: Session, id: str, user):
    _docs = get_docs_by_id(db=db, document_id=id, _user_id=user)
    if _docs:
        _docs.bookmark = True
        db.commit()
        db.refresh(_docs)
        return _docs
    else:
        return None


def un_docs(db: Session, id: str, user):
    _docs = get_docs_by_id(db=db, document_id=id, _user_id=user)
    if _docs:
        _docs.bookmark = False
        db.commit()
        db.refresh(_docs)
        return _docs
    else:
        return None


def get_bookmark_docs(db: Session, _user_id: str):
    try:
        response = db.query(Docs).filter(Docs.user_id == _user_id, Docs.bookmark == True).all()
        return response
    except Exception as err:
        return err

