
from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from home.models import MatchupModel
from microservices.api.api import Api
from microservices.utils.functions import generate_matriz_ladder

API: Api = settings.API_BOLSA_APOSTAS


async def home_page(request: WSGIRequest | ASGIRequest):
    events = list()
    async for matchup in MatchupModel.objects.all().aiterator():
        events.append(matchup)

    return render(request, "home.html", {"events": events})


async def ladder(request: WSGIRequest | ASGIRequest, event_id: str, market_id: str):
    response: dict = await API.get_market_with_prices(event_id, market_id)
    if not response:
        return render(request, "exception.html", context={"message": "Jogo expirado!"})

    generate_matriz_ladder(response['markets'])
    matchup = await MatchupModel.objects.aget(id_matchup=event_id)
    return render(request, "ladder.html", context={"market": response['markets'][0], "matchup": matchup})
