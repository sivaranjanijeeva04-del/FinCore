from django.db import models
from customers.models import Customer


class FinancialAccount(models.Model):

    ACCOUNT_TYPE_CHOICES = [
        ("Savings", "Savings"),
        ("Current", "Current"),
        ("Fixed Deposit", "Fixed Deposit"),
    ]

    ACCOUNT_STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Closed", "Closed"),
    ]

    account_number = models.CharField(
        max_length=20,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="financial_accounts"
    )

    account_type = models.CharField(
        max_length=30,
        choices=ACCOUNT_TYPE_CHOICES
    )

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    account_status = models.CharField(
        max_length=20,
        choices=ACCOUNT_STATUS_CHOICES,
        default="Active"
    )

    opened_date = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.account_number} - {self.customer.full_name}"