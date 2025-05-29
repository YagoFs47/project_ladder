from home.ladder.contracts.players_odds_ladder_interface import PlayersOddsLadderInterface


class Ladder:
    players_odds_interface: PlayersOddsLadderInterface

    def __init__(self, players_odds_interface):
        self.players_odds_interface = players_odds_interface

    def match_odds_players(self, markets: dict) -> dict:
        self.players_odds_interface.get_ladder_players_odds(markets)

    def proccess_ladder_bets(runner_id: str):
        pass
    
    