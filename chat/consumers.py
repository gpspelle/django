# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import socket
from sock import Sock
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data = text_data.replace("\'", "\"")
        text_data_json = json.loads(text_data)
        recipient = text_data_json['recipient']
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'recipient': recipient,
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):

        recipient = event['recipient']
        message = event['message']

        print(event)

        if recipient == 'itself':
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message
            }))
        else:
            # Send message back to middleware
            host_socket = '127.0.0.1'
            port = 8888

            s = Sock()
            s.connect(host_socket, port)
            data = json.dumps({'message': message})
            data = data.encode()
            s.send(data)
            s.close()




