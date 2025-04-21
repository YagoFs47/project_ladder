from django.http import JsonResponse, HttpResponse
from django.core.handlers.asgi import ASGIRequest
from django.db.models import Q
from asgiref.sync import sync_to_async
from home.models import (OpeningBetModel, ClosingBetModel, FlowModel)
from home.api.schemas import BetSchema
from microservices.utils.functions import hash_oposition_side
from ninja import Router
import time
from functools import partial
import asyncio
import json

router = Router()

@router.get(path="/")
async def get_info_database(request):
    print(request)
    @sync_to_async
    def get_all():
        # all = [item.to_json() for item in ApostaModel.objects.all()]
        all = []
        return all
    
    return JsonResponse(status=200, data={"data": await get_all()})

@router.post(path="/")
async def create_bet(request: ASGIRequest, data:BetSchema):

    print(request.POST)
    print(json.loads(request.body))
    payload:dict = json.loads(request.body)
    oposition_side = hash_oposition_side.get(payload.get("side"))
    flow = None

    #STEP1) SABER SE EXISTE ALGUM FLUXO ABERTO
    if await FlowModel.objects.filter(Q(is_open=True)).aexists():
        flow = await FlowModel.objects.filter(Q(is_open=True)).afirst()

    else:
        #STEP1) SE NÃO EXISTE FLUXO ABERTO, CRIAR UM NOVO FLUXO
        flow = await FlowModel.objects.acreate(orientation=payload.get("side"))
        await flow.asave()
        print("[FLUXO CRIADO]")
    
    if flow.orientation == payload.get("side"):
        await OpeningBetModel(
            **payload
        ).asave()

    else:
        await ClosingBetModel(
            **payload
        ).asave()



    #STEP2) SE FOR UM FECHAMENTO, ENCONTRAR O BACK OU LAY QUE MATCHED

    return JsonResponse(status=200, data={})

@router.get(path="/delete_all/")
async def test(request: ASGIRequest):
    # async for item in ApostaModel.objects.all():
        # await item.adelete()
    return JsonResponse(status=200, data={"data": "ok"})