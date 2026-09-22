from django.db import models
from financial_accounts.models import FinancialAccount


class Transaction(models.Model):

    TRANSACTION_TYPE_CHOICES = [
        ("Deposit", "Deposit"),
        ("Withdrawal", "Withdrawal"),
        ("Transfer", "Transfer"),
    ]

    TRANSACTION_STATUS_CHOICES = [
        ("Success", "Success"),
        ("Pending", "Pending"),
        ("Failed", "Failed"),
    ]

    transaction_id = models.CharField(
        max_length=30,
        unique=True
    )

    account = models.ForeignKey(
        FinancialAccount,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    to_account = models.ForeignKey(
        FinancialAccount,
        on_delete=models.CASCADE,
        related_name="incoming_transfers",
        null=True,
        blank=True
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    transaction_status = models.CharField(
        max_length=20,
        choices=TRANSACTION_STATUS_CHOICES,
        default="Success"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type}"