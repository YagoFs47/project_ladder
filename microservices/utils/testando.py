from microservices.utils.formulas import (
    tick_back_stake, 
    tick_lay_stake,
    stake_not_hedge_lay,
    stake_not_hedge_back,
    calcular_stake_lay,
    calcular_responsabilidade, 
    )

from pydantic import BaseModel, Field
from microservices.utils.functions import odds
from colorama import init, Fore

class Aposta(BaseModel):
    stake: float
    partial_stake: float
    side: str
    odd: float
    status: str = Field(default="open")
    liquidity: float = Field(default=0)

    # def __repr__(self):
    #     return f'STK={Fore.BLUE}{self.stake}{Fore.RESET} | PSTK={Fore.MAGENTA}{self.partial_stake}{Fore.RESET} | ODD={Fore.YELLOW}{self.odd}{Fore.RESET} | STATUS={Fore.LIGHTCYAN_EX}{self.status}{Fore.RESET} | SIDE={Fore.LIGHTGREEN_EX}{self.side}{Fore.RESET}'
    
    def __str__(self):
        return f'STK={Fore.BLUE}{self.stake}{Fore.RESET} | PSTK={Fore.MAGENTA}{self.partial_stake}{Fore.RESET} | ODD={Fore.YELLOW}{self.odd}{Fore.RESET} | STATUS={Fore.LIGHTCYAN_EX}{self.status}{Fore.RESET} | SIDE={Fore.LIGHTGREEN_EX}{self.side}{Fore.RESET}'


# EXEMPLO: R$100@2.00
# [BACK-STAKE] stake -> lucro == stake * (odd - 1) ->> 100 * (2 - 1) => R$100
# [BACK-STAKE] lucro -> stake == lucro / (odd - 1) ->> 100 / (2 - 1) => R$100
# [BACK-STAKE] perda == stake

#LUCRO PARCIAL -> R$59.11@1.98

# EXEMPLO: R$100@1.90
# [LAY-STAKE] stake -> R$100
# [LAY-STAKE] lucro == stake == R$100
# [LAY-STAKE] responsabilidade -> stake * (odd - 1) => R$100 * (1.90 - 1) = R$90


apostas:list[Aposta] = []

