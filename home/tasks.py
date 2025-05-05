from time import sleep
from typing import List

from celery import shared_task
from django.conf import settings
from httpx import Client

from home.models import MatchupModel
from microservices.api.api import SyncApi
from microservices.bolsa.interface import BolsaAposta
from microservices.utils.matchup import Matchup

client: Client = settings.SYNCLIENT_HTTPX
bolsa = BolsaAposta(client)


@shared_task(bind=True)
def my_task(self):
    for c in range(10):
        sleep(1)
        print(c)

    return "Task completed"


@shared_task(bind=True)
def verify_state_session_bolsa(self):
    bolsa.verify_tokens()


@shared_task(bind=True)
def refresh_matchup_db(self):
    """
    ESSA TASK PEGA NA API TODOS OS JOGOS AO VIVO
    E ATUALIZA NO BANCO DE DADOS PARA SERVIR PARA O CLIENTE
    """

    api: SyncApi = settings.SYNCAPI_BOLSA_APOSTAS
    matchups: List[Matchup] = api.get_all_matchups()
    matchups_model = list(MatchupModel.objects.all())

    for matchup in matchups:
        if not MatchupModel.objects.filter(id_matchup=matchup.id).exists():
            make_matchup = MatchupModel.objects.create(
                id_matchup=matchup.id,
                matchup_name=matchup.name,
                start=matchup.start,
                status=matchup.status,
                sport=matchup.sport,
                is_running=matchup.is_running,
                team_a=matchup.team_a,
                team_b=matchup.team_b,
            )
            make_matchup.save()

    for matchup_model in matchups_model:
        for matchup_obj in matchups:
            if str(matchup_model.id_matchup) == matchup_obj.id:
                break
        else:
            matchup_model.delete()
            # Se não encontrar o matchup na lista de matchups, deleta do banco

    return 'DONE'


@shared_task(bind=True)
def verify_correspondence(self):
    data = bolsa.verify_correspondence()
    print(data)
