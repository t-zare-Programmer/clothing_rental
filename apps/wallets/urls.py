from django.urls import path
from .views import (
    WalletRetrieveAPIView,
    WalletDepositAPIView,
    WalletTransactionListAPIView,
    WalletWithdrawAPIView
)

app_name = "wallets"

urlpatterns = [
    # GET → مشاهده کیف پول کاربر لاگین‌شده
    path("",WalletRetrieveAPIView.as_view(),name="wallet-detail"),

    # POST → شارژ کیف پول
    path("deposit/",WalletDepositAPIView.as_view(),name="wallet-deposit"),
    path("transactions/", WalletTransactionListAPIView.as_view()),
    path("withdraw/", WalletWithdrawAPIView.as_view(), name="wallet-withdraw"),
]
