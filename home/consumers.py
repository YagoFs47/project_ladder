import json
from urllib.parse import parse_qs

from channels.generic.websocket import (
    AsyncWebsocketConsumer,
)

from home.models import EventIdModel, MarketIdModel


class TestAsyncConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # aqui a conexão é aceita, podemos definir parâmetros iniciais antes
        # antes da troca de qualquer informação
        query_string = self.scope.get('query_string', b'').decode('utf-8')
        self.query_params = parse_qs(query_string)

        await self.register_channel()

        await self.accept()

    def _is_matchups_channel(self):
        return self.query_params['typeChannel'][0] == "matchups"

    def _is_ladder_channel(self):
        return self.query_params['typeChannel'][0] == "ladder"

    async def register_channel(self):

        if self._is_matchups_channel():
            await self.channel_layer.group_add(
            "matchups",
            self.channel_name
        )
            return

        self.event_id = self.query_params['eventId'][0]
        self.market_id = self.query_params['marketId'][0]
        try:
            self.event_model: EventIdModel = await EventIdModel.objects.aget(event_id=self.event_id)

        except EventIdModel.DoesNotExist:
            self.event_model: EventIdModel = await EventIdModel.objects.acreate(event_id=self.event_id)

        try:
            # tenta pegar o mercado x que pertence ao evento y
            self.market_model: MarketIdModel = await MarketIdModel.objects.aget(
                event_id=self.event_model,
                market_id=self.market_id
                )

        except MarketIdModel.DoesNotExist:

            # tenta pegar o mercado x que pertence ao evento y
            self.market_model: MarketIdModel = await MarketIdModel.objects.acreate(
                event_id=self.event_model,
                market_id=self.market_id
                )

        print(f'adicionando canal {self.event_id}')
        await self.channel_layer.group_add(
            f"{self.event_id}-{self.market_id}",
            self.channel_name
        )

    async def filter_action(self, dict_message):

        match (dict_message['action']):
            case "add_group":
                await self.channel_layer.group_add(
                    dict_message['group_name'],
                    self.channel_name
                )

            case "change_group":
                pass

            case "remove_group":
                pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        await self.channel_layer.group_send(
            f"{self.event_id}-{self.market_id}",
            {
                "message": text_data_json['message'],
                "type": "chat.message"
            }
        )

    async def disconnect(self, code):
        if self._is_matchups_channel():
            self.channel_layer.group_discard(
            "matchups",
            self.channel_name
        )
            return

        self.channel_layer.group_discard(
            f"{self.event_id}-{self.market_id}",
            self.channel_name
        )

        await self.market_model.adelete()
        if await MarketIdModel.objects.filter(event_id=self.event_id).acount() == 0:
            await self.event_model.adelete()
        # await self.channel_layer.group_add(self.group, self.channel_name)

    async def refresh_ladder(self, event):
        """Atualiza a ladder do dinheiro que contido nas odds"""
        await self.send(text_data=json.dumps(event["data"]))

    async def ladder_suggestions(self, event):
        """Envia para a ladder quando as apostas são correspondidas"""
        await self.send(text_data=json.dumps(event["data"]))

    async def notify_ladder(self, event):
        """Notifica a ladder de acontecimento externos
        Ex; "Mercado abriu" || "Mercado Fechou" || "aposta não foi concluída"
        """
        await self.send(text_data=f"{event.get('text')}".encode('utf-8'))

    async def refresh_matchups(self, event):
        """Atualiza informações dos jogos,
        os que acabaram, os que começaram e
        atualizações de tempo
        """
        await self.send(json.dumps(event.get('data')))
