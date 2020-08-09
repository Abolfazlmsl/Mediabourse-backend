# from django.db import models
#
# from bourse.models import Company
# from mediabourse import settings

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.utils import timezone

###################################################
SYMBOL_TYPE_CHOICES = (
    ('0', "شاخص کل"),
    ('1', "نماد"),
    ('2', "شاخص صنعت"),
)
###################################################


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='گروه بورسی')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:category-detail", kwargs={'category_id': self.pk})


class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, help_text='گروه')
    symbol = models.CharField(max_length=120, null=True, blank=True, help_text='نماد')
    fullName = models.CharField(max_length=120, null=True, blank=True, help_text='نام شرکت')
    alias = models.CharField(max_length=120, null=True, blank=True, help_text='نام معادل انگلیسی')
    type = models.CharField(max_length=20, help_text='نوع نماد', choices=SYMBOL_TYPE_CHOICES, default='1')
    bourseType = models.CharField(max_length=120, null=True, blank=True, help_text='بازار بورس')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    tse = models.URLField(null=True, blank=True, help_text='لینک tse')
    site = models.URLField(null=True, blank=True, help_text='وبسایت')
    isTarget = models.BooleanField(default=False, help_text='تحت نظر')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    hit_count = models.BigIntegerField(default=0)
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["createAt"]

    def __str__(self):
        return self.fullName


class Stock(models.Model):
    symbol = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False, help_text='نماد')
    status = models.CharField(max_length=250, default='ممنوع،متوقف', null=False, blank=False, help_text='وضعیت نماد')
    trade_volume = models.BigIntegerField(default=0, null=False, blank=False, help_text='حجم معاملات')
    # trade_counter = models.BigIntegerField(default=0, null=False, blank=False, help_text='تعداد معاملات')
    # trade_value = models.BigIntegerField(default=0, null=False, blank=0, help_text='ارزش معاملات')
    stock_price_max = models.IntegerField(default=0, null=False, blank=False, help_text='بیشترین قیمت سهم')
    stock_price_min = models.IntegerField(default=0, null=False, blank=False, help_text='کمترین قیمت سهم')
    latest_price = models.IntegerField(default=0, null=False, blank=False, help_text='آخرین قیمت')
    latest_price_indicator_effect = models.IntegerField(default=0, null=0, blank=False,
                                                        help_text='تاثیر آخرین قیمت بر شاخص')
    latest_price_indicator_effect_percent = models.IntegerField(default=0, null=0, blank=False,
                                                                help_text='درصد تاثیر آخرین قیمت بر شاخص')
    final_price = models.IntegerField(default=0, null=0, blank=False, help_text='قیمت پایانی')
    final_price_indicator_effect = models.IntegerField(default=0, null=0, blank=False,
                                                       help_text='تاثیر قیمت پایانی بر شاخص')
    final_price_indicator_effect_percent = models.IntegerField(default=0, null=0, blank=False,
                                                               help_text='درصد تاثیر قیمت پایانی بر شاخص')
    # real_selling_count = models.IntegerField(default=0, null=0, blank=False, help_text='تعداد فروش حقیقی')
    # real_selling_volume = models.BigIntegerField(default=0, null=0, blank=False, help_text='حجم فروش حقیقی')
    # real_selling_price = models.IntegerField(default=0, null=0, blank=False, help_text='قیمت فروش حقیقی')
    # legal_selling_count = models.IntegerField(default=0, null=0, blank=False, help_text='تعداد فروش حقوقی')
    # legal_selling_volume = models.BigIntegerField(default=0, null=0, blank=False, help_text='حجم فروش حقوقی')
    # legal_selling_price = models.IntegerField(default=0, null=0, blank=False, help_text='قیمت فروش حقوقی')


class Watcher(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False,
                                help_text='کاربر')
    stocks = models.TextField(null=False, blank=False, help_text='نام سهم ها')


