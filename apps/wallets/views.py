from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import WalletTransaction,Wallet
from .serializers import WalletSerializer
from drf_spectacular.utils import extend_schema
from .serializers import WalletDepositSerializer,WalletTransactionSerializer
from django.db import transaction
#_____________________________________________________________________________________________________________
@extend_schema(
    responses={200: WalletSerializer},
    description="Get wallet of authenticated user"
)
class WalletRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(
            user=self.request.user
        )
        return wallet
#_____________________________________________________________________________________________________________
@extend_schema(
    request=WalletDepositSerializer,
    responses={200: WalletSerializer},
    description="Charge wallet balance for authenticated user"
)
class WalletDepositAPIView(generics.GenericAPIView):
    serializer_class = WalletDepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]
        wallet = request.user.wallet

        # افزایش موجودی
        wallet.balance += amount
        wallet.save(update_fields=["balance"])

        # ثبت تراکنش
        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=WalletTransaction.Type.DEPOSIT,
            description="Wallet charge"
        )

        return Response(
            WalletSerializer(wallet).data,
            status=status.HTTP_200_OK
        )
#_____________________________________________________________________________________________________________
@extend_schema(
    responses={200: WalletTransactionSerializer(many=True)},
    description="List wallet transactions for authenticated user"
)
class WalletTransactionListAPIView(generics.ListAPIView):
    serializer_class = WalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WalletTransaction.objects.filter(
            wallet=self.request.user.wallet
        ).order_by("-created_at")

