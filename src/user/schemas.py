from pydantic import BaseModel


class UserAddDTO(BaseModel):
    username: str

class UserDTO(UserAddDTO):
    id: int | None = None

# class UserRelDTO(UserDTO):
#     post: list['PostDTO']
