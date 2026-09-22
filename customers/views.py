from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CustomerForm
from .models import Customer

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test

@login_required(login_url="/auth/login/")
def customer_register(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("customer_success")

    else:

        form = CustomerForm()

    return render(
        request,
        "customer_register.html",
        {"form": form}
    )


@login_required(login_url="/auth/login/")
def customer_success(request):

    return render(
        request,
        "customer_success.html"
    )


@login_required(login_url="/auth/login/")
def customer_list(request):

    search = request.GET.get("search", "")

    customers = Customer.objects.all().order_by(
        "-created_at"
    )

    if search:

        customers = customers.filter(
            customer_id__icontains=search
        ) | customers.filter(
            full_name__icontains=search
        ) | customers.filter(
            phone__icontains=search
        )

    return render(
        request,
        "customer_list.html",
        {
            "customers": customers,
            "search": search,
        }
    )


@login_required(login_url="/auth/login/")
def customer_edit(request, customer_id):

    customer = Customer.objects.get(
        id=customer_id
    )

    if request.method == "POST":

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():

            form.save()

            return redirect("customer_list")

    else:

        form = CustomerForm(
            instance=customer
        )

    return render(
        request,
        "customer_edit.html",
        {
            "form": form,
            "customer": customer,
        }
    )


@login_required(login_url="/auth/login/")
def customer_delete(request, customer_id):

    customer = Customer.objects.get(
        id=customer_id
    )

    if request.method == "POST":

        customer.delete()

        return redirect("customer_list")

    return render(
        request,
        "customer_delete.html",
        {
            "customer": customer,
        }
    )


def staff_required(user):
    return user.is_staff


@user_passes_test(
    staff_required,
    login_url="/auth/login/"
)
def kyc_list(request):

    search = request.GET.get("search", "")

    customers = Customer.objects.all().order_by(
        "-created_at"
    )

    if search:

        customers = customers.filter(
            customer_id__icontains=search
        ) | customers.filter(
            full_name__icontains=search
        ) | customers.filter(
            phone__icontains=search
        )

    return render(
        request,
        "kyc_list.html",
        {
            "customers": customers,
            "search": search,
        }
    )


@user_passes_test(
    staff_required,
    login_url="/auth/login/"
)
def kyc_update(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == "POST":

        kyc_status = request.POST.get(
            "kyc_status"
        )

        if kyc_status in [
            "Pending",
            "Verified",
            "Rejected"
        ]:

            customer.kyc_status = kyc_status
            customer.save()

        return redirect("kyc_list")

    return render(
        request,
        "kyc_update.html",
        {
            "customer": customer
        }
    )