import json
import os
from http import HTTPStatus
from http.client import HTTPException

from django.conf import settings
from dotenv import load_dotenv
from httpx import URL, Client

from home.auth_bolsa.contracts.headers_interface import HeadersInterface
from home.auth_bolsa.contracts.tokens_interface import BolsaTokenInterface
from home.bets.contracts.bet_interface import BetInterface
from home.schemas.bet_schemas import BetSchema
from home.schemas.schemas_bolsa_login import BolsaAuthJwtTokens

load_dotenv()


class BetManager(BolsaTokenInterface, BetInterface, HeadersInterface):

    def load_auth_tokens(self, model):
        return BolsaAuthJwtTokens.model_validate(model)

    def send_bet(self, paylaod, tokens=None, client=Client()):
        tokens = self.load_auth_tokens()
        headers = self.load_headers_exchange()
        headers.update({"cookie": tokens.tokens_to_string()})
        response = client.post(
            url=URL(os.environ.get("SEND_BET_URL")),
            headers=headers,
            json=paylaod.model_dump_json()
        )

        if response.status_code == HTTPStatus.OK:
            return BetSchema(**response.json())

        raise HTTPException(
            response.status_code,
            f"Não foi possível completar a aposta LOG -> {response.text}"
            )

    def load_headers_bolsa(self) -> dict:
        with open(f"{settings.BASE_DIR}/home/headers.json") as headers_file:
            return json.load(headers_file)['headers_bolsa']

    def load_headers_exchange(self) -> dict:
        with open(f"{settings.BASE_DIR}/home/headers.json") as headers_file:
            return json.load(headers_file)['headers_exchange']

    def save_tokens(self, model, cookies) -> None:
        pass
