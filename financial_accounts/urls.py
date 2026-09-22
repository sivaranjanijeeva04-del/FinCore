from django.urls import path
from . import views


urlpatterns = [

    path(
        "register/",
        views.account_register,
        name="account_register"
    ),

    path(
        "success/",
        views.account_success,
        name="account_success"
    ),

    path(
        "list/",
        views.account_list,
        name="account_list"
    ),

path(
    "statement/<int:account_id>/",
    views.account_statement,
    name="account_statement"
),
]