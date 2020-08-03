from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import gettext as _
from . import models

# Register your models here.


class UserAdmin(UserAdminBase):
    ordering = ['id']
    list_display = ['phone_number', 'name']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (
            _('Personal Info'),
            {
                'fields': (
                    'name',
                    'email',
                    'generated_token',
                    'is_verified',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')
            }
        ),
        (
            _('Important dates'),
            {
                'fields': ('last_login',)
            }
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
# admin.site.register(models.Company)
# admin.site.register(models.Category)
# admin.site.register(models.WatchList)
# admin.site.register(models.Stock)
# admin.site.register(models.Orders)
# admin.site.register(models.Cart)
