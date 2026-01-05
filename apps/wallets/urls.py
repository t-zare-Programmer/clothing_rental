from django.urls import path
from .views import (
    WalletRetrieveAPIView,
    WalletDepositAPIView,
)

app_name = "wallets"

urlpatterns = [
    # GET → مشاهده کیف پول کاربر لاگین‌شده
    path("wallet/",WalletRetrieveAPIView.as_view(),name="wallet-detail"),

    # POST → شارژ کیف پول
    path("wallet/deposit/",WalletDepositAPIView.as_view(),name="wallet-deposit"),
]
