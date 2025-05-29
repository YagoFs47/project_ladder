from decimal import Decimal

"""
Não existe uma 'gerar_stake_resposabilidade LAY'
pois para entrar em back ou lay, são estratégias diferentes
para entrar em back, é preciso conveter de responsabilidade para uma stake
e apostar a stake posteriormente.

para entrar em lay, o valor de aposta é a própria responsabilidade
"""

def stake_not_hedge_back(back, lay, aposta_ideal):
    porcentagem_hedgeada = round(((lay.partial_stake * 100) / aposta_ideal), 2)
    porcentamge_not_hedgeada = 100 - porcentagem_hedgeada

    return  round(porcentamge_not_hedgeada * 100 / back.partial_stake, 2)


def stake_not_hedge_lay(back, lay, aposta_ideal):
    stake_proporcional = (back.partial_stake * lay.partial_stake) / aposta_ideal
    stake_restante = lay.partial_stake - stake_proporcional
    return round(stake_restante, 2)


def calcular_stake_lay(responsabilidade, odd) -> float:
    return round((responsabilidade / (odd - 1)), 2)


def calcular_responsabilidade(stake, odd):
    return round((stake*odd)-stake, 2)


def tick_back_stake(odd_entrada, odd_saida, stake):
    # tick = ((odd_entrada/odd_saida)*stake)-stake
    tick = (stake * odd_entrada) / odd_saida
    return round(tick, 2)

def tick_lay_stake(odd_entrada, odd_saida, stake) -> float:
    return round(stake * odd_entrada / odd_saida, 2)
