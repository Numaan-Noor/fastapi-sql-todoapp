from models import models
from fastapi import FastAPI
from database.database import engine
from router_app import router_docs, Router_Auth, router_all

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_docs.router, prefix="/docs", tags=["docs"])
app.include_router(Router_Auth.router, prefix="/signup", tags=["signup"])
app.include_router(router_all.router, prefix="/router_all", tags=["router_all"])