class Orders(models.Model):
    order_num = models.BigIntegerField()
    date = models.DateTimeField()
    action = models.CharField(max_length=100, default="Buy")
    symbol = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False, help_text="نماد")
    volume = models.IntegerField(null=False, blank=False, help_text="حجم")
    price = models.IntegerField(null=False, blank=False, help_text="قیمت")
    done = models.IntegerField(help_text="حجم انجام شده")
    status = models.BooleanField(default=0, help_text="وضعیت")
    account_type = models.CharField(max_length=150, default="حساب نزد کارگزار", help_text="نوع حساب")
    source = models.CharField(max_length=150, default="وب سایت", help_text="مبدأ")


class Cart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False,
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


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)

    s = send_mail(
        # title
        "Password Reset for {title}".format(title="Media Bource"),
        # message:
        email_plaintext_message,
        # from:
        "amir.amiri2730567@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    print(s)

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

#
# class DemoStockPortfolio(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         help_text='کاربر'
#     )
#     company = models.ForeignKey(
#         Company,
#         on_delete=models.CASCADE,
#         help_text='نماد'
#     )
#     created_on = models.DateField(
#         auto_now_add=True,
#         help_text='تاریخ ایجاد'
#     )
#
#
# class DemoWatchList(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         help_text='کاربر'
#     )
#     name = models.CharField(
#         max_length=255,
#         null=False,
#         blank=False,
#         help_text='نام دیده بان'
#     )
#
#
# class DemoWatchListItem(models.Model):
#     watch_list = models.ForeignKey(
#         DemoWatchList,
#         on_delete=models.CASCADE
#     )
#     company = models.ForeignKey(
#         Company,
#         on_delete=models.CASCADE
#     )
#
#
# class DemoOrders(models.Model):
#     ACTION_CHOICES = (
#         ('buy', 'خرید'),
#         ('sell', 'فروش')
#     )
#     order_num = models.IntegerField()
#     date = models.DateTimeField()
#     action = models.CharField(
#         max_length=100,
#         choices=ACTION_CHOICES,
#         default='buy'
#     )
#     symbol = models.ForeignKey(
#         Company,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False,
#         help_text="نماد"
#     )
#     volume = models.IntegerField(
#         null=False,
#         blank=False,
#         help_text="حجم"
#     )
#     price = models.IntegerField(
#         null=False,
#         blank=False,
#         help_text="قیمت"
#     )
#     done = models.IntegerField(help_text="حجم انجام شده")
#     status = models.BooleanField(default=0, help_text="وضعیت")
#     account_type = models.CharField(
#         max_length=150,
#         default="حساب نزد کارگزار",
#         help_text="نوع حساب"
#     )
#     source = models.CharField(
#         max_length=150,
#         default="وب سایت",
#         help_text="مبدأ"
#     )
#
#
# class DemoCart(models.Model):
#     owner = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         help_text='کاربر'
#     )
#     symbol = models.ForeignKey(
#         Company,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False,
#         help_text="نماد"
#     )
#     stock_balance = models.IntegerField(
#         default=0,
#         null=False,
#         blank=False,
#         help_text="دارایی سهم"
#     )
#     selling_value = models.IntegerField(
#         default=0,
#         null=False,
#         blank=False,
#         help_text="ارزش فروش"
#     )
#     neutral_price = models.IntegerField(
#         default=0,
#         null=False,
#         blank=False,
#         help_text="قیمت سر به سر"
#     )
#     latest_price = models.IntegerField(
#         default=0,
#         null=False,
#         blank=False,
#         help_text='آخرین قیمت'
#     )
#     final_price = models.IntegerField(
#         default=0,
#         null=False,
#         blank=False,
#         help_text='قیمت پایانی'
#     )
#     today_sell = models.IntegerField(
#         default=0,
#         null=False,
#         blank=False,
#         help_text='فروش امروز'
#     )
#     today_buy = models.IntegerField(
#         default=0,
#         null=False,
#         blank=False,
#         help_text='خرید امروز'
#     )
#     open_order = models.IntegerField(
#         default=0,
#         null=False,
#         blank=False,
#         help_text='سفارشات باز'
#     )

