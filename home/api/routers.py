from colorama import init
from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.shortcuts import render
from ninja import Router

from microservices.api.api import Api
from microservices.utils.functions import generate_matriz_ladder
from http import HTTPStatus

init()

router = Router()
API: Api = settings.API_BOLSA_APOSTAS

@router.get("/{event_id}")
async def get_detail_market(request: ASGIRequest, event_id: str):
    """Retorna uma lista de dados detalhados sobre cada mercado de um evento"""
    markets = await API.get_markets(event_id) # requisita por mercados daquela partida

    if not markets: # se não tiver, retorna uma lista vazia
        return render(request=request, template_name="markets.html", context={"markets": [], "event_id": event_id})

    # filtra, pega somente mercados do tipo Over/Under
    markets = filter(lambda market: market['name'] == "Total", markets)
    markets = sorted(markets, key=lambda d: d['handicap'])

    if request.content_type == "application/json":
        return render(request=request, template_name="markets.html", context={"markets": markets, "event_id": event_id})
