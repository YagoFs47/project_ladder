
from http import HTTPStatus

from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from ninja import Router
from zoneinfo import ZoneInfo

from home.bets.bets_manager import BetManager
from home.schemas.bet_schemas import BetPayloadSchema, BetSchema
from home.models import BetModel
from datetime import datetime


UTC = ZoneInfo("UTC")
router = Router()
bet_manager = BetManager()

@router.post(path="/")
async def create_bet(request: ASGIRequest, data: BetPayloadSchema):
    # bet_schema: BetSchema = bet_manager.send_bet(data)
    created_at = datetime.now()
    data_dict = data.model_dump(exclude="keep_in_play", by_alias=True)
    data_dict.update(
            {
            'id': '123',
            'created-at': datetime.now(tz=UTC).isoformat(),
            'stake-matched': data_dict['stake'],
            'partial_stake': data_dict['stake']
            }
        )
    bet = BetSchema(
        **data_dict
    )
    
    # BetModel(**data_dict).save()
    
    # data_response = bolsa_a.send_bet(
    #     payload={
    #         "odds-type": "DECIMAL",
    #         "exchange-type": "back-lay",
    #         "offers": [data.to_json()],
    #     }
    # )

    return JsonResponse(
        status=HTTPStatus.UNAUTHORIZED, 
        data={"detail": "Algo deu errado!"}
        )
