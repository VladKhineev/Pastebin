from fastapi import Depends

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.database import async_session
from src.models import User
from src.schemas import UserRelDTO
from src.user.schemas import UserAddDTO


async def add_user(new_user: UserAddDTO = Depends(UserAddDTO)):
    async with async_session() as session:
        user = User(**new_user.dict())

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return {
            'status': 'success',
            'data': None,
            'details': f'id: {user.id}',
        }


async def section_user_and_post(user_id: int):
    async with async_session() as session:
        user = select(User).where(User.id == user_id).options(selectinload(User.post))
        result = await session.execute(user)
        res_orm = result.scalars().all()

        res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
        return res_dto


async def delete_post(user_id: int):
    async with async_session() as session:
        user = select(User).where(User.id == user_id).options(selectinload(User.post))
        result = await session.execute(user)
        res_orm = result.scalars().all()

        assert res_orm, 'Нет такой записи'

        res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]

        query = delete(User).where(User.id == user_id)
        await session.execute(query)
        await session.commit()

        return res_dto