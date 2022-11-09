from typing import Optional, TypeVar, Generic
from pydantic import BaseModel, Field, validator, Extra
from pydantic.generics import GenericModel

T = TypeVar('T')


class Response(GenericModel, Generic[T]):
    status_code: int
    message: str
    result: Optional[T]


class TodoRequestSchema(BaseModel):
    title: str
    task: str

    class Config:
        extra = Extra.forbid


class TodoAddSchema(TodoRequestSchema):
    id: str
    user_id: str


class updateSchema(TodoRequestSchema):
    id: str

    class config:
        extra = Extra.forbid


class Request_docs(BaseModel):
    parameter: TodoRequestSchema = Field(...)
