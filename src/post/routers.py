from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.post.schemas import PostAddDTO, PostUpdate, Pagination

import src.post.post_manager as post_manager

router = APIRouter(
    prefix='/post',
    tags=['Post']
)


@router.post('/add')
async def router_to_add_post(new_post: PostAddDTO = Depends(PostAddDTO)):
    '''Добавляет запись от пользователя. На выходе его id'''
    try:
        return await post_manager.add_post(new_post)
    except Exception:
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }


@router.get('/watch')
async def router_to_select_post(post_id: int):
    '''Показывает запись по id'''
    try:
        return await post_manager.select_post(post_id)
    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }


@router.get('/watch_all')
@cache(expire=30)
async def router_to_select_post_all(limit: Pagination, skip: int = 0):
    '''Показывает все записи с пагинацией'''
    try:
        return await post_manager.select_post_all(limit, skip)
    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }

@router.patch('/like')
async def router_to_add_like_post(post_id: int):
    '''Ставит лайк записи по id'''
    try:
        return await post_manager.add_like_post(post_id)
    except AssertionError as er:
        return {
            'status': 'error',
            'data': 'IndexError',
            'details': str(er),
        }
    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': str(er),
        }

@router.put('/update')
async def router_to_update_all_dep_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
    '''Обновляет полностью запись по id'''
    try:
        return await post_manager.update_all_dep_post(post_id, new_post)
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

@router.patch('/update')
async def router_to_update_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
    '''Обновляет частично запись по id'''
    try:
        return await post_manager.update_post(post_id, new_post)
    except AssertionError as er:
        return {
            'status': 'error',
            'data': 'NullError',
            'details': str(er),
        }
    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }

@router.delete('/delete')
async def router_to_delete_post(post_id: int):
    '''Удаляет запись по id'''
    try:
        return await post_manager.delete_post(post_id)
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