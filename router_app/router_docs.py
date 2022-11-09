from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.Auth import get_user_credentials
from schemas.schemas import Response, TodoRequestSchema, updateSchema
from database.database import SessionLocal
from crud import docs

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def app(
        schema: TodoRequestSchema,
        user: dict = Depends(get_user_credentials),
        db: Session = Depends(get_db),

):
    # schema_in = schema.dict()
    # schema_in.update({"user_id": user.get("id")})
    _user_id = user.get("id")
    _docs = docs.create_docs(db, _user_id, schema)
    return Response(status_code=200, message="Created", result=_docs).dict(exclude_none=True)


@router.get("/all")
async def app(
        db: Session = Depends(get_db),
        _user: dict = Depends(get_user_credentials),
):
    _user_id = _user.get("id")
    _docs = docs.get_docs(db, _user_id)
    if not _docs:
        return Response(status_code=400, message="Invalid token or id").dict()
    return Response(status_code=200, message="all data", result=_docs).dict(exclude_none=True)


# @router.get("/", dependencies=[Depends(JWTBearer())])
@router.get("/")
async def app(
        id: str,
        user: dict = Depends(get_user_credentials),
        db: Session = Depends(get_db)):
    _user_id = user.get("id")
    _docs = docs.get_docs_by_id(db, id, _user_id)
    if not _docs:
        return Response(status_code=400, message="Invalid token or id").dict()
    return Response(status_code=200, message="get by id", result=_docs).dict(exclude_none=True)


@router.patch("/")
async def app(request: updateSchema,
              user: dict = Depends(get_user_credentials),
              db: Session = Depends(get_db)):
    user_id = user.get("id")
    _docs = docs.update_docs(db, document_id=request.id, title=request.title,
                             task=request.task, user_id=user_id)
    if not _docs:
        return Response(status_code=400, message="Invalid token or id").dict()
    return Response(status_code=200, message="update", result=_docs).dict(exclude_none=True)


@router.delete("/")
async def app(id: str,
              user: dict = Depends(get_user_credentials),
              db: Session = Depends(get_db)):
    user_id = user.get("id")
    _docs = docs.remove_docs(db, document_id=id, user_id=user_id)
    if not _docs:
        return Response(status_code=400, message="Invalid token or id").dict()
    else:
        return Response(status_code=200, message="deleted", result=_docs).dict(exclude_none=True)
