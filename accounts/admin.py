from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

# Assuming Company model is located in 'reviews.models'
from reviews.models import Company


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'company', 'job_title', 'department')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': (
            'username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'company', 'job_title', 'department')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'company', 'job_title', 'department')
    search_fields = ('username', 'first_name', 'last_name',
                     'email', 'company__name', 'job_title', 'department')
    list_filter = ('is_staff', 'is_superuser', 'is_active',
                   'groups', 'company')


admin.site.register(CustomUser, CustomUserAdmin)
