# import asyncio
# import json
# from django.contrib.auth import get_user_model
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async
#
# # from .models import Thread, ChatMessage
#
#
# class chartConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print("connected", event)
#         await self.send({
#             "type": "websocket.accept"
#         })
#         # await asyncio.sleep(10)
#         # other_user = self.scope['url_route']['kwargs']['username']
#         # me = "sample" #self.scope['user']
#         # print(other_user, me)
#         # thread_obj = await self.get_thread(me, other_user)
#         # print(thread_obj)
#         chat_room = "broadcast"#f"thraed_{thread_obj.id}"
#         self.chat_room = chat_room
#
#         await self.channel_layer.group_add(
#             chat_room,
#             self.channel_name
#         )
#         # await self.send({
#         #     "type": "websocket.close"
#         # })
#
#     async def websocket_receive(self, event):
#         print("receive", event)
#         fron_text = event.get('text', None)
#         if fron_text is not None:
#             # loaded_dict_data = json.loads(fron_text)
#             # msg = loaded_dict_data.get('message')
#             print(fron_text)
#             # user = self.scope['user']
#             # username = 'default'
#             # if user.is_authenticated:
#             #     username = user.username
#             myResponse = {
#                 'message': fron_text,#msg,
#                 'username': "username"
#             }
#             print('start send data')
#
#             # broadcast the message event to be send
#             await self.channel_layer.group_send(
#                 self.chat_room,
#                 {
#                     "type": "chat_message",
#                     "text": json.dumps(myResponse)
#                 }
#
#             )
#
#     async def chat_message(self, event):
#         # send the actual the message
#         await self.send({
#             "type": "websocket.send",
#             "text": event["text"]
#         })
#
#     async def websocket_disconnect(self, event):
#         print("disconnected", event)
#
#     # @database_sync_to_async
#     # def get_thread(self, user, other_user):
#     #     return Thread.objects.get_or_new(user, other_user)[0]
# chat/consumers.py

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer


import json
from channels.generic.websocket import AsyncWebsocketConsumer

from bourse.models import Article

from bourse.serializers import ArticleListSerializer


@database_sync_to_async
def get_data():
    articles = Article.objects.all()
    return ArticleListSerializer(articles, many=True).data


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            'nanaz',
            self.channel_name
        )
        data = await get_data()

        # Send message to room group
        await self.channel_layer.group_send(
            'nanaz',
            {
                'type': 'chat_message',
                'message': data
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            'nanaz',
            self.channel_name
        )

    # # Receive message from WebSocket
    # async def receive(self, text_data):
    #     data = await get_data()
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         'nanaz',
    #         {
    #             'type': 'chat_message',
    #             'message': data
    #         }
    #     )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
