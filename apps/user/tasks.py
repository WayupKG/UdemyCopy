from settings.celery import app
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


@app.task
def reset_password_email_send(**kwargs):
    title, from_email = settings.EMAIL_TITLE_FROM, settings.EMAIL_HOST_USER
    title_send = '"Udemy" Сброс пароля'
    to_form, headers = f'{kwargs.get("full_name")} <{kwargs.get("email")}>', {'From': f'{title} <{from_email}>'}
    html_content = render_to_string('reset_password_email.html', kwargs)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(title_send, text_content, from_email, [to_form], headers=headers)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
    return str(f'Sent to {kwargs.get("email")}')