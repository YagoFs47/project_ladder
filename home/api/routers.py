from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.core.handlers.asgi import ASGIRequest
from microservices.api.api import Api
from microservices.utils.matchup import Matchup
from ninja import Router
from typing import List
from colorama import init
from microservices.utils.functions import generate_odds_back_lay, compair_odd, generate_matriz_ladder, hash_oposition_side
init()

router = Router()
API: Api = settings.API_BOLSA_APOSTAS


@router.get("")
async def get_markets(request: ASGIRequest, event_id: str):
    print("[REQUESTING...] 1")
    markets = await API.get_markets(event_id)
    print("[RESPOSTA] 1")

    #mostrar os mercados disponíveis para uma certa partida
    #retorno é um html

    if request.content_type == "application/json":
        return JsonResponse(markets[0], safe=False)

    if request.content_type == "text/html":
        market_ids = ",".join([market['id'] for market in markets])
        markets_with_prices = await API.get_market(event_id=event_id, market_ids=market_ids)
        generate_matriz_ladder(markets_with_prices['markets'])
        html = render(request, "ladder.html", {"markets": markets_with_prices})
        return html


@router.get("/prices")
async def get_prices(request, market_ids: str, event_id: str):
    markets_with_prices = await API.get_market(event_id=event_id, market_ids=market_ids)
    generate_matriz_ladder(markets_with_prices['markets'])
    return JsonResponse({"event_info": markets_with_prices})
