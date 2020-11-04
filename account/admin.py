from django.contrib import admin
from .models import User, Customer
from django.contrib.auth.admin import UserAdmin as UA


class UserAdmin(UA):
    ordering = ('email',)
    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email',
                           'password1', 'password2', 'profile_pic', 'is_superuser', 'is_staff', 'is_active', 'gender', 'user_type')}),
    )
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email',
                           'password', 'profile_pic', 'is_superuser', 'is_staff', 'is_active', 'gender', 'user_type')}),
    )


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Customer)
