import json

from channels.generic.websocket import (
    AsyncWebsocketConsumer,
)


class TestAsyncConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # aqui a conexão é aceita, podemos definir parâmetros iniciais antes
        # antes da troca de qualquer informação
        print("CHAMADA PARA CONNECT")
        await self.channel_layer.group_add(
            "common_chat",
            self.channel_name
        )
        await self.accept()
        print("ACCEPT!")

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
            "common_chat",
            {
                "message": text_data_json['message'],
                "type": "chat_message"
            }
        )

    async def disconnect(self, code):
        pass
        # await self.channel_layer.group_add(self.group, self.channel_name)

    async def chat_message(self, event):
        print(event)
        await self.send(text_data=json.dumps(event["message"]))
