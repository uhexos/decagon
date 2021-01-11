from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class CustomUser(AbstractUser):
    pass


class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)


class Profile(models.Model):
    currency = models.ForeignKey(
        "Currency", on_delete=models.CASCADE, related_name="main_currency")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="main_currency")


class Wallet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet_owner")
    currency = models.ForeignKey(
        "Currency", on_delete=models.CASCADE, related_name="wallet_currency")
    balance = models.DecimalField(max_digits=8, decimal_places=2,default=0)