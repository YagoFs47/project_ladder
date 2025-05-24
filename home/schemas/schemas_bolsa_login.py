from datetime import datetime, timedelta
from os import environ

from dotenv import load_dotenv
from jwt import decode
from pydantic import BaseModel, ConfigDict

load_dotenv()


class PayloadLoginBolsaApostas(BaseModel):
    ipDto: dict
    longitude: float | int = None
    latitude: float | int = None
    login: str = environ.get("LOGIN")
    password: str = environ.get('PASSWORD')


class BolsaAuthJwtTokens(BaseModel):

    biab_customer: str
    authorization: str
    sb: str
    device_token: str = environ.get('DEVICE_TOKEN')
    model_config = ConfigDict(from_attributes=True)

    def get_exp_token(self, token_name: str) -> datetime:
        sub = decode(
            self.__getattribute__(token_name),
            options={"verify_signature": False})
        exp_datetime = datetime.fromtimestamp(sub.get("exp"))
        return exp_datetime

    def is_expired(self, token_name: str) -> bool:
        """retorna True se estiver vencido, False se ainda estiver válido"""
        sub = decode(
            self.__getattribute__(token_name),
            options={"verify_signature": False}
            )
        exp_datetime = datetime.fromtimestamp(sub.get("exp"))

        return datetime.now() >= exp_datetime

    def is_need_token_renew(self, token_name: str) -> bool:
        """retorna True se estiver perto de vencer, False se ainda estiver válido"""
        sub = decode(
            self.__getattribute__(token_name),
            options={"verify_signature": False})
        exp_datetime = datetime.fromtimestamp(
            sub.get("exp")
            )

        return (
            datetime.now() + timedelta(minutes=5)
            ) >= exp_datetime

    def tokens_to_string(self) -> str:
        """
        coloca os tokens num formato de string para
        enviar nos cookies de um headers de requisição
        no caso de requisições comuns, o Device_Token não é necessário
        enviar por padrão, somente no login()
        """
        return f"BIAB_CUSTOMER={self.biab_customer};Authorization={self.authorization};sb={self.sb};"
