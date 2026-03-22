import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.dataclasses.user_dataclass import User
from core.services.jwt_service import ActionToken, ActivateToken, JWTService, RecoveryToken

from configs.celery import app


class EmailService:
    @staticmethod
    @app.task
    def __send_email(to:str, template_name:str, context:dict, subject:str) -> None:
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject=subject, from_email=os.environ.get("EMAIL_HOST_USER"), to=[to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


    @classmethod
    def register(cls, user:User):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email.delay(
            user.email,
            'register.html',
            {'name':user.profile.name, 'url':url},
            'Registration')

    @classmethod
    def recovery_password(cls, user: User):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost:8888/recovery/{token}'
        cls.__send_email.delay(
            user.email,
            'recovery_password.html',
            {
                'name': user.profile.name,
                'url': url
            },
            'Recovery Password'
        )