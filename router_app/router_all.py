from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.Auth import get_user_credentials
from schemas.schemas import Response, TodoRequestSchema, updateSchema
from database.database import SessionLocal
from crud import docs, all_docs
from crud.all_docs import get_all_docs

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.patch("/ ")
async def Bookmark(
        id: str,
        db: Session = Depends(get_db),
        user: dict = Depends(get_user_credentials)
):
    user_id = user.get("id")
    _docs = all_docs.bookmark_docs(db, id, user_id)
    if not _docs:
        return Response(status_code=400, message="Invalid ID Or It Is Already Bookmarked").dict()
    return Response(status_code=200, message="Changed", result=_docs).dict(exclude_none=True)


@router.patch("/")
async def remove_bookmark(
        id: str,
        db: Session = Depends(get_db),
        user: dict = Depends(get_user_credentials)
):
    user_id = user.get("id")
    _docs = all_docs.un_docs(db, id, user_id)
    if not _docs:
        return Response(status_code=400, message="Invalid ID Or It Is Not Bookmarked").dict()
    return Response(status_code=200, message="Changed", result=_docs).dict(exclude_none=True)


@router.get("/")
async def All_Bookmarked(
        db: Session = Depends(get_db),
        _user: dict = Depends(get_user_credentials),
):
    _user_id = _user.get("id")
    _docs = all_docs.get_bookmark_docs(db, _user_id)
    if not _docs:
        return Response(status_code=400, message="Invalid token").dict()
    return Response(status_code=200, message="Bookmarked data", result=_docs).dict(exclude_none=True)



