from time import sleep
from typing import List

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.conf import settings
from httpx import Client

from home.models import (
    EventIdModel,
    MarketIdModel,
    MatchupModel,
    FlowModel,
    OpeningBetModel,
    ClosingBetModel
)

from microservices.api.api import SyncApi
from microservices.bolsa.interface import BolsaAposta
from microservices.utils.event import Event
from home.bets.bet import Bet

client: Client = settings.SYNCLIENT_HTTPX
api: SyncApi = settings.SYNCAPI_BOLSA_APOSTAS
bolsa = BolsaAposta(client)
channel_layer = get_channel_layer()


@shared_task(bind=True)
def my_task(self):
    for c in range(10):
        sleep(1)
        print(c)

    return "Task completed"


@shared_task(bind=True)
def verify_state_session_bolsa(self):
    print("Executando e verificando state_session")
    bolsa.verify_tokens()


@shared_task(bind=True)
def refresh_matchup_db(self):
    """
    ESSA TASK PEGA NA API TODOS OS JOGOS AO VIVO
    E ATUALIZA NO BANCO DE DADOS PARA SERVIR PARA O CLIENTE
    """

    api: SyncApi = settings.SYNCAPI_BOLSA_APOSTAS
    events: List[Event] = api.get_live_matchups()
    matchups_model = list(MatchupModel.objects.all())
    events_json = []

    for event in events:
        matchup = MatchupModel.objects.filter(id_matchup=event.get_id())
        events_json.append(event.to_json())
        if not matchup.exists():
            MatchupModel.objects.create(
                id_matchup=event.get_id(),
                matchup_name=event.get_matchup_name(),
                status=event.get_status(),
                team_a=event.get_home_name(),
                team_b=event.get_away_name(),
                is_running=True,
                time_elapsed=event.get_time()
            )
            continue
        matchup.update(time_elapsed=event.get_time())

    async_to_sync(channel_layer.group_send)(
            "matchups",
            {
                "type": "refresh.matchups",
                "data": events_json
            }
        )

    for matchup_model in matchups_model:
        for event in events:
            if event.compair_id(matchup_model.id_matchup):
                break
        else:
            matchup_model.delete()


@shared_task(bind=True)
def refresh_ladders(self):
    partidas = EventIdModel.objects.all()
    for event in partidas:
        # para cada partida, quero pegar todos os mercados registrados naquele jogo.
        markets_ids = [market_model.market_id for market_model in MarketIdModel.objects.filter(event_id=event)]  # o(n)
        mercados_em_string = ",".join(markets_ids)  # o(n)

        data = api.get_market_with_prices(event_id=event.event_id, market_ids=mercados_em_string)
        if not data:  # o(1)
            event.delete()
            continue

        for market_data in data.get('markets'):  # o(n)
            # o(1)
            async_to_sync(channel_layer.group_send)(
                f"{event.event_id}-{market_data.get('id')}",
                {
                    "type": "refresh.ladder",
                    "data": market_data
                }
            )


@shared_task(bind=True)
def verify_correspondence(self):

    data = bolsa.get_checkout()
    
    for data_bet in data['offers']:

        bet = Bet(data_bet)

        if not bet.is_matched():
            continue

        flow = FlowModel.objects.get(
            market_id=bet.get_market_id(),
            event_Id=bet.get_event_id()
            )

        if flow.orientation == bet.get_side():
            bet_model = OpeningBetModel.objects.get(market_id=bet.get_market_id())
            bet_model.status = bet.MATCHED
            
        else:
            bet_model = ClosingBetModel.objects.get(market_id=bet.get_market_id())
            bet_model.status = bet.CLOSED
        
        bet_model.save()
        
        bet_model_suggestions = OpeningBetModel.objects.filter(
            market_id=bet.get_market_id(),
            event_id=bet.get_event_id(),
            status=bet.MATCHED,
            ).all()

        #TODO -> Enviar a lista de apostas correspondidas para a ladder aberta via websockets
        async_to_sync(
            channel_layer.group_send,
            f"{bet.get_event_id()}-{bet.get_market_id()}",
            {
                    "type": "ladder.suggestions",
                    "data": [bms.to_json() for bms in bet_model_suggestions]
            }
        )


            
        
    
