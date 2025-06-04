from abc import ABC, abstractmethod
from home.ladder.settings_ladder import ODDS

class PlayersOddsLadderInterface(ABC):
    
    @abstractmethod
    def get_ladder_players_available_amout(self, markets: dict) -> dict:
        """
        retorna uma ladder(uma lista de odds), onde será incluído o dinheiro
        """

    @abstractmethod
    def converte_prices_to_dict(self, prices: list) -> dict:
        """
        Converte a lista de odds que serão exibidas na ladder
        para dicionários, pois posterimente, será verificado quais dessas odds
        estão contidas na ladder, e para não ter 2 conjuntos de dados em lista
        gerando uma ação O(n2), um dos conjutos será transformado em MAP, para 
        transformar a ação em O(n + m) diminuindo dratiscamente o número de iterações;
        """
        pass