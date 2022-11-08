from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, ForeignKeyConstraint
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from uuid import uuid1


class User(Base):
    __tablename__ = "login_user"
    id = Column(String, primary_key=True)
    username = Column(String(20))
    email = Column(String(30))
    password = Column(String(30))
    docs = relationship("Docs", back_populates="user")

class Docs(Base):
    __tablename__ = "docs"
    id = Column(String, primary_key=True)
    title = Column(String(20))
    task = Column(String(60))
    user_id = Column(String, ForeignKey("login_user.id"))

    user = relationship("User", back_populates="docs")



