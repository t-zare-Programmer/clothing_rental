from django.conf import settings
from django.db import models
from decimal import Decimal

#_____________________________________________________________________________________________________________
class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet({self.user})"
#_____________________________________________________________________________________________________________
class WalletTransaction(models.Model):
    class Type(models.TextChoices):
        INITIAL = "initial", "Initial"
        DEPOSIT = "deposit", "Deposit"
        WITHDRAW = "withdraw", "Withdraw"
        COMMISSION = "commission", "Commission"

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10,
        choices=Type.choices
    )
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
#_____________________________________________________________________________________________________________
from django.db import models


class CommissionConfig(models.Model):
    percentage = models.DecimalField(max_digits=5,decimal_places=2,help_text="Commission percentage (e.g. 10.00 for 10%)")
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(help_text="Commission start datetime")
    end_date = models.DateTimeField(null=True,blank=True,help_text="Commission end datetime (optional)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Commission Config"
        verbose_name_plural = "Commission Configs"

    def __str__(self):
        return f"{self.percentage}% | active={self.is_active}"

