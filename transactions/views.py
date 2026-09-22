from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction

from .forms import TransactionForm
from .models import Transaction


@login_required(login_url="/auth/login/")
def transaction_create(request):

    if request.method == "POST":

        form = TransactionForm(request.POST)

        if form.is_valid():

            transaction_data = form.save(commit=False)

            source_account = transaction_data.account
            destination_account = transaction_data.to_account
            amount = transaction_data.amount
            transaction_type = transaction_data.transaction_type
            transaction_status = transaction_data.transaction_status

            # Balance update only for successful transactions
            if transaction_status == "Success":

                with db_transaction.atomic():

                    # Deposit
                    if transaction_type == "Deposit":

                        source_account.balance += amount
                        source_account.save()

                    # Withdrawal
                    elif transaction_type == "Withdrawal":

                        if amount > source_account.balance:

                            messages.error(
                                request,
                                "Insufficient account balance."
                            )

                            return render(
                                request,
                                "transaction_create.html",
                                {"form": form}
                            )

                        source_account.balance -= amount
                        source_account.save()

                    # Transfer
                    elif transaction_type == "Transfer":

                        if destination_account is None:

                            messages.error(
                                request,
                                "Destination account is required."
                            )

                            return render(
                                request,
                                "transaction_create.html",
                                {"form": form}
                            )

                        if amount > source_account.balance:

                            messages.error(
                                request,
                                "Insufficient account balance."
                            )

                            return render(
                                request,
                                "transaction_create.html",
                                {"form": form}
                            )

                        source_account.balance -= amount

                        destination_account.balance += amount

                        source_account.save()
                        destination_account.save()

                    transaction_data.save()

            else:

                # Pending / Failed transaction
                # will be recorded without changing balance

                transaction_data.save()

            if transaction_status == "Success":

                messages.success(
                    request,
                    "Transaction processed successfully."
                )

            elif transaction_status == "Pending":

                messages.warning(
                    request,
                    "Transaction recorded as Pending."
                )

            elif transaction_status == "Failed":

                messages.error(
                    request,
                    "Transaction recorded as Failed."
                )

            return redirect("transaction_success")

    else:

        form = TransactionForm()

    return render(
        request,
        "transaction_create.html",
        {"form": form}
    )


@login_required(login_url="/auth/login/")
def transaction_success(request):

    return render(
        request,
        "transaction_success.html"
    )


@login_required(login_url="/auth/login/")
def transaction_list(request):

    search = request.GET.get("search", "")

    transaction_type = request.GET.get(
        "transaction_type", ""
    )

    transaction_status = request.GET.get(
        "transaction_status", ""
    )

    transactions = Transaction.objects.select_related(
        "account",
        "account__customer",
        "to_account",
    ).order_by("-created_at")

    if search:

        if transaction_type:
            transactions = transactions.filter(
                transaction_type=transaction_type
            )

        if transaction_status:
            transactions = transactions.filter(
                transaction_status=transaction_status
            )

        transactions = transactions.filter(
            transaction_id__icontains=search
        ) | transactions.filter(
            account__account_number__icontains=search
        ) | transactions.filter(
            account__customer__full_name__icontains=search
        )

    return render(
        request,
        "transaction_list.html",
        {
            "transactions": transactions,
            "search": search,
            "transaction_type": transaction_type,
            "transaction_status": transaction_status,
        }
    )

@login_required(login_url="/auth/login/")
def profile_view(request):

    return render(
        request,
        "profile.html"
    )