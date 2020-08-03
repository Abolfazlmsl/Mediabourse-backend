from django.db import models

from bourse.models import Company
from mediabourse import settings

# Ali rasti
# class DemoStock(models.Model):
#     symbol = models.ForeignKey(
#         Company,
#         on_delete=models.CASCADE,
#         help_text='نماد'
#     )
#     status = models.CharField(
#         max_length=255,
#         default='ممنوع،متوقف',
#         null=False,
#         blank=False,
#         help_text='وضعیت نماد'
#     )
#     trade_volume = models.BigIntegerField(
#         default=0,
#         null=False,
#         blank=False,
#         help_text='حجم معاملات'
#     )
#     # trade_counter = models.BigIntegerField(default=0, null=False, blank=False, help_text='تعداد معاملات')
#     # trade_value = models.BigIntegerField(default=0, null=False, blank=0, help_text='ارزش معاملات')
#     stock_price_max = models.IntegerField(default=0, null=False, blank=False, help_text='بیشترین قیمت سهم')
#     stock_price_min = models.IntegerField(default=0, null=False, blank=False, help_text='کمترین قیمت سهم')
#     latest_price = models.IntegerField(default=0, null=False, blank=False, help_text='آخرین قیمت')
#     latest_price_indicator_effect = models.IntegerField(default=0, null=0, blank=False,
#                                                         help_text='تاثیر آخرین قیمت بر شاخص')
#     latest_price_indicator_effect_percent = models.IntegerField(default=0, null=0, blank=False,
#                                                                 help_text='درصد تاثیر آخرین قیمت بر شاخص')
#     final_price = models.IntegerField(default=0, null=0, blank=False, help_text='قیمت پایانی')
#     final_price_indicator_effect = models.IntegerField(default=0, null=0, blank=False,
#                                                        help_text='تاثیر قیمت پایانی بر شاخص')
#     final_price_indicator_effect_percent = models.IntegerField(default=0, null=0, blank=False,
#                                                                help_text='درصد تاثیر قیمت پایانی بر شاخص')
#     # real_selling_count = models.IntegerField(default=0, null=0, blank=False, help_text='تعداد فروش حقیقی')
#     # real_selling_volume = models.BigIntegerField(default=0, null=0, blank=False, help_text='حجم فروش حقیقی')
#     # real_selling_price = models.IntegerField(default=0, null=0, blank=False, help_text='قیمت فروش حقیقی')
#     # legal_selling_count = models.IntegerField(default=0, null=0, blank=False, help_text='تعداد فروش حقوقی')
#     # legal_selling_volume = models.BigIntegerField(default=0, null=0, blank=False, help_text='حجم فروش حقوقی')
#     # legal_selling_price = models.IntegerField(default=0, null=0, blank=False, help_text='قیمت فروش حقوقی')


class DemoStockPortfolio(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        help_text='نماد'
    )
    created_on = models.DateField(
        auto_now_add=True,
        help_text='تاریخ ایجاد'
    )


class DemoWatchList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='کاربر'
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text='نام دیده بان'
    )


class DemoWatchListItem(models.Model):
    watch_list = models.ForeignKey(
        DemoWatchList,
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )


class DemoOrders(models.Model):
    order_num = models.IntegerField()
    date = models.DateTimeField()
    action = models.CharField(max_length=100, default="Buy")
    symbol = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False, help_text="نماد")
    volume = models.IntegerField(null=False, blank=False, help_text="حجم")
    price = models.IntegerField(null=False, blank=False, help_text="قیمت")
    done = models.IntegerField(help_text="حجم انجام شده")
    status = models.BooleanField(default=0, help_text="وضعیت")
    account_type = models.CharField(max_length=150, default="حساب نزد کارگزار", help_text="نوع حساب")
    source = models.CharField(max_length=150, default="وب سایت", help_text="مبدأ")


class DemoCart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                help_text='کاربر')
    symbol = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False, help_text="نماد")
    stock_balance = models.IntegerField(default=0, null=False, blank=False, help_text="دارایی سهم")
    selling_value = models.IntegerField(default=0, null=False, blank=False, help_text="ارزش فروش")
    neutral_price = models.IntegerField(default=0, null=False, blank=False, help_text="قیمت سر به سر")
    latest_price = models.IntegerField(default=0, null=False, blank=False, help_text='آخرین قیمت')
    final_price = models.IntegerField(default=0, null=0, blank=False, help_text='قیمت پایانی')
    today_sell = models.IntegerField(default=0, null=0, blank=False, help_text='فروش امروز')
    today_buy = models.IntegerField(default=0, null=0, blank=False, help_text='خرید امروز')
    open_order = models.IntegerField(default=0, null=0, blank=False, help_text='سفارشات باز')

