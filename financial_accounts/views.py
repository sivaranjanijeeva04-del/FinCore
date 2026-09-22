from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random

from .forms import FinancialAccountForm
from .models import FinancialAccount

from transactions.models import Transaction

def generate_account_number():

    while True:

        account_number = (
            "FC"
            + str(random.randint(10000000, 99999999))
        )

        if not FinancialAccount.objects.filter(
            account_number=account_number
        ).exists():

            return account_number


@login_required(login_url="/auth/login/")
def account_register(request):

    if request.method == "POST":

        form = FinancialAccountForm(request.POST)

        if form.is_valid():

            account = form.save(commit=False)

            account.account_number = (
                generate_account_number()
            )

            account.save()

            return redirect("account_success")

    else:

        form = FinancialAccountForm()

    return render(
        request,
        "account_register.html",
        {"form": form}
    )


@login_required(login_url="/auth/login/")
def account_success(request):

    return render(
        request,
        "account_success.html"
    )


@login_required(login_url="/auth/login/")
def account_list(request):

    search = request.GET.get("search", "")

    accounts = FinancialAccount.objects.select_related(
        "customer"
    ).order_by("-opened_date")

    if search:

        accounts = accounts.filter(
            account_number__icontains=search
        ) | accounts.filter(
            customer__customer_id__icontains=search
        ) | accounts.filter(
            customer__full_name__icontains=search
        )

    return render(
        request,
        "account_list.html",
        {
            "accounts": accounts,
            "search": search,
        }
    )

@login_required(login_url="/auth/login/")
def account_statement(request, account_id):

    account = FinancialAccount.objects.select_related(
        "customer"
    ).get(
        id=account_id
    )

    transactions = Transaction.objects.filter(
        account=account
    ) | Transaction.objects.filter(
        to_account=account
    )

    transactions = transactions.select_related(
        "account",
        "to_account"
    ).order_by(
        "-created_at"
    )

    for transaction in transactions:

        if transaction.transaction_type == "Deposit":

            transaction.entry_type = "Credit"

        elif transaction.transaction_type == "Withdrawal":

            transaction.entry_type = "Debit"

        elif transaction.transaction_type == "Transfer":

            if transaction.account == account:

                transaction.entry_type = "Debit"

            else:

                transaction.entry_type = "Credit"

    total_deposits = sum(
        transaction.amount
        for transaction in transactions
        if transaction.account == account
        and transaction.transaction_type == "Deposit"
        and transaction.transaction_status == "Success"
    )

    total_withdrawals = sum(
        transaction.amount
        for transaction in transactions
        if transaction.account == account
        and transaction.transaction_type == "Withdrawal"
        and transaction.transaction_status == "Success"
    )

    total_transfers = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == "Transfer"
        and transaction.transaction_status == "Success"
    )

    return render(
        request,
        "account_statement.html",
        {
            "account": account,
            "transactions": transactions,
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals,
            "total_transfers": total_transfers,
        }
    )