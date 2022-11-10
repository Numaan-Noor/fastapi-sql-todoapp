from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.Auth import get_user_credentials
from schemas.schemas import Response, TodoRequestSchema, updateSchema
from database.database import SessionLocal
from crud import docs, all_docs, Save_docs
from crud.all_docs import get_all_docs

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/All")
async def All_Docs_Without_Auth(
        db: Session = Depends(get_db),
):
    _docs = all_docs.get_all_docs(db)
    return Response(status_code=200, message="all data", result=_docs).dict(exclude_none=True)


@router.post("/")
async def Save_Docs(
        id: str,
        user: dict = Depends(get_user_credentials),
        db: Session = Depends(get_db),

):
    _user_id = user.get("id")
    _docs = Save_docs.save_docs(db, _user_id, id)
    if not _docs:
        return Response(status_code=400, message="Invalid ID Or Data is Already Present").dict()
    return Response(status_code=200, message="Created").dict(exclude_none=True)


@router.get("/")
async def Saved_Docs(
        db: Session = Depends(get_db),
        _user: dict = Depends(get_user_credentials),
):
    _user_id = _user.get("id")
    _docs = Save_docs.get_saved_docs(db, _user_id)
    if not _docs:
        return Response(status_code=400, message="No Data Found Or Invalid Token").dict()
    return Response(status_code=200, message="all data", result=_docs).dict(exclude_none=True)
