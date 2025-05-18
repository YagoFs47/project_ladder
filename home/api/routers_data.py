import json

from http import HTTPStatus

from django.core.handlers.asgi import ASGIRequest
from django.db.models import Q
from django.http import JsonResponse, Http404
from ninja import Router

from home.api.schemas import BetSchema
from home.tasks import bolsa
from microservices.bolsa.interface import BolsaAposta
from home.utils import check_or_create_flow, create_bet_bolsa
from home.bet import Bet

router = Router()
bolsa_a: BolsaAposta = bolsa

@router.post(path="/")
async def create_bet(request: ASGIRequest, data: BetSchema):
    payload: dict = json.loads(request.body)
    print(data)
    print(payload)
    # data_response = bolsa_a.send_bet(
    #     payload={
    #         "odds-type": "DECIMAL",
    #         "exchange-type": "back-lay",
    #         "offers": [data.to_json()],
    #     }
    # )
    Bet(
        
    )
    # if data_response: # Salva as informações no banco de dados
    #     flow = await check_or_create_flow(payload)
    #     await create_bet_bolsa(payload, flow, data_response['offers'][0])
    #     return JsonResponse(status=200, data={})
    
    return JsonResponse(status=HTTPStatus.UNAUTHORIZED, data={"detail": "Algo deu errado!"})