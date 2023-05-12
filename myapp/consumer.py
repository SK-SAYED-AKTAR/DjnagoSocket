from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import SyncConsumer

# Database Related
from .models import CustomUser
from django.db.models import Q

# Json Serializer
from django.core import serializers
import json


class SayedAsyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        self.send({"type": "websocket.accept"})
        username = str(self.scope['query_string'].decode()[7:])

        # Add the user to the chat_group
        async_to_sync(self.channel_layer.group_add)("chat_group", self.channel_name)
        # self.friend_channel_name = f'friend_{username}'
        
        # self.channel_layer.group_add(
        #     self.friend_channel_name,
        #     self.channel_name
        # )
        

        try:
            user = CustomUser.objects.get(email_or_phone=username)
            print("The User", user)
            cur_user = user
        except CustomUser.DoesNotExist:
            cur_user = None
        ret_data = self.get_friend_details(cur_user)
        friend_details = ret_data[1]
        if ret_data[0] == "nothing":
            data = {
                "gotUser": "no"
            }
            self.send({
                "type": "websocket.send",
                "text": json.dumps(data)
            })
        elif ret_data[0] == True:
            data = {
                    "gotUser": "yes",
                    "name": friend_details.full_name, 
                    "contact": friend_details.email_or_phone, 
                    "gender":  friend_details.gender,
                    "country":  friend_details.country,
                    "interests": friend_details.interests
                }
        else:
            data = {
                    "gotUser": "yes",
                    "name": friend_details['full_name'], 
                    "contact": friend_details['email_or_phone'], 
                    "gender":  friend_details['gender'],
                    "country":  friend_details['country'],
                    "interests": friend_details['interests']
                }

        self.send({
            "type": "websocket.send",
            "text": json.dumps(data)
        })

    def websocket_receive(self, event):
        
        # Instantiate the channel_layer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chat_group",  # Group name to send the message to
            {
                "type": "chat.message",  # Message type that the consumers will handle
                "text": event['text']
            }
        )
        print("Websocket receive called ...")
        

    def chat_message(self, event):
        data = json.loads(event['text'])
        print(data)
        self.send({
            "type": "websocket.send",
            "text": json.dumps(data)
        })

        
    def websocket_disconnect(self, event):
        print("Websocket disconnect called ...")


    def update_connected_with(self, me, frnd):
        # Update My-Self
        myself = me
        myself.connected_with = frnd['email_or_phone']
        myself.save()

        # Update Friend 
        frienddata = CustomUser.objects.get(email_or_phone=frnd['email_or_phone'])
        frienddata.connected_with = me.email_or_phone
        frienddata.save()

    def get_friend_details(self, user):
    # If user already connected return with True else False
        if user.connected_with != "":
            frnd = CustomUser.objects.get(email_or_phone = user.connected_with)
            return (True, frnd)
        
        current_interests = user.interests.split(',')
        online_users = CustomUser.objects.filter(Q(online_status=True) & ~Q(email_or_phone=user.email_or_phone) & Q(connected_with=""))
        if len(online_users)>0:
            similar_users = CustomUser.objects.none()
            for interest in current_interests:
                interest_users = online_users.filter(interests__contains=interest)
                if interest_users.exists():
                    similar_users |= interest_users
            
            if not similar_users.exists():
                online_users = serializers.serialize('python', [online_users.first()])
                online_users = online_users[0]['fields']
                self.update_connected_with(user, online_users)
                return (False, online_users)

            similar_users = serializers.serialize('python', similar_users)
            similar_users = similar_users[0]['fields']
            self.update_connected_with(user, similar_users)
            return (False, similar_users)
        
        return ("nothing", "No User at this moment")
    


