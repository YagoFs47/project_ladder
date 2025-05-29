from abc import ABC, abstractmethod
from home.schemas.bet_schemas import BetSchema

class LadderMatchHedgesBackLayInterface(ABC):

    @abstractmethod
    def match_hedge_back_lay(self, bets: list[BetSchema], bet_active: BetSchema) -> None:
        """
        Essa função irá iterar sobre todas as apostas backs 'bets'
        para cada itereção, irá calcular o valor necessário para
        corresponder em lucro aquele back, se o valor for o valor exato

        a aposta back e a aposta lay terão seus valores de 'status' trocados para 'hedgeado'

        se o valor for abaixo do esperado, a aposta back terá o seu valor de 'status' trocado para "partial",
        pois ela (back) foi parcialmente correspondida, será realizado um calculo para determinar o valor restante a ser
        correspondido, e esse valor será colocando na variável 'partial_stake' da aposta.
        Enquanto a aposta lay que tinha o valor abaixo do esperado, terá seu valor de 'status' trocado para 'hedgeado'
        pois ele já não pode mais corresponder ninguém.
        """

    @abstractmethod
    def check_coverage_level_hedge(self):
        """Checa o quão a aposta ativa está cobrindo a(s) aposta(s) passiva(s)"""
        pass

