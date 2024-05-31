from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_daily_notifications():
    print('--------------------------------------task------------------------------------------')
    send_mail(
        'Ежедневное уведомление',
        'Это ваше ежедневное уведомление.',
        'ksasagan@yandex.ru',
        ['ksasagan@yandex.ru']
    )