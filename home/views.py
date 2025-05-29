
from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from home.models import MatchupModel
from microservices.api.api import Api
from microservices.utils.functions import generate_matriz_ladder

from home.ladder.ladder_players_match_odds import LadderManager

API: Api = settings.API_BOLSA_APOSTAS
ladder_manager = LadderManager()

async def home_page(request: WSGIRequest | ASGIRequest):
    events = list()
    async for matchup in MatchupModel.objects.all().aiterator():
        events.append(matchup)

    return render(request, "home.html", {"events": events})


async def ladder(request: WSGIRequest | ASGIRequest, event_id: str, market_id: str):
    response: dict = await API.get_market_with_prices(event_id, market_id)

    ladder = ladder_manager.get_ladder_players_odds(markets=response['markets'])

    if not response:
        return render(request, "exception.html", context={"message": "Jogo expirado!"})
    
    # generate_matriz_ladder(response['markets'])

    matchup = await MatchupModel.objects.aget(id_matchup=event_id)
    return render(request, "ladder.html", context={"market": response['markets'][0], "matchup": matchup, "ladder": ladder})
