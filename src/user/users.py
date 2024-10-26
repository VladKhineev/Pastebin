from src.database import static_engine, static_session
from src.models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.schemas import UserDTO, UserRelDTO


from src.task.tasks import message

def insert_user():
    with static_session() as session:
        user1 = User(username='Sasha')
        user2 = User(username='Dima')

        session.add_all([user1, user2])
        session.commit()


def section_user():
    with static_session() as session:
        # user_id = 1
        # user1 = session.get(User, user_id)
        # print(f'{user1=}')

        query = select(User)
        result = session.execute(query)
        res_orm = result.scalars().all()
        print(f'{res_orm=}')
        res_dto = [UserDTO.model_validate(row, from_attributes=True) for row in res_orm]
        print(f'{res_dto=}')

def section_user_rel():
    with static_session() as session:
        query = select(User).options(selectinload(User.post))
        result = session.execute(query)
        res_orm = result.scalars().all()
        print(f'{res_orm=}')
        res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        print(f'{res_dto=}')

def section_user_rel_one(user_id: int):
    with static_session() as session:
        user = select(User).where(User.id == user_id).options(selectinload(User.post))
        result = session.execute(user)
        res_orm = result.scalars().all()
        res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        print(f'{res_dto=}')

def section_user_api():
    with static_session() as session:
        query = select(User)
        result = session.execute(query)
        res_orm = result.scalars().all()
        res_dto = [UserDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return f'{res_dto=}'


def section_user_rel_api():
    with static_session() as session:
        query = select(User).options(selectinload(User.post))
        result = session.execute(query)
        res_orm = result.scalars().all()
        res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return f'{res_dto=}'

def section_user_rel_dict():
    with static_session() as session:
        query = select(User).options(selectinload(User.post))
        result = session.execute(query)
        res_orm = result.scalars().all()
        res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return message(res_dto[0].dict())

print(section_user_rel_dict())