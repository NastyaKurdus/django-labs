from django.contrib import admin
from .models import MyUser, OnlineUser

admin.site.register(MyUser)
admin.site.register(OnlineUser)
