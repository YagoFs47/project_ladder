from home.ladder.contracts.formulas_hedges_interface import FormulasHedgesInterface


class CalcHedgeAdapter(FormulasHedgesInterface):

    def get_necessary_bet(self, bet_passive=None, bet_active=None, only_odds=False, active_odd=None, passive_odd=None, passive_partial_stake=None):
        if only_odds:
            return round(passive_partial_stake * passive_odd / active_odd, 2)
        return round(bet_passive.partial_stake * bet_passive.odd / bet_active.odd, 2)

    def get_level_over_hedge(
        self, 
        bet_active,
        value_necessary
        ):
        return round(bet_active.partial_stake - value_necessary, 2)

    def get_level_coberture_info(self, bet_passive, bet_active, value_necessary):
        """Retorna dados sobre aquela aposta
            - liquidez;
            - valor percentual de cobertura;
            - valor restante para cobrir;
            - valor de exposição cobertor;
            - valor de exposição restante;
            - valor de overheder;
            """
        percent_matched = 0
        exposition_matched = 0
        percent_rest = 0
        expostion_rest = 0
        liquidity = 0
        over_hedge = 0

        if bet_active.partial_stake > value_necessary:
            over_hedge = round(bet_active.partial_stake - value_necessary, 2)

            percent_matched = round(bet_active.partial_stake * 100 / value_necessary, 2)

            exposition_matched = bet_passive.partial_stake

            liquidity = round(value_necessary - exposition_matched, 2) if bet_active.side == "lay" \
                else round(exposition_matched - value_necessary , 2)
        
        else:
            exposition_matched = round( bet_active.partial_stake * bet_passive.partial_stake / value_necessary, 2)

            percent_matched = round(exposition_matched * 100 / bet_passive.partial_stake, 2)

            percent_rest = round(100 - percent_matched, 2)

            expostion_rest = round(bet_passive.partial_stake - exposition_matched, 2)

            liquidity = round(bet_active.partial_stake - exposition_matched, 2) if bet_active.side == "lay" \
                else round(exposition_matched - bet_active.partial_stake, 2)
    

        return {
                "liquidity": liquidity, 
                "exp_matched": exposition_matched, 
                "exp_rest": expostion_rest, 
                "percent_matched": percent_matched,
                "percent_rest": percent_rest,
                "over_hedge": over_hedge
                }

    def get_level_under_hedge( 
        self, 
        bet_passive, 
        bet_active,
        value_necessary
        ):
        # value_necessary == 141
        # bet_passive.partial_stake == 150
        # bet_active.partial_stake = 30
        # exp_initial == 141
        # exp_matched == 30 * 150 / 141 ->> 31.91
        # exp_finally == exp_initial(150) - exp_matched(31.91) == exp_finally(111.00)
        exp_intial = bet_passive.partial_stake
        exp_matched = (
            bet_active.partial_stake * bet_passive.partial_stake / value_necessary
            )
        exp_finally = round(exp_intial - exp_matched, 2)

        if (bet_active.side == "lay"):
            exp_matched - bet_active.partial_stake

        return {"exp_final": exp_finally, "exp_matched": exp_matched, "liquidity": 0}
    
    def get_responsability(self, bet_lay):
        return round(bet_lay.partial_stake * (bet_lay.odd - 1), 2)