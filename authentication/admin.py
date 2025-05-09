from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('whatsapp_number', 'bonus_balance', 'referral_code')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('whatsapp_number', 'bonus_balance', 'referral_code')}),
    )
    list_display = ['username', 'email', 'whatsapp_number', 'bonus_balance', 'referral_code']
    search_fields = ['username', 'email', 'whatsapp_number']

admin.site.register(CustomUser, CustomUserAdmin)
