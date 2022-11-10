from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, ForeignKeyConstraint, Boolean
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from uuid import uuid1


class User(Base):
    __tablename__ = "login_user"
    id = Column(String, primary_key=True)
    username = Column(String(20))
    email = Column(String(30))
    password = Column(String(30))
    docs = relationship("Docs", back_populates="user")
    personal = relationship("Personal", back_populates="personal_data")


class Docs(Base):
    __tablename__ = "docs"
    id = Column(String, primary_key=True)
    title = Column(String(20))
    task = Column(String(60))
    bookmark = Column(Boolean, default=False)
    personal_docs = relationship("Personal", back_populates="docs")
    user_id = Column(String, ForeignKey("login_user.id"))

    user = relationship("User", back_populates="docs")


class Personal(Base):
    __tablename__ = "personal"
    id = Column(String, primary_key=True)
    docs_id = Column(String, ForeignKey("docs.id"))

    docs = relationship("Docs", back_populates="personal_docs")
    user_id = Column(String, ForeignKey("login_user.id"))

    personal_data = relationship("User", back_populates="personal")
