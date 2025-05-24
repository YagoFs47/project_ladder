from abc import ABC, abstractmethod

from httpx import Client, Cookies

from home.schemas.schemas_bolsa_login import BolsaAuthJwtTokens


class AuthInterface(ABC):

    @abstractmethod
    def update_tokens(self, client: Client, tokens: BolsaAuthJwtTokens) -> Cookies:
        pass

    @abstractmethod
    def login_bolsa(self, client: Client) -> Cookies:
        pass
