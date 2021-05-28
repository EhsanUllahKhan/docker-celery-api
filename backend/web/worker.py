import os
from celery import Celery

CELERY_BROKER_URL = os.getenv("REDISSERVER", "redis://redis_server:6379")
CELERY_RESULT_BACKEND = os.getenv("REDISSERVER", "redis://redis_server:6379")

# CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "db+mysql+pymysql://ehsan:ehsan@db:3306/vmi_db")

celery = Celery("celery",broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND,include=['backend.celery.tasks'])
# celery.conf.update(CELERY_RESULT_BACKEND="db+mysql+pymysql://ehsan:ehsan@db:3306/vmi_db")