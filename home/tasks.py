from typing import List

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.conf import settings
import json

from home.auth_bolsa.auth_manager import AuthProccess
from home.models import (
    EventIdModel,
    MarketIdModel,
    MatchupModel,
    SessionsBolsaApostaModel,
    BetModel
)
from microservices.api.api import SyncApi
from microservices.utils.event import Event

from home.ladder.ladder import Ladder
from home.ladder.ladder_players_match_odds import LadderPlayersMatchOdds
from home.ladder.ladder_match_hedge import LadderMatchHedges

api: SyncApi = settings.SYNCAPI_BOLSA_APOSTAS
channel_layer = get_channel_layer()
auth_proccess = AuthProccess()
ladder_manager = Ladder(LadderPlayersMatchOdds(), LadderMatchHedges())
auth_proccess.proccess(SessionsBolsaApostaModel.objects.first())

@shared_task(bind=True)
def verify_state_session_bolsa(self):
    # identificar um paradeiro de session
    auth_proccess.proccess(SessionsBolsaApostaModel.objects.first())


@shared_task(bind=True)
def refresh_matchup_db(self):
    """
    ESSA TASK PEGA NA API TODOS OS JOGOS AO VIVO
    E ATUALIZA NO BANCO DE DADOS PARA SERVIR PARA O CLIENTE
    """

    api: SyncApi = settings.SYNCAPI_BOLSA_APOSTAS
    events: List[Event] = api.get_live_matchups2()
    matchups_model = list(MatchupModel.objects.all())
    events_json = []

    for event in events:
        matchup = MatchupModel.objects.filter(id_matchup=event.get_id())
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

    for matchup_model in matchups_model:
        for event in events:
            if event.compair_id(matchup_model.id_matchup):
                events_json.append(event.to_json())
                break
        else:
            matchup_model.delete()

    async_to_sync(channel_layer.group_send)(
            "matchups",
            {
                "type": "refresh.matchups",
                "data": events_json
            }
        )


@shared_task(bind=True)
def refresh_ladders(self):
    partidas = EventIdModel.objects.all()
    for event in partidas:
        # para cada partida, quero pegar todos os mercados registrados naquele jogo.
        markets_ids = [market_model.market_id for market_model in MarketIdModel.objects.filter(event_id=event)]  # o(n)
        mercados_em_string = ",".join(markets_ids)  # o(n)

        print("mercados = {}".format(mercados_em_string))
        print("EVENT = {}".format(event))

        data = api.get_market_with_prices(event_id=event.event_id, market_ids=mercados_em_string)
        if not data:  # o(1)
            event.delete()
            continue
        
        for market_data in data.get('markets'):  # o(n)
            # o(1)
            # market_data.update()
            ladder = async_to_sync(ladder_manager.get_complete_ladder)(market=market_data)
            async_to_sync(channel_layer.group_send)(
                f"{event.event_id}-{market_data.get('id')}",
                {
                    "type": "refresh.ladder",
                    "data": ladder,
                }
            )


@shared_task(bind=True)
def verify_correspondence(self):
    headers = auth_proccess.load_headers_exchange()
    model = SessionsBolsaApostaModel.objects.first()
    tokens = auth_proccess.load_auth_tokens(model)
    headers.update({"cookie": tokens.tokens_to_string()})
    client = auth_proccess.client
    r = client.get(
        url="https://mexchange-api.bolsadeaposta.bet.br/api/offers?offset=0&per-page=200", 
        headers=headers
        )
    # print(r)
    # print(r.json())
    with open(settings.BASE_DIR / "aposta.json", "w") as file:
        json.dump(r.json(), file, indent=4)

    for offer in r.json()['offers']:
        if BetModel.objects.filter(bet_id=offer['id']).exists():
            bet = BetModel.objects.get(bet_id=offer['id'])
            print(bet)
            if bet.status == "waiting" and offer['status'] == "matched":
                print(bet)
                bet.stake_matched = offer['stake-matched']
                bet.partial_stake = offer['stake-matched']
                bet.status = "open"
                bet.save()
    
    # data = bolsa.get_checkout()

    # for data_bet in data['offers']: