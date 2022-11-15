from fastapi import Depends
from fastapi.testclient import TestClient

from models.models import Docs
from router_app.router_docs import router, get_todo_by_id, read_main, All_Docs_Without_Auth, post_todo, get_db
from main import app
import uvicorn

client = TestClient(router)


def test_read_main():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_All_Docs_Without_Auth():
    response = client.get("/All")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
