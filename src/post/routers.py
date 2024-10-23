from fastapi import APIRouter, Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.models import Post
from src.database import static_session
from src.post.schemas import PostDTO, PostAddDTO, PostUpdate



router = APIRouter(
    prefix='/post',
    tags=['Post']
)

@router.get('/watch')
def select(post_id: int):
    try:
        with static_session() as session:
            post = session.get(Post, post_id)
            # res = PostDTO.model_validate(post, from_attributes=True)
            return post
    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }


@router.post('/add')
def insert(new_post: PostAddDTO = Depends(PostAddDTO)):
    try:
        with static_session() as session:
            post = Post(**new_post.dict())

            session.add(post)
            session.commit()
            return {
                'status': 'success',
                'data': None,
                'details': None,
            }
    except Exception:
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }



@router.put('/update')
def update_all_dep_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
    try:
        with static_session() as session:
            post = session.get(Post, post_id)
            post.title = new_post.title
            post.text = new_post.text

            session.commit()
            return {
                'status': 'success',
                'data': None,
                'details': None,
            }
    except Exception:
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }


@router.patch('/update')
def update_all_post(post_id: int, new_post: PostUpdate = Depends(PostUpdate)):
    try:
        with static_session() as session:
            post = session.get(Post, post_id)

            if new_post.title:
                post.title = new_post.title
            if new_post.text:
                post.text = new_post.text

            session.commit()
            return {
                'status': 'success',
                'data': None,
                'details': None,
            }
    except Exception:
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }

@router.delete('/delete')
def delete_post(post_id: int):
    try:
        with static_session() as session:
            stmt = delete(Post).where(Post.id == post_id)
            session.execute(stmt)

            session.commit()
            return {
                'status': 'success',
                'data': None,
                'details': None,
            }
    except Exception:
        return {
            'status': 'error',
            'data': None,
            'details': None,
        }