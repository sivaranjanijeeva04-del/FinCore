from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:

        model = Transaction

        fields = [
            "transaction_id",
            "account",
            "to_account",
            "transaction_type",
            "amount",
            "description",
            "transaction_status",
        ]

        widgets = {

            "amount": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01"
                }
            ),

            "description": forms.TextInput(
                attrs={
                    "placeholder":
                    "Enter transaction description"
                }
            ),
        }


    def clean(self):

        cleaned_data = super().clean()

        transaction_type = cleaned_data.get(
            "transaction_type"
        )

        account = cleaned_data.get(
            "account"
        )

        to_account = cleaned_data.get(
            "to_account"
        )

        amount = cleaned_data.get(
            "amount"
        )

        transaction_status = cleaned_data.get(
            "transaction_status"
        )


        # Amount validation

        if amount is not None and amount <= 0:

            raise forms.ValidationError(
                "Transaction amount must be greater than zero."
            )


        # Source account status

        if account:

            if account.account_status != "Active":

                raise forms.ValidationError(
                    "Transactions are allowed only "
                    "for active accounts."
                )


        # Destination account status

        if (
            transaction_type == "Transfer"
            and to_account
        ):

            if to_account.account_status != "Active":

                raise forms.ValidationError(
                    "Destination account must be active."
                )


        # Transfer validation

        if transaction_type == "Transfer":

            if not to_account:

                raise forms.ValidationError(
                    "Destination account is required "
                    "for a transfer."
                )


            if account and to_account:

                if account == to_account:

                    raise forms.ValidationError(
                        "Source and destination accounts "
                        "must be different."
                    )


            if account and amount:

                if amount > account.balance:

                    raise forms.ValidationError(
                        "Insufficient account balance "
                        "for this transfer."
                    )


        # Withdrawal validation

        if transaction_type == "Withdrawal":

            if account and amount:

                if amount > account.balance:

                    raise forms.ValidationError(
                        "Insufficient account balance "
                        "for this withdrawal."
                    )


        # Deposit validation

        if transaction_type == "Deposit":

            cleaned_data["to_account"] = None


        # Pending / Failed transfer validation

        if transaction_status in [
            "Pending",
            "Failed"
        ]:

            if transaction_type == "Transfer":

                if not to_account:

                    raise forms.ValidationError(
                        "Destination account is required "
                        "for a transfer."
                    )


        return cleaned_data