from typing import Optional, TypeVar, Generic
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


T = TypeVar('T')


class Response(GenericModel, Generic[T]):
    status_code: int
    message: str
    result: Optional[T]


class TodoRequestSchema(BaseModel):
    title: Optional[str]
    task: Optional[str]

    class Config:
        orm_mode = True


class TodoAddSchema(TodoRequestSchema):
    id: str
    user_id: Optional[str]


class updateSchema(TodoRequestSchema):
    id: str


class Request_docs(BaseModel):
    parameter: TodoRequestSchema = Field(...)
