"""
Esse módulo é responsável por mander uma conexão entre o servidor Django
e a o servidor oficial da Bolsa de Apostas, é responsável por manter o login

"""
from httpx import Client, AsyncClient
from home.login_bolsa_apostas import BolsaApostasLogin

class BolsaApostasManager:
    client: Client | AsyncClient
    login: BolsaApostasLogin

    def __init__(self):
        self.client = Client()

