from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Artist
    list_display = ("email", "username", "first_name", "last_name", "description", "image", "is_staff", "is_active", "is_superuser",)
    list_filter = ("email", "username", "first_name", "last_name", "description", "image", "is_staff", "is_active", "is_superuser",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Artist Info", {"fields": ( "first_name", "last_name", "username", "image", "description")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2", "image", "description", "is_staff",
                "is_active", "is_superuser", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Artist, CustomUserAdmin)
