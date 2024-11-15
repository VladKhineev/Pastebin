from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from fastapi_cache.decorator import cache

from src.models import Post
from src.database import static_session, async_session
from src.post.schemas import PostDTO, PostAddDTO, PostUpdate, Pagination
from pydantic import BaseModel

router = APIRouter(
    prefix='/post',
    tags=['Post']
)

# @router.get('/t/watch')
# def select_post_static(post_id: int):
#     try:
#         with static_session() as session:
#             post = session.get(Post, post_id)
#             # res = PostDTO.model_validate(post, from_attributes=True)
#             return post
#     except Exception as er:
#         print(er)
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None,
#         }
#
#
# @router.post('/t/add')
# async def insert_post_static(new_post: PostAddDTO):
#     # try:
#     async with async_session() as session:
#         post = Post(**new_post.dict())
#
#         session.add(post)
#         await session.commit()
#         return {
#             'status': 'success',
#             'data': None,
#             'details': None,
#         }
#     # except Exception:
#     #     return {
#     #         'status': 'error',
#     #         'data': None,
#     #         'details': None,
#     #     }
#
# @router.get('/t/watch_all')
# @cache(expire=30)
# def select_post_all_static(lemit: Pagination, skip: int = 0):
#     try:
#         with static_session() as session:
#             posts = select(Post)
#             res = session.execute(posts)
#             result = res.scalars().all()
#             return result[lemit * skip:lemit + (skip * lemit)]
#
#     except Exception as er:
#         print(er)
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None,
#         }
#
# @router.patch('/t/like')
# def add_like_post_static(post_id: int):
#     try:
#         with static_session() as session:
#             post = session.get(Post, post_id)
#
#             post.like += 1
#
#             session.commit()
#             return f'Likes: {post.like}'
#     except Exception:
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None,
#         }
#
#
# @router.put('/t/update')
# def update_all_dep_post_static(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
#     try:
#         with static_session() as session:
#             post = session.get(Post, post_id)
#             post.title = new_post.title
#             post.text = new_post.text
#
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
#         }
#
#
# @router.patch('/t/update')
# def update_all_post_static(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
#     try:
#         with static_session() as session:
#             post = session.get(Post, post_id)
#
#             if new_post.title:
#                 post.title = new_post.title
#             if new_post.text:
#                 post.text = new_post.text
#
#             session.commit()
#             return {
#                 'status': 'success',
#                 'data': None,
#                 'details': None,
#             }
#     except TypeError:
#         return {
#             'status': 'error',
#             'data': 'Не верный индекс',
#             'details': 'Нет такой записи',
#         }
#     except Exception as er:
#         print(er)
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None,
#         }
#
# @router.delete('/t/delete')
# def delete_post_static(post_id: int):
#     try:
#         with static_session() as session:
#             post = session.get(Post, post_id)
#
#             stmt = delete(Post).where(Post.id == post_id)
#             session.execute(stmt)
#
#             session.commit()
#             return post
#     except Exception as er:
#         print(er)
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None,
#         }



#--------------------------------------------------------------------------asynchronously



@router.post('/add')
async def insert_post(new_post: PostAddDTO = Depends(PostAddDTO)): # = Depends(PostAddDTO)
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
    try:
        async with async_session() as session:
            post = await session.get(Post, post_id)
            # res = PostDTO.model_validate(post, from_attributes=True)

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
async def update_all_dep_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)): # = Depends(PostUpdate)
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
async def update_all_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)): # = Depends(PostUpdate)
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
    try:
        async with async_session() as session:
            post = await session.get(Post, post_id)

            assert post, 'Нет такой записи'

            stmt = delete(Post).where(Post.id == post_id)
            await session.execute(stmt)

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