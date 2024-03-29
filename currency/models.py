from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from decimal import Decimal
from django.core.validators import MinValueValidator
# Create your models here.


class CustomUser(AbstractUser):
    pass


class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3,primary_key=True)


class Profile(models.Model):
    ADMIN = 'AD'
    NOOB = 'NB'
    ELITE = 'EL'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (NOOB, 'Noob'),
        (ELITE, 'Elite'),
    ]
    currency = models.ForeignKey(
        "Currency", on_delete=models.CASCADE, related_name="main_currency")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=NOOB,
    )


class Wallet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet_owner")
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="wallet_currency")
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.01'))])

class Fund(models.Model):
    # from_wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name="funded_from")
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="fund_owner")
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)
    amount =  models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    approved = models.BooleanField(default=False)

class Withdrawal(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="withdrawal_owner")
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)
    amount =  models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    approved = models.BooleanField(default=False)
