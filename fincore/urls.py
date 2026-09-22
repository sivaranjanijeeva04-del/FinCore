from django.contrib import admin
from django.urls import path, include

from dashboard import views as dashboard_views


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "auth/",
        include("accounts.urls")
    ),

    path(
        "customers/",
        include("customers.urls")
    ),

    path(
        "accounts/",
        include("financial_accounts.urls")
    ),

    path(
        "transactions/",
        include("transactions.urls")
    ),

    path(
        "reports/",
        include("reports.urls")
    ),

    # Home Page
    path(
        "",
        dashboard_views.home,
        name="home"
    ),

    # Dashboard
    path(
        "dashboard/",
        include("dashboard.urls")
    ),

]