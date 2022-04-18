from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json, asyncio

from django.shortcuts import get_object_or_404
from chats.models import Chat, Group

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        # print('Websocket connected...', event)
        self.group_name = self.scope['url_route']['kwargs'].get('groupname').strip().lower()
        # group = Group.objects.filter(name__iexact = group_name)
        # print(group.exists())

        async_to_sync( self.channel_layer.group_add) (
            self.group_name,
            self.channel_name
        )
        
        self.send({
            'type': 'websocket.accept'
        })

    
    def websocket_receive(self, event):
        # print('Received...', event)

        user = self.scope['user']
        if user.is_authenticated:
            msg = json.loads(event['text'])['message'].strip()
            group_obj = get_object_or_404(Group, name=self.group_name)
            if msg == '':
                 self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({'user':user.username , 'message': '!!! Empty Message !!!', 'alert': True })
                }) 
            else:
                chat = Chat(
                    group = group_obj, 
                    content = msg,
                    user = user
                )
                chat.save()
                
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name, {
                        'type': 'chat.send',
                        'message': msg,
                        'user': user.username 
                    }
                )
        else:
            self.send({
                'type': 'websocket.send',
                'text': json.dumps({'user':'Anonymous User', 'message': '!!! Login Required !!!', 'alert': True })
            })

    def chat_send(self, event):
        # print(event['message'])
        
        self.send({
            'type': 'websocket.send',
            'text': json.dumps({'user': event['user'],'message':event['message'], 'alert': False})
        })

    def websocket_disconnect(self, event):
        # print('Disconnected...', event)

        async_to_sync(self.channel_layer.group_discard )(
            self.group_name, 
            self.channel_name
        )
        raise StopConsumer()