from fastapi import APIRouter, Depends

from src.schemas import UserRelDTO
from src.user.schemas import UserAddDTO

import src.user.user_manager as user_manager


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/add')
async def router_to_add_user(new_user: UserAddDTO = Depends(UserAddDTO)):
    '''Добавляет пользователя. На выходе его id'''

    try:
        return await user_manager.add_user(new_user,)
    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': None,
    }


@router.get('/{user_id}', response_model=list[UserRelDTO])
async def router_to_section_user_and_post(user_id: int):
    '''Показывает пользователя и его записи по id'''

    try:
        return await user_manager.section_user_and_post(user_id)
    except Exception:
        return {
            'status': 'error',
            'data': None,
            'details': None,
    }


@router.delete('/delete')
async def router_to_delete_post(user_id: int):
    '''Удаляет пользователя вместе с его записями по id'''

    try:
        return await user_manager.delete_post(user_id)
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
