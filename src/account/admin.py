from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    ordering = ('phone_number',)
    list_display = ('phone_number', 'email', 'first_name', 'last_name', 'ip', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name', 'ip')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)