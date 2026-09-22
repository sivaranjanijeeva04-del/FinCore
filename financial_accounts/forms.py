from django import forms
from .models import FinancialAccount


class FinancialAccountForm(forms.ModelForm):

    class Meta:

        model = FinancialAccount

        fields = [
            "customer",
            "account_type",
            "balance",
            "account_status",
        ]

        widgets = {

            "balance": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0"
                }
            ),
        }


    def clean(self):

        cleaned_data = super().clean()

        customer = cleaned_data.get("customer")

        account_status = cleaned_data.get(
            "account_status"
        )

        balance = cleaned_data.get("balance")


        # KYC validation

        if customer:

            if customer.kyc_status != "Verified":

                raise forms.ValidationError(
                    "Account cannot be opened. "
                    "Customer KYC must be verified first."
                )


        # Balance validation

        if balance is not None and balance < 0:

            raise forms.ValidationError(
                "Account balance cannot be negative."
            )


        # New account cannot be Closed

        if account_status == "Closed":

            raise forms.ValidationError(
                "A new account cannot be created "
                "with Closed status."
            )


        return cleaned_data