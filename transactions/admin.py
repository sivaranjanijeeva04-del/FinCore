from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "transaction_id",
        "account",
        "to_account",
        "transaction_type",
        "amount",
        "transaction_status",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "transaction_status",
        "created_at",
    )

    search_fields = (
        "transaction_id",
        "account__account_number",
        "account__customer__full_name",
        "to_account__account_number",
    )

    ordering = (
        "-created_at",
    )