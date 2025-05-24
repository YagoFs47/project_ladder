import json
import os
from http import HTTPStatus
from http.client import HTTPException

from django.conf import settings
from httpx import URL, Client, Cookies

from home.auth_bolsa.contracts.auth_interface import AuthInterface
from home.auth_bolsa.contracts.headers_interface import HeadersInterface
from home.auth_bolsa.contracts.tokens_interface import BolsaTokenInterface
from home.models import SessionsBolsaApostaModel
from home.schemas.schemas_bolsa_login import (
    BolsaAuthJwtTokens,
    PayloadLoginBolsaApostas,
)


class AuthProccess(BolsaTokenInterface, HeadersInterface, AuthInterface):
    AUTHORIZATION = "authorization"

    def __init__(self):
        self.client = Client()

    def proccess(self, model: SessionsBolsaApostaModel):
        """
        verifica se existe tokens
        verifica se os tokens estão expirados ou perto de expirar
        se tiver perto de expirar, renova para tokens novos
        se não, continua com os tokens atuais
        se tiver expirado, realiza o login e recebe novos tokens
        já que se os tokens estiverem expirados, não é possível renovar
        por tokes novos

        """
        if not model:
            cookies = self.login_bolsa(self.client)
            model = SessionsBolsaApostaModel()
            self.save_tokens(model, cookies)

        tokens = self.load_auth_tokens(model)
        if tokens.is_expired(self.AUTHORIZATION):
            cookies = self.login_bolsa(self.client)
            self.save_tokens(model, cookies)

        elif tokens.is_need_token_renew(self.AUTHORIZATION):
            cookies = self.update_tokens(self.client, tokens=tokens)
            self.save_tokens(model, cookies)

        print("\033[34;7m Os tokens são válidos\033[m")

    def update_tokens(self, client: Client, tokens: BolsaAuthJwtTokens) -> Cookies:
        print("\033[35;7m Atualizando o token \033[m")

        headers = self.load_headers_bolsa()
        headers.update({"cookie": tokens.tokens_to_string()})
        response = client.post(
            url=URL(os.environ.get('REFRESH_TOKEN_BOLSA_URL')),
            headers=headers
            )

        if response.status_code == HTTPStatus.OK:
            return response.cookies

        raise HTTPException(response.status_code, f"Não possível dar refresh no token ->> {response.text}")

    def save_tokens(self, model: SessionsBolsaApostaModel, cookies: Cookies) -> None:
        tokens = BolsaAuthJwtTokens(
            authorization=cookies.get("Authorization"),
            biab_customer=cookies.get("BIAB_CUSTOMER"),
            sb=cookies.get("sb"),
            )
        model.authorization = tokens.authorization
        model.biab_customer = tokens.biab_customer
        model.sb = tokens.sb
        model.save()

    def load_auth_tokens(self, model: SessionsBolsaApostaModel) -> BolsaAuthJwtTokens:
        return BolsaAuthJwtTokens.model_validate(model)

    def login_bolsa(self, client: Client) -> Cookies:
        print("\033[33;7m Fazendo login \033[m")
        google_form = self.get_google_cloudflare()  # pegando dados do google
        headers = self.load_headers_bolsa()  # carregando headers
        headers.update({"cookie": f"DEVICE_TOKEN_173565={os.environ.get('DEVICE_TOKEN')}"})  # colocando um token de device
        # chamando o endpoint de sessão do bolsa
        response = client.post(
            url=URL(os.environ.get("AUTHENTICATE_BOLSA_URL")),
            headers=headers,
            json=PayloadLoginBolsaApostas(ipDto=google_form).model_dump()
        )
        if response.status_code == HTTPStatus.OK:  # se for ok, retorna os cookies, senão, estoura exception
            return response.cookies

        # estoura uma excessão de erro de request
        raise HTTPException(response.status_code, f"Não possível efetuar login LOG => {response.text}")

    def load_headers_bolsa(self) -> dict:
        with open(f"{settings.BASE_DIR}/home/headers.json") as headers_file:
            return json.load(headers_file)['headers_bolsa']

    def load_headers_exchange(self) -> dict:
        with open(f"{settings.BASE_DIR}/home/headers.json") as headers_file:
            return json.load(headers_file)['headers_exchange']

    def get_google_cloudflare(self) -> dict:
        """PEGA INFORMAÇÕES DO GOOGLE PARA PODER VALIDAR NO SERVIDOR DA BOLSA DE APOSTAS"""
        response = self.client.get("https://cloudflare.com/cdn-cgi/trace")
        form_google = response.read().decode().split("\n")
        form_google = {line.split("=")[0]: line.split("=")[1] for line in form_google if line}
        form_google["uag"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        form_google["longitude"] = None
        form_google["latitude"] = None
        return form_google
