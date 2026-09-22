from django.urls import path
from . import views


urlpatterns = [

    path(
        "register/",
        views.customer_register,
        name="customer_register"
    ),

    path(
        "success/",
        views.customer_success,
        name="customer_success"
    ),

    path(
        "list/",
        views.customer_list,
        name="customer_list"
    ),

    path(
        "edit/<int:customer_id>/",
        views.customer_edit,
        name="customer_edit"
    ),

    path(
        "delete/<int:customer_id>/",
        views.customer_delete,
        name="customer_delete"
    ),

path(
    "kyc/",
    views.kyc_list,
    name="kyc_list"
),

path(
    "kyc/<int:customer_id>/",
    views.kyc_update,
    name="kyc_update"
),
]