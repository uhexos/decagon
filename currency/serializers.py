from rest_framework import serializers
from .models import Currency, Profile, Wallet


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name', 'code']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['currency', 'balance']
        read_only_fields = ['balance']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "currency", "role"]
        read_only_fields = ['id']

class FundSerializer(serializers.ModelSerializer):
    pass