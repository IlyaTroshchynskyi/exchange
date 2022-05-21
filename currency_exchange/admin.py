"""
Collect admin models
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from currency_exchange.models import CurrencyRates, UsersExchangeOperations


@admin.register(CurrencyRates)
class CurrencyRatesAdmin(admin.ModelAdmin):
    pass


@admin.register(UsersExchangeOperations)
class UsersExchangeOperationsViewAdmin(admin.ModelAdmin):
    pass


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'password')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
