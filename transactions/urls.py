from django.urls import path
from . import views


urlpatterns = [

    path(
        "create/",
        views.transaction_create,
        name="transaction_create"
    ),

    path(
        "success/",
        views.transaction_success,
        name="transaction_success"
    ),

    path(
        "list/",
        views.transaction_list,
        name="transaction_list"
    ),
]