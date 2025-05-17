from colorama import init
from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.shortcuts import render
from ninja import Router

from microservices.api.api import Api
from microservices.utils.functions import generate_matriz_ladder

init()

router = Router()
API: Api = settings.API_BOLSA_APOSTAS


@router.get("/{event_id}")
async def get_detail_market(request: ASGIRequest, event_id: str):
    """Retorna uma lista de dados detalhados sobre cada mercado de um evento"""
    markets = await API.get_markets(event_id)

    total_markets = []
    for index, market in enumerate(markets):

        if (market["name"] == "Total"):
            total_markets.append(market)

    total_markets = sorted(total_markets, key=lambda d: d['handicap'])
    if request.content_type == "application/json":
        return render(request=request, template_name="markets.html", context={"markets": total_markets, "event_id": event_id})


@router.get("/prices")
async def get_prices(request, market_ids: str, event_id: str):
    markets_with_prices = await API.get_market_with_prices(event_id=event_id, market_ids=market_ids)
    generate_matriz_ladder(markets_with_prices['markets'])
    return JsonResponse({"event_info": markets_with_prices})
