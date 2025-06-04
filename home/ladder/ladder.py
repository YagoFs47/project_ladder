from home.ladder.contracts.players_odds_ladder_interface import PlayersOddsLadderInterface
from home.ladder.contracts.ladder_hedges_interface import LadderMatchHedgesBackLayInterface
from home.models import BetModel
from home.schemas.bet_schemas import BetSchema
import json

class Ladder:
    players_odds_interface: PlayersOddsLadderInterface
    ladder_match_odd_interface: LadderMatchHedgesBackLayInterface
    

    def __init__(
            self, 
            players_odds_interface,
            ladder_match_odds_interface
            ):
        self.players_odds_interface = players_odds_interface
        self.ladder_match_odd_interface = ladder_match_odds_interface
    
    async def get_complete_ladder(self, market:dict) -> dict:
        """Retorna uma ladder com todo o dinheiro de todos os players em cada odd
        + exposição de mercado do user com dicas de fechamento;
        """
        ladder_with_amout_players = await self._get_ladder_players_available_amout(market)

        suggestions_and_bets = await self._proccess_ladder_bets(ladder_with_amout_players['runner_under_id'])

        self.join_suggestions_with_prices(ladder_with_amout_players, suggestions_and_bets)

        return ladder_with_amout_players

    async def _get_ladder_players_available_amout(self, market: dict) -> dict:

        return self.players_odds_interface.get_ladder_players_available_amout(market)

    def join_suggestions_with_prices(self, prices, suggestions):

        for i, suggestion in enumerate(suggestions['suggestions']):
            prices['prices'][i].update(suggestion)

    async def _proccess_ladder_bets(self, runner_id: str):
        bets = [bet async for bet in BetModel.objects.filter(runner_id=runner_id).all().aiterator()]
        bets_schemas = [BetSchema(**bet.to_bet_schema_model()) for bet in bets]

        suggestions = self.ladder_match_odd_interface.match_hedge_back_lay(bets_schemas)

        for i, bet in enumerate(bets):
            bet.partial_stake = bets_schemas[i].partial_stake
            bet.status = bets_schemas[i].status
            bet.liquidity = bets_schemas[i].liquidity
            await bet.asave()

        return suggestions



    