from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sait_Zaytcev.settings')

app = Celery('sait_Zaytcev')

# Используем настройки Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в ваших приложениях
app.autodiscover_tasks()