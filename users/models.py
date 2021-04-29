from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField, EmailField


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
