import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fincore.settings")
django.setup()

from django.contrib.auth.models import User

username = "admin"
email = "sivaranjanijeeva04@gmail.com"

password = os.environ.get(
    "ADMIN_PASSWORD",
    "FinCore@Admin2026"
)

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        "email": email,
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
    }
)

user.email = email
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.set_password(password)
user.save()

print("FinCore admin user ready.")