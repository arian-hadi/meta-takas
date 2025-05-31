from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OneTimePassword

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('first_name', 'last_name', 'email', 'username', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_verified')
    ordering = ('email',)
    search_fields = ('email', 'username', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Verification', {'fields': ('is_verified',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_verified', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OneTimePassword)
