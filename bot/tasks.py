from celery import Celery
from bot.config import REDIS_URL

app = Celery('tasks', broker=REDIS_URL)


@app.task
def add(x, y):
    return x + y
