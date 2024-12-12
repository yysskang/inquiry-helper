from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab  # crontab 임포트

# '셀러리' 프로그램을 위해 기본 장고 설정파일을 설정합니다.
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

app = Celery(
    "config",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["api.tasks"],
)

# 여기서 문자열을 사용하는 것은 워커(worker)가 자식 프로세스로 설정 객체를 직렬화(serialize)하지 않아도 된다는 뜻입니다.
# 뒤에 namespace='CELERY'는 모든 셀러리 관련 설정 키는 'CELERY_' 라는 접두어를 가져야 한다고 알려줍니다.
# app.config_from_object('django.conf:settings.local', namespace='CELERY')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

app.conf.timezone = settings.CELERY_TIMEZONE

beat_schedule_obj = {
    "test_check": {
        "task": "api.tasks.my_test_add",
        "schedule": timedelta(seconds=30),
        'args': (10, 20)
    },
}

app.conf.beat_schedule = beat_schedule_obj

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
