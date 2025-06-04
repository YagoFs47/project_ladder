
from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from home.models import MatchupModel, StakeDefaultModel
from microservices.api.api import Api

from home.ladder.ladder import Ladder
from home.ladder.ladder_players_match_odds import LadderPlayersMatchOdds
from home.ladder.ladder_match_hedge import LadderMatchHedges

API: Api = settings.API_BOLSA_APOSTAS
ladder_manager = Ladder(LadderPlayersMatchOdds(), LadderMatchHedges())

async def home_page(request: WSGIRequest | ASGIRequest):
    events = list()
    stakes_defaults = [stake async for stake in StakeDefaultModel.objects.all().aiterator()]
    async for matchup in MatchupModel.objects.all().aiterator():
        events.append(matchup)

    return render(request, "home.html", {"events": events, "stakes_defaults": stakes_defaults})

async def ladder(request: WSGIRequest | ASGIRequest, event_id: str, market_id: str):
    response: dict = await API.get_market_with_prices(event_id, market_id)
    stakes_defaults = [stake async for stake in StakeDefaultModel.objects.all().order_by("stake").aiterator()]

    if not response:
        return render(request, "exception.html", context={"message": " Jogo expirado! "})

    ladder = await ladder_manager.get_complete_ladder(market=response['markets'][0])

    if (await MatchupModel.objects.filter(id_matchup=event_id).aexists()):
        matchup = await MatchupModel.objects.aget(id_matchup=event_id)

    else:
        matchup = {
            "id_matchup": response['id'], 
            "matchup_name": response['name'],
            "status": response['status'],
            "team_a": response["event-participants"][0]['participant-name'],
            "team_b": response["event-participants"][1]['participant-name']
            }

    return render(
        request, 
        "ladder.html", 
        context={
            "market": response['markets'][0], 
            "matchup": matchup, "ladder": ladder,
            "stakes_defaults": stakes_defaults
            })
