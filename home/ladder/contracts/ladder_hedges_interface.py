from abc import ABC, abstractmethod
from home.schemas.bet_schemas import BetSchema

class LadderMatchHedgesBackLayInterface(ABC):

    @abstractmethod
    def match_hedge_back_lay(self, bets: list[BetSchema]) -> None:
        """
        filtra uma lista de apostas no estado "open", são apostas que não foram contabilizadas
        no processo de hedgeamento, que nada mais é o processo de corresponder uma aposta oposta.

        então ao receber uma lista de apostas, irá, fechar outra aposta que esteja também "open"
        porém no lado oposto, então se a aposta da vez for um "back" irá realizar outro filtro,
        vai pegar todas as apostas "open", mas dessa vez vai pegar apena o lado oposto "lay"

        estado atual: temos uma lista de "lays" não contabilizados, e 1 "back" que irá corresponder
        esses "lays", nesse caso temos 3 possíveis casos
            1 - O "back" vai corresponder perfeitamente todos os "Lays"
            2 - O "back" irá corresponder somente uma parte da exposição em lay
            ou seja, num lay de 200, corresponder só 100, ou numa lista de 5 lays, corresponde so 2;
            3 - O "back" irá corresponder todos os "lays" porém irá passar do valor correto e criará uma 
            exposição agora e back;

            a função "check_coverage_level_hedge", se certificará de que tudo seja feito corretamente independente do caso
        
            obs: tudo o que foi exemplificando em back, tabém acontece em lay, no caso de 1 lay corresponder os backs;
        """

    @abstractmethod
    def match_one_to_many(self, active:BetSchema, passives: list[BetSchema]) -> None:
        """faz o hedgeamento de 1 apostas com todas as outras apostas do lado oposto;"""
        pass

    @abstractmethod
    def generate_suggestions_hedge(self, bets: list[BetSchema]) -> dict:
        """
        Retorna um dicionário contendo a liquidez e contendo um valor ideal para hedge
        em cada possível odd;
        """
        pass

