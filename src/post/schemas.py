from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class PostAddDTO(BaseModel):
    title: str = Field(min_length=4, max_length=10)
    text: str = Field(max_length=500)
    user_id: int

class PostDTO(PostAddDTO):
    id: int | None = None
    like: int
    # created_ad: datetime
    # updated_ad: datetime

# class PostRelDTO(PostDTO):
#     user: 'UserDTO'


class PostUpdate(BaseModel):
    title: str | None = None
    text: str | None = None


class Pagination(int, Enum):
    defolt = 3
    big = 5
    maxBig = 10