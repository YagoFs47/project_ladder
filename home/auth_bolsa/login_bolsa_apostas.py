import json
from http import HTTPStatus
from http.client import HTTPException

from django.conf import settings
from httpx import Client

from home.models import SessionsBolsaApostaModel
from home.schemas.schemas_bolsa_login import (
    CookieBolsaApostas,
    PayloadLoginBolsaApostas,
)

"""Classe obsoleta!"""


class BolsaApostasLogin:
    _CookieSchema: CookieBolsaApostas
    _HEADERS: dict
    client = Client

    def __init__(self, client: Client):
        self.client = client

    def _load_cookies(self) -> CookieBolsaApostas:
        if SessionsBolsaApostaModel.objects.all().count() > 0:
            self._CookieSchema = CookieBolsaApostas.model_validate(
                SessionsBolsaApostaModel.objects.all().first()
                )
            return self._CookieSchema

    def proccess(self) -> None:
        if not self._load_cookies():
            self._login()

        match self._validate_token(self._CookieSchema):
            case "expired":
                self._login()

            case "need_review":
                self._refresh_tokens(self._CookieSchema)

        print("\033[33;7m Os tokens são válidos ou foram atualizados \033[m")

    def _refresh_tokens(self, cookies: CookieBolsaApostas):
        print("\033[35;7m Atualizando o token \033[m")

        self._load_headers("headers_bolsa")
        self._HEADERS['cookie'] = cookies.tokens_to_string()
        refresh = self.client.post(
            url="https://bolsadeaposta.bet.br/client/api/auth/refresh",
            headers=self._HEADERS
            )

        if refresh.status_code == HTTPStatus.FORBIDDEN:
            raise HTTPException(refresh.status_code, f"Não possível dar refresh no token ->> {refresh.text}")

        elif refresh.status_code == HTTPStatus.OK:
            self._CookieSchema = CookieBolsaApostas(authorization=self.client.cookies.get("Authorization"),
                biab_customer=self.client.cookies.get("BIAB_CUSTOMER"),
                sb=self.client.cookies.get("sb"))
            SessionsBolsaApostaModel.objects.all().update(**self._CookieSchema.model_dump())

            print("\033[36;7m Tokens atualizados \033[m")

    def _load_headers(self, headers_name) -> None:
        with open(f"{settings.BASE_DIR}/home/headers.json") as headers_file:
            self._HEADERS = json.load(headers_file)[headers_name]

    def _validate_token(self, cookies: CookieBolsaApostas) -> str:
        """para determinar se o token é válido, é só pegar as datas de expiração"""
        if cookies.is_expired("authorization"):
            return "expired"

        elif cookies.is_need_token_renew("authorization"):
            return "need_review"

        return "valid"

    def _login(self) -> None:
        print("\033[33;7m Fazendo login \033[m")
        google_form = self.get_google_cloudflare()
        self._load_headers(headers_name="headers_bolsa")
        payload = PayloadLoginBolsaApostas(
            ipDto=google_form,
            )

        print(payload.model_dump())

        response = self.client.post(
            cookies={
                "DEVICE_TOKEN_173565": self._CookieSchema.device_token,
                "BIAB_LANGUAGE": "PT_BR",
                "BIAB_TZ": "180",
                "twk_idm_key": "M4S2qIsUiCVbgOOWyDKY6",
                "BIAB_CURRENCY": "BRL",
                "TawkConnectionTime": "0",
                "C_U_I": ""
            },
            headers=self._HEADERS,
            url="https://bolsadeaposta.bet.br/client/api/auth/login",
            json=payload.model_dump()
        )
        # recycledApprovalId
        if response.status_code == HTTPStatus.OK:
            print("\033[33;7m Deu bom \033[m")
            self._CookieSchema = CookieBolsaApostas(
                authorization=response.cookies.get("Authorization"),
                biab_customer=response.cookies.get("BIAB_CUSTOMER"),
                sb=response.cookies.get("sb"))

            SessionsBolsaApostaModel.objects.update(
                **self._CookieSchema.model_dump()
                )

        # raise HTTPException(response.status_code, "Não foi possível realizar o login")

    def get_google_cloudflare(self) -> dict:
        """PEGA INFORMAÇÕES DO GOOGLE PARA PODER VALIDAR NO SERVIDOR DA BOLSA DE APOSTAS"""
        response = self.client.get("https://cloudflare.com/cdn-cgi/trace")
        form_google = response.read().decode().split("\n")
        form_google = {line.split("=")[0]: line.split("=")[1] for line in form_google if line}
        form_google["uag"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        form_google["longitude"] = None
        form_google["latitude"] = None
        return form_google
