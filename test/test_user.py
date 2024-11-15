import pytest
from conftest import client
from httpx import AsyncClient




@pytest.mark.parametrize(
    'username, user_id',
    [
        ('Vlad', 1),
        ('12445', 2),
        ('что за', 3),
    ]
)
async def test_add_user_valid(ac: AsyncClient, username, user_id):
    data = {
        'username': f'{username}',
    }
    response = await ac.post(f'/user/add', json=data)

    assert response.status_code == 200
    assert response.json() == {'status': 'success', 'data': None, 'details': f'id: {user_id}'}

@pytest.mark.parametrize(
    'username, user_id',
    [
        (1, 1),
        ('Dmitry Khineev', 2),
        ('Po', 3),
    ]
)
async def test_add_user_not_valid(ac: AsyncClient, username, user_id):
    data = {
        'username': f'{username}',
    }
    response = await ac.post(f'/user/add', json=data)

    assert response.status_code == 200
    assert response.json() == {'status': 'success', 'data': None, 'details': f'id: {user_id}'}



@pytest.mark.parametrize(
    'user_id',
    [
        1,
        '2',
    ]
)
async def test_section_user_and_post_valid(ac: AsyncClient, user_id):
    response = await ac.get(f'/user/{user_id}')

    print(response.json())
    assert response.status_code == 200

@pytest.mark.parametrize(
    'user_id',
    [
        -1,
        20000,
        True,

    ]
)
async def test_section_user_and_post_not_valid(ac: AsyncClient, user_id):
    response = await ac.get(f'/user/{user_id}')

    print(response.json())
    assert response.status_code == 200




@pytest.mark.parametrize(
    'user_id',
    [
        1,
        '2',
    ]
)
async def test_delete_post_valid(ac: AsyncClient, user_id):
    response = await ac.get(f'/user/{user_id}')

    print(response.json())
    assert response.status_code == 200

@pytest.mark.parametrize(
    'user_id',
    [
        -1,
        20000,
        True,

    ]
)
async def test_delete_post_not_valid(ac: AsyncClient, user_id):
    response = await ac.get(f'/user/{user_id}')

    print(response.json())
    assert response.status_code == 200