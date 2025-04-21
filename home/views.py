from re import match
from ladder_server.tasks import my_task
from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from microservices.api.api import Api
from django.conf import settings
from django import template
from itertools import zip_longest
from pprint import pprint
from typing import List
import json

#get os micros serviços de modulo bot para incluir os dados no servidor





async def home(request: WSGIRequest):
    api: Api = settings.API_BOLSA_APOSTAS
    matchups = await api.get_all_matchups()

    my_task.delay()

    return render(request, "home2.html", {"matchups": matchups})


# def get_event_detail(request: WSGIRequest, event_id: str) -> HttpResponse:
#     api: Api = settings.API_BOLSA_APOSTAS
#     matchup = api.search_event(event_id)

#     generate_matriz_ladder(matchup)

#     return render(request, "event.html", {"matchup": matchup})