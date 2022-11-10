from models import models
from fastapi import FastAPI
from database.database import engine
from router_app import router_docs, Router_Auth, router_all, router_Save

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_docs.router, prefix="/docs", tags=["docs"])
app.include_router(router_all.router, prefix="/bookmark", tags=["Bookmark"])
app.include_router(Router_Auth.router, prefix="/signup", tags=["signup"])
app.include_router(router_Save.router, prefix="/save", tags=["save"])

