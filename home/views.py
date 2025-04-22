from re import match
from home.tasks import my_task
from django.shortcuts import render
from django.http import HttpResponse
from microservices.utils.matchup import Matchup
from django.core.handlers.wsgi import WSGIRequest
from microservices.api.api import Api
from django.conf import settings
from django import template
from itertools import zip_longest
from pprint import pprint
from typing import List
import json
from asgiref.sync import sync_to_async
from home.models import MatchupModel

#get os micros serviços de modulo bot para incluir os dados no servidor





async def home(request: WSGIRequest):
    api: Api = settings.API_BOLSA_APOSTAS
    # matchups = await api.get_all_matchups()

    @sync_to_async
    def get_all_matchups():
        matchups = [matchup_db.to_json() for matchup_db in MatchupModel.objects.all()]
        return matchups
    
    matchups = await get_all_matchups()

    return render(request, "home2.html", {"matchups": matchups})


# def get_event_detail(request: WSGIRequest, event_id: str) -> HttpResponse:
#     api: Api = settings.API_BOLSA_APOSTAS
#     matchup = api.search_event(event_id)

#     generate_matriz_ladder(matchup)

#     return render(request, "event.html", {"matchup": matchup})