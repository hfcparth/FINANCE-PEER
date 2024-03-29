from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display=('email','adhar','last_login','is_admin')
    search_fields=('email','adhar','first_name')
    readonly_fields=('date_joined','last_login')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(Account,AccountAdmin)
