from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import Model, CharField, DateField, EmailField, \
    OneToOneField, IntegerField, DateTimeField, CASCADE


class MyUser(AbstractUser):
    SEX_CHOICES = (
        ('F', "Female"),
        ('M', 'Male'),
    )
    sex = CharField(max_length=1, choices=SEX_CHOICES)
    birth_date = DateField(null=True, blank=True)
    email = EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('username',)


class OnlineUser(Model):
    user = OneToOneField(get_user_model(), on_delete=CASCADE)
    last_joined = DateTimeField(auto_now=True)
    connections = IntegerField(default=1)
