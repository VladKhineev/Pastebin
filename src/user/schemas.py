from pydantic import BaseModel, Field


class UserAddDTO(BaseModel):
    '''Схема для пользователя'''
    username: str = Field(min_length=3, max_length=10)


class UserDTO(UserAddDTO):
    id: int | None = None
