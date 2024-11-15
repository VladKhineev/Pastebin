import pytest
from httpx import AsyncClient

@pytest.mark.parametrize(
    'user_id, email',
    [
        (1, 'vlad.khineev@gmail.com'),
        (2, 'vlad.khineev@gmail.com'),
        (3, 'vlad.khineev@gmail.com'),
        (4, 'vlad.khineev@gmail.com'),
    ]
)
async def test_get_dashboard_report(ac: AsyncClient, user_id, email):
    response = await ac.get(f'/task/dashboard?user_id={user_id}&email={email}')

    assert response.status_code == 200
    print(response.json())
