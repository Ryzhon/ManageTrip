from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json
from .models import ChatModel
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_'+str(self.room_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print(self.scope)
        # print("----------")
        # print(self.scope['url_route'])
        # print("----------------")
        # print(self.scope['url_route']['kwargs'])
        # print(self.scope['user'])
        # print(self.scope['path'])
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.room_group_name)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        loginUser = text_data_json['loginUser']

        await sync_to_async(ChatModel(room_slug=self.room_name, message=message, author=loginUser).save)()
        await self.channel_layer.group_send(self.room_group_name, {'message': message,'loginUser':loginUser ,'type':'send_back'})

    async def send_back(self, event):
        message = event['message']
        loginUser = event['loginUser']
        print(event)
        await self.send(text_data=json.dumps({'message': message, 'loginUser': loginUser}))

