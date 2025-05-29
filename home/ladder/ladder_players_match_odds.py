from home.ladder.contracts.players_odds_ladder_interface import PlayersOddsLadderInterface
from json import dumps
from home.ladder.default_data import ODDS

class LadderPlayersMatchOdds(PlayersOddsLadderInterface):

    def __init__(self):
        pass

    def get_ladder_players_odds(self, markets):
        # print(dumps(markets, indent=4))
        markets_dict:dict[str, dict] = self.converte_prices_to_dict(
            markets[0]["runners"][1]['prices']
            )

        ladder: dict = {
            "runner_under_id": markets[0]["runners"][1]['id'],
            "runner_over_id": markets[0]["runners"][0]['id'],
            "handicap": markets[0]['handicap'],
            "market_id": markets[0]['id'],
            "status": markets[0]['status'],
            "prices": list()
        }
        
        for odd in ODDS:
            exists_back = markets_dict.get("back").get(odd)
            exists_lay = markets_dict.get("lay").get(odd)
            odd_ladder = {"odd": odd, "back": 0, "lay": 0}

            if exists_back:
                odd_ladder['back'] = exists_back['available-amount']
                
            elif exists_lay:
                odd_ladder['lay'] = exists_lay['available-amount']

            ladder['prices'].append(odd_ladder)
        
        return ladder
    
    def converte_prices_to_dict(self, prices) -> dict:
        prices_dict = {"back": dict(), "lay": dict()}

        for price in prices:
            prices_dict.get(
                price.get('side')
            ).setdefault(
                price.get('odds'),
                price
            )
        
        return prices_dict