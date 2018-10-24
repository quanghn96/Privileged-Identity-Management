# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

# class SSHConsumer(WebsocketConsumer):
#     def connect(self):
#         self.idconnection = self.scope['url_route']['kwargs']['id']
#         self.room_group_name = 'ssh_%s' % self.idconnection

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))
# chat/consumers.py
import paramiko
from .models import SSHPermission ,SSH
from django.shortcuts import get_object_or_404
client = paramiko.SSHClient()

status = False
class SSHConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        if message.split(":")[0]=='connect' :
        	statusConnect = SSHManage.connectSSH(self, message.split(":")[1])
        	if statusConnect==1 :
        		self.send(text_data=json.dumps({
        			'message':'Connect successfully'
        			}))
        	else:
        		self.send(text_data=json.dumps({
        			'message':'Connect fail !'
        			}))	
        elif message=='disconnect' :
        	SSHManage.disconnect(self)
        else:
        	SSHManage.command(self, message)
        	
class SSHManage:
    def connectSSH(self , id):
    	
    	obj = get_object_or_404(SSH, id=id)
    	client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    	try:
    		client.connect(obj.ip, port=obj.port, username=obj.username,password=obj.password)
    	except:
    		return 0	
    	return 1;    
    def disconnect(self):
    	client.close()

    def command(self, message):
    	stdin, stdout, stderr = client.exec_command(message)
    	for line in stdout:
    		self.send(text_data=json.dumps({
    			'message':line.rstrip()
    			}))

    		