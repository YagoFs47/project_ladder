from datetime import datetime
from http import HTTPStatus

from httpx import Client
from jwt import decode

from home.models import SessionsBolsaApostaModel


class BolsaAposta:
    headers_bolsa = {
        "origin": "https://bolsadeaposta.bet.br",
        "accept": "application/json, text/plain, */*",
        "referer": "https://bolsadeaposta.bet.br/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    }
    HEADERS_EXCHANGE = {
      "Origin": "https://mexchange.bolsadeaposta.bet.br",
      "Accept": "application/json",
      "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
      "Priority": "u=1, i",
      "Sec-Ch-Ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
      "Sec-Ch-Ua-Mobile": "?0",
      "Sec-Ch-Ua-Platform": "\"Windows\"",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-site",
      "Cookie": "",
      "Referer": "https://mexchange.bolsadeaposta.bet.br/",
      "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    DEVICE_TOKEN_173565 = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJZYWdvRnJlaXJlIiwiZXhwIjoxNzQ1Nzg2NzczLCJ1bmlxdWUiOiJ4QlFoeTM3UiJ9.q2VE08apbnPqExI4TvSAUpehB2-tA9xZQvPywPXNmS_hX9uJQc1HvjahMauyf-MV1Vwr_kHEL0Uv9l_Vh4QIzg"

    def __init__(self, client: Client):
        self.client = client

    def login(self):
        """FAZ O LOGIN NO SERVIDOR DA BOLSA DE APOSTAS"""
        print("Fazendo login na bolsa de apostas")
        form_google = self.get_google()
        response = self.client.post(
            cookies={
                "DEVICE_TOKEN_173565": self.DEVICE_TOKEN_173565
            },
            headers=self.headers_bolsa,
            url="https://bolsadeaposta.bet.br/client/api/auth/login",
            json={
            "ipDto": form_google,
            "longitude": None,
            "latitude": None,
            "login": "YagoFreire",
            "password": "Thifler47!",
            }
        )

        # SE O LOGIN FOR REALIZADO COM SUCESSO, O CÓDIGO DE STATUS SERÁ 200
        if response.status_code == 200:
            print("\033[36mLogin realizado com sucesso\033[m")
            self.delete_muiltiple_cookies()
            SessionsBolsaApostaModel.objects.all().delete()
            SessionsBolsaApostaModel(
                biab_customer=self.client.cookies.get("BIAB_CUSTOMER"),
                authorization=self.client.cookies.get("Authorization"),
                sb=self.client.cookies.get("sb"),
            ).save()
            # SE O LOGIN FOR REALIZADO COM SUCESSO, O CÓDIGO DE STATUS SERÁ 200
            self.client.cookies.set("DEVICE_TOKEN_173565", self.DEVICE_TOKEN_173565)
            return True

    def delete_muiltiple_cookies(self):
        """DELETA OS COOKIES DO CLIENTE"""
        for ck in self.client.cookies.jar:
            if ck.name == "Authorization" and ck.domain != "bolsadeaposta.bet.br":
                self.client.cookies.delete(name=ck.name, domain=ck.domain)
            if ck.name == "BIAB_CUSTOMER" and ck.domain != ".bolsadeaposta.bet.br":
                self.client.cookies.delete(name=ck.name, domain=ck.domain)

    def refresh_token(self, tokens_model: SessionsBolsaApostaModel):
        print("REFRESH TOKENS")
        refresh = self.client.post(url="https://bolsadeaposta.bet.br/client/api/auth/refresh", headers=self.HEADERS_EXCHANGE)

        if refresh.status_code == HTTPStatus.FORBIDDEN:
            return False

        elif refresh.status_code == HTTPStatus.OK:
            self.delete_muiltiple_cookies()

            tokens_model.biab_customer = self.client.cookies.get("BIAB_CUSTOMER")
            tokens_model.authorization = self.client.cookies.get("Authorization")
            tokens_model.sb = self.client.cookies.get("sb")
            tokens_model.save()

            return True

    def set_cookies_of_model(self, model: SessionsBolsaApostaModel):
        self.HEADERS_EXCHANGE['Cookie'] = f'BIAB_CUSTOMER={model.biab_customer};Authorization={model.authorization};sb={model.sb};'

    def verify_exp_token(self, tokens_model: SessionsBolsaApostaModel):
        payload = decode(tokens_model.biab_customer, algorithms=['HS512'], options={"verify_signature": False})
        exp = payload.get("exp")
        time_exp_token = datetime.fromtimestamp(exp)
        calc_exp_token = time_exp_token - datetime.now()
        print(calc_exp_token.seconds)
        if calc_exp_token.days == 0 and calc_exp_token.seconds <= 300:
            # TA NA HORA DE RENOVAR O TOKEN
            print("PRECISA RENOVAR OS TOKENS")
            self.refresh_token(tokens_model)
        elif calc_exp_token.days < 0:
            # token expirado
            self.login()

    def verify_tokens(self):
        # VERIFICA SE EXISTE ALGUM TOKEN NO BANCO DE DADOS
        if SessionsBolsaApostaModel.objects.count() > 0:  # EXISTE
            # SÃO VÁLIDOS ?
            tokens_model = SessionsBolsaApostaModel.objects.first()
            self.verify_exp_token(tokens_model=tokens_model)
            # VERIFICA SE OS COOKIES SÃO VÁLIDOS
            # SE O CÓDIGO DE STATUS FOR 200, OS COOKIES SÃO VÁLIDOS
            # SE O CÓDIGO DE STATUS FOR 401, OS COOKIES NÃO SÃO VÁLIDOS
            # SE O CÓDIGO DE STATUS FOR 403, OS COOKIES NÃO SÃO VÁLIDOS
            # SE O CÓDIGO DE STATUS FOR 500, OS COOKIES NÃO SÃO VÁLIDOS
            self.set_cookies_of_model(tokens_model)
            # test_session = self.client.get(
            #     url="https://mexchange-api.bolsadeaposta.bet.br/api/offers?offset=0&per-page=200",
            #     headers=self.HEADERS_EXCHANGE,
            # )

            # if test_session.status_code == 200:
            #     print("\033[36mOs cookies são válidos\033[m")
            #     return True

    def get_google(self,):
        """PEGA INFORMAÇÕES DO GOOGLE PARA PODER VALIDAR NO SERVIDOR DA BOLSA DE APOSTAS"""
        response = self.client.get("https://cloudflare.com/cdn-cgi/trace")
        form_google = response.read().decode().split("\n")
        form_google = {line.split("=")[0]: line.split("=")[1] for line in form_google if line}
        form_google["uag"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        form_google["longitude"] = None
        form_google["latitude"] = None
        return form_google

    def verify_correspondence(self):
        return self.client.get(url="https://mexchange-api.bolsadeaposta.bet.br/api/offers?offset=0&per-page=200", headers=self.HEADERS_EXCHANGE).json()
