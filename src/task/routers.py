from fastapi import APIRouter, BackgroundTasks, Depends

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .tasks import send_email_report_dashboard
from src.database import static_session, async_session
from src.models import User
from src.schemas import UserRelDTO

router = APIRouter(
    prefix="/report",
    tags=['Report'])


@router.get("/dashboard")
async def get_dashboard_report(user_id: int, email: str = 'vlad.khineev@gmail.com'):
    try:
        async with async_session() as session:
            user = select(User).where(User.id == user_id).options(selectinload(User.post))
            result = await session.execute(user)
            res_orm = result.scalars().all()
            res_dto = [UserRelDTO.model_validate(row, from_attributes=True) for row in res_orm]

            result = res_dto[0].dict()
            send_email_report_dashboard.delay(email, result)
            return {
                "status": 'success',
                "data": "Письмо отправлено",
                "details": None
            }
    except Exception as er:
        print(er)
        return {
            'status': 'error',
            'data': None,
            'details': None,
    }

