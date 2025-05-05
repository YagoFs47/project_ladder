import json

from asgiref.sync import sync_to_async
from django.core.handlers.asgi import ASGIRequest
from django.db.models import Q
from django.http import JsonResponse
from ninja import Router

from home.api.schemas import BetSchema
from home.models import ClosingBetModel, FlowModel, OpeningBetModel
from microservices.utils.functions import hash_oposition_side
from microservices.utils.formulas import (gerar_stake_responsabilidade_BACK, 
sair_em_responsabilidade_BACK_LAY)

router = Router()



@router.post(path="/")
async def create_bet(request: ASGIRequest, data: BetSchema):
    print(request.POST)
    print(json.loads(request.body))
    payload: dict = json.loads(request.body)
    oposition_side = hash_oposition_side.get(payload.get("side"))
    flow = None

    # STEP1) SABER SE EXISTE ALGUM FLUXO ABERTO
    if await FlowModel.objects.filter(
        Q(is_open=True,
          event_id=payload.get('event_id'),
          market_id=payload.get('market_id')
          )).aexists():
        flow = await FlowModel.objects.filter(Q(is_open=True)).afirst()

    else:
        # STEP1) SE NÃO EXISTE FLUXO ABERTO, CRIAR UM NOVO FLUXO
        flow = await FlowModel.objects.acreate(
            orientation=payload.get("side"),
            event_id=payload.get("event_id"),
            market_id=payload.get("market_id"),
            )
        await flow.asave()
        print("[FLUXO CRIADO]")

    if flow.orientation == payload.get("side"):
        model_bet = OpeningBetModel(
            **payload
        )

        if payload.get("side") == "back":
            # DECOBRIR A STAKE DE APOSTA.
            # APLICAR A FORMULA -> RESPONSABILIDADE/(odd_entrada-1) => gera a estake
            # uma responsabilidade em back de 625 em odd 5 tem uma stake de 125
            # model_bet.stake = 125
            # model_bet.responsabilidade = 625
            model_bet.stake = gerar_stake_responsabilidade_BACK(payload.get("stake"), model_bet.odd)
            model_bet.responsabilidade = payload.get('stake')
            await model_bet.asave()

        else:
            # já aposta em responsabilidade em lay, stake é a propria resposabilidade que seria 625
            model_bet.responsabilidade = payload.stake
            await model_bet.asave()
        

    else:
        # É UM FECHAMENTO, MAS TA FECHANDO QUEM ???
        await ClosingBetModel(
            **payload
        ).asave()

        #FECHAR EM BACK OU LAY É A MESMA COISA
        objects = OpeningBetModel.objects.filter(
            Q( #query para  filtrar por evento, mercado e status
                event_id=payload.get('event_id'),
                market_id=payload.get('market_id'),
                status="matched"
            )
        )
        
        async for item in objects.aiterator(): # é para descobrir se ta tentando fechar uma odd em específica
            stake_saida = sair_em_responsabilidade_BACK_LAY(item.stake, item.odd, payload.get("odd"))
            if stake_saida != payload.get('odd'): #o valor que ta sendo apostado é o valor correto ?
                continue
            
            item.status="closed"
            await item.asave()
            break
        
        else:
             # para saber se ta tentando fechar todas as odds
            await objects.aupdate(status="closed")

        #[FAÇA A APOSTA DESSE AQUI]


        # STEP2) SE FOR UM FECHAMENTO, ENCONTRAR O BACK OU LAY QUE MATCHED

    return JsonResponse(status=200, data={})

