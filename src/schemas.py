from src.user.schemas import UserDTO
from src.post.schemas import PostDTO


class UserRelDTO(UserDTO):
    post: list['PostDTO'] | None = None

class PostRelDTO(PostDTO):
    user: 'UserDTO'
