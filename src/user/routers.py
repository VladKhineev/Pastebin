from fastapi import APIRouter, Depends

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.database import async_session
from src.models import User
from src.schemas import UserRelDTO
from src.user.schemas import UserAddDTO


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/add')
async def add_user(new_user: UserAddDTO = Depends(UserAddDTO)):
    '''Добавляет пользователя. На выходе его id'''

    try:
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
    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': None,
    }

@router.get('/{user_id}', response_model=list[UserRelDTO])
async def section_user_and_post(user_id: int):
    '''Показывает пользователя и его записи по id'''

    try:
        async with async_session() as session:
            user = select(User).where(User.id == user_id).options(selectinload(User.post))
            result = await session.execute(user)
            res_orm = result.scalars().all()

            res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
            return res_dto
    except Exception:
        return {
            'status': 'error',
            'data': None,
            'details': None,
    }

@router.delete('/delete')
async def delete_post(user_id: int):
    '''Удаляет пользователя вместе с его записями по id'''

    try:
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

    except AssertionError as er:
        return {
            'status': 'error',
            'data': 'NullError',
            'details': str(er),
        }
    except Exception as er:
        return {
            'status': 'error',
            'data': None,
            'details': str(er),
        }
