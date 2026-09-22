from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from customers.models import Customer
from financial_accounts.models import FinancialAccount
from transactions.models import Transaction


@login_required(login_url="/auth/login/")
def dashboard_home(request):

    total_customers = Customer.objects.count()

    total_accounts = FinancialAccount.objects.count()

    total_balance = sum(
        account.balance
        for account in FinancialAccount.objects.all()
    )

    total_transactions = Transaction.objects.count()

    # KYC counts
    kyc_pending = Customer.objects.filter(
        kyc_status="Pending"
    ).count()

    kyc_verified = Customer.objects.filter(
        kyc_status="Verified"
    ).count()

    kyc_rejected = Customer.objects.filter(
        kyc_status="Rejected"
    ).count()

    # Recent transactions
    recent_transactions = Transaction.objects.select_related(
        "account",
        "account__customer",
        "to_account",
    ).order_by(
        "-created_at"
    )[:5]

    context = {
        "total_customers": total_customers,
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "total_transactions": total_transactions,

        "kyc_pending": kyc_pending,
        "kyc_verified": kyc_verified,
        "kyc_rejected": kyc_rejected,

        "recent_transactions": recent_transactions,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


def home(request):

    return render(
        request,
        "home.html"
    )