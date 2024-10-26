from pydantic import BaseModel, field_validator
from datetime import datetime

class PostAddDTO(BaseModel):
    title: str
    text: str
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
