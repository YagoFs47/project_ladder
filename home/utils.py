from django.db.models import Q

from home.models import ClosingBetModel, FlowModel, OpeningBetModel
from microservices.utils.formulas import (
    gerar_stake_responsabilidade_BACK,
    sair_em_responsabilidade_BACK_LAY,
)


async def check_or_create_flow(payload):
    if await FlowModel.objects.filter(
        Q(is_open=True,
          event_id=payload.get('event_id'),
          market_id=payload.get('market_id')
          )).aexists():
        return await FlowModel.objects.filter(Q(is_open=True)).afirst()

    # STEP1) SE NÃO EXISTE FLUXO ABERTO, CRIAR UM NOVO FLUXO
    flow = await FlowModel.objects.acreate(
        orientation=payload.get("side"),
        event_id=payload.get("event_id"),
        market_id=payload.get("market_id"),
        )
    await flow.asave()
    print("[FLUXO CRIADO]")

    return flow


async def create_bet_bolsa(payload: dict, flow: FlowModel, data_response: dict) -> None:
    if flow.orientation == payload.get("side"):  # back - back
        model_bet = OpeningBetModel(
            **payload,
            bet_id=data_response['id']
        )

        if payload.get("side") == "back":
            # DECOBRIR A STAKE DE APOSTA.
            # APLICAR A FORMULA -> RESPONSABILIDADE/(odd_entrada-1) => gera a estake
            # uma responsabilidade em back de 625 em odd 5 tem uma stake de 125
            # model_bet.stake = 125
            # model_bet.responsabilidade = 625
            model_bet.stake = gerar_stake_responsabilidade_BACK(payload.get("stake"), payload.get('odd'))
            model_bet.responsabilidade = payload.get('stake')
            await model_bet.asave()

        else:
            # já aposta em responsabilidade em lay, stake é a propria resposabilidade que seria 625
            model_bet.responsabilidade = payload.get('stake')
            await model_bet.asave()

    else:
        # É UM FECHAMENTO, MAS TA FECHANDO QUEM ???
        await ClosingBetModel(
            **payload,
            bet_id=data_response['id']
        ).asave()

        # FECHAR EM BACK OU LAY É A MESMA COISA
        objects = OpeningBetModel.objects.filter(
            Q(  # query para  filtrar por evento, mercado e status
                event_id=payload.get('event_id'),
                market_id=payload.get('market_id'),
                status="matched"
            )
        )

        async for item in objects.aiterator():  # é para descobrir se ta tentando fechar uma odd em específica
            print(item.stake, item.odd, payload.get("odd"))
            stake_saida = sair_em_responsabilidade_BACK_LAY(item.stake, item.odd, payload.get("odd"))
            if stake_saida != payload.get('odd'):  # o valor que ta sendo apostado é o valor correto ?
                continue

            item.status = "closed"
            await item.asave()
            break

        else:
             # para saber se ta tentando fechar todas as odds
            await objects.aupdate(status="closed")
