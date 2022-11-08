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


@router.get("/all_data")
async def app(
        db: Session = Depends(get_db),
):
    _docs = all_docs.get_all_docs(db)
    return Response(status_code=200, message="all data", result=_docs).dict(exclude_none=True)


@router.post("/")
async def app(
        schema: TodoRequestSchema,
        db: Session = Depends(get_db),

):
    _docs = docs.create_docs(db)
    return Response(status_code=200, message="Created", result=_docs).dict(exclude_none=True)
