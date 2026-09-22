from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = [
            "customer_id",
            "full_name",
            "date_of_birth",
            "gender",
            "phone",
            "email",
            "address",
            "city",
            "state",
            "postal_code",
            "kyc_type",
            "kyc_number",

        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            ),

            "address": forms.Textarea(
                attrs={"rows": 3}
            ),
        }