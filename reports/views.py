from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from transactions.models import Transaction
from customers.models import Customer
from financial_accounts.models import FinancialAccount

from django.http import HttpResponse
import csv


@login_required(login_url="/auth/login/")
def reports_home(request):

    # -----------------------------
    # BASIC COUNTS
    # -----------------------------

    total_customers = Customer.objects.count()

    total_accounts = FinancialAccount.objects.count()

    total_transactions = Transaction.objects.count()


    # -----------------------------
    # REPORT PERIOD
    # -----------------------------

    report_period = request.GET.get(
        "period",
        "all"
    )

    today = timezone.localdate()

    if report_period == "today":

        start_date = today

    elif report_period == "7days":

        start_date = today - timedelta(days=7)

    elif report_period == "30days":

        start_date = today - timedelta(days=30)

    else:

        start_date = None


    # -----------------------------
    # SUCCESSFUL TRANSACTIONS
    # -----------------------------

    successful_transactions = Transaction.objects.filter(
        transaction_status="Success"
    )


    # Apply date filter

    if start_date:

        successful_transactions = successful_transactions.filter(
            created_at__date__gte=start_date
        )


    # -----------------------------
    # TOTAL DEPOSITS
    # -----------------------------

    total_deposits = sum(
        transaction.amount
        for transaction in successful_transactions.filter(
            transaction_type="Deposit"
        )
    )


    # -----------------------------
    # TOTAL WITHDRAWALS
    # -----------------------------

    total_withdrawals = sum(
        transaction.amount
        for transaction in successful_transactions.filter(
            transaction_type="Withdrawal"
        )
    )


    # -----------------------------
    # TOTAL TRANSFERS
    # -----------------------------

    total_transfers = sum(
        transaction.amount
        for transaction in successful_transactions.filter(
            transaction_type="Transfer"
        )
    )


    # -----------------------------
    # RECENT TRANSACTIONS
    # -----------------------------

    recent_transactions = Transaction.objects.select_related(
        "account",
        "account__customer",
        "to_account",
    ).order_by(
        "-created_at"
    )[:10]


    # -----------------------------
    # CONTEXT
    # -----------------------------

    context = {

        "total_customers":
            total_customers,

        "total_accounts":
            total_accounts,

        "total_transactions":
            total_transactions,

        "total_deposits":
            total_deposits,

        "total_withdrawals":
            total_withdrawals,

        "total_transfers":
            total_transfers,

        "recent_transactions":
            recent_transactions,

        "report_period":
            report_period,
    }


    return render(
        request,
        "reports.html",
        context
    )

@login_required(login_url="/auth/login/")
def export_transactions_csv(request):

    transactions = Transaction.objects.select_related(
        "account",
        "account__customer",
        "to_account",
    ).order_by("-created_at")

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="fincore_transactions.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Transaction ID",
        "Source Account",
        "Customer",
        "Destination Account",
        "Transaction Type",
        "Amount",
        "Status",
        "Date",
    ])

    for transaction in transactions:

        writer.writerow([
            transaction.transaction_id,
            transaction.account.account_number,
            transaction.account.customer.full_name,
            (
                transaction.to_account.account_number
                if transaction.to_account
                else "-"
            ),
            transaction.transaction_type,
            transaction.amount,
            transaction.transaction_status,
            transaction.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        ])

    return response