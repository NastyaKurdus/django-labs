import datetime
from celery import shared_task, Task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from .models import Calculator, History


class CallbackTaskMixin(Task):
    task_name = None

    def on_success(self, result, task_id, args, kwargs):
        self.report('success', task_id, args, result)

    def on_failure(self, exc, task_id, args, kwargs, info):
        self.report('error', task_id, args, repr(exc))

    def report(self, response_type, task_id, args, result):
        channel_layer = get_channel_layer()
        if not channel_layer:
            return

        async_to_sync(channel_layer.group_send)(
            f"finished_tasks_{args[0]}",
            {
                'type': 'message.handle',
                'content':
                    {'type': response_type,
                     'taskId': task_id,
                     'taskName': self.task_name,
                     'taskArgs': args,
                     'finishTime': str(datetime.datetime.now()),
                     'result': result},
            }
        )

    def run(self, *args, **kwargs):
        pass


class InfoTask(CallbackTaskMixin):
    task_name = 'info'


class EmailsTask(CallbackTaskMixin):
    task_name = 'emails'


@shared_task(name='info', base=InfoTask)
def get_user_info(username):
    return {'calculators': Calculator.objects.filter(owner__username=username).count(),
            'computedExpressions': History.objects.filter(calculator__owner__username=username).count()}


@shared_task(name='emails', base=EmailsTask)
def send_invitations(username, receivers):
    message = f'Hi, my name is "{username}". I am calculate expressions in calculator app. Try to use it.'
    send_mail('Calculator', message, EMAIL_HOST_USER, receivers, fail_silently=False)
    return True
