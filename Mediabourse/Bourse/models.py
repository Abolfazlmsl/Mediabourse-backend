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


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

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
