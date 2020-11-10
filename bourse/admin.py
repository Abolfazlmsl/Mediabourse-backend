from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import gettext as _
from . import models

# Register your models here.


class UserAdmin(UserAdminBase):
    ordering = ['id']
    list_display = ['phone_number', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (
            _('Personal Info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'generated_token',
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


@admin.register(models.Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "meta")
    list_filter = ("name", "meta")


@admin.register(models.Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "english_title", "meta")
    list_filter = ("title", "meta")


@admin.register(models.Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "english_title", "meta")
    list_filter = ("title", "meta")


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "english_title", "meta")
    list_filter = ("title", "meta")


@admin.register(models.Instrumentgroup)
class InstrumentgroupAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "english_title", "code", "meta")
    list_filter = ("title", "meta")


@admin.register(models.Instrumentexchangestate)
class InstrumentexchangestateAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "meta")
    list_filter = ("title", "meta")


@admin.register(models.Assettype)
class AssettypeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "english_title", "code", "meta")
    list_filter = ("title", "meta")


@admin.register(models.Assetstate)
class AssetstateAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "english_title", "meta")
    list_filter = ("title", "meta")


@admin.register(models.Companystate)
class CompanystateAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "meta")
    list_filter = ("title", "meta")


@admin.register(models.Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_name", "state", "meta")
    list_filter = ("state", "meta")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent_id", "code", "meta")
    list_filter = ("parent_id",)


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "trade_symbol", "state", "english_trade_symbol", "description", "meta")
    list_filter = ("state",)


@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "trade_symbol",  "state", "meta")
    list_filter = ("state", "assetType", "exchange", "categories",)


@admin.register(models.Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_name", "type", "exchange", "exchange_state", "market", "group", "board", "index", "asset", "stock",)
    list_filter = ("type", "market", "board", "group", "exchange", "exchange_state", "index", "group", "board",)


@admin.register(models.Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ("id", "instrument", "timeFrame", "last_candle_date",)
    list_filter = ("timeFrame", "instrument",)


@admin.register(models.Instrumentsel)
class InstrumentselAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_name", "type", "exchange", "exchange_state", "market", "group", "board", "index", "asset", "stock",)
    list_filter = ("type", "market", "board", "group", "exchange", "exchange_state", "index", "group", "board",)


@admin.register(models.Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ("id", "instrument_name", "date_time",  "volume", "trade_count")
    list_filter = ("date_time",)

    def instrument_name(self, obj):
        return obj.instrument.name


@admin.register(models.Tradedetail)
class TradedetailAdmin(admin.ModelAdmin):
    list_display = ("version", "instrument_name", "date_time",  "value")
    list_filter = ("instrument", "date_time",)

    def instrument_name(self, obj):
        return obj.instrument.short_name



@admin.register(models.TechnicalJSONUser)
class TechnicalJSONUserAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "instrument", "created_on", "isShare")
    list_filter = ("user", "instrument", "isShare", )


@admin.register(models.BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "email", "status", "created_on", "fixed_on")
    list_filter = ("email", "status",)


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "reference", "created_on", "is_approved", "hit_count", "instrument")
    list_filter = ("reference", "is_approved", "created_on",)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.WatchList)
admin.site.register(models.RequestSymbol)
admin.site.register(models.WatchListItem)
admin.site.register(models.Technical)
admin.site.register(models.ChatMessage)
admin.site.register(models.Basket)
admin.site.register(models.Webinar)
admin.site.register(models.Filter)
admin.site.register(models.Fundamental)
admin.site.register(models.Bazaar)
admin.site.register(models.UserTechnical)
admin.site.register(models.TutorialCategory)
admin.site.register(models.TutorialSubCategory)
admin.site.register(models.Tutorial)
admin.site.register(models.CompanyFinancial)
admin.site.register(models.UserComment)
admin.site.register(models.FileRepository)
admin.site.register(models.Software)
admin.site.register(models.TutorialOwner)
admin.site.register(models.Note)
admin.site.register(models.Bookmark)
admin.site.register(models.TutorialFile)
admin.site.register(models.Meta)
admin.site.register(models.TutorialFreeFile)
admin.site.register(models.Notification)
admin.site.register(models.Trademidday)