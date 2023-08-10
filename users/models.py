from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    is_active = models.BooleanField(default=False, verbose_name='пользователь верифицирован')
    verification_code = models.CharField(max_length=10, **NULLABLE, verbose_name='код верификации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
