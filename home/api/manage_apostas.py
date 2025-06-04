
from http import HTTPStatus
from http.client import HTTPException

from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from ninja import Router
from zoneinfo import ZoneInfo

from home.bets.bets_manager import BetManager
from home.schemas.bet_schemas import BetPayloadSchema, BetSchema
from home.models import StakeDefaultModel
from datetime import datetime
from home.schemas.default_stakes import StakeDefaultSchema, StakeDefaultPublic
from django.urls import reverse
from django.shortcuts import redirect, resolve_url




UTC = ZoneInfo("UTC")
router = Router()
bet_manager = BetManager()


@router.get(path="/", response=list[StakeDefaultPublic])
async def get_stakes(request: ASGIRequest):
    return list(
        [
            StakeDefaultPublic(stake) async for stake in StakeDefaultModel.objects.all().aiterator()
            ]
        )

@router.post(path="/{stake_id}", response=StakeDefaultPublic)
async def save_stake(request: ASGIRequest, stake_id: int):
    print("CHEGUEI AQUI")
    print(stake_id)
    if (await StakeDefaultModel.objects.filter(pk=stake_id).aexists()):
        await StakeDefaultModel.objects.filter(pk=stake_id).adelete()
        return redirect(resolve_url("home"))
    
    return JsonResponse({"status": 400, "detail": "Essa stake não existe!"})

@router.post(path="", response=StakeDefaultPublic)
async def save_stake(request: ASGIRequest, stake: StakeDefaultSchema):
    print("CHEGUEI AQUI")
    
    if not (await StakeDefaultModel.objects.filter(stake=stake.stake).aexists()):
        stake_model = await StakeDefaultModel.objects.acreate(
            stake = stake.stake
        )
        return stake_model
    
    return JsonResponse({"status": 400, "detail": "Stake já criada"})