from decimal import Decimal

"""
Não existe uma 'gerar_stake_resposabilidade LAY'
pois para entrar em back ou lay, são estratégias diferentes
para entrar em back, é preciso conveter de responsabilidade para uma stake
e apostar a stake posteriormente.

para entrar em lay, o valor de aposta é a própria responsabilidade
"""


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
