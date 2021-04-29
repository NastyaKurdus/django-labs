from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from .models import MyUser


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
