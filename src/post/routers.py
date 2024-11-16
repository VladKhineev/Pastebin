from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from fastapi_cache.decorator import cache

from src.models import Post
from src.database import async_session
from src.post.schemas import PostAddDTO, PostUpdate, Pagination

router = APIRouter(
    prefix='/post',
    tags=['Post']
)


@router.post('/add')
async def insert_post(new_post: PostAddDTO = Depends(PostAddDTO)):
    '''Добавляет запись от пользователя. На выходе его id'''

    try:
        async with async_session() as session:
            post = Post(**new_post.dict())

            session.add(post)
            await session.commit()
            await session.refresh(post)
            return {
                'status': 'success',
                'data': None,
                'details': f'id: {post.id}',
            }

    except Exception:
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }


@router.get('/watch')
async def select_post(post_id: int):
    '''Показывает запись по id'''

    try:
        async with async_session() as session:
            post = await session.get(Post, post_id)
            return post

    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }


@router.get('/watch_all')
@cache(expire=30)
async def select_post_all(limit: Pagination, skip: int = 0):
    '''Показывает все записи с пагинацией'''


    try:
        async with async_session() as session:
            posts = select(Post)
            res = await session.execute(posts)
            result = res.scalars().all()
            return result[limit * skip:limit + (skip * limit)]

    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }

@router.patch('/like')
async def add_like_post(post_id: int):
    '''Ставит лайк записи по id'''

    try:
        async with async_session() as session:
            post = await session.get(Post, post_id)

            assert post, 'Нет такой записи'

            post.like += 1
            post_like = post.like

            await session.commit()
            return f'Likes: {post_like}'

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
async def update_all_dep_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
    '''Обновляет полностью запись по id'''

    try:
        async with async_session() as session:
            post = await session.get(Post, post_id)

            assert new_post.title and new_post.text, 'Не все данные введены'

            post.title = new_post.title
            post.text = new_post.text

            await session.commit()
            return {
                'status': 'success',
                'data': None,
                'details': None,
            }

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
async def update_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
    '''Обновляет частично запись по id'''

    try:
        async with async_session() as session:
            post = await session.get(Post, post_id)

            if new_post.title:
                post.title = new_post.title
            if new_post.text:
                post.text = new_post.text

            await session.commit()
            return {
                'status': 'success',
                'data': None,
                'details': None,
            }

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
async def delete_post(post_id: int):
    '''Удаляет запись по id'''

    try:
        async with async_session() as session:
            post = await session.get(Post, post_id)

            assert post, 'Нет такой записи'

            query = delete(Post).where(Post.id == post_id)
            await session.execute(query)
            await session.commit()

            return post

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