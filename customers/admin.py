from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "customer_id",
        "full_name",
        "phone",
        "email",
        "kyc_type",
        "kyc_status",
        "created_at",
    )

    list_filter = (
        "gender",
        "kyc_type",
        "kyc_status",
    )

    search_fields = (
        "customer_id",
        "full_name",
        "phone",
        "email",
        "kyc_number",
    )

    ordering = (
        "-created_at",
    )