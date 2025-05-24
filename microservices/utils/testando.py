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





ladder = Ladder()
# ladder.add_bet(Aposta(partial_stake=100, odd=2, side="back", stake=100))
# ladder.add_bet(Aposta(partial_stake=100, odd=1.99, side="back", stake=100))
# ladder.add_bet(Aposta(partial_stake=100, odd=1.98, side="back", stake=100))