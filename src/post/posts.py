from sqlalchemy import select

from src.database import static_engine, static_session
from src.models import Post, Base
from src.schemas import PostDTO, PostRelDTO
from src.post.schemas import PostAddDTO


def create_tables():
    static_engine.echo = False
    Base.metadata.drop_all(static_engine)
    Base.metadata.create_all(static_engine)
    static_engine.echo = False


def insert_post():
    with static_session() as session:
        post1 = Post(title='rec1', text='Hello', user_id=1)
        post2 = Post(title='rec2', text='How are you', user_id=1)

        session.add_all([post1, post2])
        session.commit()


def select_post():
    with static_session() as session:
        query = select(Post)
        result = session.execute(query)
        res_orm = result.scalars().all()
        print(f'{res_orm=}')
        res_dto = [PostDTO.model_validate(row, from_attributes=True) for row in res_orm]
        print(f'{res_dto=}')


# def update_post(post_id: int, new_post: PostAddDTO):
#     with static_session() as session:
#         post = session.get(Post, post_id)
#         new_post_dict = new_post.dict()


def select_post_one(post_id: int):
    with static_session() as session:
        with static_session() as session:
            post = session.get(Post, post_id)
            print(post)
            res = PostDTO.model_validate(post, from_attributes=True)
            return res

print(select_post_one(9))