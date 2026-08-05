import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.users.models import CustomUser
from apps.subscriptions.models import Plan

print("=== Setting up Admin Users ===")

# 1. Update naveenmalik@gmail.com if present
user1 = CustomUser.objects.filter(email="naveenmalik@gmail.com").first()
if user1:
    user1.full_name = "Magnivel International Media"
    user1.is_staff = True
    user1.is_superuser = True
    user1.set_password("Admin@123456")
    user1.save()
    print("Updated user naveenmalik@gmail.com -> is_staff=True, is_superuser=True, full_name='Magnivel International Media'")

# 2. Ensure admin@magnivel.com exists
admin_user, created = CustomUser.objects.get_or_create(
    email="admin@magnivel.com",
    defaults={
        "username": "admin",
        "full_name": "Magnivel International Media",
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
    }
)
admin_user.full_name = "Magnivel International Media"
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.set_password("Admin@123456")
admin_user.save()

# 3. Update all staff/superuser full_name
CustomUser.objects.filter(is_staff=True).update(full_name="Magnivel International Media")
CustomUser.objects.filter(full_name__icontains="Naveen").update(full_name="Magnivel International Media")

if created:
    print("Created superuser admin@magnivel.com (password: Admin@123456)")
else:
    print("Updated superuser admin@magnivel.com (password: Admin@123456)")

print("\n=== Seeding Subscription Plans ===")

plans_data = [
    {
        "name": "Free",
        "slug": "free",
        "duration_days": 30,
        "price": 0,
        "currency": "INR",
        "price_usd": 0,
        "is_popular": False,
        "sort_order": 1,
        "description": "Standard access to public articles and community discussion.",
        "features": ["Access to public articles", "Community discussion", "Basic newsletter"],
        "is_active": True,
    },
    {
        "name": "Pro Monthly",
        "slug": "pro-monthly",
        "duration_days": 30,
        "price": 499,
        "currency": "INR",
        "price_usd": 6,
        "is_popular": True,
        "sort_order": 2,
        "description": "Full uninhibited access to all premium publications, deep dives, and expert analysis.",
        "features": ["Unlimited full article access", "Exclusive deep-dive reports", "Ad-free reading experience", "Author comments & Q&A", "Cancel anytime"],
        "is_active": True,
    },
    {
        "name": "Pro Annual",
        "slug": "pro-annual",
        "duration_days": 365,
        "price": 3999,
        "currency": "INR",
        "price_usd": 49,
        "is_popular": False,
        "sort_order": 3,
        "description": "Save 33% per year with full annual access, early research papers, and priority support.",
        "features": ["All Pro Monthly features", "Save 33% per year", "Early access to research papers", "Priority support", "Download PDF reports"],
        "is_active": True,
    },
]

for pdata in plans_data:
    plan, pcreated = Plan.objects.update_or_create(
        slug=pdata["slug"],
        defaults=pdata
    )
    status_str = "Created" if pcreated else "Updated"
    print(f"{status_str} plan: {plan.name} (Price: {plan.price} {plan.currency} / ${plan.price_usd} USD)")

print(f"\nTotal Active Plans: {Plan.objects.filter(is_active=True).count()}")
