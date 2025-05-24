from abc import ABC, abstractmethod

from httpx import Cookies

from home.models import SessionsBolsaApostaModel
from home.schemas.schemas_bolsa_login import BolsaAuthJwtTokens


class BolsaTokenInterface(ABC):

    @abstractmethod
    def save_tokens(self, model: SessionsBolsaApostaModel, cookies: Cookies) -> None:
        pass

    @abstractmethod
    def load_auth_tokens(self, model: SessionsBolsaApostaModel) -> BolsaAuthJwtTokens:
        pass
