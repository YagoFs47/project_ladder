from home.ladder.contracts.players_odds_ladder_interface import PlayersOddsLadderInterface
from json import dumps
from home.ladder.settings_ladder import ODDS

class LadderPlayersMatchOdds(PlayersOddsLadderInterface):

    def get_ladder_players_available_amout(self, market):
        # print(dumps(markets, indent=4))
        markets_dict:dict[str, dict] = self.converte_prices_to_dict(
            market["runners"][1]['prices']
            )
        

        ladder: dict = {
            "runner_under_id": market["runners"][1]['id'],
            "runner_over_id": market["runners"][0]['id'],
            "handicap": market['handicap'],
            "market_id": market['id'],
            "status": market['status'],
            "prices": list()
        }
        
        for odd in ODDS:
            exists_back = markets_dict.get("back").get(odd)
            exists_lay = markets_dict.get("lay").get(odd)
            odd_ladder = {"odd": odd, "back": "", "lay": "", "lay_color": "", "back_color": ""}

            if exists_back:
                odd_ladder['lay'] = round(exists_back['available-amount'], 0)
                odd_ladder['lay_color'] = "odd_color_lay"

            if exists_lay:
                odd_ladder['back'] = round(exists_lay['available-amount'], 0)
                odd_ladder['back_color'] = "odd_color_back"

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