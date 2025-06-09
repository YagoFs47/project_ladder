from home.ladder.contracts.ladder_hedges_interface import LadderMatchHedgesBackLayInterface
from home.ladder.adapters.ladder_calc_adpter import CalcHedgeAdapter
from home.ladder.settings_ladder import ODDS
import json
from colorama import init, Fore
init()

CALC = CalcHedgeAdapter()

class LadderMatchHedges(LadderMatchHedgesBackLayInterface):
    oposition_side = {
        "back": "lay",
        "lay": "back"
    }

    def match_hedge_back_lay(self, bets) -> dict:
        """"""
        
        #bets = []

        #faz o hedgeamento e muda os estados e valores parciais de cada objeto
        for active in filter(lambda bet: bet.status == "open", bets):
            passives = filter(lambda bet: (bet.status == "open" and bet.side == self.oposition_side[active.side]), bets)
            self.match_one_to_many(active, passives)
        
        # com os objetos e seus estados ajustados, monta uma lista de sugestões para hedgeamento em cada possível odd
        # e liquidez(+|-) total
        # organiza todos esses dados e depois envia tudo para o front-end
        return self.generate_suggestions_hedge(bets)

    def match_one_to_many(self, active, passives):
        """Check o quão a aposta ativa está cobrindo a(s) aposta(s) passiva(s)"""
        for passive in passives:
            if active.status == "closed":
                break
            necessary_value = CALC.get_necessary_bet(bet_active=active, bet_passive=passive)
            exp_info = CALC.get_level_coberture_info(bet_active=active, bet_passive=passive, value_necessary=necessary_value)

            print(f'{str(active)} {Fore.YELLOW}FECHANDO{Fore.RESET} {str(passive)}')

            if (exp_info['percent_matched'] == 100): # hedge perfeito
                active.status = "closed"
                passive.status = "closed"
                active.liquidity += exp_info["liquidity"]
                active.partial_stake = passive.partial_stake = 0

            elif exp_info['percent_matched'] < 100: # under hedge
                active.status = "closed"
                active.partial_stake = 0
                active.liquidity += exp_info['liquidity']
                # calcs_exposistion = calc.get_level_under_hedge(bet_passive=passive, bet_active=active, value_necessary=necessary_value)
                passive.partial_stake = exp_info['exp_rest']
                
            elif exp_info['percent_matched'] > 100: # over hedge
                passive.status = "closed"
                active.partial_stake = exp_info['over_hedge']
                active.liquidity += exp_info['liquidity']
                print(str(active))
                # active.partial_stake = calc.get_level_over_hedge(
                #     bet_active=active, value_necessary=necessary_value
                # )
                passive.partial_stake = 0
            
            print(f'{str(active)} {Fore.YELLOW}FECHANDO{Fore.RESET} {str(passive)}')

    def generate_suggestions_hedge(self, bets):

        stake_apostas = dict()


        for bet in bets:
            if stake_apostas.get(bet.odd):
                if bet.status == "waiting":
                    stake_apostas[bet.odd] += bet.stake
                    continue

                stake_apostas[bet.odd] += bet.stake_matched
                continue

            elif bet.status == "waiting":
                stake_apostas.update({bet.odd : bet.stake_matched})
                continue

            stake_apostas.update({bet.odd : bet.stake_matched})


        apostas = list(filter(lambda bet: bet.status == "open", bets))

        data = {"liquidity": 0, "suggestions": []}


        liquidity = sum([aposta.liquidity for aposta in bets])

        data['liquidity'] = liquidity

        #bets = []
        # stake_apostas = {}
        # data = {"liquidity": 0, "suggestions": []}
        # apostas = []
        # liquidity = 0

        for odd in ODDS:
            tot_tick = 0
            tot_lucro = 0

            for aposta in apostas:
                necesssary_value_bet = CALC.get_necessary_bet(
                    only_odds=True, 
                    active_odd=odd, 
                    passive_odd=aposta.odd, 
                    passive_partial_stake=aposta.partial_stake
                    )
                lucro = (necesssary_value_bet - aposta.partial_stake) if aposta.side == "back" else (aposta.partial_stake - necesssary_value_bet)
                tot_lucro += lucro
                tot_tick += necesssary_value_bet
                

            if liquidity + tot_lucro > 0:
                exposition_direction = "suggestions-positive"

            elif liquidity + tot_lucro == 0:
                exposition_direction = "suggestions-middle"

            else:
                exposition_direction = "suggestions-negative"
            
            if apostas:
                side_exposition = self.oposition_side.get(apostas[0].side)
                
            else:
                side_exposition = None

            data['suggestions'].append(
                    {   
                        "tot_liquidity": round(liquidity+tot_lucro, 2),
                        "necessary_stake": round(tot_tick, 2), 
                        "liquidity_on_hedge": round(tot_lucro, 2),
                        "liquidity": round(liquidity, 2),
                        "is_positive": True if liquidity + tot_lucro > 0 else False,
                        "is_zero": True if liquidity + tot_lucro == 0 else False,
                        "stake": stake_apostas.get(odd) if stake_apostas.get(odd) else 0,
                        "contains_stake": "contains_stake" if stake_apostas.get(odd) else None,
                        "side_to_apply_stake": side_exposition,
                        "exposition_diretion": exposition_direction
                    }
                 )
        
        return data
