from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    MALE, FEMALE, SECRET = range(3)
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (SECRET, 'Secret'))

    gender = models.SmallIntegerField(choices=GENDERS, default=SECRET)
