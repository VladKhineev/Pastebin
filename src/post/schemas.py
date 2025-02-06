from pydantic import BaseModel, Field
from enum import Enum

class PostAddDTO(BaseModel):
    title: str = Field(min_length=4, max_length=10)
    text: str = Field(max_length=500)
    user_id: int

class PostDTO(PostAddDTO):
    id: int | None = None
    like: int


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=4, max_length=10)
    text: str | None = Field(default=None, max_length=500)


class Pagination(int, Enum):
    '''Схема для пагинации записей'''
    defolt = 3
    big = 5
    maxBig = 10