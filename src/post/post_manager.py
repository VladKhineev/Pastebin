from fastapi import Depends
from sqlalchemy import delete, select

from src.models import Post
from src.database import async_session
from src.post.schemas import PostAddDTO, PostUpdate, Pagination


async def add_post(new_post: PostAddDTO = Depends(PostAddDTO)):
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


async def select_post(post_id: int):
    async with async_session() as session:
        post = await session.get(Post, post_id)
        return post


async def select_post_all(limit: Pagination, skip: int = 0):
    async with async_session() as session:
        posts = select(Post)
        res = await session.execute(posts)
        result = res.scalars().all()
        return result[limit * skip:limit + (skip * limit)]


async def add_like_post(post_id: int):
    async with async_session() as session:
        post = await session.get(Post, post_id)

        assert post, 'Нет такой записи'

        post.like += 1
        post_like = post.like

        await session.commit()
        return f'Likes: {post_like}'


async def update_all_dep_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
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


async def update_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
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


async def delete_post(post_id: int):
    async with async_session() as session:
        post = await session.get(Post, post_id)

        assert post, 'Нет такой записи'

        query = delete(Post).where(Post.id == post_id)
        await session.execute(query)
        await session.commit()

        return post