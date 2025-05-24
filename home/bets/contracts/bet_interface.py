from abc import ABC, abstractmethod

from httpx import Client

from home.schemas.bet_schemas import BetPayloadSchema, BetSchema
from home.schemas.schemas_bolsa_login import BolsaAuthJwtTokens


class BetInterface(ABC):

    @abstractmethod
    def send_bet(
        self, paylaod: BetPayloadSchema, tokens: BolsaAuthJwtTokens = None, client: Client = Client()) -> BetSchema:
        """Envia uma dados de uma aposta para realizar
        uma aposta no site da Bolsa de Apostas
        """
        pass
