from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

from colorama import Fore, init

init()


class Matchup:
    """Essa classe representa um jogo, transforma um matchup json em matchup object"""

    id: str
    name: str
    start: datetime
    status: str
    sport: int
    is_runnig: bool
    sp = ZoneInfo("America/Sao_Paulo")
    utc = ZoneInfo("UTC")
    formated_start: str
    team_a: str
    team_b: str
    time_elapsed: str
    home_score: str
    away_score: str
    back_odd_home: str = "X"
    lay_odd_home: str = "X"
    back_odd_away: str = "X"
    lay_odd_away: str = "X"
    back_odd_draw: str = "X"
    lay_odd_draw: str = "X"
    markets = []

    def __init__(self, json):
        self.qtd_participants = len(json['event-participants'])
        self.id = json["id"]
        self.name = json["name"]
        print(json['name'])
        self.team_a, self.team_b = json["name"].split(" vs ")
        self.start = datetime.fromisoformat(json["start"])
        self.formated_start = self.start.astimezone(self.sp).strftime("%d/%m/%Y %H:%M")
        self.status = json["status"]
        self.sport = json["sport-id"]
        self.is_running = json["in-running-flag"]
        self.implement_odds_moneyline(json)

    def is_live(self):
        return self.qtd_participants == 2 and self.is_runnig

    def implement_odds_moneyline(self, data):
        # estrutura json
        if data.get("markets"):
            # markets -> [0] runners -> [0] home -> prices [0] back-odd -> odds = float
            # markets -> [0] runners -> [0] home -> prices [1] lay-odd -> odds = float

            back_lay_string = [
                ["back_odd_home", "lay_odd_home"],
                ["back_odd_away", "lay_odd_away"],
                ["back_odd_draw", "lay_odd_draw"]
            ]
            for c in range(3):
                for d in range(2):
                    try:
                        self.__setattr__(back_lay_string[c][d], str(data.get("markets")[0].get("runners")[c].get("prices")[d].get("odds")))
                    except IndexError:
                        pass

    def __repr__(self):
        return f'[{Fore.GREEN}ID {self.id}{Fore.RESET}][{Fore.GREEN}NOME {self.name}{Fore.RESET}][{Fore.GREEN}TIME {self.formated_start}{Fore.RESET}][{Fore.GREEN}STATUS {self.status}{Fore.RESET}][{Fore.GREEN}SPORT {self.sport}{Fore.RESET}]'


class ManageMatchups:

    matchups: List[Matchup] = []

    def __init__(self):
        pass

    def register_matchup(self, matchup: Matchup):
        self.matchups.append(matchup)

    def find_matchup(self, **kwargs):
        for matchup in self.matchups:
            for k, v in kwargs.items():
                if hasattr(matchup, k) and getattr(matchup, k) == v:
                    return matchup

    def delete_matchup(self, matchup: Matchup):
        self.matchups.remove(matchup)

    def set_matchups(self, matchups: List[Matchup]):
        self.matchups = matchups.copy()
