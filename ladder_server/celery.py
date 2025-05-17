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
        'schedule': 10,  # executa a cada segundo
    },
    'refresh_tokens': {
        'task': 'home.tasks.verify_state_session_bolsa',
        'schedule': 10,  # executa a cada segundo
    },
    'refresh_ladders': {
        'task': 'home.tasks.refresh_ladders',
        'schedule': 5,  # executa a cada segundo
    },
    'verify_correspondence': {
        'task': 'home.tasks.verify_correspondence',
        'schedule': 5,  # executa a cada segundo
    },
}
