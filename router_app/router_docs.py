from fastapi_pagination import Page, add_pagination, paginate, Params
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.Auth import get_user_credentials
from schemas.schemas import Response, TodoRequestSchema, updateSchema
from database.database import SessionLocal
from crud import docs, all_docs, Save_docs

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ ")
async def post_todo(
        schema: TodoRequestSchema,
        user: dict = Depends(get_user_credentials),
        db: Session = Depends(get_db),

):
    # schema_in = schema.dict()
    # schema_in.update({"user_id": user.get("id")})
    _user_id = user.get("id")
    _docs = docs.create_docs(db, _user_id, schema)
    return Response(status_code=200, message="Created", result=_docs).dict(exclude_none=True)


@router.get("/all", response_model=Page)
async def get_all_todo(
        db: Session = Depends(get_db),
        _user: dict = Depends(get_user_credentials),
        params: Params = Depends()
):
    _user_id = _user.get("id")
    _docs = docs.get_docs(db, _user_id)
    if not _docs:
        return Response(status_code=400, message="No Data Found Or Invalid Token").dict()
    return paginate(_docs, params)


add_pagination(router)


# @router.get("/", dependencies=[Depends(JWTBearer())])
@router.get("/")
async def get_todo_by_id(
        id: str,
        user: dict = Depends(get_user_credentials),
        db: Session = Depends(get_db)):
    _user_id = user.get("id")
    _docs = docs.get_docs_by_id(db, id, _user_id)
    if not _docs:
        return Response(status_code=400, message="No Data Found Or Invalid Token").dict()
    return Response(status_code=200, message="Get By Id", result=_docs).dict(exclude_none=True)


@router.patch("/")
async def update_todo(request: updateSchema,
                      user: dict = Depends(get_user_credentials),
                      db: Session = Depends(get_db)):
    user_id = user.get("id")
    _docs = docs.update_docs(db, document_id=request.id, title=request.title,
                             task=request.task, user_id=user_id)
    if not _docs:
        return Response(status_code=400, message="No Data Found Or Invalid Token").dict()
    return Response(status_code=200, message="Updated", result=_docs).dict(exclude_none=True)


@router.delete("/")
async def delete_todo(id: str,
                      user: dict = Depends(get_user_credentials),
                      db: Session = Depends(get_db)):
    user_id = user.get("id")
    _docs = docs.remove_docs(db, document_id=id, user_id=user_id)
    if not _docs:
        return Response(status_code=400, message="No Data Found Or Invalid Token").dict()
    else:
        return Response(status_code=200, message="deleted", result=_docs).dict(exclude_none=True)


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


@router.get("/test")
async def read_main():
    return {"msg": "Hello World"}
