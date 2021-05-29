from channels.generic.websocket import JsonWebsocketConsumer
from users.models import OnlineUser
from asgiref.sync import async_to_sync
from rest_framework.authtoken.models import Token
from django.db.models import F


class ConsumerMixin(JsonWebsocketConsumer):
    group_name = None

    def get_group_name(self):
        pass

    @staticmethod
    def inc_connections(online_user, delta=1):
        online_user.connections = F('connections') + delta
        online_user.save()

    def send_message(self, obj):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {'type': 'message.handle', 'content': obj})

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
            online_user = OnlineUser.objects.get(user=self.scope['user'])
            if online_user.connections == 1:
                online_user.delete()
            else:
                self.inc_connections(online_user, -1)

    def receive_json(self, content, **kwargs):
        try:
            if content['type'] == 'data':
                if self.scope['user'].is_authenticated:
                    message = content
                else:
                    message = {
                        'type': 'error',
                        'text': 'No authenticated used is trying to send message.'
                    }
                self.send_message(message)
            elif content['type'] == 'auth' and not self.scope['user'].is_authenticated:
                current_user = Token.objects.get(key=content['token']).user
                online_user, created = OnlineUser.objects.get_or_create(user=current_user)
                self.scope['user'] = current_user
                self.group_name = self.get_group_name()
                if not created:
                    self.inc_connections(online_user)
                async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

                self.send_message({'type': 'newConnection', 'username': current_user.username})
        except Exception as e:
            self.send_json({'type': 'error', 'text': repr(e), 'response': content})

    def message_handle(self, event):
        self.send_json(event['content'])


class CalculatorConsumer(ConsumerMixin):
    def get_group_name(self):
        return "%s_group" % self.scope['url_route']['kwargs']['room']


class TasksConsumer(ConsumerMixin):
    def get_group_name(self):
        return "finished_tasks_%s" % self.scope['user'].username
