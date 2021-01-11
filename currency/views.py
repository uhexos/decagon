from django.shortcuts import render
from rest_framework import status, viewsets
from .models import Currency
from .serializers import CurrencySerializer
from rest_framework.response import Response

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
