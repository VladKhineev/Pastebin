import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import GO_PASS, GO_USER

GO_HOST = 'smtp.gmail.com'
GO_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')

def message(data: dict):
    '''Создает внутренность посылки(Страничка пользователя)'''

    res = []
    keys_ignore = ['id', 'user_id']
    for key, value in data.items():
        if key in keys_ignore:
            continue
        if type(value) == list and value:
            res.append('<br>')
            for d in value:
                for key2, value2 in d.items():
                    if key2 in keys_ignore:
                        continue
                    if key2 == 'like':
                        res.append(f'<h3 style="color: #75e96d;">{key2}:  ')
                        res.append(f'{value2}</h3>\n')
                    else:
                        res.append(f'<h3>{key2}:  ')
                        res.append(f'{value2}</h3>\n')
                res.append('<br>')
        else:
            res.append(f'<h2>{key}:  ')
            res.append(f'{value}</h2>\n')

    return ''.join(res)


def get_email_template_dashboard(email_user: str, data: dict):
    '''Создание посылки'''

    email = EmailMessage()
    email['Subject'] = 'Pastebin'
    email['From'] = GO_USER
    email['To'] = email_user


    email.set_content(
        '<div>'
        f'<h1 style="color: #647ace;">Зацени свои(или не свои) текста😊</h1>'
        '<div>'f'{message(data)}''</div>'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(email_user: str, data: dict):
    '''Отправка посылки'''
    email = get_email_template_dashboard(email_user, data)
    with smtplib.SMTP_SSL(GO_HOST, GO_PORT) as server:
        server.login(GO_USER, GO_PASS)
        server.send_message(email)
