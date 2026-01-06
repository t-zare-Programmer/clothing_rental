from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Wallet, WalletTransaction
#_____________________________________________________________________________________________________________
User = get_user_model()

@receiver(post_save, sender=User)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
#_____________________________________________________________________________________________________________
@receiver(post_save, sender=Wallet)
def create_initial_wallet_transaction(sender, instance, created, **kwargs):
    if created and instance.balance > 0:
        WalletTransaction.objects.create(
            wallet=instance,
            amount=instance.balance,
            transaction_type=WalletTransaction.Type.INITIAL,
            description="Initial wallet balance"
        )
