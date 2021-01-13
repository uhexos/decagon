from django.shortcuts import render
from rest_framework import status, viewsets
from .models import Currency, Profile, Wallet, Fund, Withdrawal
from .serializers import CurrencySerializer, ProfileSerializer, WalletSerializer, FundSerializer, WithdrawalSerializer
from rest_framework.response import Response
from .permissions import HasProfilePermission
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
import requests
import json
import decimal


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [HasProfilePermission]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        wallet = WalletSerializer(
            data={"currency": serializer.validated_data.get("currency").code})
        if wallet.is_valid():
            wallet.save(user=self.request.user)


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [HasProfilePermission]

    @action(detail=False, methods=['post'])
    def fund(self, request):
        serializer = FundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(detail=False, methods=['post'])
    def approve_funding(self, request):
        print('hit')
        fund = get_object_or_404(Fund, id=request.POST.get("fund_id"))
        main_wallet = get_object_or_404(
            Wallet, user=request.user, currency=request.user.profile.currency)
        if fund.approved == False:
            if request.user.profile.role == "NB":
                if main_wallet.currency.code == fund.currency.code:
                    main_wallet.balance += fund.amount
                    main_wallet.save()
                    fund.approved = True
                    fund.save()
                else:
                    main_wallet.balance += self.convert_currency(
                        from_currency=fund.currency.code, to_currency=main_wallet.currency.code, amount=fund.amount)
                    main_wallet.save()
                    fund.approved = True
                    fund.save()
            elif request.user.profile.role == "EL":
                wallet = Wallet.objects.get_or_create(
                    user=request.user, currency=fund.currency)[0]
                wallet.balance += fund.amount
                wallet.save()
                fund.approved = True
                fund.save()
                ws = WalletSerializer(wallet)
                return Response(ws.data)

        ws = WalletSerializer(main_wallet)
        return Response(ws.data)

    @action(detail=False, methods=['post'])
    def withdrawal(self, request):
        serializer = WithdrawalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(detail=False, methods=['post'])
    def approve_withdrawal(self, request):
        withdrawal = get_object_or_404(
            Withdrawal, id=request.POST.get("withdrawal_id"))
        main_wallet = get_object_or_404(
            Wallet, user=request.user, currency=request.user.profile.currency)
        if withdrawal.approved == False:
            if request.user.profile.role == "NB":
                if main_wallet.currency.code == withdrawal.currency.code:
                    main_wallet.balance -= withdrawal.amount
                    main_wallet.save()
                    withdrawal.approved = True
                    withdrawal.save()
                else:
                    main_wallet.balance -= self.convert_currency(
                        from_currency=withdrawal.currency.code, to_currency=main_wallet.currency.code, amount=withdrawal.amount)
                    main_wallet.save()
                    withdrawal.approved = True
                    withdrawal.save()
            elif request.user.profile.role == "EL":
                wallet = Wallet.objects.filter(
                    user=request.user, currency=withdrawal.currency.code).first()
                if wallet != None:
                    wallet.balance -= withdrawal.amount
                    wallet.save()
                    withdrawal.approved = True
                    withdrawal.save()
                    return Response(WalletSerializer(wallet).data)
                else:
                    main_wallet.balance -= self.convert_currency(
                        withdrawal.currency.code, main_wallet.currency.code, withdrawal.amount)
                    main_wallet.save()
                    withdrawal.approved = True
                    withdrawal.save()

                    ws = WalletSerializer(main_wallet)
                    return Response(ws.data)

                ws = WalletSerializer(wallet)
                return Response(ws.data)
        else:
            return Response({"detail":"Already approved"},status="204")

    def convert_currency(self, from_currency, to_currency, amount):
        url = "http://data.fixer.io/api/latest?access_key=9f4cd464b7e8ff9e6f8594af5882eea1&format=1&symbols=%s,%s" % (
            from_currency, to_currency)
        response = requests.request(
            "GET", url)
        response_dict = json.loads(response.text)

        converted_amount = amount / \
            decimal.Decimal(response_dict['rates'][from_currency]) * \
            decimal.Decimal(response_dict['rates'][to_currency])
        return converted_amount
