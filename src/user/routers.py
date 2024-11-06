from fastapi import APIRouter, Depends

from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload

from fastapi_cache.decorator import cache

from src.database import static_session, async_session
from src.models import User
from src.schemas import UserRelDTO
from src.user.schemas import UserDTO, UserAddDTO


router = APIRouter(
    prefix='/user',
    tags=['User']
)

# @router.get('/watch/{user_id}', response_model=UserDTO)
# def select_user(user_id: int):
#     with static_session() as session:
#         user = session.get(User, user_id)
#         # res = UserDTO.model_validate(user, from_attributes=True)
#         return user


# @router.get('/{user_id}', response_model=list[UserRelDTO])
# def section_user_and_post(user_id: int):
#     try:
#         with static_session() as session:
#             user = select(User).where(User.id == user_id).options(selectinload(User.post))
#             result = session.execute(user)
#             res_orm = result.scalars().all()
#             res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
#             return res_dto
#     except Exception:
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None,
#     }
#
# @router.post('/add')
# def add_user(new_user: UserDTO = Depends(UserAddDTO)):
#     try:
#         with static_session() as session:
#             user = User(**new_user.dict())
#
#             session.add(user)
#             session.commit()
#             return {
#                 'status': 'success',
#                 'data': None,
#                 'details': None,
#             }
#     except Exception:
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None,
#     }
#
#
# @router.delete('/delete')
# def delete_post(user_id: int):
#     try:
#         with static_session() as session:
#             user = select(User).where(User.id == user_id).options(selectinload(User.post))
#             result = session.execute(user)
#             res_orm = result.scalars().all()
#             res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]
#
#             stmt = delete(User).where(User.id == user_id)
#             session.execute(stmt)
#
#             session.commit()
#             return res_dto
#     except Exception:
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None,
#         }


##--------------------------------------------------------------------------asynchronously





@router.get('/{user_id}', response_model=list[UserRelDTO])
async def section_user_and_post(user_id: int):
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

@router.post('/add')
async def add_user(new_user: UserDTO = Depends(UserAddDTO)):
    try:
        async with (async_session() as session):
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


@router.delete('/delete')
async def delete_post(user_id: int):
    try:
        async with async_session() as session:
            user = select(User).where(User.id == user_id).options(selectinload(User.post))
            result = await session.execute(user)

            res_orm = result.scalars().all()

            assert res_orm, 'Нет такой записи'

            res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]

            stmt = delete(User).where(User.id == user_id)

            await session.execute(stmt)
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