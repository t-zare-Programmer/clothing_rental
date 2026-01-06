from rest_framework import serializers
from .models import Wallet, WalletTransaction

#_____________________________________________________________________________________________________________
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance']
#_____________________________________________________________________________________________________________
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = (
            "id",
            "amount",
            "transaction_type",
            "description",
            "created_at",
        )
#_____________________________________________________________________________________________________________
class WalletDepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)