class Ladder:
    on_new_bet_get_hedge_hash = {
        "back": None,
        "lay": None,
    }

    def __init__(self):
        self.on_new_bet_get_hedge_hash.update({
            "back": self.search_hedge_back,
            "lay": self.search_hedge_lay,
        })

    def search_hedge_lay(self, lay: Aposta):
        backs = filter(
            lambda aposta: 
            aposta.side == "back" 
            and (aposta.status == "open" or aposta.status == "partial"),
            apostas)

        for back in backs:
            stake_ideal = tick_back_stake(stake=back.partial_stake, odd_entrada=back.odd, odd_saida=lay.odd)
            print(f"Stake p/ HEDGE= {Fore.GREEN}{stake_ideal}{Fore.RESET} | Stake={Fore.RED}{lay.partial_stake}{Fore.RESET}")
            # hedge
            if stake_ideal == lay.partial_stake:
                back.status = "hedgeado"
                lay.status = "hedgeado"
                back.partial_stake = 0
                lay.partial_stake = 0
                break
            
            # partial hedge
            if lay.partial_stake < stake_ideal:
                back.status = "partial"
                back.partial_stake = stake_not_hedge_back(back, lay, stake_ideal)
                lay.status = "hedgeado"
                lay.partial_stake = 0
                #descobrir quanto ainda falta ser coberto
                break
            
            # overhedge
            if lay.partial_stake > stake_ideal:
                back.status = "hedgeado"
                back.partial_stake = 0

                lay.status = "exposto"
                lay.partial_stake = round(lay.partial_stake - stake_ideal, 2)
                continue

        #inversão de mercado
        if lay.status == 'exposto':
            data = lay.model_dump(exclude="status")
            data.update({"stake": lay.partial_stake})
            apostas.append(Aposta(**data))
            lay.stake -= lay.partial_stake
            lay.partial_stake = 0
            lay.status = "hedgeado"
    
    def search_hedge_back(self, back: Aposta):
        lays = filter(
            lambda aposta: 
            aposta.side == "lay" 
            and (aposta.status == "open" or aposta.status == "partial"),
            apostas)
        
        for lay in lays:
            # hedge
            stake_ideal = tick_lay_stake(odd_entrada=lay.odd, odd_saida=back.odd, stake=lay.partial_stake)
            if stake_ideal == back.partial_stake:
                lay.status = "hedgeado"
                lay.partial_stake = 0
                
                back.status = "hedgeado"
                back.partial_stake = 0
                break
            
            # partial hedge
            if back.partial_stake < stake_ideal:
                lay.status = "partial"
                lay.partial_stake = stake_not_hedge_lay(aposta_ideal=stake_ideal, back=back, lay=lay) #CALCULAR O VALOR NESCESSÁRIO  
                
                back.status = "hedgeado"
                back.partial_stake = 0
                #descobrir quanto ainda falta ser coberto
                break
            
            # overhedge
            if back.partial_stake > stake_ideal:
                lay.status = "hedgeado"
                lay.partial_stake = 0
                
                back.status = "exposto"
                back.partial_stake = round(back.partial_stake - stake_ideal, 2)
                continue
        
        if back.status == 'exposto':
            data = back.model_dump(exclude="status")
            data.update({"stake": back.partial_stake})
            back.stake -= back.partial_stake
            back.partial_stake = 0
            back.status = "hedgeado"
            return Aposta(**data)

    def add_bet(self, aposta: Aposta):
        r = self.on_new_bet_get_hedge_hash.get(aposta.side)(aposta)
        apostas.append(aposta)
        if r:
            apostas.append(r)

    def gerar_ladder(self):
        apostas_expostas:list[Aposta] = list(
            filter(
                lambda aposta: aposta.status == "open" 
                or aposta.status == "partial" , apostas
                    )
                )

        text_ladder = ""
        for odd in odds:
            text_ladder += f"ODD={Fore.YELLOW}{odd:.2f}{Fore.RESET}"
            tot_tick = 0
            tot_lucro = 0
            for aposta in apostas_expostas:
                if aposta.side == "back":
                    tick = tick_back_stake(odd_entrada=aposta.odd, odd_saida=odd, stake=aposta.partial_stake)
                    lucro = round(tick - aposta.partial_stake, 2)
                    tot_tick += tick
                    tot_lucro += lucro

                else:
                    tick = tick_lay_stake(odd_entrada=aposta.odd, odd_saida=odd, stake=aposta.partial_stake)
                    lucro = round(aposta.partial_stake - tick, 2)
                    tot_tick += tick
                    tot_lucro += lucro
                
                if lucro < 0:
                    text_ladder += f" | {Fore.RED}({tick}, {lucro}){Fore.RESET}"
                    continue

                text_ladder += f" | {Fore.GREEN}{tick:.2f}, {lucro:.2f}{Fore.RESET}"
            
            text_ladder += f" | {Fore.CYAN}{tot_tick:.2f}, {tot_lucro:.2f}{Fore.RESET} \n"
        print(text_ladder)
    
    def exposition_info(self):
        backs = filter(lambda aposta: aposta.side == "back", apostas)
        lays = filter(lambda aposta: aposta.side == "lay", apostas)
        lucro_potencial_back = 0
        lucro_potencial_lay = 0
        perda_potencial_back = 0
        perda_potencial_lay = 0

        for back in backs:
            lucro_potencial_back += round((back.odd - 1) * back.stake, 2)
            perda_potencial_back += back.stake
    
        for lay in lays:
            lucro_potencial_lay += lay.stake
            perda_potencial_lay += round((lay.odd - 1) * lay.stake, 2)

        exposition_back = round(lucro_potencial_lay - perda_potencial_back, 2)
        exposition_lay = round(lucro_potencial_back - perda_potencial_lay, 2)

        print(f'{Fore.BLUE}{lucro_potencial_back}{Fore.RESET} | {Fore.BLUE}{perda_potencial_back}{Fore.RESET}')
        print(f'{Fore.MAGENTA}{lucro_potencial_lay}{Fore.RESET} | {Fore.MAGENTA}{perda_potencial_lay}{Fore.RESET}')
        print(f'exposition back ->> {Fore.BLUE}{exposition_back}{Fore.RESET}')
        print(f'exposition lay ->> {Fore.BLUE}{exposition_lay}{Fore.RESET}')

        match ([exposition_back, exposition_lay]):

            case [exp_b, exp_l] if exp_b > 0 and exp_l > 0:
                print("Sem exposição")
            
            case [exp_b, exp_l] if exp_b < 0 and exp_l > 0:
                print("Exposição em back")
            
            case [exp_b, exp_l] if exp_b > 0 and exp_l < 0:
                print("Exposição em lay")
            
            case _:
                print("Exposto em ambos lados")


