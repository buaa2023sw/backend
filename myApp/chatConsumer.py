import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from models import Group

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # get roomid from websocket request url kwargs
        self.room_id = int(self.scope['url_route']['kwargs']['roomId'])
        self.room = Group.objects.get(id = self.room_id)
        self.room_group_name = 'char_room_%s' % self.room_id

        # join room group
        async_to_sync(self.channel_layer.group_add) (
            self.room_group_name, self.channel_name
        )

        # accept the connect request
        self.accept()

    def disconnect(self, code):
        # disconnect the websocket connection
        async_to_sync(self.channel_layer.group_discard) (
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        assert text_data is not None
        # read the message from webcokect scope['text']['message']
        message = json.loads(text_data)['message']




