

class Event:
    """
    Essa classe tenta abstrair um evento onde cada evento pode conter classificações
    diferentes

    pode ser tanto um evento(partida); Real Madrid vs Paris Saint German
    quanto pode ser um event(serie) Ex; Seríe A, Chanpions-League

    """

    _event_id: str
    _minute: str
    _name_home: str
    _name_away: str
    _score_home: str
    _score_away: str
    _status: str

    def __init__(self, json: dict):
        self._minute = json.get("timeElapsed")
        self._status = json.get("status")
        self._name_home = json.get("score").get("home").get("name")
        self._name_away = json.get("score").get("away").get("name")
        self._score_home = json.get("score").get("home").get("score")
        self._score_away = json.get("score").get("away").get("score")
        self._event_id = json.get('eventId')

    def get_id(self):
        return self._event_id

    def get_matchup_name(self):
        return f"{self._name_home} X {self._name_away}"

    def get_home_name(self):
        return self._name_home

    def get_away_name(self):
        return self._name_away

    def get_time(self):
        return self._minute

    def get_score_home(self):
        return self._score_home

    def get_score_away(self):
        return self._score_away

    def get_status(self):
        return self._score_away

    def compair_id(self, event_id):
        return self._event_id == event_id

    def to_json(self):
        return {
            "id": self.get_id(),
            "minute": self.get_time(),
            "matchup_name": self.get_matchup_name(),
            "name_home": self.get_home_name(),
            "name_away": self.get_away_name(),
            "score_home": self.get_score_home(),
            "score_away": self.get_score_away(),
            "status": self.get_status()
        }
