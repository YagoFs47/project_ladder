from celery import shared_task
from time import sleep

@shared_task(bind=True)
def my_task(self):
    for c in range(10):
        sleep(1)
        print(c)
    
    return "Task completed"