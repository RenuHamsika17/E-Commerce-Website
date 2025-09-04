# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Seller

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "is_customer", "is_seller", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("User Type", {"fields": ("is_customer", "is_seller")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (("User Type", {"fields": ("is_customer", "is_seller")}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Seller)