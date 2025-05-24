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

def gerar_stake_responsabilidade_BACK(responsabilidade: float | Decimal, odd_entrada: float | Decimal):
    """
    [entrada]
    params: responsabilidade: float
    params: odd_entrada: float
    return float:2f

    Recebe o valor de responsabilidade para entrar em back, a odd entrada
    e gera um valor de saída que a STAKE, valor que será apostado
    na casa de apostas.
    """
    print(f"stake gerada {responsabilidade / (odd_entrada - 1)}")
    return round(responsabilidade / (odd_entrada - 1), 4)

def sair_em_responsabilidade_BACK_LAY(stake: float | Decimal, odd_entrada: float | Decimal, odd_saida: float | Decimal) -> float:
    """
    [saída]
    params: stake: float
    params: odd_entrada: float
    params: odd_saida: float
    return float:2f

    Apos apostar [entrada], é preciso sair, neste casa, podendo ser em back ou lay,
    para sair em back ou lay, a fórmula em a mesma
    esse valor gera o valor que deveria ser apostado para ter lucro naquela odd
    o valor muda de odd para odd, essa formula é executada centenas de vezes também
    para gerar uma lista de sugestão para todas as odds.
    """
    stake = float(stake)
    odd_entrada = float(stake)
    odd_saida = float(stake)
    hedge = ((stake * (odd_entrada - 1)) + stake) / odd_saida
    return round(hedge, 4)  # hedge

