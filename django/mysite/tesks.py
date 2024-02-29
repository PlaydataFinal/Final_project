from celery import Celery
import time

app = Celery('tasks', broker='pyamqp://guest:guest@rabbitmq//')

@app.task
def add(x, y):
    time.sleep(5)  # 예시로 작업이 시간이 걸리는 것처럼 보이도록 추가
    return x + y