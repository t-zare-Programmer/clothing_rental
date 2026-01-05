from rest_framework.response import Response
from rest_framework import status
from .models import WalletTransaction,Wallet
from .serializers import WalletSerializer
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .serializers import WalletDepositSerializer



@extend_schema(
    responses={200: WalletSerializer},
    description="Get wallet of authenticated user"
)
class WalletRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Wallet.objects.get(user=self.request.user)

@extend_schema(
    request=WalletDepositSerializer,
    responses={200: WalletSerializer},
    description="Charge wallet balance for authenticated user"
)
class WalletDepositAPIView(generics.GenericAPIView):
    serializer_class = WalletDepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += serializer.validated_data["amount"]
        wallet.save()

        return Response(
            WalletSerializer(wallet).data,
            status=status.HTTP_200_OK
        )

