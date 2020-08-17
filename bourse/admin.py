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
                    'picture',
                    'national_code',
                    'father_name',
                    'birth_date',
                    'postal_code',
                    'address'
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
admin.site.register(models.Company)
admin.site.register(models.Category)
admin.site.register(models.WatchList)
admin.site.register(models.RequestSymbol)
admin.site.register(models.WatchListItem)
admin.site.register(models.News)
admin.site.register(models.Technical)
admin.site.register(models.ChatMessage)
admin.site.register(models.Basket)
admin.site.register(models.Webinar)
admin.site.register(models.Filter)
admin.site.register(models.Fundamental)
admin.site.register(models.Bazaar)
admin.site.register(models.Chart)
admin.site.register(models.UserTechnical)
admin.site.register(models.TutorialCategory)
admin.site.register(models.TutorialSubCategory)
admin.site.register(models.Tutorial)
admin.site.register(models.CompanyFinancial)
admin.site.register(models.UserComment)
admin.site.register(models.FileRepository)
admin.site.register(models.TutorialOwner)
admin.site.register(models.Note)
admin.site.register(models.Bookmark)
admin.site.register(models.TutorialFile)
