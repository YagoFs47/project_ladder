
from http import HTTPStatus

from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from ninja import Router

from home.bets.bets_manager import BetManager
from home.schemas.bet_schemas import BetPayloadSchema, BetSchema
from home.models import BetModel
from datetime import datetime

router = Router()
bet_manager = BetManager()

@router.post(path="/")
async def create_bet(request: ASGIRequest, data: BetPayloadSchema):
    # bet_schema: BetSchema = bet_manager.send_bet(data)
    created_at = datetime.now()
    data_dict = data.model_dump(exclude="keep_in_play")
    data_dict.update({"created_at": created_at})
    print(data_dict)
    BetModel(**data_dict).save()
    
    # data_response = bolsa_a.send_bet(
    #     payload={
    #         "odds-type": "DECIMAL",
    #         "exchange-type": "back-lay",
    #         "offers": [data.to_json()],
    #     }
    # )

    # if data_response: # Salva as informações no banco de dados
    #     flow = await check_or_create_flow(payload)
    #     await create_bet_bolsa(payload, flow, data_response['offers'][0])
    #     return JsonResponse(status=200, data={})

    return JsonResponse(status=HTTPStatus.UNAUTHORIZED, data={"detail": "Algo deu errado!"})
