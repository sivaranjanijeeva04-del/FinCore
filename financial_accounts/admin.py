from django.contrib import admin
from .models import FinancialAccount


@admin.register(FinancialAccount)
class FinancialAccountAdmin(admin.ModelAdmin):

    list_display = (
        "account_number",
        "customer",
        "account_type",
        "balance",
        "account_status",
        "opened_date",
    )

    list_filter = (
        "account_type",
        "account_status",
    )

    search_fields = (
        "account_number",
        "customer__customer_id",
        "customer__full_name",
        "customer__phone",
    )

    ordering = (
        "-opened_date",
    )