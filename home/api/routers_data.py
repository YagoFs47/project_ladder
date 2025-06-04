
from http import HTTPStatus

from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from ninja import Router
from zoneinfo import ZoneInfo

from home.bets.bets_manager import BetManager
from home.schemas.bet_schemas import BetPayloadSchema, BetSchema
from home.models import BetModel, SessionsBolsaApostaModel
from datetime import datetime



UTC = ZoneInfo("UTC")
router = Router()
bet_manager = BetManager()


@router.post(path="/")
async def create_bet(request: ASGIRequest, data: BetPayloadSchema):
    data_dict = data.model_dump(exclude="keep_in_play", by_alias=True)
    data_dict.update(
            {
            'id': str(datetime.now().timestamp()),
            'created-at': datetime.now(tz=UTC).isoformat(),
            'stake-matched': 0,
            'partial_stake': data_dict['stake']
            }
        )
    
    # bet = BetSchema(
    #     **data_dict
    # )

    # await BetModel(
    #     **bet.model_dump()
    # ).asave()
    token = bet_manager.load_auth_tokens(model=await SessionsBolsaApostaModel.objects.afirst())
    bet_schema = bet_manager.send_bet(
        paylaod=data,
        tokens=token
    )

    print(bet_schema)
    if bet_schema:
        BetModel.objects.acreate(
            **bet_schema.model_dump(),
        )

    # data_response = bolsa_a.send_bet(
    #     payload={
    #         "odds-type": "DECIMAL",
    #         "exchange-type": "back-lay",
    #         "offers": [data.to_json()],
    #     }
    # )

    return JsonResponse( 
        data={
            "status": HTTPStatus.OK,
            "detail": "Algo deu errado!"
            },
        )
