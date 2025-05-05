
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.core.handlers.asgi import ASGIRequest
from django.shortcuts import render

from home.models import MatchupModel
from microservices.api.api import Api

# get os micros serviços de modulo bot para incluir os dados no servidor


# async def home(request: WSGIRequest):
#     api: Api = settings.API_BOLSA_APOSTAS
#     # matchups = await api.get_all_matchups()

#     @sync_to_async
#     def get_all_matchups():
#         matchups = [matchup_db.to_json() for matchup_db in MatchupModel.objects.all()]
#         return matchups

#     matchups = await get_all_matchups()

#     return render(request, "home2.html", {"matchups": matchups})

async def home_page(request: WSGIRequest|ASGIRequest):
    matchups = []
    async for matchup in MatchupModel.objects.all().aiterator():
        matchups.append(matchup)

        print(matchup)
    
    return render(request, "v2/home.html", {"matchups": matchups})