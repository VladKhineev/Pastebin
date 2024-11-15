import pytest
from httpx import AsyncClient
from conftest import client

from src.post.routers import select_post, insert_post

@pytest.mark.parametrize(
    'title, text, user_id, post_id',
    [
        ('post1', 'Hello1', 1, 1),
        ('post2', 'Hello2', '2', 2),
        ('2222', '111111', 3, 3),
    ]
)
async def test_insert_post_valid(ac: AsyncClient, title, text, user_id, post_id):
    data = {
        'title': f'{title}',
        'text': f'{text}',
        'user_id': f'{user_id}',
    }
    response = await ac.post('post/add', json=data)

    assert response.status_code == 200
    assert response.json() == {'status': 'success', 'data': None, 'details': f'id: {post_id}'}

@pytest.mark.parametrize(
    'title, text, user_id, post_id',
    [
        ('ok', 'Hello1', 1, 1),
        ('what do I do?', 'Hello2', '2', 2),
        ('post3', 'Hello3', 4, 3),
    ]
)
async def test_insert_post_not_valid(ac: AsyncClient, title, text, user_id, post_id):
    data = {
        'title': f'{title}',
        'text': f'{text}',
        'user_id': f'{user_id}',
    }
    response = await ac.post('post/add', json=data)

    assert response.status_code == 200
    assert response.json() == {'status': 'success', 'data': None, 'details': f'id: {post_id}'}

@pytest.mark.parametrize(
    'post_id',
    [
        1,
        2,
        3,
    ]
)
async def test_select_post(ac: AsyncClient, post_id):
    response = await ac.get(f'/post/watch?post_id={post_id}')

    print(response.json())
    assert response.status_code == 200

@pytest.mark.parametrize(
    'limit, skip',
    [
        (3, 0),
        (5, 0),
        (10, 0),
    ]
)
async def test_select_post_all(ac: AsyncClient, limit, skip):
    response = await ac.get(f'post/watch_all?limit={limit}&skip={skip}')

    assert response.status_code == 200
    print(response.json())


@pytest.mark.parametrize(
    'post_id',
    [
        1,
        2,
        3,
    ]
)
async def test_add_like_post(ac: AsyncClient, post_id):
    response = await ac.patch(f'post/like?post_id={post_id}')

    assert response.status_code == 200
    print(response.json())

@pytest.mark.parametrize(
    'title, text, post_id',
    [
        ('rec1', 'Hello1', 1),
        ('post2', 'Hello2', 2),
        ('rec3', 'Hello3', 3),
        ('post4', 'Hello4', 4),
    ]
)
async def test_update_all_dep_post(ac: AsyncClient, title, text, post_id):
    data = {
        'title': f'{title}',
        'text': f'{text}',
    }
    response = await ac.put(f'post/update?post_id={post_id}', json=data)

    assert response.status_code == 200
    print(response.json())

@pytest.mark.parametrize(
    'title, text, post_id',
    [
        ('post1', 'Hello1', 1),
        ('post2', 'Hello2', 2),
        ('post3', 'Hello3', 3),
        ('post4', 'Hello4', 4),
    ]
)
async def test_update_all_post(ac: AsyncClient, title, text, post_id):
    data = {
        'title': f'{title}',
        'text': f'{text}',
    }
    response = await ac.patch(f'post/update?post_id={post_id}', json=data)

    assert response.status_code == 200
    print(response.json())

@pytest.mark.parametrize(
    'post_id',
    [
        1,
        2,
        3,
        4,
    ]
)
async def test_delete_post(ac: AsyncClient, post_id):
    response = await ac.delete(f'/post/delete?post_id={post_id}')

    print(response.json())
    assert response.status_code == 200