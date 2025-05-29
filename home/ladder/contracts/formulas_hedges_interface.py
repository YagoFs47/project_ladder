from abc import ABC, abstractmethod
from home.schemas.bet_schemas import BetSchema

class FormulasHedgesInterface(ABC):
    """
    Essa classe fica responsável por efetuar todos os calculos
    para toda a dinâmica de hedges de back-lay
    
    * valor da aposta necessária para hedge em lucro (back-lay)
    * valor da aposta necessária para hedge em lucro (lay-back)
    * calcular responsabilidade de um lay
    * calcular o valor de lucro para em uma aposta back
    * calcular o valor restante caso a cobertura não seja completa (back)
    * calcular o valor de exposição caso a cobertura ultrapasse (back)
    * calcular o valor restante caso a cobertura não seja completa (lay)
    * calcular o valor de exposição caso a cobertura ultrapasse (lay)
    """

    @abstractmethod
    def get_necessary_bet(
        self, 
        bet_passive: BetSchema,
        bet_active: BetSchema, 
        ) -> float:
        """Retorna o valor necessário para cobrir a exposição em lucro, agnóstico de (back/lay)"""

    @abstractmethod
    def get_level_over_hedge(
        self, 
        bet_active: BetSchema, 
        value_necessary: float
        ) -> float:
        """Retorna o quanto aquela aposta está ultrapassando(expondo) o usuário
        no mercado, agnóstico de (back/lay)
        """
        pass
    
    @abstractmethod
    def get_level_under_hedge(
        self, 
        bet_passive: BetSchema, 
        bet_active: BetSchema, 
        value_necessary: float
        ) -> dict:
        """
        Retorna a parcialidade de uma entrada, o valor que ainda
        não foi correspondido, agnóstico de (back/lay)
        """
        pass

    @abstractmethod
    def get_responsability(self, bet_lay: BetSchema) -> float:
        """Retorna a responsabilidade de uma aposta lay"""
        pass
    
    @abstractmethod
    def get_level_coberture_info(self, bet_passive: BetSchema, bet_active: BetSchema, value_necessary: float) -> dict:
        pass