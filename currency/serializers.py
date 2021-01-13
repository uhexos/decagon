from rest_framework import serializers
from .models import Currency, Profile, Wallet, Fund,Withdrawal


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
    class Meta:
        model = Fund
        fields = "__all__"
        read_only_fields = ['approved']

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = "__all__"
        read_only_fields = ['approved']
