from pydantic import BaseModel


class todoBase(BaseModel):
    Name: str
    isEnd : int


class todoCreate(todoBase):
    pass


class todo_(todoBase):
    id: int