from home.ladder.adapters.ladder_calc_adpter import CalcHedgeAdapter
from typing import Generator
from random import Random

# from string import Formatter
random = Random()

calc = CalcHedgeAdapter()

class LadderV2:

    oposition_map_side = {
        "back": "lay",
        "lay": "back",
    }
    
    def match_one_to_many(self, active: Aposta, passives: list[Aposta]):
        print('-~' * 30)
        for passive in passives:
            if active.status == "closed":
                print('SAINDO...')
                break
            
            necessary_value = calc.get_necessary_bet(bet_active=active, bet_passive=passive)
            # print(f"{active} FECHANDO ->> {passive}")
            # print(f"{active.partial_stake} FECHANDO ->> {necessary_value}")
            
            exp_info = calc.get_level_coberture_info(bet_active=active, bet_passive=passive, value_necessary=necessary_value)

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
                # active.partial_stake = calc.get_level_over_hedge(
                #     bet_active=active, value_necessary=necessary_value
                # )
                passive.partial_stake = 0

    def show_bets(self):
        print('-='*20, "APOSTAS", '-='*20)
        for aposta in apostas:
            print(aposta)

    def match_all_bets(self, apostas: Generator[Aposta]):
        
        self.show_bets()
        for aposta in apostas:
            if not aposta.status == "closed":
                print(f"{Fore.GREEN}Entrado com: {aposta}{Fore.RESET}")
                self.match_one_to_many(
                    aposta, 
                    filter(
                        lambda x: x.status == "open" and x.side == self.oposition_map_side[aposta.side], 
                        apostas
                        )
                    )

    def gerar_apostas(self, qtd: int):
        for c in range(qtd):
            stake = random.randint(10, 1000)
            partial_stake = stake
            odd = random.choice(odds[280:])
            side = random.choice(["back", "lay"])
            apostas.append(Aposta(odd=odd, partial_stake=partial_stake, side=side, stake=stake))

    def suggestions(self):
        apostas_expostas:list[Aposta] = list(
            filter(
                lambda aposta: aposta.status == "open" 
                or aposta.status == "partial" , apostas
                    )
                )

        text_ladder = ""
        liquidity = sum([aposta.liquidity for aposta in apostas])
        print(liquidity)
        for odd in odds:
            text_ladder += f"ODD={Fore.YELLOW}{odd:.2f}{Fore.RESET}"
            tot_tick = 0
            tot_lucro = 0
            for aposta in apostas_expostas:

                if aposta.side == "back":
                    tick = tick_back_stake(odd_entrada=aposta.odd, odd_saida=odd, stake=aposta.partial_stake)
                    lucro = round(tick - aposta.partial_stake, 2)

                else:
                    tick = tick_lay_stake(odd_entrada=aposta.odd, odd_saida=odd, stake=aposta.partial_stake)
                    lucro = round(aposta.partial_stake - tick, 2)

                tot_tick += tick
                tot_lucro += lucro
                
                if liquidity + tot_lucro < 0:
                    text_ladder += f" | {Fore.RED}({tick}, {(lucro + liquidity):.2f}){Fore.RESET}"
                    continue

                text_ladder += f" | {Fore.GREEN}{tick:.2f}, {(lucro + liquidity):.2f}{Fore.RESET}"
            
            text_ladder += f" | {Fore.CYAN}{tot_tick:.2f}, {(tot_lucro + liquidity):.2f}{Fore.RESET} \n"
        print(text_ladder)

ladder = LadderV2()
# ladder = Ladder()
# ladder.add_bet(Aposta(partial_stake=100, odd=2, side="back", stake=100))
# ladder.add_bet(Aposta(partial_stake=100, odd=1.99, side="back", stake=100))
# ladder.add_bet(Aposta(partial_stake=100, odd=1.98, side="back", stake=100))