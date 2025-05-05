import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ladder_server.settings')
app = Celery('ladder_server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.enable_utc = False
app.conf.update(timezone='America/Sao_Paulo')


# CELERY BEAT CONFIG
app.conf.beat_schedule = {
    'refresh_matchup_db': {
        'task': 'home.tasks.refresh_matchup_db',
        'schedule': 10,  # executa a cada minuto
    },
    'refresh_tokens': {
        'task': 'home.tasks.verify_state_session_bolsa',
        'schedule': 60,  # executa a cada minuto
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    print(f'Current task: {self.name}')
    print(f'Current task id: {self.request.id}')
    print(f'Current task args: {self.request.args}')
    print(f'Current task kwargs: {self.request.kwargs}')
