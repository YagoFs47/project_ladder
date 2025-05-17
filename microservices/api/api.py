from json import JSONDecodeError

from httpx import AsyncClient, Client
from http.client import HTTPException

from microservices.utils.matchup import ManageMatchups, Matchup
from microservices.utils.event import Event
import json


class Api:
    """essa classe é uma interface de interação com a api da bolsa de apostas bet"""

    client: AsyncClient
    PATH_GET_ALLMATCHUPS = "api/events?offset=0&per-page=100&sort-by=start&sort-direction=asc&sport-ids=15"
    # PATH_GET_EVENTSNOW = "https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplayInfo/eventsNow"
    PATH_INPLAY_INFO = "https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplayInfo?eventIds="
    "https://mexchange-api.bolsadeaposta.bet.br/api/events/30049108214900076?market-ids=30049108845200076"
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
        # requisitando os jogos na api
        response = await self.client.get(self.PATH_GET_ALLMATCHUPS, timeout=None)
        # convertendo para json
        data = response.json()
        # filtrando os eventos que jogos e não ligar ou outros exportes
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

            # adiciona esse evento na url de eventos para pegar mais informações
            PATH_INPLAY_INFO += f"{matchup.id},"
            self.all_matchups.append(matchup)

        # requisitar na api detalhes dos jogos ao vivo
        detail_matchups = await self.client.get(PATH_INPLAY_INFO, timeout=None)
        detail_matchups = detail_matchups.json()
        # criar uma regra de ordem entre os jogos por horar de incio da partida de forma crescente
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

    async def get_market_with_prices(self, event_id, market_ids) -> dict:
        """Essa função retorna o mercado e os preços de todos os mercados"""
        path = f"api/events/{event_id}?market-ids={market_ids}"
        response = await self.client.get(path, timeout=None)
        try:
            return response.json()
        except JSONDecodeError:
            pass


class SyncApi:
    """essa classe é uma interface de interação com a api da bolsa de apostas bet"""

    client: Client
    PATH_GET_ALLMATCHUPS = "api/events?offset=0&per-page=100&sort-by=start&sort-direction=asc&sport-ids=15"
    # PATH_GET_EVENTSNOW = "https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplayInfo/eventsNow"
    PATH_INPLAY_INFO = "https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplay-info?eventIds="
    LIVE_MATCHUPS_URL = "https://bolsadeaposta.bet.br/client/api/jumper/feedSports/inplay-info"
    DEVICE_TOKEN_173565 = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJZYWdvRnJlaXJlIiwiZXhwIjoxNzQ1Nzg2NzczLCJ1bmlxdWUiOiJ4QlFoeTM3UiJ9.q2VE08apbnPqExI4TvSAUpehB2-tA9xZQvPywPXNmS_hX9uJQc1HvjahMauyf-MV1Vwr_kHEL0Uv9l_Vh4QIzg"

    all_matchups: list = []

    def __init__(self, client, manager_matchups: ManageMatchups):
        self.client = client
        self.manager_matchups = manager_matchups

    def get_all_matchups(self):
        
        response = self.client.get(self.PATH_GET_ALLMATCHUPS, timeout=None) # requisitando os jogos na api
        
        data = response.json()
        ids_to_request_more_detail = str()
        
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
        for data_json in data['events']:
            matchup = Event(data_json)
            # if matchup.is_live():
                # ids_to_request_more_detail += f"{matchup.id},"
                # self.all_matchups.append(matchup)

        # filter_lambda = lambda event: len(event['event-participants']) == 2 and event['in-running-flag'] == True # filtrando os eventos que jogos e não ligar ou outros exportes
        
        self.all_matchups = []


        detail_matchups = self.client.get(self.PATH_INPLAY_INFO, timeout=None) # requisitar na api detalhes dos jogos ao vivo
        detail_matchups = detail_matchups.json()
        
        all_matchups_sorted = sorted(
            self.all_matchups, 
            key=lambda event: event.start
            ) # criar uma regra de ordem entre os jogos por horar de incio da partida de forma crescente
        
        # self.implement_detail_live_event(all_matchups_sorted, detail_matchups) # self.manager_matchups.set_matchups(all_matchups_sorted)

        return all_matchups_sorted

    def get_live_matchups(self):
        response = self.client.get(self.LIVE_MATCHUPS_URL)

        if response.status_code != 200:
            raise HTTPException(response.status_code, "A busca pelo jogos não funcinou!")

        events = [Event(event) for event in response.json()]

        return events

    def get_market_with_prices(self, event_id, market_ids) -> dict:
        """Essa função retorna o mercado e os preços de todos os mercados"""
        path = f"api/events/{event_id}?market-ids={market_ids}"
        response = self.client.get(path, timeout=None)
        try:
            return response.json()
        except JSONDecodeError:
            pass
