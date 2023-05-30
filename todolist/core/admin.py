from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['last_login', 'date_joined']
    exclude = ['password', ]
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name']


admin.site.register(User, UserAdmin)
