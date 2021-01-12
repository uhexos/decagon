from django.shortcuts import render
from rest_framework import status, viewsets
from .models import Currency, Profile, Wallet
from .serializers import CurrencySerializer, ProfileSerializer, WalletSerializer
from rest_framework.response import Response
from .permissions import HasProfilePermission
from rest_framework.decorators import action


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [HasProfilePermission]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        wallet = WalletSerializer()


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [HasProfilePermission]

    @action(detail=False, methods=['post'])
    def fund(self, request):
        return True

    def withdraw(self, request):
        pass

    def convert_currency(self, request):
        pass
