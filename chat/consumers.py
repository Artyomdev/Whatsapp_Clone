import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import Message, Room
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        #print(self.scope["user"])
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive(self, text_data):
        room_name = self.scope['url_route']['kwargs']['room_name']
        text_data_json = json.loads(text_data)
        typee = text_data_json['type']
        username = text_data_json['username']
        if typee == "text":
            message = text_data_json['message']
            await self.channel_layer.group_send(
            self.room_group_name,
                {
                    'type': 'chat_message',
                    'tur': typee,
                    'message': message,
                    'username':username
                }
            )
            await self.create_message( username , message ,room_name)
        elif typee == "read":
            await self.channel_layer.group_send(
            self.room_group_name,
                {
                    'type': 'chat_message',
                    'tur': typee,
                    'username':username
                }
            )
        else:
            url = text_data_json['url']
            filename = text_data_json['filename']
            filetype = text_data_json['ftype']
            await self.channel_layer.group_send(
            self.room_group_name,
                {
                    'type': 'chat_message',
                    'tur': typee,
                    '1': url,
                    '2': filename,
                    '3': filetype,
                    'username':username
                }
            )
        
    async def chat_message(self, event):
        room_name = self.scope['url_route']['kwargs']['room_name']
        username = event['username']
        mtype = event['tur']
        if mtype == "text":
            message = event['message']
            await self.send(text_data=json.dumps({
            'message': message,
            'username':username,
            'type': mtype,
            }))
        elif mtype == "read":
            await self.send(text_data=json.dumps({
            'username':username,
            'type': mtype,
            }))
            await self.read_message( username, room_name)
        else:
            t1 = event['1']
            t2 = event['2']
            t3 = event['3']
            await self.send(text_data=json.dumps({
            
            '1': t1,
            '2': t2,
            '3': t3,
            'username':username,
            'type': mtype,
            }))

    
    @database_sync_to_async
    def create_message(self, username , message ,room_name):
        user = User.objects.get(username = username)
        room = Room.objects.get(rid = room_name)
        Message.objects.create(mtype = "text" , user =user , content = message , room = room)
    @database_sync_to_async
    def read_message(self, username  ,room_name):
        room = Room.objects.get(rid = room_name)
        user = User.objects.get(username = username)
        Message.objects.filter(room=room).exclude(user =user).update(okundu = True)