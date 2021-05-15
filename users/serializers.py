from rest_framework.serializers import ModelSerializer, CharField, ValidationError, SerializerMethodField
from .models import MyUser, OnlineUser


class MyUserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'email', 'username', 'sex', 'birth_date', 'password')

    def validate_password(self, value):
        if self.instance and value != self.instance.password:
            raise ValidationError("'password' should be changed using endpoint - '/api/auth/users/set_password/'.")
        return value

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class OnlineUserSerializer(ModelSerializer):
    username = SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.user.username

    class Meta:
        model = OnlineUser
        fields = ['username', 'last_joined']
