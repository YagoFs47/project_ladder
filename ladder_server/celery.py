import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ladder_server.settings')
app = Celery('ladder_server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    print(f'Current task: {self.name}')
    print(f'Current task id: {self.request.id}')
    print(f'Current task args: {self.request.args}')
    print(f'Current task kwargs: {self.request.kwargs}')