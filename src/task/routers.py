from fastapi import APIRouter

import src.task.task_manager as task_manager

router = APIRouter(
    prefix="/report",
    tags=['Report'])


@router.get("/dashboard")
async def get_dashboard_report(user_id: int, email: str):
    '''Отсылает на email отчет его странички'''
    try:
            data = await task_manager.get_email_template_dashboard(user_id)
            task_manager.send_email_report_dashboard.delay(email, data)
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

