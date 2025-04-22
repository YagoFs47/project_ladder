from re import search, match
from django.conf import settings
from httpx import AsyncClient, Client
from datetime import datetime
from zoneinfo import ZoneInfo
from microservices.utils.matchup import Matchup, ManageMatchups
import json


class Api:
    """essa classe é uma interface de interação com a api da bolsa de apostas bet"""

    client: AsyncClient
    PATH_GET_ALLMATCHUPS = "api/events?offset=0&per-page=100&sort-by=start&sort-direction=asc&sport-ids=15"
    PATH_GET_EVENTSNOW = "https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplayInfo/eventsNow"
    PATH_INPLAY_INFO = "https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplayInfo?eventIds="
    all_matchups: list = []

    def __init__(self, client, manager_matchups: ManageMatchups):
        self.client = client
        self.manager_matchups = manager_matchups

    async def get_markets(self, id_matchup):
        path = f"api/events/{id_matchup}"
        response = await self.client.get(path, timeout=None)
        data = response.json()
        markets = data.get("markets")

        return markets

    async def get_all_matchups(self):
        #requisitando os jogos na api
        response = await self.client.get(self.PATH_GET_ALLMATCHUPS, timeout=None)
        #convertendo para json
        data = response.json()
        #filtrando os eventos que jogos e não ligar ou outros exportes
        filter_lambda = lambda event: len(event['event-participants']) == 2 and event["id"][0:2] == '29'
        # data_sorted = filter(filter_lambda, data["events"])

        PATH_INPLAY_INFO = self.PATH_INPLAY_INFO
        self.all_matchups = []
        for event in data['events']:
            if not filter_lambda(event):
                continue

            matchup = Matchup(event)
            if matchup.matchup_expired():
                continue
    
            if not matchup.is_running:
                continue
            
            #adiciona esse evento na url de eventos para pegar mais informações
            PATH_INPLAY_INFO += f"{matchup.id},"
            self.all_matchups.append(matchup)

        #requisitar na api detalhes dos jogos ao vivo
        detail_matchups = await self.client.get(PATH_INPLAY_INFO, timeout=None)
        detail_matchups = detail_matchups.json()
        #criar uma regra de ordem entre os jogos por horar de incio da partida de forma crescente
        all_matchups_sorted = sorted(self.all_matchups, key=lambda event: event.start)
        # self.manager_matchups.set_matchups(all_matchups_sorted)
        self.implement_detail_live_event(all_matchups_sorted, detail_matchups)

        # with open("project_ladder_elite/all_matchups.json", "w") as file:
        #     data = json.dump(data, file, indent=4)

        return all_matchups_sorted
    
    def implement_detail_live_event(self, all_matchups_sorted, detail_matchups):
        """Essa função busca informações mais detalhadas de cada jogo que estiver (ao vivo|in live)"""
        for matchup in all_matchups_sorted:
            for detail_matchup in detail_matchups:
                if str(detail_matchup["eventId"]) == matchup.id:
                    matchup.implement_detail_live(detail_matchup)

    async def get_market(self, event_id, market_ids):
        """Essa função retorna o mercado e os preços de todos os mercados"""
        path = f"api/events/{event_id}?market-ids={market_ids}"
        response = await self.client.get(path, timeout=None)
        return response.json()


class SyncApi:
    """essa classe é uma interface de interação com a api da bolsa de apostas bet"""

    client: Client
    PATH_GET_ALLMATCHUPS = "api/events?offset=0&per-page=100&sort-by=start&sort-direction=asc&sport-ids=15"
    PATH_GET_EVENTSNOW = "https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplayInfo/eventsNow"
    PATH_INPLAY_INFO = "https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplayInfo?eventIds="
    all_matchups: list = []

    def __init__(self, client, manager_matchups: ManageMatchups):
        self.client = client
        self.manager_matchups = manager_matchups


    def get_all_matchups(self):
        #requisitando os jogos na api
        response = self.client.get(self.PATH_GET_ALLMATCHUPS, timeout=None)
        #convertendo para json
        data = response.json()
        #filtrando os eventos que jogos e não ligar ou outros exportes
        filter_lambda = lambda event: len(event['event-participants']) == 2 and event["id"][0:2] == '29'
        # data_sorted = filter(filter_lambda, data["events"])

        PATH_INPLAY_INFO = self.PATH_INPLAY_INFO
        self.all_matchups = []
        for event in data['events']:
            if not filter_lambda(event):
                continue

            matchup = Matchup(event)
            if matchup.matchup_expired():
                continue
    
            if not matchup.is_running:
                continue
            
            #adiciona esse evento na url de eventos para pegar mais informações
            PATH_INPLAY_INFO += f"{matchup.id},"
            self.all_matchups.append(matchup)

        #requisitar na api detalhes dos jogos ao vivo
        detail_matchups = self.client.get(PATH_INPLAY_INFO, timeout=None)
        detail_matchups = detail_matchups.json()
        #criar uma regra de ordem entre os jogos por horar de incio da partida de forma crescente
        all_matchups_sorted = sorted(self.all_matchups, key=lambda event: event.start)
        # self.manager_matchups.set_matchups(all_matchups_sorted)
        self.implement_detail_live_event(all_matchups_sorted, detail_matchups)

        # with open("project_ladder_elite/all_matchups.json", "w") as file:
        #     data = json.dump(data, file, indent=4)

        return all_matchups_sorted
    
    def implement_detail_live_event(self, all_matchups_sorted, detail_matchups):
        """Essa função busca informações mais detalhadas de cada jogo que estiver (ao vivo|in live)"""
        
        for matchup in all_matchups_sorted:
            for detail_matchup in detail_matchups:
                if str(detail_matchup["eventId"]) == matchup.id:
                    matchup.implement_detail_live(detail_matchup)
